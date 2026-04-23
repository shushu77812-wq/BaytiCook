from flask import Blueprint, render_template, request, redirect, session
from app.models.meal_model import Meal
from app.models.kitchen_model import Kitchen

home = Blueprint("home", __name__)

# =============================
# الصفحة الرئيسية
# =============================
@home.route("/")
def index():
    try:
        # ✅ المطابخ المميزة (فقط المفتوحة والموافقة)
        featured_kitchens = Kitchen.query.filter(
            Kitchen.featured == 1,
            Kitchen.is_open == 1,
            Kitchen.status == "approved"
        ).all()

        # ✅ جميع الأطباق (فقط الموافقة والمطابخ المفتوحة)
        meals = Meal.query.join(Kitchen).filter(
            Meal.status == "approved",
            Kitchen.is_open == 1,
            Kitchen.status == "approved"
        ).all()

    except Exception as e:
        return f"Database Error: {e}"

    cart_count = len(session.get("cart", {}))

    return render_template(
        "base.html",
        meals=meals,
        featured_kitchens=featured_kitchens,
        cart_count=cart_count
    )

# =============================
# صفحة المطبخ
# =============================
@home.route("/kitchen/<int:id>")
def kitchen_page(id):
    kitchen = Kitchen.query.get_or_404(id)

    # 🔴 إذا المطبخ مغلق
    if kitchen.is_open == 0:
        return "❌ هذا المطبخ مغلق حالياً"

    meals = Meal.query.filter(
        Meal.kitchen_id == id,
        Meal.status == "approved"
    ).all()

    cart_count = len(session.get("cart", {}))

    return render_template(
        "main/kitchen_page.html",
        kitchen=kitchen,
        meals=meals,
        cart_count=cart_count
    )

# =============================
# البحث
# =============================
@home.route("/search")
def search():
    q = request.args.get("q")

    if not q:
        return redirect("/")

    meals = Meal.query.join(Kitchen).filter(
        (Meal.name.contains(q)) |
        (Kitchen.kitchen_name.contains(q)),
        Meal.status == "approved",
        Kitchen.is_open == 1,
        Kitchen.status == "approved"
    ).all()

    cart_count = len(session.get("cart", {}))

    return render_template(
        "main/search.html",
        meals=meals,
        query=q,
        cart_count=cart_count
    )

# =============================
# الطلب
# =============================
@home.route("/order/<int:meal_id>")
def order_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    # هنا تضيفي منطق إنشاء الطلب أو صفحة تأكيد الطلب
    return render_template("home/order_meal.html", meal=meal)
