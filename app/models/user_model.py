from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="customer")
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    kitchen = db.relationship("Kitchen", backref="user", uselist=False)

    # علاقة مع الطلبات (اللي سجلها المستخدم)
    orders = db.relationship(
        "Order",
        back_populates="user",
        foreign_keys="Order.user_id",
        cascade="all, delete-orphan"
    )

    # علاقة مع الطلبات كعميل
    customer_orders = db.relationship(
        "Order",
        back_populates="customer",
        foreign_keys="Order.customer_id"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name} - {self.role} - {self.status}>"
