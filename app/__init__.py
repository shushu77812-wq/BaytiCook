import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "123456789"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    ##app.config["SESSION_PERMANENT"] = False   # 🔥 مهم للسلة

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