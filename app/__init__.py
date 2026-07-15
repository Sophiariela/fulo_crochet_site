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
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        from app import models # Register models

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        if not user_id:
            return None
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError, Exception):
            return None
    
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
    def inject_global_data():
        from app.services.cart_service import CartService
        from app.models.cms import PopupConfig
        from flask_login import current_user
        try:
            items, _ = CartService.get_cart_data(current_user)
            count = sum(item.get('quantity', 0) for item in items)
        except Exception:
            count = 0
            
        popup_config = PopupConfig.query.first()
        
        return dict(cart_count=count, popup_config=popup_config, config=app.config)
    
    return app
