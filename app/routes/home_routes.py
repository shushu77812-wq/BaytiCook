from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from app.models.meal_model import Meal
from app.models.kitchen_model import Kitchen
from app.models.user_model import User
from app import db, mail
from flask_mail import Message

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

        # ✅ جميع الأطباق (فقط الموافقة + المتوفرة + المطابخ المفتوحة)
        meals = Meal.query.join(Kitchen).filter(
            Meal.status == "approved",
            Meal.is_available == 1,
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
# موافقة الطاهية من الرئيسية
# =============================
@home.route("/approve-chef/<int:user_id>")
def approve_chef(user_id):
    user = User.query.get_or_404(user_id)
    user.status = "approved"
    db.session.commit()

    # إرسال إيميل للطاهية
    if user.email:
        msg = Message(
            subject="تمت الموافقة على حسابك في BaytiCook",
            recipients=[user.email],
            body=f"""
        مرحباً {user.name},

        مبروك! حسابك كمطبخ منزلي تمت الموافقة عليه من قبل الإدارة.
        يمكنك الآن الدخول وإضافة أطباقك.

        فريق BaytiCook
        """
        )
        mail.send(msg)

    flash("✅ تمّت الموافقة على الطاهية وإرسال رسالة عبر البريد الإلكتروني", "success")
    return redirect(url_for("home.index"))

# =============================
# رفض الطاهية من الرئيسية
# =============================
@home.route("/reject-chef/<int:user_id>")
def reject_chef(user_id):
    user = User.query.get_or_404(user_id)
    user.status = "rejected"
    db.session.commit()

    # إرسال إيميل للطاهية
    if user.email:
        msg = Message(
            subject="تم رفض حسابك في BaytiCook",
            recipients=[user.email],
            body=f"""
        مرحباً {user.name},

        نعتذر، حسابك كمطبخ منزلي لم تتم الموافقة عليه حالياً.
        يمكنك التواصل مع الإدارة لمزيد من التفاصيل.

        فريق BaytiCook
        """
        )
        mail.send(msg)

    flash("❌ تم رفض الطاهية وإرسال رسالة عبر البريد الإلكتروني", "danger")
    return redirect(url_for("home.index"))

# =============================
# جميع المطابخ
# =============================
@home.route("/all-kitchens")
def all_kitchens():
    try:
        kitchens = Kitchen.query.filter(
            Kitchen.is_open == 1,
            Kitchen.status == "approved"
        ).all()
    except Exception as e:
        return f"Database Error: {e}"

    cart_count = len(session.get("cart", {}))

    return render_template(
        "main/all_kitchens.html",
        kitchens=kitchens,
        cart_count=cart_count
    )
