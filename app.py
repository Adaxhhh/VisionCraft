from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('VISIONCRAFT_SECRET', 'dev-secret-change-me')

# --- Advanced Data Structure: Artworks and Artist Info ---
# Added more complex fields like artist, category, model_url, and likes_count
artworks = [
    {
        "id": 1,
        "title": "Terracotta Pot of Marwar",
        "artist": "Sanjay Varma",
        "price": 299,
        "image": "/static/images/pottery.jpg",
        "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
        "category": "Pottery",
        "likes_count": 145,
        "rating": 4.8,
        "description": "Handmade terracotta pot from Rajasthan, featuring traditional Marwari motifs. Ideal for rustic decor.",
        "state": "Rajasthan",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "video_thumbnail": "https://placehold.co/400x300/8B4513/ffffff?text=Making+Pottery",
        "making_process": "Traditional clay molding and hand-painting technique passed down through generations",
        "views": 1247,
        "favorites": 89,
        "ar_tries": 156
    },
    {
        "id": 2,
        "title": "Cosmic Elephant Toy",
        "artist": "Priya Sharma",
        "price": 499,
        "image": "/static/images/wooden_toy.jpg",
        "model_url": "https://modelviewer.dev/shared-assets/models/RobotExpressive/RobotExpressive.glb",
        "category": "Woodcraft",
        "likes_count": 92,
        "rating": 4.5,
        "description": "A beautifully carved wooden elephant toy from Karnataka, painted with vibrant, non-toxic colors.",
        "state": "Karnataka",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "video_thumbnail": "https://placehold.co/400x300/D2691E/ffffff?text=Wood+Carving",
        "making_process": "Hand-carved from sustainable sandalwood with traditional Channapatna techniques",
        "views": 892,
        "favorites": 67,
        "ar_tries": 134
    },
    {
        "id": 3,
        "title": "Himalayan Bamboo Weave",
        "artist": "Tenzin Gyatso",
        "price": 349,
        "image": "/static/images/basket.jpg",
        "model_url": "https://modelviewer.dev/shared-assets/models/Chair/Chair.glb",
        "category": "Weaving",
        "likes_count": 301,
        "rating": 4.9,
        "description": "Eco-friendly, hand-woven bamboo basket from the foothills of Assam. Durable and lightweight."
    },
    {
        "id": 4,
        "title": "Indigo Dye Scarf",
        "artist": "Meena Khan",
        "price": 899,
        "image": "https://placehold.co/400x300/3c5a77/ffffff?text=Indigo+Scarf",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/DamagedHelmet/glTF/DamagedHelmet.gltf",
        "category": "Textiles",
        "likes_count": 210,
        "rating": 4.6,
        "description": "Traditional block-printed cotton scarf using natural indigo dyes."
    },
    {
        "id": 5,
        "title": "Bronze Ganesha Sculpture",
        "artist": "Ramesh Patel",
        "price": 1599,
        "image": "https://placehold.co/400x300/8B4513/ffffff?text=Ganesha",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/BrainStem/glTF/BrainStem.gltf",
        "category": "Sculpture",
        "likes_count": 456,
        "rating": 5.0,
        "description": "Exquisite bronze sculpture of Lord Ganesha, handcrafted using ancient lost-wax casting technique."
    },
    {
        "id": 6,
        "title": "Madhubani Fish Painting",
        "artist": "Lakshmi Devi",
        "price": 799,
        "image": "https://placehold.co/400x300/FF6347/ffffff?text=Madhubani+Art",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/MetalRoughSpheres/glTF/MetalRoughSpheres.gltf",
        "category": "Painting",
        "likes_count": 234,
        "rating": 4.7,
        "description": "Traditional Madhubani folk art from Bihar, depicting colorful fish symbolizing prosperity."
    },
    {
        "id": 7,
        "title": "Kashmiri Papier-Mâché Box",
        "artist": "Abdul Rashid",
        "price": 649,
        "image": "https://placehold.co/400x300/DAA520/000000?text=Papier+Mache",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/Box/glTF/Box.gltf",
        "category": "Decorative",
        "likes_count": 178,
        "rating": 4.4,
        "description": "Intricately hand-painted papier-mâché box with traditional Kashmiri floral patterns."
    },
    {
        "id": 8,
        "title": "Temple Bell (Ghanti)",
        "artist": "Krishna Moorthy",
        "price": 459,
        "image": "https://placehold.co/400x300/FFD700/000000?text=Temple+Bell",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/MetalRoughSpheresNoTextures/glTF/MetalRoughSpheresNoTextures.gltf",
        "category": "Metalwork",
        "likes_count": 321,
        "rating": 4.8,
        "description": "Brass temple bell with melodious sound, handcrafted in traditional South Indian style."
    },
    {
        "id": 9,
        "title": "Warli Art Wall Hanging",
        "artist": "Sunita Patil",
        "price": 549,
        "image": "https://placehold.co/400x300/8B7355/ffffff?text=Warli+Art",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/Triangle/glTF/Triangle.gltf",
        "category": "Painting",
        "likes_count": 267,
        "rating": 4.6,
        "description": "Authentic Warli tribal art from Maharashtra, depicting daily village life in geometric patterns."
    },
    {
        "id": 10,
        "title": "Rajasthani Silver Jewelry Set",
        "artist": "Anjali Sharma",
        "price": 2499,
        "image": "https://placehold.co/400x300/C0C0C0/000000?text=Silver+Jewelry",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/DragonAttenuation/glTF/DragonAttenuation.gltf",
        "category": "Jewelry",
        "likes_count": 589,
        "rating": 4.9,
        "description": "Handcrafted oxidized silver jewelry with traditional Rajasthani designs and gemstone inlays."
    },
    {
        "id": 11,
        "title": "Blue Pottery Vase",
        "artist": "Mohan Joshi",
        "price": 749,
        "image": "https://placehold.co/400x300/4169E1/ffffff?text=Blue+Pottery",
        "model_url": "https://modelviewer.dev/shared-assets/models/glTF-Sample-Assets/Models/WaterBottle/glTF/WaterBottle.gltf",
        "category": "Pottery",
        "likes_count": 412,
        "rating": 4.7,
        "description": "Stunning blue pottery vase from Jaipur with Persian-inspired floral motifs."
    },
    {
        "id": 12,
        "title": "Cane Furniture Chair",
        "artist": "Joseph D'Souza",
        "price": 3299,
        "image": "https://placehold.co/400x300/D2691E/ffffff?text=Cane+Chair",
        "model_url": "https://modelviewer.dev/shared-assets/models/Chair/Chair.glb",
        "category": "Furniture",
        "likes_count": 156,
        "rating": 4.5,
        "description": "Ergonomic cane chair with contemporary design, perfect blend of comfort and aesthetics."
    },
]

