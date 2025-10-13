"""
VisionCraft AR Marketplace - Complete E-commerce Application
Full-featured application with authentication, shopping cart, orders, and more
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Artwork, CartItem, Order, OrderItem, Like, Event, EventRSVP
import os
from datetime import datetime, timedelta
import secrets

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visioncraft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# File upload configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MODELS_DIR = os.path.join(STATIC_DIR, 'models')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
AVATARS_DIR = os.path.join(STATIC_DIR, 'avatars')

ALLOWED_MODEL_EXT = {'.glb', '.gltf'}
ALLOWED_IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

# Ensure directories exist
for directory in [MODELS_DIR, IMAGES_DIR, AVATARS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor to inject cart count and user info
@app.context_processor
def inject_user_data():
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = current_user.get_cart_count()
    return dict(cart_count=cart_count)

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'customer')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! Welcome, {username}!', 'success')
        login_user(user)
        
        if role == 'seller':
            return redirect(url_for('seller_analytics'))
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.role == 'seller':
                return redirect(url_for('seller_analytics'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('landing'))

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def landing():
    """Landing page - choose between customer or seller"""
    if current_user.is_authenticated:
        if current_user.role == 'seller':
            return redirect(url_for('seller_analytics'))
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
def home():
    """Customer home page with artwork gallery"""
    # Get filter and sort parameters
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'default')
    state = request.args.get('state', '')
    
    # Base query - only active artworks
    query = Artwork.query.filter_by(is_active=True)
    
    # Apply filters
    if category != 'all':
        query = query.filter_by(category=category)
    
    if state:
        query = query.filter_by(state=state)
    
    # Apply sorting
    if sort_by == 'price-low':
        query = query.order_by(Artwork.price.asc())
    elif sort_by == 'price-high':
        query = query.order_by(Artwork.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Artwork.rating.desc())
    elif sort_by == 'likes':
        # Sort by likes count (this requires a subquery or join)
        from sqlalchemy import func
        query = query.outerjoin(Like).group_by(Artwork.id).order_by(func.count(Like.id).desc())
    else:
        query = query.order_by(Artwork.created_at.desc())
    
    artworks = query.all()
    
    # Get user's liked artworks
    liked_artwork_ids = []
    if current_user.is_authenticated:
        liked_artwork_ids = [like.artwork_id for like in current_user.likes.all()]
    
    return render_template('home.html', artworks=artworks, liked_artwork_ids=liked_artwork_ids)

@app.route('/art/<int:art_id>')
def art_detail(art_id):
    """Artwork detail page"""
    art = Artwork.query.get_or_404(art_id)
    
    # Increment view count
    art.views += 1
    db.session.commit()
    
    # Check if user has liked this artwork
    is_liked = False
    if current_user.is_authenticated:
        is_liked = Like.query.filter_by(user_id=current_user.id, artwork_id=art_id).first() is not None
    
    # Get related artworks (same category)
    related_artworks = Artwork.query.filter(
        Artwork.category == art.category,
        Artwork.id != art_id,
        Artwork.is_active == True
    ).limit(4).all()
    
    return render_template('art_detail.html', art=art, is_liked=is_liked, related_artworks=related_artworks)

@app.route('/ar/<int:art_id>')
def view_in_ar(art_id):
    """AR viewer for artwork"""
    art = Artwork.query.get_or_404(art_id)
    return render_template('ar_viewer.html', art=art)

@app.route('/search')
def search():
    """Search artworks"""
    query_text = request.args.get('q', '').lower().strip()
    
    search_results = []
    if query_text:
        search_results = Artwork.query.filter(
            Artwork.is_active == True
        ).filter(
            (Artwork.title.ilike(f'%{query_text}%')) |
            (Artwork.category.ilike(f'%{query_text}%')) |
            (Artwork.artist_name.ilike(f'%{query_text}%')) |
            (Artwork.description.ilike(f'%{query_text}%'))
        ).all()
    
    return render_template('search.html', query=query_text, search_results=search_results)

# ==================== CART ROUTES ====================

@app.route('/cart')
@login_required
def cart():
    """Shopping cart page"""
    cart_items = current_user.cart_items.all()
    
    # Calculate totals
    subtotal = sum(item.get_subtotal() for item in cart_items)
    shipping_fee = 149.0 if subtotal > 0 else 0
    total = subtotal + shipping_fee
    
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, 
                          shipping_fee=shipping_fee, total=total)

@app.route('/api/cart/add/<int:art_id>', methods=['POST'])
@login_required
def add_to_cart(art_id):
    """Add artwork to cart"""
    artwork = Artwork.query.get_or_404(art_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        artwork_id=art_id
    ).first()
    
    if cart_item:
        # Increase quantity
        cart_item.quantity += 1
    else:
        # Create new cart item
        cart_item = CartItem(user_id=current_user.id, artwork_id=art_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{artwork.title} added to cart!',
        'cart_count': current_user.get_cart_count()
    })

@app.route('/api/cart/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_item(cart_item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    # Verify ownership
    if cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    quantity = request.json.get('quantity', 1)
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    return jsonify({'success': True, 'cart_count': current_user.get_cart_count()})

@app.route('/api/cart/remove/<int:cart_item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    # Verify ownership
    if cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'success': True, 'cart_count': current_user.get_cart_count()})

# ==================== CHECKOUT & ORDER ROUTES ====================

@app.route('/checkout')
@login_required
def checkout():
    """Checkout page"""
    cart_items = current_user.cart_items.all()
    
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('cart'))
    
    # Calculate totals
    subtotal = sum(item.get_subtotal() for item in cart_items)
    shipping_fee = 149.0
    total = subtotal + shipping_fee
    
    return render_template('checkout.html', cart_items=cart_items, 
                          subtotal=subtotal, shipping_fee=shipping_fee, total=total)

@app.route('/checkout/process', methods=['POST'])
@login_required
def process_checkout():
    """Process checkout and create order"""
    cart_items = current_user.cart_items.all()
    
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('cart'))
    
    # Get form data
    shipping_name = request.form.get('name', '').strip()
    shipping_email = request.form.get('email', '').strip()
    shipping_phone = request.form.get('phone', '').strip()
    shipping_address = request.form.get('address', '').strip()
    shipping_city = request.form.get('city', '').strip()
    shipping_state = request.form.get('state', '').strip()
    shipping_pincode = request.form.get('pincode', '').strip()
    payment_method = request.form.get('payment_method', 'COD')
    upi_id = request.form.get('upi_id', '')
    
    # Validation
    if not all([shipping_name, shipping_email, shipping_phone, shipping_address, 
                shipping_city, shipping_state, shipping_pincode]):
        flash('Please fill in all shipping details!', 'error')
        return redirect(url_for('checkout'))
    
    # Calculate totals
    subtotal = sum(item.get_subtotal() for item in cart_items)
    shipping_fee = 149.0
    total = subtotal + shipping_fee
    
    # Generate order number
    order_number = f'VC-{datetime.utcnow().strftime("%Y%m%d")}-{secrets.token_hex(4).upper()}'
    
    # Create order
    order = Order(
        order_number=order_number,
        user_id=current_user.id,
        status='pending',
        payment_method=payment_method,
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        total_amount=total,
        shipping_name=shipping_name,
        shipping_email=shipping_email,
        shipping_phone=shipping_phone,
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_pincode=shipping_pincode,
        upi_id=upi_id
    )
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            artwork_id=cart_item.artwork_id,
            artwork_title=cart_item.artwork.title,
            artwork_price=cart_item.artwork.price,
            quantity=cart_item.quantity,
            subtotal=cart_item.get_subtotal()
        )
        db.session.add(order_item)
        
        # Update artwork stock
        cart_item.artwork.stock_quantity -= cart_item.quantity
    
    # Clear cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_confirmation', order_id=order.id))

@app.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    order = Order.query.get_or_404(order_id)
    
    # Verify ownership
    if order.user_id != current_user.id:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))
    
    order_items = order.items.all()
    
    return render_template('order_confirmation.html', order=order, order_items=order_items)

@app.route('/orders')
@login_required
def my_orders():
    """User's order history"""
    orders = current_user.orders.order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

