from app import db

class MealImage(db.Model):

    __tablename__ = "meal_images"

    id = db.Column(db.Integer, primary_key=True)

    meal_id = db.Column(
        db.Integer,
        db.ForeignKey("meals.id"),   # هذا السطر مهم
        nullable=False
    )

    image = db.Column(db.String(255))