# Simple in-memory storage for likes (Advanced Feature Placeholder)
# In a real app, this would use a database
liked_art_ids = [2, 4] # Artworks liked by the current user

# User profile data (in-memory storage)
user_profile = {
    "username": "Art_Explorer_99",
    "email": "explorer@visioncraft.com",
    "joined": "March 2024",
    "uploads_count": 0,
    "likes_given": len(liked_art_ids),
    "orders_count": 3,
    "total_spent": 1497,
    "bio": "Curator of handcrafted wonders. Supporting local artisans globally.",
    "phone": "+91 98765 43210",
    "location": "Mumbai, Maharashtra",
    "avatar": None,
    "rsvps": []  # simple RSVP store per current user
}

# Local events & workshops (in-memory). In a real app, fetch from DB or an API
EVENTS = [
    {
        "id": 1,
        "title": "Jaipur Craft Fair",
        "type": "Fair",
        "date": "2025-10-20",
        "time": "10:00 AM",
        "location": "Jaipur, Rajasthan",
        "address": "Rava Bazaar Grounds",
        "description": "Explore hundreds of artisan stalls, live demos, and regional food courts.",
        "tags": ["Pottery", "Textiles", "Folk Art"],
    },
    {
        "id": 2,
        "title": "Hands-on Pottery Workshop",
        "type": "Workshop",
        "date": "2025-10-22",
        "time": "02:00 PM",
        "location": "Pune, Maharashtra",
        "address": "Kala Studio, FC Road",
        "description": "Learn wheel throwing and glazing basics with master potter Meera Kulkarni.",
        "tags": ["Pottery", "Beginner Friendly"],
    },
    {
        "id": 3,
        "title": "Textile Natural Dyeing Class",
        "type": "Class",
        "date": "2025-10-25",
        "time": "11:00 AM",
        "location": "New Delhi, Delhi",
        "address": "Dilli Haat, INA",
        "description": "Hands-on introduction to indigo and madder dyeing with sustainable techniques.",
        "tags": ["Textiles", "Eco"],
    },
    {
        "id": 4,
        "title": "Channapatna Toys Showcase",
        "type": "Exhibition",
        "date": "2025-10-28",
        "time": "04:00 PM",
        "location": "Bengaluru, Karnataka",
        "address": "Crafts Museum, MG Road",
        "description": "Meet woodcraft artisans, try your hand at eco-friendly lacquering.",
        "tags": ["Woodcraft", "Family"],
    },
]

