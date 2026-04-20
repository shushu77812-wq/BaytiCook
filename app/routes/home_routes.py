from flask import Blueprint, render_template, request, redirect, session
from app.models.meal_model import Meal
from app.models.kitchen_model import Kitchen

home = Blueprint("home", __name__)


# =============================
# الصفحة الرئيسية
# =============================
@home.route("/")
def index():

    meals = Meal.query.all()
    featured_kitchens = Kitchen.query.filter_by(featured=True).all()

    # 🛒 عدد عناصر السلة
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
    if not kitchen.is_open:
        return "❌ هذا المطبخ مغلق حالياً"

    meals = Meal.query.filter_by(kitchen_id=id).all()

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
        (Kitchen.kitchen_name.contains(q))
    ).all()

    cart_count = len(session.get("cart", {}))

    return render_template(
        "main/search.html",
        meals=meals,
        query=q,
        cart_count=cart_count
    )

@home.route("/order/<int:meal_id>")
def order_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    # هنا تضيفي منطق إنشاء الطلب أو صفحة تأكيد الطلب
    return render_template("home/order_meal.html", meal=meal)
