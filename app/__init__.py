from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "123456789"

    # ✅ SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ✅ استدعاء الموديلات (بدون مشاكل import *)
    from app.models.kitchen_model import Kitchen
    from app.models.meal_model import Meal
    from app.models.meal_image_model import MealImage
    from app.models.order_model import Order
    from app.models.order_item_model import OrderItem
    from app.models.user_model import User
    from app.models.password_reset_model import PasswordReset

    # ✅ تسجيل الروترات
    from app.routes.home_routes import home
    from app.routes.auth_routes import auth
    from app.routes.admin_routes import admin
    from app.routes.chef_routes import chef
    from app.routes.shop_routes import shop

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(chef)
    app.register_blueprint(shop)

    # ✅ إنشاء الجداول
    with app.app_context():
        db.create_all()

    return app