# Upload settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MODELS_DIR = os.path.join(STATIC_DIR, 'models')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

ALLOWED_MODEL_EXT = {'.glb', '.gltf'}
ALLOWED_IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# ----------------- ROUTES -----------------

@app.before_request
def infer_role_from_path():
    """Infer role based on path if not explicitly set.
    Defaults to 'customer'. Visiting seller paths sets role to 'seller'.
    """
    try:
        role = session.get('role')
        path = request.path or ''
        if path.startswith('/seller') and role != 'seller':
            session['role'] = 'seller'
        elif role is None:
            session['role'] = 'customer'
    except Exception:
        # Session might not be available in some contexts
        pass

@app.route('/enter/customer')
def enter_customer():
    session['role'] = 'customer'
    return redirect(url_for('home'))

@app.route('/enter/seller')
def enter_seller():
    session['role'] = 'seller'
    return redirect(url_for('seller_analytics'))

@app.route('/')
def landing():
    """Landing page - choose between customer or seller"""
    return render_template('landing.html')

@app.route('/home')
def home():
    """Customer home page with artwork gallery"""
    return render_template('home.html', artworks=artworks)

@app.route('/seller')
def seller_dashboard():
    """Seller/Artisan dashboard with analytics"""
    return redirect(url_for('seller_analytics'))

@app.route('/seller/analytics')
def seller_analytics():
    """Seller Analytics Dashboard"""
    return render_template('seller_analytics.html', artworks=artworks)

@app.route('/art/<int:art_id>')
def art_detail(art_id):
    art = next((a for a in artworks if a["id"] == art_id), None)
    if art is None:
        return render_template('error.html', message="Artwork not found."), 404
    return render_template('art_detail.html', art=art)

@app.route('/ar/<int:art_id>')
def view_in_ar(art_id):
    art = next((a for a in artworks if a["id"] == art_id), None)
    if art is None:
        return render_template('error.html', message="Artwork not found for AR view."), 404
    return render_template('ar_viewer.html', art=art)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    
    # Advanced Feature: Implement in-memory search across title, category, and artist
    search_results = []
    if query:
        search_results = [
            art for art in artworks 
            if query in art['title'].lower() or 
               query in art['category'].lower() or
               query in art['artist'].lower()
        ]
    
    return render_template('search.html', query=query, search_results=search_results)

