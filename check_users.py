from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Users found: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Name: {u.name}")
