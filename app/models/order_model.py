from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    # ربط الطلب بالمستخدم (اللي سجل الدخول)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="orders", foreign_keys=[user_id])

    # ربط الطلب بالعميل (ممكن نفس المستخدم أو شخص آخر)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = db.relationship("User", foreign_keys=[customer_id])

    customer_name = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="new")
    proof_image = db.Column(db.String(200))

    kitchen_id = db.Column(db.Integer, db.ForeignKey("kitchens.id"), nullable=False)
    kitchen = db.relationship("Kitchen", backref="orders")

    meals = db.relationship("Meal", secondary="order_meals", backref="orders")


order_meals = db.Table(
    "order_meals",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id"), primary_key=True)
)
