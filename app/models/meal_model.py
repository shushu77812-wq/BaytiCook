from app import db

class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    kitchen_id = db.Column(db.Integer, db.ForeignKey("kitchens.id"))

    # الحالة (متاح/غير متاح)
    is_available = db.Column(db.Boolean, default=True)

    # العلاقة مع المطبخ
    kitchen = db.relationship("Kitchen", backref="meals")

    # العلاقة مع الصور
    images = db.relationship(
        "MealImage",
        backref="meal",
        lazy=True,
        cascade="all, delete"
    )
