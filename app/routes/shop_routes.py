from flask import Blueprint, render_template, session, request, redirect, url_for
from app import db
from app.models.meal_model import Meal
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.kitchen_model import Kitchen

shop = Blueprint("shop", __name__)

# =============================
# تفاصيل الوجبة
# =============================
@shop.route("/meal/<int:id>")
def meal_details(id):
    meal = Meal.query.get_or_404(id)
    return render_template("meal_details.html", meal=meal)


# =============================
# السلةfrom flask import Blueprint, render_template, request, redirect, session, url_for
from app import db
from app.models.meal_model import Meal
from app.models.order_model import Order
from app.models.order_item_model import OrderItem

shop = Blueprint("shop", __name__)


# =============================
# عرض السلة
# =============================
@shop.route("/cart")
def cart():
    cart = session.get("cart", {})
    meals = []
    total_price = 0

    for meal_id, quantity in cart.items():
        meal = Meal.query.get(meal_id)
        if meal:
            meal.quantity = quantity
            meals.append(meal)
            total_price += meal.price * quantity

    return render_template("main/cart.html", meals=meals, total_price=total_price)


# =============================
# إضافة للسلة
# =============================
@shop.route("/add-to-cart/<int:meal_id>", methods=["POST"])
def add_to_cart(meal_id):
    cart = session.get("cart", {})

    if str(meal_id) in cart:
        cart[str(meal_id)] += 1
    else:
        cart[str(meal_id)] = 1

    session["cart"] = cart
    return redirect(url_for("shop.cart"))  # فقط تعديل بسيط


# =============================
# حذف من السلة
# =============================
@shop.route("/remove-from-cart/<int:meal_id>")
def remove_from_cart(meal_id):
    cart = session.get("cart", {})

    if str(meal_id) in cart:
        del cart[str(meal_id)]

    session["cart"] = cart
    return redirect(url_for("shop.cart"))


# =============================
# إنشاء الطلب
# =============================
@shop.route("/checkout", methods=["POST"])
def checkout():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("shop.cart"))

    total_price = 0
    kitchen_id = None

    for meal_id, quantity in cart.items():
        meal = Meal.query.get(meal_id)
        if meal:
            total_price += meal.price * quantity
            kitchen_id = meal.kitchen_id

    new_order = Order(
        user_id=session["user_id"],
        customer_id=session["user_id"],
        kitchen_id=kitchen_id,
        total_price=total_price,
        status="pending"   # التعديل المهم هنا فقط
    )

    db.session.add(new_order)
    db.session.commit()

    for meal_id, quantity in cart.items():
        meal = Meal.query.get(meal_id)
        if meal:
            item = OrderItem(
                order_id=new_order.id,
                meal_id=meal.id,
                quantity=quantity,
                price=meal.price
            )
            db.session.add(item)

    db.session.commit()

    session["cart"] = {}

    return redirect(url_for("shop.my_orders"))


# =============================
# عرض الطلبات
# =============================
@shop.route("/my-orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    orders = Order.query.filter_by(user_id=session["user_id"]).all()

    return render_template("main/my_orders.html", orders=orders)  # فقط تعديل .html
# =============================
@shop.route("/cart")
def cart():
    cart = session.get("cart", {})

    if isinstance(cart, list):
        cart = {}
        session["cart"] = cart

    meal_ids = [int(id) for id in cart.keys()]
    meals = Meal.query.filter(Meal.id.in_(meal_ids)).all()

    total = 0
    grouped_cart = {}

    for meal in meals:
        quantity = cart.get(str(meal.id), 0)
        subtotal = meal.price * quantity
        total += subtotal
        kitchen_id = meal.kitchen_id

        if kitchen_id not in grouped_cart:
            grouped_cart[kitchen_id] = []

        grouped_cart[kitchen_id].append({
            "meal": meal,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render_template(
        "main/cart.html",
        grouped_cart=grouped_cart,
        total=total
    )


# =============================
# إضافة للسلة
# =============================
@shop.route("/add-to-cart/<int:id>", methods=["POST"])
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    session["cart"] = cart
    return redirect("/cart")


# =============================
# حذف عنصر
# =============================
@shop.route("/remove/<int:id>")
def remove_item(id):
    cart = session.get("cart", {})
    cart.pop(str(id), None)
    session["cart"] = cart
    return redirect("/cart")


# =============================
# زيادة / نقصان
# =============================
@shop.route("/update/<int:id>/<action>")
def update_qty(id, action):
    cart = session.get("cart", {})

    if str(id) in cart:
        if action == "plus":
            cart[str(id)] += 1
        elif action == "minus" and cart[str(id)] > 1:
            cart[str(id)] -= 1

    session["cart"] = cart
    return redirect("/cart")


# =============================
# إنشاء الطلب
# =============================
@shop.route("/create-order", methods=["POST"])
def create_order():
    if "user_id" not in session:
        return redirect("/login")

    cart = session.get("cart", {})
    if not cart:
        return "السلة فارغة"

    kitchens_orders = {}
    for meal_id, quantity in cart.items():
        meal = Meal.query.get(int(meal_id))
        kitchen_id = meal.kitchen_id

        if not meal.kitchen.is_open:
            return "❌ هذا المطبخ مغلق"

        if kitchen_id not in kitchens_orders:
            kitchens_orders[kitchen_id] = []

        kitchens_orders[kitchen_id].append({
            "meal": meal,
            "quantity": quantity
        })

    for kitchen_id, items in kitchens_orders.items():
        total_price = sum(item["meal"].price * item["quantity"] for item in items)

        new_order = Order(
    user_id=session["user_id"],
    customer_id=session["user_id"],  
    kitchen_id=kitchen_id,
    total_price=total_price,
    status="قيد المراجعة"
    )

        db.session.add(new_order)
        db.session.commit()

        for item in items:
            order_item = OrderItem(
                order_id=new_order.id,
                meal_id=item["meal"].id,
                quantity=item["quantity"]
            )
            db.session.add(order_item)

        db.session.commit()

    session["cart"] = {}

    return redirect(url_for("shop.my_orders"))


# =============================
# صفحة متابعة الطلبات
# =============================
@shop.route("/my_orders")
def my_orders():
    if "user_id" not in session:
        return redirect("/login")

    orders = Order.query.filter_by(user_id=session["user_id"]).all()
    return render_template("main/my_orders", orders=orders)


# =============================
# صفحة المطبخ
# =============================
@shop.route("/kitchen/<int:id>")
def kitchen_page(id):
    kitchen = Kitchen.query.get_or_404(id)

    if not kitchen.is_open:
        return "❌ هذا المطبخ مغلق حالياً"

    meals = Meal.query.filter_by(kitchen_id=id).all()
    return render_template("kitchen_page.html", kitchen=kitchen, meals=meals)


# =============================
# صفحة الدفع
# =============================
@shop.route("/checkout", methods=["GET","POST"])
def checkout():
    cart = session.get("cart", {})
    meal_ids = [int(id) for id in cart.keys()]
    meals = Meal.query.filter(Meal.id.in_(meal_ids)).all()

    grouped_cart = {}
    for meal in meals:
        quantity = cart.get(str(meal.id), 0)
        kitchen_id = meal.kitchen_id

        if kitchen_id not in grouped_cart:
            grouped_cart[kitchen_id] = []

        grouped_cart[kitchen_id].append({
            "meal": meal,
            "quantity": quantity,
            "subtotal": meal.price * quantity
        })

    return render_template("main/checkout.html", grouped_cart=grouped_cart)

