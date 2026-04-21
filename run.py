from app import create_app, db
import os
from werkzeug.security import generate_password_hash
from app.models.user_model import User

app = create_app()

with app.app_context():
    db.create_all()

    # 🔥 تعديل كلمة مرور الادمن
    user = User.query.filter_by(role="admin").first()
    if user:
        user.password_hash = generate_password_hash("123456")
        db.session.commit()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)