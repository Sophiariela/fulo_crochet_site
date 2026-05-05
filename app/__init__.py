from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        if not user_id:
            return None
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    from app import models
    
    # Import Blueprints
    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.cart import cart_bp
    from app.routes.checkout import checkout_bp
    
    # Register Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    
    @app.context_processor
    def inject_cart_count():
        from app.services.cart_service import CartService
        from flask_login import current_user
        try:
            items, _ = CartService.get_cart_data(current_user)
            # items is a list of dicts, so use item['quantity']
            count = sum(item['quantity'] for item in items)
        except Exception:
            count = 0
        return dict(cart_count=count)
    
    return app
