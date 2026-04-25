from app import create_app, db
from app.models.user_model import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(phone="781765358").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("🗑️ تم حذف المستخدم القديم")

    new_user = User(
        name="شروق يحيى محمد",
        phone="781765358",
        role="admin",
        status="approved"
    )
    new_user.set_password("2002")
    db.session.add(new_user)
    db.session.commit()
    print("✅ تم إنشاء حساب الأدمن من جديد")

