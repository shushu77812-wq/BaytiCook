from app import db
from app.models.kitchen_model import Kitchen

# عدل كل المطابخ الموجودة
for kitchen in Kitchen.query.all():
    kitchen.status = "approved"
    kitchen.is_open = 1
    kitchen.featured = 1

db.session.commit()
