from app import create_app, db
from app.models.kitchen_model import Kitchen

# أنشئي التطبيق
app = create_app()

# افتحي سياق التطبيق
with app.app_context():
    # عدلي كل المطابخ الموجودة
    for kitchen in Kitchen.query.all():
        kitchen.status = "approved"
        kitchen.is_open = 1
        kitchen.featured = 1

    db.session.commit()
    print("تم تحديث جميع المطابخ بنجاح ✅")
