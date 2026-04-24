from app import db

class MealImage(db.Model):
    __tablename__ = "meal_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(255), nullable=False)

    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), nullable=False)
    meal = db.relationship("Meal", back_populates="images")

    def __repr__(self):
        return f"<MealImage {self.image}>"
