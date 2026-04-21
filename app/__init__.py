import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456789"

    # أولاً نحاول نقرأ DATABASE_URL (لـ Render)
    uri = os.environ.get("DATABASE_URL")

    if uri:
        if uri.startswith("mysql://"):
            uri = uri.replace("mysql://", "mysql+pymysql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
    else:
        # إذا ما فيه DATABASE_URL (يعني محلي)، نستخدم MySQL المحلي
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/bayticook"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

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

    return app
