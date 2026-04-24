from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app import db
from app.models.user_model import User
from app.models.password_reset_model import PasswordReset
from app.models.kitchen_model import Kitchen
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

        # تحقق من رقم الهاتف
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash("📱 رقم الهاتف مستخدم بالفعل.", "danger")
            return redirect(url_for("auth.register"))

        # تحقق من البريد الإلكتروني
        if email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("📧 البريد الإلكتروني مستخدم بالفعل.", "danger")
                return redirect(url_for("auth.register"))

        # إنشاء مستخدم جديد
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
            flash("✅ تم إنشاء الحساب بنجاح!", "success")
            return redirect(url_for("home.index"))

        flash("⏳ تم إرسال طلبك للإدارة للموافقة.", "info")
        return redirect(url_for("auth.login"))

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
                flash("⏳ حسابك بانتظار موافقة الأدمن.", "warning")
                return redirect(url_for("auth.login"))

            elif user.status == "rejected":
                flash("❌ حسابك مرفوض، تواصل مع الإدارة.", "danger")
                return redirect(url_for("auth.login"))

            # ✅ حفظ الجلسة بعد التأكد
            session["user_id"] = user.id
            session["role"] = user.role

            # 🔥 التوجيه حسب الدور
            if user.role == "chef":
                kitchen = Kitchen.query.filter_by(user_id=user.id).first()
                if kitchen:
                    flash("👩‍🍳 مرحبًا بك في لوحة التحكم!", "success")
                    return redirect(url_for("chef.dashboard"))
                else:
                    flash("✨ أنشئ مطبخك الأول الآن!", "info")
                    return redirect(url_for("chef.create_kitchen"))

            elif user.role == "admin":
                flash("🔧 مرحبًا بك في لوحة الأدمن.", "success")
                return redirect("/admin")

            else:  # customer
                flash("🍽️ أهلاً بك في BaytiCook!", "success")
                return redirect(url_for("home.index"))

        else:
            flash("⚠️ الرقم أو كلمة المرور غير صحيحة.", "danger")
            return redirect(url_for("auth.login"))

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
            flash("❌ لا يوجد حساب بهذا الرقم.", "danger")
            return redirect(url_for("auth.forgot_password"))

        code = f"{random.randint(100000, 999999)}"

        pr = PasswordReset(
            user_id=user.id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(pr)
        db.session.commit()

        flash("📩 تم إرسال رمز التحقق، أدخله لتغيير كلمة المرور.", "info")
        return render_template("home/enter_otp.html", phone=phone)

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
        flash("❌ رقم غير موجود.", "danger")
        return redirect(url_for("auth.forgot_password"))

    pr = PasswordReset.query.filter_by(
        user_id=user.id, code=code, used=False
    ).order_by(PasswordReset.expires_at.desc()).first()

    if not pr or not pr.is_valid():
        flash("⚠️ الرمز غير صحيح أو منتهي الصلاحية.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user.set_password(new_password)
    pr.used = True
    db.session.commit()

    flash("✅ تم تحديث كلمة المرور، يمكنك تسجيل الدخول الآن.", "success")
    return redirect(url_for("auth.login"))


# ----------------------
# تسجيل خروج
# ----------------------
@auth.route("/logout")
def logout():
    session.clear()
    flash("👋 تم تسجيل الخروج بنجاح.", "info")
    return redirect(url_for("home.index"))
