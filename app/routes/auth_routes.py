from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, session, url_for
from app import db
from app.models.user_model import User
from app.models.password_reset_model import PasswordReset
from app.models.kitchen_model import Kitchen   # ← لازم نستورد الموديل Kitchen
import random

auth = Blueprint("auth", __name__)

# ----------------------
# تسجيل حساب
# ----------------------
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].strip()
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]

        status = "approved"
        if role == "chef":
            status = "pending"

        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return "رقم الهاتف مستخدم بالفعل"

        if email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return "البريد الإلكتروني مستخدم بالفعل"

        new_user = User(
            name=name,
            email=email if email else None,
            phone=phone,
            role=role,
            status=status
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        if role == "customer":
            session["user_id"] = new_user.id
            session["role"] = new_user.role
            # ✅ الزبون يروح للصفحة الرئيسية الصحيحة
            return redirect(url_for("home.index"))

        return "تم إرسال طلبك للإدارة للموافقة"

    return render_template("register.html")


# ----------------------
# تسجيل دخول
# ----------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        user = User.query.filter_by(phone=phone).first()

        if user and user.check_password(password):
            # التحقق من حالة الحساب
            if user.status == "pending":
                return "⏳ حسابك بانتظار موافقة الأدمن"
            elif user.status == "rejected":
                return "❌ حسابك مرفوض، تواصل مع الإدارة"

            # تخزين بيانات الجلسة
            session["user_id"] = user.id
            session["role"] = user.role

            # التوجيه حسب الدور
            if user.role == "chef":
                kitchen = Kitchen.query.filter_by(user_id=user.id).first()
                if kitchen:
                    return redirect(url_for("chef.dashboard"))
                else:
                    return redirect(url_for("chef.create_kitchen"))
            elif user.role == "admin":
                return redirect("/admin")
            else:
                # الزبون → الصفحة الرئيسية
                return redirect(url_for("home.index"))  # ✅ هذا هو الصحيح
        else:
            return "الرقم أو كلمة المرور غير صحيحة"

    return render_template("login.html")


# ----------------------
# نسيت كلمة المرور - إرسال رمز
# ----------------------
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        phone = request.form.get("phone")
        user = User.query.filter_by(phone=phone).first()
        if not user:
            return "لا يوجد حساب بهذا الرقم"

        code = f"{random.randint(100000, 999999)}"

        pr = PasswordReset(
            user_id=user.id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(pr)
        db.session.commit()

        # ✅ تعديل اسم القالب
        return render_template("home/enter_otp.html", phone=phone)

    # ✅ تعديل اسم القالب
    return render_template("home/forgot_password.html")


# ----------------------
# التحقق من الرمز
# ----------------------
@auth.route("/verify-otp", methods=["POST"])
def verify_otp():
    phone = request.form.get("phone")
    code = request.form.get("code")
    new_password = request.form.get("new_password")

    user = User.query.filter_by(phone=phone).first()
    if not user:
        return "رقم غير موجود"

    pr = PasswordReset.query.filter_by(
        user_id=user.id, code=code, used=False
    ).order_by(PasswordReset.expires_at.desc()).first()

    if not pr or not pr.is_valid():
        return "الرمز غير صحيح أو منتهي الصلاحية"

    user.set_password(new_password)
    pr.used = True
    db.session.commit()

    return "تم تحديث كلمة المرور، يمكنك تسجيل الدخول الآن"

@auth.route("/logout")
def logout():
    # تنظيف السيشن
    session.clear()
    return redirect(url_for("home.index"))
