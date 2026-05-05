from app import db
from app.models.base import TimestampMixin

class Banner(db.Model, TimestampMixin):
    __tablename__ = 'banners'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(255))
    button_text = db.Column(db.String(50), default='Ver agora')
    image_url = db.Column(db.String(255), nullable=False)
    mobile_image_url = db.Column(db.String(255))
    link_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

class Storytelling(db.Model, TimestampMixin):
    __tablename__ = 'storytelling'
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(50), unique=True, nullable=False) # e.g., 'about_us', 'our_craft'
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    content = db.Column(db.Text)
    button_text = db.Column(db.String(50))
    button_link = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    layout_type = db.Column(db.String(20), default='image_left') # image_left, image_right, full_width
    is_visible = db.Column(db.Boolean, default=True)

class NewsletterSubscriber(db.Model, TimestampMixin):
    __tablename__ = 'newsletter_subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
