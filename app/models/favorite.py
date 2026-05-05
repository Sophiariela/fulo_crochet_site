from app import db
from app.models.base import TimestampMixin

class Favorite(db.Model, TimestampMixin):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Ensure a user can't favorite the same product multiple times
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_favorite'),)
