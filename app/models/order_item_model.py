from app import db

class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    meal_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)