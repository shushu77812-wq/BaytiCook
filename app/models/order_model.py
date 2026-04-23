from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 🔑 ربط الطلب بالمستخدم (اللي سجل الدخول)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="orders", foreign_keys=[user_id])

    # 🔑 ربط الطلب بالعميل (ممكن نفس المستخدم أو شخص آخر)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = db.relationship("User", foreign_keys=[customer_id])

    customer_name = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # 💰 السعر الإجمالي
    total_price = db.Column(db.Float, nullable=False)

    # 📌 حالة الطلب: new / pending / preparing / delivered / cancelled
    status = db.Column(db.String(50), default="new")

    # 💳 طريقة الدفع: bank / cash
    payment_method = db.Column(db.String(20), default="cash")

    # 🖼️ صورة إثبات التحويل البنكي
    proof_image = db.Column(db.String(200))

    # 🔑 ربط مع المطبخ
    kitchen_id = db.Column(db.Integer, db.ForeignKey("kitchens.id"), nullable=False)
    kitchen = db.relationship("Kitchen", backref="orders")

    # 🔗 العلاقة مع العناصر (OrderItem)
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
