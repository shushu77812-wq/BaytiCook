from app import db
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = "password_resets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 🔑 ربط مع المستخدم
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="password_resets")

    # رمز التحقق (OTP)
    code = db.Column(db.String(10), nullable=False)

    # وقت انتهاء صلاحية الرمز
    expires_at = db.Column(db.DateTime, nullable=False)

    # هل تم استخدام الرمز أم لا
    used = db.Column(db.Boolean, default=False)

    # وقت الإنشاء
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_valid(self):
        """يتحقق إذا الرمز صالح للاستخدام"""
        return (not self.used) and (datetime.utcnow() < self.expires_at)

    def __repr__(self):
        return f"<PasswordReset user={self.user_id} code={self.code}>"
