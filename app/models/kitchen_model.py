from app import db

class Kitchen(db.Model):
    __tablename__ = "kitchens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    kitchen_name = db.Column(db.String(150), nullable=False)
    kitchen_logo = db.Column(db.String(255))   # مطابق للجدول
    bank_account_name = db.Column(db.String(150))
    bank_account_number = db.Column(db.String(100))
    status = db.Column(db.Enum("pending", "approved"), default="pending")
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    featured = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    is_open = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Kitchen {self.kitchen_name}>"
