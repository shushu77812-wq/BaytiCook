from app import create_app, db
import os
from werkzeug.security import generate_password_hash
from app.models.user_model import User

app = create_app()

with app.app_context():
    db.create_all()

    # 🔥 إنشاء أدمن إذا ما كان موجود
    admin = User.query.filter_by(phone="781765358").first()

    if not admin:
        admin = User(
            name="Admin",
            phone="781765358",
            password_hash=generate_password_hash("123456"),
            role="admin",
            status="approved"
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