# ==================== LIKES/FAVORITES ROUTES ====================

@app.route('/likes')
@login_required
def likes():
    """User's liked artworks"""
    liked_artworks = [like.artwork for like in current_user.likes.all() if like.artwork.is_active]
    return render_template('likes.html', liked_artworks=liked_artworks)

@app.route('/api/toggle_like/<int:art_id>', methods=['POST'])
@login_required
def toggle_like(art_id):
    """Toggle like status for an artwork"""
    artwork = Artwork.query.get_or_404(art_id)
    
    like = Like.query.filter_by(user_id=current_user.id, artwork_id=art_id).first()
    
    if like:
        # Unlike
        db.session.delete(like)
        db.session.commit()
        return jsonify({'success': True, 'liked': False, 'likes_count': artwork.get_likes_count()})
    else:
        # Like
        like = Like(user_id=current_user.id, artwork_id=art_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'success': True, 'liked': True, 'likes_count': artwork.get_likes_count()})

# TO BE CONTINUED IN NEXT PART...
# APPEND THESE ROUTES TO app_new.py TO COMPLETE THE APPLICATION

# ==================== PROFILE ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Get user's artworks (if seller)
    user_artworks = []
    if current_user.role == 'seller':
        user_artworks = current_user.artworks.filter_by(is_active=True).limit(6).all()
    
    # Get liked artworks
    liked_artworks = [like.artwork for like in current_user.likes.limit(6).all() if like.artwork.is_active]
    
    # Get recent orders
    orders = current_user.orders.order_by(Order.created_at.desc()).limit(3).all()
    
    return render_template('profile.html', 
                         profile=current_user,
                         user_artworks=user_artworks,
                         liked_artworks=liked_artworks,
                         orders=orders)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    current_user.bio = request.form.get('bio', current_user.bio)
    current_user.phone = request.form.get('phone', current_user.phone)
    current_user.location = request.form.get('location', current_user.location)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/profile/avatar', methods=['POST'])
