from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Advanced Data Structure: Artworks and Artist Info ---
# Added more complex fields like artist, category, model_url, and likes_count
artworks = [
    {
        "id": 1,
        "title": "Terracotta Pot of Marwar",
        "artist": "Sanjay Varma",
        "price": 299,
        "image": "/static/images/pottery.jpg",
        # Use a public glb for demo. In production this would be an uploaded file under /static/uploads/*.glb
        "model_url": "https://modelviewer.dev/shared-assets/models/Monster/Monster.gltf",
        "category": "Pottery",
        "likes_count": 145,
        "description": "Handmade terracotta pot from Rajasthan, featuring traditional Marwari motifs. Ideal for rustic decor."
    },
    {
        "id": 2,
        "title": "Cosmic Elephant Toy",
        "artist": "Priya Sharma",
        "price": 499,
        "image": "/static/images/wooden_toy.jpg",
        "model_url": "/static/models/benjarong.glb",
        "category": "Woodcraft",
        "likes_count": 92,
        "description": "A beautifully carved wooden elephant toy from Karnataka, painted with vibrant, non-toxic colors."
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
        "description": "Eco-friendly, hand-woven bamboo basket from the foothills of Assam. Durable and lightweight."
    },
    {
        "id": 4,
        "title": "Indigo Dye Scarf",
        "artist": "Meena Khan",
        "price": 899,
        "image": "https://placehold.co/400x300/3c5a77/ffffff?text=Indigo+Scarf",
        "model_url": "https://modelviewer.dev/shared-assets/models/Reciprocal%20Stairs/Reciprocal_Stairs.glb",
        "category": "Textiles",
        "likes_count": 210,
        "description": "Traditional block-printed cotton scarf using natural indigo dyes."
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
    "avatar": None
}

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
    """Seller/Artisan dashboard"""
    # For now, redirect to upload page
    # In future, this will have analytics, sales, inventory management
    return redirect(url_for('upload'))

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
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_post():
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
