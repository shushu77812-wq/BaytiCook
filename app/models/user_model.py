from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    # نخزن كلمة المرور مشفرة بدل نص عادي
    password_hash = db.Column(db.String(200), nullable=False)

    # دور المستخدم: customer / chef / admin
    role = db.Column(db.String(20), nullable=False, default="customer")

    # حالة الحساب للطاهية: pending / approved / rejected
    status = db.Column(db.String(20), default="pending")

    # وقت إنشاء الحساب
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # علاقة مع جدول Kitchen (إذا عنده مطبخ واحد)
    kitchen = db.relationship("Kitchen", backref="user", uselist=False)

    # علاقة مع الطلبات
    orders = db.relationship("Order", backref="user", lazy=True, foreign_keys="Order.user_id")

    # دوال مساعدة للتعامل مع كلمة المرور
    def set_password(self, password):
        """تشفير كلمة المرور وتخزينها في العمود password_hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور عند تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name} - {self.role} - {self.status}>"
