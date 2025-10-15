"""
Database models for VisionCraft AR Marketplace
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profiles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')  # 'customer' or 'seller'
    
    # Profile information
    bio = db.Column(db.Text, default='')
    phone = db.Column(db.String(20), default='')
    location = db.Column(db.String(100), default='')
    avatar = db.Column(db.String(200), default=None)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    artworks = db.relationship('Artwork', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    rsvps = db.relationship('EventRSVP', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def get_cart_count(self):
        """Get number of items in cart"""
        return self.cart_items.count()
    
    def get_total_spent(self):
        """Calculate total amount spent"""
        completed_orders = self.orders.filter_by(status='delivered').all()
        return sum(order.total_amount for order in completed_orders)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Artwork(db.Model):
    """Artwork/Product model"""
    __tablename__ = 'artworks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(50), nullable=False, index=True)
    
    # Media
    image = db.Column(db.String(300), default='')
    model_url = db.Column(db.String(300), default='')
    
    # Artisan information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artist_name = db.Column(db.String(100), default='')
    state = db.Column(db.String(100), default='')
    making_process = db.Column(db.Text, default='')
    
    # Stats
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    
    # Inventory
    stock_quantity = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    likes = db.relationship('Like', backref='artwork', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='artwork', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='artwork', lazy='dynamic')
    
    def get_likes_count(self):
        """Get number of likes"""
        return self.likes.count()
    
    def get_ar_tries_count(self):
        """Get number of AR views (estimated from views)"""
        return int(self.views * 0.15)  # Estimate 15% of viewers try AR
    
    def is_in_stock(self):
        """Check if item is in stock"""
        return self.stock_quantity > 0
    
    def __repr__(self):
        return f'<Artwork {self.title}>'


class CartItem(db.Model):
    """Shopping cart items"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.artwork.price * self.quantity
    
    def __repr__(self):
        return f'<CartItem user={self.user_id} artwork={self.artwork_id}>'


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order details
    status = db.Column(db.String(30), default='pending')  # pending, processing, shipped, delivered, cancelled
    payment_method = db.Column(db.String(30), default='')
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    shipping_fee = db.Column(db.Float, default=149.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Shipping information
    shipping_name = db.Column(db.String(100), nullable=False)
    shipping_email = db.Column(db.String(120), nullable=False)
    shipping_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(100), nullable=False)
    shipping_pincode = db.Column(db.String(10), nullable=False)
    
    # Payment details (for UPI)
    upi_id = db.Column(db.String(100), default='')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)
    
    # Snapshot of artwork details at time of order
    artwork_title = db.Column(db.String(200), nullable=False)
    artwork_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem order={self.order_id} artwork={self.artwork_id}>'


class Like(db.Model):
    """User likes/favorites for artworks"""
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: user can like an artwork only once
    __table_args__ = (db.UniqueConstraint('user_id', 'artwork_id', name='unique_user_artwork_like'),)
    
    def __repr__(self):
        return f'<Like user={self.user_id} artwork={self.artwork_id}>'


class Event(db.Model):
    """Events and workshops"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    event_type = db.Column(db.String(50), nullable=False)  # Fair, Workshop, Class, Exhibition
    
    # Date and time
    event_date = db.Column(db.Date, nullable=False, index=True)
    event_time = db.Column(db.String(20), default='')
    
    # Location
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, default='')
    
    # Tags (comma-separated)
    tags = db.Column(db.String(300), default='')
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    rsvps = db.relationship('EventRSVP', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_rsvp_count(self):
        """Get number of RSVPs"""
        return self.rsvps.count()
    
    def get_tags_list(self):
        """Get tags as list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def __repr__(self):
        return f'<Event {self.title}>'


class EventRSVP(db.Model):
    """Event RSVPs"""
    __tablename__ = 'event_rsvps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: user can RSVP to an event only once
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_user_event_rsvp'),)
    
    def __repr__(self):
        return f'<EventRSVP user={self.user_id} event={self.event_id}>'