@app.route('/upload')
def upload():
    if session.get('role') != 'seller':
        return render_template('error.html', message="Uploads are available only for sellers. Please choose 'I'm an Artisan/Seller' on the landing page."), 403
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_post():
    if session.get('role') != 'seller':
        return render_template('error.html', message="Uploads are available only for sellers. Please choose 'I'm an Artisan/Seller' on the landing page."), 403
    """Handle uploaded image and/or 3D model files, create a new artwork entry.

    Saves images to /static/images and models to /static/models and appends
    a new artwork dictionary to the in-memory `artworks` list.
    """
    # Get form data
    title = request.form.get('title', 'Untitled')
    description = request.form.get('description', '')
    category = request.form.get('category', 'Other')
    price = request.form.get('price', 0)
    artist_name = request.form.get('artist_name', 'Anonymous Artist')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    location = request.form.get('location', '')

    # Get uploaded files
    image = request.files.get('image')
    model = request.files.get('model')

    image_url = None
    model_url = None

    # Save image if provided
    if image and image.filename:
        filename = secure_filename(image.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in ALLOWED_IMAGE_EXT:
            dest = os.path.join(IMAGES_DIR, filename)
            image.save(dest)
            image_url = f"/static/images/{filename}"

    # Save model if provided
    if model and model.filename:
        filename = secure_filename(model.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in ALLOWED_MODEL_EXT:
            dest = os.path.join(MODELS_DIR, filename)
            model.save(dest)
            model_url = f"/static/models/{filename}"

    # Create artwork entry with all fields
    new_id = max([a['id'] for a in artworks]) + 1 if artworks else 1
    new_art = {
        'id': new_id,
        'title': title,
        'artist': artist_name,
        'price': int(price) if price else 0,
        'image': image_url or 'https://placehold.co/400x300/cccccc/000000?text=No+Image',
        'model_url': model_url,
        'category': category,
        'likes_count': 0,
        'description': description,
        # Additional artisan info (would be stored in separate table in real app)
        'email': email,
        'phone': phone,
        'location': location
    }
    artworks.append(new_art)

    return redirect(url_for('art_detail', art_id=new_id))

@app.route('/likes')
def likes():
    liked_artworks = [art for art in artworks if art['id'] in liked_art_ids]
    return render_template('likes.html', liked_artworks=liked_artworks)

@app.route('/profile')
def profile():
    """User profile page with uploads, orders, favorites, and settings"""
    
    # Update profile stats
    user_profile['uploads_count'] = len([a for a in artworks if a.get('artist') == user_profile['username']])
    user_profile['likes_given'] = len(liked_art_ids)
    
    # User's uploaded artworks
    user_artworks = [a for a in artworks if a.get('artist') == user_profile['username']][:6]
    
    # User's liked artworks
    liked_artworks = [art for art in artworks if art['id'] in liked_art_ids]
    
    # Sample order history (in real app, fetch from database)
    orders = [
        {
            'id': 'VC-001-2024',
            'art': artworks[0],
            'date': '2024-12-15',
            'total': 448,
            'status': 'delivered',
            'status_text': 'Delivered'
        },
        {
            'id': 'VC-002-2024',
            'art': artworks[1],
            'date': '2024-12-20',
            'total': 648,
            'status': 'shipping',
            'status_text': 'In Transit'
        },
        {
            'id': 'VC-003-2024',
            'art': artworks[2],
            'date': '2025-01-05',
            'total': 498,
            'status': 'processing',
            'status_text': 'Processing'
        }
    ]
    
    return render_template('profile.html', 
                         profile=user_profile,
                         user_artworks=user_artworks,
                         liked_artworks=liked_artworks,
                         orders=orders)

@app.route('/purchase/<int:art_id>')
def purchase(art_id):
    """Purchase page for a specific artwork"""
    art = next((a for a in artworks if a["id"] == art_id), None)
    if art is None:
        return render_template('error.html', message="Artwork not found."), 404
    return render_template('purchase.html', art=art)

@app.route('/purchase/process', methods=['POST'])
def process_purchase():
    """Process purchase form submission"""
    # Get form data
    art_id = request.form.get('art_id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    pincode = request.form.get('pincode')
    payment_method = request.form.get('payment_method')
    
    # Get UPI ID if payment method is UPI
    upi_id = request.form.get('upi_id', '')
    
    # In a real application, this would:
    # 1. Validate all form data
    # 2. Process payment through payment gateway
    # 3. Store order in database
    # 4. Send confirmation email
    # 5. Notify artisan
    
    # For now, we'll just create a success message
    art = next((a for a in artworks if a["id"] == int(art_id)), None)
    
    if art is None:
        return render_template('error.html', message="Artwork not found."), 404
    
    # Create order data (in real app, save to database)
    order_data = {
        'order_id': f'VC-{art_id}-{hash(name) % 10000:04d}',
        'art': art,
        'customer': {
            'name': name,
            'email': email,
            'phone': phone
        },
        'address': f'{address}, {city}, {state} - {pincode}',
        'payment_method': payment_method,
        'total': art['price'] + 149
    }
    
    return render_template('order_confirmation.html', order=order_data)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Update user profile information"""
    global user_profile
    
    user_profile['username'] = request.form.get('username', user_profile['username'])
    user_profile['email'] = request.form.get('email', user_profile['email'])
    user_profile['bio'] = request.form.get('bio', user_profile['bio'])
    user_profile['phone'] = request.form.get('phone', user_profile.get('phone', ''))
    user_profile['location'] = request.form.get('location', user_profile.get('location', ''))
    
    return redirect(url_for('profile'))

@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    """Upload and update user avatar"""
    from flask import jsonify
    
    avatar_file = request.files.get('avatar')
    
    if avatar_file and avatar_file.filename:
        filename = secure_filename(avatar_file.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in ALLOWED_IMAGE_EXT:
            # Create avatars directory if it doesn't exist
            avatars_dir = os.path.join(STATIC_DIR, 'avatars')
            os.makedirs(avatars_dir, exist_ok=True)
            
            # Save with unique filename
            avatar_filename = f"avatar_{user_profile['username']}{ext}"
            dest = os.path.join(avatars_dir, avatar_filename)
            avatar_file.save(dest)
            
            # Update profile
            user_profile['avatar'] = f"/static/avatars/{avatar_filename}"
            
            return jsonify({'success': True, 'avatar_url': user_profile['avatar']})
    
    return jsonify({'success': False, 'error': 'Invalid file'})

@app.route('/update_settings', methods=['POST'])
def update_settings():
    """Update user settings/preferences"""
    # In a real app, save these to database
    # For now, just redirect back
    return redirect(url_for('profile'))

@app.route('/change_password', methods=['POST'])
def change_password():
    """Change user password"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # In a real app, validate current password and update
    # For demo, just redirect back
    return redirect(url_for('profile'))

@app.route('/api/toggle_like/<int:art_id>', methods=['POST'])
def toggle_like(art_id):
    """Toggle like status for an artwork"""
    from flask import jsonify
    
    if art_id in liked_art_ids:
        liked_art_ids.remove(art_id)
        # Also decrement the likes_count for that artwork
        for art in artworks:
            if art['id'] == art_id:
                art['likes_count'] = max(0, art['likes_count'] - 1)
                break
        return jsonify({'success': True, 'liked': False})
    else:
        liked_art_ids.append(art_id)
        # Increment the likes_count for that artwork
        for art in artworks:
            if art['id'] == art_id:
                art['likes_count'] += 1
                break
        return jsonify({'success': True, 'liked': True})

@app.route('/api/delete_art/<int:art_id>', methods=['DELETE'])
def delete_art(art_id):
    """Delete an artwork"""
    from flask import jsonify
    
    # Find and remove the artwork
    global artworks
    artworks = [art for art in artworks if art['id'] != art_id]
    
    # Remove from liked_art_ids if present
    if art_id in liked_art_ids:
        liked_art_ids.remove(art_id)
    
    return jsonify({'success': True})

@app.route('/api/delete_account', methods=['DELETE'])
def delete_account():
    """Delete user account"""
    from flask import jsonify
    
    # In a real app, this would delete all user data
    # For demo, just return success
    return jsonify({'success': True})

@app.route('/wall-stylist')
def wall_stylist():
    """AR Wall Stylist - Cycle through multiple decor options"""
    return render_template('wall_stylist.html')

@app.route('/crafts-map')
def crafts_map():
    """Interactive Crafts Map of India with state-wise AR portal"""
    return render_template('crafts_map.html')

# ----------------- EVENTS ROUTES -----------------

@app.route('/events')
def events():
    """Local Events & Workshops Calendar and list view"""
    # Mark RSVP status per event for current user
    user_rsvps = set(user_profile.get('rsvps', []))
    events_with_status = []
    for e in EVENTS:
        e_copy = dict(e)
        e_copy['rsvped'] = e['id'] in user_rsvps
        events_with_status.append(e_copy)
    return render_template('events.html', events=events_with_status)

@app.route('/api/events/rsvp/<int:event_id>', methods=['POST'])
def api_rsvp_event(event_id):
    from flask import jsonify
    # Validate event exists
    event = next((e for e in EVENTS if e['id'] == event_id), None)
    if not event:
        return jsonify({"success": False, "error": "Event not found"}), 404

    rsvps = set(user_profile.get('rsvps', []))
    if event_id in rsvps:
        rsvps.remove(event_id)
        user_profile['rsvps'] = list(rsvps)
        return jsonify({"success": True, "rsvped": False, "message": "RSVP cancelled"})
    else:
        rsvps.add(event_id)
        user_profile['rsvps'] = list(rsvps)
        return jsonify({"success": True, "rsvped": True, "message": "RSVP confirmed"})

@app.route('/edit/<int:art_id>')
def edit_artwork(art_id):
    """Edit artwork page"""
    art = next((a for a in artworks if a['id'] == art_id), None)
    if art is None:
        return render_template('error.html', message="Artwork not found."), 404
    
    # For now, redirect to upload page with artwork data
    # In a full implementation, create a dedicated edit page
    return redirect(url_for('upload'))

@app.route('/order/<order_id>')
def order_details(order_id):
    """View order details"""
    # In a real app, fetch order from database
    return render_template('error.html', message="Order details page coming soon!"), 404

@app.route('/reorder/<order_id>')
def reorder(order_id):
    """Reorder from a previous order"""
    # In a real app, fetch order and redirect to purchase
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Set debug=True for easier development - it gives more detailed error messages
    # host='0.0.0.0' allows access from other devices on the same network (required for mobile AR testing)
    # For production, set debug=False and use a proper WSGI server like gunicorn
    
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*60)
    print("🎨 VisionCraft AR Application Starting...")
    print("="*60)
    print(f"\n📍 Local Access:")
    print(f"   http://localhost:5000")
    print(f"   http://127.0.0.1:5000")
    print(f"\n📱 Mobile Access (same WiFi network):")
    print(f"   http://{local_ip}:5000")
    print(f"\n💡 For AR Testing:")
    print(f"   - Open the mobile URL on your phone/tablet")
    print(f"   - Make sure your mobile is on the same WiFi")
    print(f"   - Grant camera permissions when prompted")
    print(f"\n⚠️  Note: AR features require HTTPS in production")
    print(f"   Use ngrok or similar for HTTPS testing")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
