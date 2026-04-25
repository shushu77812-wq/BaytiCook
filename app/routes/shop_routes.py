from flask import Blueprint, render_template, request, redirect, session, url_for
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
# عرض السلة (مجمعة حسب المطبخ)
# =============================
@shop.route("/cart")
def cart():
    cart = session.get("cart", {})

    if isinstance(cart, list):
        cart = {}
        session["cart"] = cart

    meal_ids = [int(mid) for mid in cart.keys()]
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

    return render_template("main/cart.html", grouped_cart=grouped_cart, total=total)

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
    return redirect(url_for("shop.cart"))

# =============================
# حذف عنصر من السلة
# =============================
@shop.route("/remove/<int:meal_id>")
def remove_item(meal_id):
    cart = session.get("cart", {})
    cart.pop(str(meal_id), None)
    session["cart"] = cart
    return redirect(url_for("shop.cart"))

# =============================
# زيادة / نقصان الكمية
# =============================
@shop.route("/update/<int:meal_id>/<action>")
def update_qty(meal_id, action):
    cart = session.get("cart", {})

    if str(meal_id) in cart:
        if action == "plus":
            cart[str(meal_id)] += 1
        elif action == "minus" and cart[str(meal_id)] > 1:
            cart[str(meal_id)] -= 1

    session["cart"] = cart
    return redirect(url_for("shop.cart"))

# =============================
# إنشاء الطلب (يدعم تعدد المطابخ)
# =============================
@shop.route("/create-order", methods=["POST"])
def create_order():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cart = session.get("cart", {})
    if not cart:
        return "السلة فارغة"

    try:
        kitchens_orders = {}
        for meal_id, quantity in cart.items():
            meal = Meal.query.get(int(meal_id))
            if not meal.kitchen.is_open:
                return "❌ هذا المطبخ مغلق"

            kitchen_id = meal.kitchen_id
            if kitchen_id not in kitchens_orders:
                kitchens_orders[kitchen_id] = []

            kitchens_orders[kitchen_id].append({"meal": meal, "quantity": quantity})

        # ننشئ الطلبات لكل مطبخ
        created_orders = []
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
            db.session.flush()  # يخلي الـ order.id جاهز بدون commit

            for item in items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    meal_id=item["meal"].id,
                    quantity=item["quantity"],
                    price=item["meal"].price
                )
                db.session.add(order_item)

            created_orders.append(new_order.id)

        db.session.commit()
        session["cart"] = {}

        # نوجه المستخدم لأول طلب أنشأناه إلى صفحة الدفع
        return redirect(url_for("shop.checkout", order_id=created_orders[0]))

    except Exception as e:
        db.session.rollback()
        return f"❌ خطأ أثناء تأكيد الطلب: {e}"

# =============================
# صفحة الدفع
# =============================
@shop.route("/checkout/<int:order_id>", methods=["GET", "POST"])
def checkout(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == "POST":
        payment_method = request.form.get("payment_method")

        if payment_method == "cod":  # الدفع عند الاستلام
            order.status = "مؤكد"
        elif payment_method == "bank":  # تحويل بنكي
            order.status = "بانتظار الدفع"
        db.session.commit()

        return redirect(url_for("shop.my_orders"))

    return render_template("main/checkout.html", order=order)

# =============================
# صفحة متابعة الطلبات
# =============================
@shop.route("/my-orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    orders = Order.query.filter(
    Order.user_id == session["user_id"],
    Order.status != "delivered"
    ).all()
    return render_template("main/my_orders.html", orders=orders)

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
