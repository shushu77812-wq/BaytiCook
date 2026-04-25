from app import db

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 🔑 ربط مع الطلب
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("Order", back_populates="order_items")

    # 🔑 ربط مع الطبق
    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), nullable=False)
    meal = db.relationship("Meal", back_populates="order_items")

    # 🔢 الكمية
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # 💰 السعر وقت الطلب
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem order={self.order_id} meal={self.meal_id} qty={self.quantity} price={self.price}>"
