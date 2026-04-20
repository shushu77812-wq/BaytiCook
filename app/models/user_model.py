from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    # نخزن كلمة المرور مشفرة بدل نص عادي
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")
    
    # علاقة مع جدول Kitchen (إذا عندك جدول مطابخ)
    kitchen = db.relationship("Kitchen", backref="user", uselist=False)

    # دوال مساعدة للتعامل مع كلمة المرور
    def set_password(self, password):
        """تشفير كلمة المرور وتخزينها في العمود password_hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور عند تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)
