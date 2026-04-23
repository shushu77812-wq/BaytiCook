from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()   # ✅ تهيئة البريد

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "123456789"

    # ✅ SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ إعدادات البريد
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")  # بريدك
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")  # كلمة مرور التطبيقات

    db.init_app(app)
    mail.init_app(app)   # ✅ ربط البريد مع التطبيق

    # ✅ استدعاء الموديلات
    from app.models.kitchen_model import Kitchen
    from app.models.meal_model import Meal
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
