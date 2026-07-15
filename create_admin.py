from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    user = User.query.filter_by(email='admin@fulo.com').first()

    if not user:

        admin = User( 
            name='Admin',
            email='admin@fulo.com', 
            password=generate_password_hash('admin123', method='sha256'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('ADMIN CRIADO')