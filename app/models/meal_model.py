from app import db

class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

    # 🔑 ربط مع المطبخ
    kitchen_id = db.Column(db.Integer, db.ForeignKey("kitchens.id"), nullable=False)
    kitchen = db.relationship("Kitchen", back_populates="meals")

    # 🖼️ صور الأكلة
    images = db.relationship("MealImage", back_populates="meal", cascade="all, delete-orphan")

    # 🟢 حالة الطبق (approved / pending)
    status = db.Column(db.String(20), default="pending")

    # 🟢 التمييز (0 = عادي، 1 = مميز)
    is_featured = db.Column(db.Integer, default=0)

    # 🟢 التوفر اليومي (1 = متوفر، 0 = غير متوفر)
    is_available = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Meal {self.name}>"

# =============================
# جدول صور الأكلات
# =============================
class MealImage(db.Model):
    __tablename__ = "meal_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(255), nullable=False)

    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), nullable=False)
    meal = db.relationship("Meal", back_populates="images")

    def __repr__(self):
        return f"<MealImage {self.image}>"
