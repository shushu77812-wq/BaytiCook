from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from sqlalchemy import or_
from app import db
from app.models import User, Kitchen, Meal, MealImage, Order

chef = Blueprint("chef", __name__)

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# تأكد من إنشاء المجلد
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# لوحة التحكم
@chef.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    kitchen = Kitchen.query.filter_by(user_id=user_id).first()

    if not kitchen:
        flash("⚠️ يجب إنشاء مطبخ أولاً")
        return redirect(url_for("chef.create_kitchen"))

    meals_count = Meal.query.filter_by(kitchen_id=kitchen.id).count()
    orders = Order.query.filter_by(kitchen_id=kitchen.id).all()
    orders_count = len(orders)
    preparing_count = Order.query.filter_by(kitchen_id=kitchen.id, status="preparing").count()
    completed_count = Order.query.filter_by(kitchen_id=kitchen.id, status="completed").count()
    cancelled_count = Order.query.filter_by(kitchen_id=kitchen.id, status="cancelled").count()
    pending_count = Order.query.filter_by(kitchen_id=kitchen.id, status="pending").count()

    return render_template(
        "chef/dashboard.html",
        user=user,
        meals_count=meals_count,
        orders_count=orders_count,
        preparing_count=preparing_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        pending_count=pending_count
    )

# إنشاء مطبخ
@chef.route("/create_kitchen", methods=["GET", "POST"])
def create_kitchen():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)

    if request.method == "POST":
        kitchen_name = request.form.get("kitchen_name")
        kitchen_logo_file = request.files.get("kitchen_logo")  
        description = request.form.get("description")

        # ✅ الحقول الجديدة
        location = request.form.get("location")
        address = request.form.get("address")
        
        logo_filename = None
        if kitchen_logo_file and kitchen_logo_file.filename != "" and allowed_file(kitchen_logo_file.filename):
            logo_filename = secure_filename(kitchen_logo_file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, logo_filename)
            kitchen_logo_file.save(save_path)

        new_kitchen = Kitchen(
            kitchen_name=kitchen_name,
            kitchen_logo=logo_filename,             
            description=description,
            user_id=user_id,
            location=location,   # ✅ جديد
            address=address      # ✅ جديد
        )

        db.session.add(new_kitchen)
        db.session.commit()

        flash("✅ تم إنشاء المطبخ بنجاح")
        return redirect(url_for("chef.dashboard"))

    return render_template("chef/create_kitchen.html", user=user)

# إدارة الأطباق
@chef.route("/meals", methods=["GET", "POST"])
def meals():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    kitchen = Kitchen.query.filter_by(user_id=user_id).first()

    if not kitchen:
        flash("⚠️ يجب إنشاء مطبخ أولاً")
        return redirect(url_for("chef.create_kitchen"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price"))

        new_meal = Meal(
            name=name,
            description=description,
            price=price,
            kitchen_id=kitchen.id,
            is_available=True
        )
        db.session.add(new_meal)
        db.session.commit()

        images = request.files.getlist("images")
        for img in images:
            if img and img.filename != "" and allowed_file(img.filename):
                filename = secure_filename(img.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                img.save(save_path)

                meal_img = MealImage(image=filename, meal_id=new_meal.id)
                db.session.add(meal_img)

        db.session.commit()
        flash("✅ تم إضافة الطبق بنجاح")
        return redirect(url_for("chef.meals"))

    query = request.args.get("q")
    if query:
        meals = Meal.query.filter(
            Meal.kitchen_id == kitchen.id,
            or_(Meal.name.contains(query), Meal.description.contains(query))
        ).all()
    else:
        meals = Meal.query.filter_by(kitchen_id=kitchen.id).all()

    return render_template("chef/meals.html", meals=meals, user=user)

# تعديل طبق
@chef.route("/meals/edit/<int:meal_id>", methods=["GET", "POST"])
def edit_meal(meal_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    meal = Meal.query.get_or_404(meal_id)

    if request.method == "POST":
        meal.name = request.form.get("name")
        meal.description = request.form.get("description")
        meal.price = float(request.form.get("price"))

        images = request.files.getlist("images")
        for img in images:
            if img and img.filename != "" and allowed_file(img.filename):
                filename = secure_filename(img.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                img.save(save_path)

                new_img = MealImage(image=filename, meal_id=meal.id)
                db.session.add(new_img)

        db.session.commit()
        flash("✅ تم تعديل الطبق بنجاح")
        return redirect(url_for("chef.meals"))

    return render_template("chef/edit_meal.html", meal=meal, user=user)

# إدارة الطلبات
@chef.route("/orders")
def orders():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    kitchen = Kitchen.query.filter_by(user_id=user_id).first()

    if not kitchen:
        flash("⚠️ يجب إنشاء مطبخ أولاً")
        return redirect(url_for("chef.create_kitchen"))

    orders = Order.query.filter_by(kitchen_id=kitchen.id).all()

    orders_count = len(orders)
    preparing_count = Order.query.filter_by(kitchen_id=kitchen.id, status="preparing").count()
    completed_count = Order.query.filter_by(kitchen_id=kitchen.id, status="completed").count()
    cancelled_count = Order.query.filter_by(kitchen_id=kitchen.id, status="cancelled").count()
    pending_count = Order.query.filter_by(kitchen_id=kitchen.id, status="pending").count()

    return render_template(
        "chef/orders.html",
        user=user,
        orders=orders,
        orders_count=orders_count,
        preparing_count=preparing_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        pending_count=pending_count
    )

@chef.route("/orders/update/<int:order_id>/<string:new_status>")
def update_order(order_id, new_status):
    order = Order.query.get_or_404(order_id)

    if new_status in ["pending", "preparing", "completed", "cancelled"]:
        order.status = new_status
        db.session.commit()
        flash(f"✅ تم تحديث حالة الطلب إلى {new_status}")
    else:
        flash("❌ حالة غير صحيحة")

    return redirect(url_for("chef.orders"))

# عرض طبق
@chef.route("/meals/view/<int:meal_id>")
def view_meal(meal_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    meal = Meal.query.get_or_404(meal_id)
    images = MealImage.query.filter_by(meal_id=meal.id).all()

    return render_template("chef/view_meal.html", meal=meal, images=images)

# تسجيل الخروج
@chef.route("/logout")
def logout():
    session.clear()
    flash("🚪 تم تسجيل الخروج بنجاح")
    return redirect(url_for("auth.login"))
