from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admins = User.query.filter_by(is_admin=True).all()
    print(f"Admins found: {len(admins)}")
    for a in admins:
        print(f"ID: {a.id}, Email: {a.email}, Name: {a.name}")
