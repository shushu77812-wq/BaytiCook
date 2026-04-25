from app import db, create_app
from app.models.user_model import User

app = create_app()

with app.app_context():
    # ابحث عن المستخدم برقم الهاتف
    user = User.query.filter_by(phone="781765358").first()
    if not user:
        # إذا ما فيه مستخدم، أنشئ واحد جديد كأدمن
        user = User(
            name="شروق يحيى محمد",
            phone="781765358",
            role="admin",
            status="approved"
        )
        user.set_password("2002")  # كلمة المرور اللي تختاريها
        db.session.add(user)
        db.session.commit()
        print("✅ تم إنشاء حساب الأدمن بنجاح")
    else:
        # إذا موجود، بس عدل الدور والحالة
        user.role = "admin"
        user.status = "approved"
        user.set_password("2002")  # تحديث كلمة المرور
        db.session.commit()
        print("✅ تم تحديث المستخدم ليكون أدمن")
