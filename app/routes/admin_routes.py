from flask import Blueprint, render_template, redirect, url_for
from app import db
from app.models.user_model import User
from app.models.meal_model import Meal
from app.models.order_model import Order
from app.models.kitchen_model import Kitchen

admin = Blueprint("admin", __name__)

# لوحة التحكم الرئيسية
@admin.route("/admin")
def admin_dashboard():
    chefs_count = User.query.filter_by(role="chef").count()
    meals_count = Meal.query.count()
    orders_count = Order.query.count()
    users_count = User.query.count()

    return render_template(
        "admin/dashboard.html",
        chefs_count=chefs_count,
        meals_count=meals_count,
        orders_count=orders_count,
        users_count=users_count
    )

# إدارة الطاهيات
@admin.route("/admin/chefs")
def admin_chefs():
    chefs = User.query.filter_by(role="chef").all()
    return render_template("admin/chefs.html", chefs=chefs)

# الموافقة على الطاهية
@admin.route("/admin/approve-chef/<int:id>")
def approve_chef(id):
    chef = User.query.get_or_404(id)
    chef.status = "approved"
    db.session.commit()
    return redirect("/admin/chefs")

# رفض الطاهية
@admin.route("/admin/reject-chef/<int:id>")
def reject_chef(id):
    chef = User.query.get_or_404(id)
    chef.status = "rejected"
    db.session.commit()
    return redirect("/admin/chefs")

# إدارة المطابخ
@admin.route("/admin/kitchens")
def kitchens():
    kitchens = Kitchen.query.all()
    return render_template("admin/kitchens.html", kitchens=kitchens)

# فتح/إغلاق المطبخ
@admin.route("/admin/toggle-kitchen/<int:kitchen_id>")
def toggle_kitchen(kitchen_id):
    kitchen = Kitchen.query.get_or_404(kitchen_id)
    kitchen.is_open = not kitchen.is_open
    db.session.commit()
    return redirect("/admin/kitchens")  # ✅ تعديل

# ⭐ تمييز / إلغاء تمييز المطبخ
@admin.route("/admin/toggle-feature/<int:kitchen_id>")
def toggle_feature(kitchen_id):
    kitchen = Kitchen.query.get_or_404(kitchen_id)
    kitchen.featured = not kitchen.featured
    db.session.commit()
    return redirect("/admin/kitchens")

# إدارة الأكلات
@admin.route("/admin/meals")
def admin_meals():
    meals = Meal.query.all()
    return render_template("admin/meals.html", meals=meals)

# حذف أكلة
@admin.route('/admin/delete-meal/<int:meal_id>')
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    try:
        db.session.delete(meal)
        db.session.commit()
        return redirect(url_for('admin.admin_meals'))
    except Exception as e:
        db.session.rollback()
        return f"خطأ: {e}"

# إدارة الطلبات
@admin.route("/admin/orders")
def admin_order():
    orders = Order.query.all()
    return render_template("admin/orders.html", orders=orders)

# حذف طاهية
@admin.route('/admin/delete-chef/<int:chef_id>')
def delete_chef(chef_id):
    chef = User.query.get_or_404(chef_id)
    try:
        kitchen = Kitchen.query.filter_by(user_id=chef.id).first()
        if kitchen:
            db.session.delete(kitchen)
        db.session.delete(chef)
        db.session.commit()
        return redirect(url_for('admin.admin_chefs'))
    except Exception as e:
        db.session.rollback()
        return f"خطأ: {e}"


# ✅ تحديث حالة الطلب 
@admin.route("/admin/update-order/<int:order_id>/<string:new_status>")
def update_order(order_id, new_status):
    order = Order.query.get_or_404(order_id)

    if new_status in ["preparing", "delivered"]:
        order.status = new_status
        db.session.commit()

    return redirect("/admin/orders")