from app import db
from app.models.base import TimestampMixin

class Order(db.Model, TimestampMixin):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending') # pending, paid, shipped, delivered, cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    shipping_address = db.relationship('Address', lazy=True)

class OrderItem(db.Model, TimestampMixin):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Numeric(10, 2), nullable=False)
