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
        "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
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
def home():
    return render_template('home.html', artworks=artworks)

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
    """Handle uploaded image and/or 3D model files, create a simple artwork entry.

    Saves images to /static/images and models to /static/models and appends
    a new artwork dictionary to the in-memory `artworks` list.
    """
    title = request.form.get('title', 'Untitled')
    description = request.form.get('description', '')

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

    # Create artwork entry using minimal fields
    new_id = max([a['id'] for a in artworks]) + 1 if artworks else 1
    new_art = {
        'id': new_id,
        'title': title,
        'artist': 'Uploaded Artist',
        'price': 0,
        'image': image_url or 'https://placehold.co/400x300/cccccc/000000?text=No+Image',
        'model_url': model_url,
        'category': 'Uploaded',
        'likes_count': 0,
        'description': description,
    }
    artworks.append(new_art)

    return redirect(url_for('art_detail', art_id=new_id))

@app.route('/likes')
def likes():
    liked_artworks = [art for art in artworks if art['id'] in liked_art_ids]
    return render_template('likes.html', liked_artworks=liked_artworks)

@app.route('/profile')
def profile():
    # **THIS IS THE NEW ROUTE** that needs to exist for url_for('profile') to work.
    user_profile = {
        "username": "Art_Explorer_99",
        "joined": "2024-03-15",
        "uploads_count": 7,
        "likes_given": len(liked_art_ids),
        "bio": "Curator of handcrafted wonders. Supporting local artisans globally."
    }
    return render_template('profile.html', profile=user_profile)

if __name__ == '__main__':
    # Set debug=True for easier development - it gives more detailed error messages
    app.run(debug=True, host='0.0.0.0', port=5000)
