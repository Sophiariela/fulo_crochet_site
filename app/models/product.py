from app import db
from app.models.base import TimestampMixin

class Category(db.Model, TimestampMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    
    products = db.relationship('Product', backref='category_rel', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model, TimestampMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(255)) # Main image
    image_url_2 = db.Column(db.String(255)) # Hover image
    image_url_3 = db.Column(db.String(255))
    image_url_4 = db.Column(db.String(255))
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    collection = db.Column(db.String(100)) # e.g., 'Brasilidade', 'Lançamentos'
    stock = db.Column(db.Integer, default=0)
    sizes = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    technical_details = db.Column(db.Text) # JSON or markdown string
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    favorited_by = db.relationship('Favorite', backref='product', lazy=True)

    @property
    def category_name(self):
        return self.category_rel.name if self.category_rel else "Sem Categoria"