@login_required
def update_avatar():
    """Upload and update user avatar"""
    avatar_file = request.files.get('avatar')
    
    if avatar_file and avatar_file.filename:
        filename = secure_filename(avatar_file.filename)
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ALLOWED_IMAGE_EXT:
            # Create unique filename
            avatar_filename = f"avatar_{current_user.id}_{secrets.token_hex(8)}{ext}"
            dest = os.path.join(AVATARS_DIR, avatar_filename)
            avatar_file.save(dest)
            
            # Update profile
            current_user.avatar = f"/static/avatars/{avatar_filename}"
            db.session.commit()
            
            return jsonify({'success': True, 'avatar_url': current_user.avatar})
    
    return jsonify({'success': False, 'error': 'Invalid file'}), 400

# ==================== SELLER/UPLOAD ROUTES ====================

@app.route('/seller/analytics')
@login_required
def seller_analytics():
    """Seller Analytics Dashboard"""
    if current_user.role != 'seller':
        flash('Access denied! Seller account required.', 'error')
        return redirect(url_for('home'))
    
    # Get seller's artworks
    artworks = current_user.artworks.filter_by(is_active=True).all()
    
    # Calculate metrics
    total_views = sum(art.views for art in artworks)
    total_favorites = sum(art.get_likes_count() for art in artworks)
    total_ar_tries = sum(art.get_ar_tries_count() for art in artworks)
    
    # Calculate revenue from orders
    from sqlalchemy import func
    revenue_query = db.session.query(func.sum(OrderItem.subtotal)).join(
        Artwork
    ).filter(
        Artwork.user_id == current_user.id
    ).scalar()
    total_revenue = revenue_query or 0
    
    return render_template('seller_analytics.html', 
                         artworks=artworks,
                         total_views=total_views,
                         total_favorites=total_favorites,
                         total_ar_tries=total_ar_tries,
                         total_revenue=total_revenue)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload new artwork"""
    if current_user.role != 'seller':
        flash('Upload feature is only available for sellers!', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Other')
        price = request.form.get('price', 0)
        artist_name = request.form.get('artist_name', current_user.username)
        state = request.form.get('state', '')
        making_process = request.form.get('making_process', '')
        stock_quantity = request.form.get('stock_quantity', 10)
        
        # Validate
        if not title or not price:
            flash('Title and price are required!', 'error')
            return render_template('upload.html')
        
        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except ValueError:
            flash('Invalid price or stock quantity!', 'error')
            return render_template('upload.html')
        
        # Get uploaded files
        image = request.files.get('image')
        model = request.files.get('model')
        
        image_url = None
        model_url = None
        
        # Save image
        if image and image.filename:
            filename = secure_filename(image.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_IMAGE_EXT:
                unique_filename = f"{secrets.token_hex(8)}_{filename}"
                dest = os.path.join(IMAGES_DIR, unique_filename)
                image.save(dest)
                image_url = f"/static/images/{unique_filename}"
        
        # Save model
        if model and model.filename:
            filename = secure_filename(model.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_MODEL_EXT:
                unique_filename = f"{secrets.token_hex(8)}_{filename}"
                dest = os.path.join(MODELS_DIR, unique_filename)
                model.save(dest)
                model_url = f"/static/models/{unique_filename}"
        
        # Create artwork
        artwork = Artwork(
            title=title,
            description=description,
            price=price,
            category=category,
            image=image_url or 'https://placehold.co/400x300/cccccc/000000?text=No+Image',
            model_url=model_url,
            user_id=current_user.id,
            artist_name=artist_name,
            state=state,
            making_process=making_process,
            stock_quantity=stock_quantity,
            rating=0.0,
            views=0
        )
        
        db.session.add(artwork)
        db.session.commit()
        
        flash(f'Artwork "{title}" uploaded successfully!', 'success')
        return redirect(url_for('art_detail', art_id=artwork.id))
    
    return render_template('upload.html')

@app.route('/edit/<int:art_id>', methods=['GET', 'POST'])
@login_required
def edit_artwork(art_id):
    """Edit artwork"""
    artwork = Artwork.query.get_or_404(art_id)
    
    # Verify ownership
    if artwork.user_id != current_user.id:
        flash('You can only edit your own artworks!', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        artwork.title = request.form.get('title', artwork.title)
        artwork.description = request.form.get('description', artwork.description)
        artwork.price = float(request.form.get('price', artwork.price))
        artwork.category = request.form.get('category', artwork.category)
        artwork.stock_quantity = int(request.form.get('stock_quantity', artwork.stock_quantity))
        
        db.session.commit()
        flash('Artwork updated successfully!', 'success')
        return redirect(url_for('art_detail', art_id=art_id))
    
    return render_template('edit_artwork.html', artwork=artwork)

@app.route('/api/delete_art/<int:art_id>', methods=['DELETE'])
@login_required
def delete_art(art_id):
    """Delete artwork"""
    artwork = Artwork.query.get_or_404(art_id)
    
    # Verify ownership
    if artwork.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Soft delete (set inactive)
    artwork.is_active = False
    db.session.commit()
    
    return jsonify({'success': True})

# ==================== EVENTS ROUTES ====================

@app.route('/events')
def events():
    """Local Events & Workshops Calendar"""
    events_list = Event.query.filter_by(is_active=True).order_by(Event.event_date).all()
    
    # Mark RSVP status for authenticated users
    events_with_status = []
    for event in events_list:
        event_dict = {
            'id': event.id,
            'title': event.title,
            'type': event.event_type,
            'date': event.event_date.strftime('%Y-%m-%d'),
            'time': event.event_time,
            'location': event.location,
            'address': event.address,
            'description': event.description,
            'tags': event.get_tags_list(),
            'rsvped': False
        }
        
        if current_user.is_authenticated:
            rsvp = EventRSVP.query.filter_by(
                user_id=current_user.id,
                event_id=event.id
            ).first()
            event_dict['rsvped'] = rsvp is not None
        
        events_with_status.append(event_dict)
    
    return render_template('events.html', events=events_with_status)

@app.route('/api/events/rsvp/<int:event_id>', methods=['POST'])
@login_required
def api_rsvp_event(event_id):
    """RSVP to an event"""
    event = Event.query.get_or_404(event_id)
    
    rsvp = EventRSVP.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()
    
    if rsvp:
        # Cancel RSVP
        db.session.delete(rsvp)
        db.session.commit()
        return jsonify({'success': True, 'rsvped': False, 'message': 'RSVP cancelled'})
    else:
        # Create RSVP
        rsvp = EventRSVP(user_id=current_user.id, event_id=event_id)
        db.session.add(rsvp)
        db.session.commit()
        return jsonify({'success': True, 'rsvped': True, 'message': 'RSVP confirmed'})

# ==================== ADDITIONAL FEATURES ====================

@app.route('/wall-stylist')
def wall_stylist():
    """AR Wall Stylist"""
    return render_template('wall_stylist.html')

@app.route('/crafts-map')
def crafts_map():
    """Interactive Crafts Map of India"""
    return render_template('crafts_map.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         message='Page not found',
                         error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html',
                         message='Internal server error',
                         error_code=500), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html',
                         message='Access forbidden',
                         error_code=403), 403

# ==================== MAIN ====================

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    app.run(debug=True, host='0.0.0.0', port=5000)
