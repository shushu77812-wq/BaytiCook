from app import db

class MealImage(db.Model):
    __tablename__ = "meal_images"

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    # علاقة مع جدول Meal
    meal = db.relationship("Meal", backref="images")

    def __repr__(self):
        return f"<MealImage {self.id} - {self.image_url}>"
