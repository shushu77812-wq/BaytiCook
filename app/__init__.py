from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from dotenv import load_dotenv   # ✅ إضافة مكتبة dotenv

db = SQLAlchemy()
mail = Mail()   # ✅ تهيئة البريد

def create_app():
    # ✅ تحميل القيم من ملف .env
    load_dotenv()

    app = Flask(__name__)

    # ✅ القيم من ملف .env
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "123456789")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ إعدادات البريد من ملف .env
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

    db.init_app(app)
    mail.init_app(app)

    # ✅ استيراد الموديلات (تأكد أن MealImage موجود في ملف واحد فقط)
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
