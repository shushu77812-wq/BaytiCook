from app import db

class Kitchen(db.Model):
    __tablename__ = "kitchens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    kitchen_name = db.Column(db.String(150), nullable=False)
    kitchen_logo = db.Column(db.String(255))   # مطابق للجدول
    bank_account_name = db.Column(db.String(150))
    bank_account_number = db.Column(db.String(100))

    # ✅ تعديل ENUM إلى String
    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ✅ تعديل Boolean إلى Integer
    featured = db.Column(db.Integer, default=0)  # 0 = عادي، 1 = مميز
    is_open = db.Column(db.Integer, default=1)   # 1 = مفتوح، 0 = مغلق

    location = db.Column(db.String(150))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Kitchen {self.kitchen_name}>"
