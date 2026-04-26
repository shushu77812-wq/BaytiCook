from app import db

class Kitchen(db.Model):
    __tablename__ = "kitchens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    kitchen_name = db.Column(db.String(150), nullable=False)
    kitchen_logo = db.Column(db.String(255))   # صورة شعار المطبخ
    bank_account_name = db.Column(db.String(150))
    bank_account_number = db.Column(db.String(100))

    # الحقول الجديدة
    chef_name = db.Column(db.String(150))   # اسم الطاهية
    chef_phone = db.Column(db.String(50))   # رقم الطاهية

    # حالة المطبخ: pending / approved / rejected
    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # مميز أو عادي
    featured = db.Column(db.Integer, default=0)  # 0 = عادي، 1 = مميز
    # مفتوح أو مغلق
    is_open = db.Column(db.Integer, default=1)   # 1 = مفتوح، 0 = مغلق

    # الموقع أو نقطة الاستلام
    location = db.Column(db.String(150))
    address = db.Column(db.String(255))  # أدق من location

    description = db.Column(db.Text)

    # العلاقة مع الأطباق
    meals = db.relationship("Meal", back_populates="kitchen", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Kitchen {self.kitchen_name}>"
