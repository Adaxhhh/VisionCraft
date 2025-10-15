"""
Initialize database with sample data for VisionCraft AR Marketplace
Run this script once to set up the database
"""
from app import app, db
from models import User, Artwork, Event
from datetime import date

def init_database():
    """Initialize database and create sample data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if User.query.first():
            print("Database already initialized!")
            return
        
        print("Adding sample users...")
        
        # Create sample customers
        customer1 = User(
            username='demo_customer',
            email='customer@visioncraft.com',
            role='customer',
            bio='Art enthusiast and collector',
            phone='+91 98765 43210',
            location='Mumbai, Maharashtra'
        )
        customer1.set_password('password123')
        
        customer2 = User(
            username='art_lover',
            email='artlover@example.com',
            role='customer',
            bio='Supporting local artisans',
            phone='+91 88888 99999',
            location='Delhi, India'
        )
        customer2.set_password('password123')
        
        # Create sample sellers/artisans
        seller1 = User(
            username='sanjay_potter',
            email='sanjay@craftmakers.com',
            role='seller',
            bio='Traditional potter from Rajasthan with 20 years of experience',
            phone='+91 97654 32100',
            location='Jaipur, Rajasthan'
        )
        seller1.set_password('seller123')
        
        seller2 = User(
            username='priya_woodcraft',
            email='priya@woodartisans.com',
            role='seller',
            bio='Skilled woodcraft artist specializing in Channapatna toys',
            phone='+91 98111 22333',
            location='Bangalore, Karnataka'
        )
        seller2.set_password('seller123')
        
        seller3 = User(
            username='lakshmi_painter',
            email='lakshmi@madhubani.com',
            role='seller',
            bio='Madhubani folk artist from Bihar, preserving ancient traditions',
            phone='+91 99900 11122',
            location='Patna, Bihar'
        )
        seller3.set_password('seller123')
        
        db.session.add_all([customer1, customer2, seller1, seller2, seller3])
        db.session.commit()
        
        print("Adding sample artworks...")
        
        # Sample artworks - ONLY using existing images and 3D models
        artworks_data = [
            {
                'title': 'Terracotta Pot of Marwar',
                'artist_name': 'Sanjay Varma',
                'price': 299,
                'user_id': seller1.id,
                'image': '/static/images/pottery.jpg',
                'model_url': '/static/models/pottery.glb',
                'category': 'Pottery',
                'rating': 4.8,
                'description': 'Handmade terracotta pot from Rajasthan, featuring traditional Marwari motifs. Ideal for rustic decor.',
                'state': 'Rajasthan',
                'making_process': 'Traditional clay molding and hand-painting technique passed down through generations',
                'views': 1247,
                'stock_quantity': 15
            },
            {
                'title': 'Himalayan Bamboo Basket',
                'artist_name': 'Tenzin Gyatso',
                'price': 349,
                'user_id': seller1.id,
                'image': '/static/images/basket.jpg',
                'model_url': '/static/models/basket.glb',
                'category': 'Weaving',
                'rating': 4.9,
                'description': 'Eco-friendly, hand-woven bamboo basket from the foothills of Assam. Durable and lightweight.',
                'state': 'Assam',
                'making_process': 'Traditional bamboo weaving technique from the tribes of Northeast India',
                'views': 1534,
                'stock_quantity': 10
            },
            {
                'title': 'Bronze Ganesha Sculpture',
                'artist_name': 'Ramesh Patel',
                'price': 1599,
                'user_id': seller2.id,
                'image': '/static/images/ganesha.png',
                'model_url': '/static/models/ganesha.glb',
                'category': 'Sculpture',
                'rating': 5.0,
                'description': 'Exquisite bronze sculpture of Lord Ganesha, handcrafted using ancient lost-wax casting technique.',
                'state': 'Tamil Nadu',
                'making_process': 'Ancient lost-wax bronze casting technique from Thanjavur',
                'views': 2156,
                'stock_quantity': 5
            },
            {
                'title': 'Temple Bell (Ghanti)',
                'artist_name': 'Krishna Moorthy',
                'price': 459,
                'user_id': seller2.id,
                'image': '/static/images/bell.png',
                'model_url': '/static/models/bell.glb',
                'category': 'Metalwork',
                'rating': 4.8,
                'description': 'Brass temple bell with melodious sound, handcrafted in traditional South Indian style.',
                'state': 'Kerala',
                'making_process': 'Traditional bell metal casting from Kerala\'s Aranmula region',
                'views': 1456,
                'stock_quantity': 18
            },
            {
                'title': 'Blue Pottery Vase',
                'artist_name': 'Mohan Joshi',
                'price': 749,
                'user_id': seller3.id,
                'image': '/static/images/blue_vase.jpeg',
                'model_url': '/static/models/blue_vase.glb',
                'category': 'Pottery',
                'rating': 4.7,
                'description': 'Stunning blue pottery vase from Jaipur with Persian-inspired floral motifs.',
                'state': 'Rajasthan',
                'making_process': 'Jaipur blue pottery with Persian-inspired glazing techniques',
                'views': 1923,
                'stock_quantity': 11
            },
            {
                'title': 'Handcrafted Cane Chair',
                'artist_name': 'Joseph D\'Souza',
                'price': 3299,
                'user_id': seller3.id,
                'image': '/static/images/chair.png',
                'model_url': '/static/models/chair.glb',
                'category': 'Furniture',
                'rating': 4.5,
                'description': 'Ergonomic cane chair with contemporary design, perfect blend of comfort and aesthetics.',
                'state': 'Goa',
                'making_process': 'Traditional cane and bamboo furniture making from Goa',
                'views': 876,
                'stock_quantity': 4
            }
        ]
        
        for artwork_data in artworks_data:
            artwork = Artwork(**artwork_data)
            db.session.add(artwork)
        
        db.session.commit()
        
        print("Adding sample events...")
        
        # Sample events
        events_data = [
            {
                'title': 'Jaipur Craft Fair',
                'event_type': 'Fair',
                'event_date': date(2025, 10, 20),
                'event_time': '10:00 AM',
                'location': 'Jaipur, Rajasthan',
                'address': 'Rava Bazaar Grounds',
                'description': 'Explore hundreds of artisan stalls, live demos, and regional food courts.',
                'tags': 'Pottery,Textiles,Folk Art'
            },
            {
                'title': 'Hands-on Pottery Workshop',
                'event_type': 'Workshop',
                'event_date': date(2025, 10, 22),
                'event_time': '02:00 PM',
                'location': 'Pune, Maharashtra',
                'address': 'Kala Studio, FC Road',
                'description': 'Learn wheel throwing and glazing basics with master potter Meera Kulkarni.',
                'tags': 'Pottery,Beginner Friendly'
            },
            {
                'title': 'Textile Natural Dyeing Class',
                'event_type': 'Class',
                'event_date': date(2025, 10, 25),
                'event_time': '11:00 AM',
                'location': 'New Delhi, Delhi',
                'address': 'Dilli Haat, INA',
                'description': 'Hands-on introduction to indigo and madder dyeing with sustainable techniques.',
                'tags': 'Textiles,Eco'
            },
            {
                'title': 'Channapatna Toys Showcase',
                'event_type': 'Exhibition',
                'event_date': date(2025, 10, 28),
                'event_time': '04:00 PM',
                'location': 'Bengaluru, Karnataka',
                'address': 'Crafts Museum, MG Road',
                'description': 'Meet woodcraft artisans, try your hand at eco-friendly lacquering.',
                'tags': 'Woodcraft,Family'
            }
        ]
        
        for event_data in events_data:
            event = Event(**event_data)
            db.session.add(event)
        
        db.session.commit()
        
        print("\n✅ Database initialized successfully!")
        print("\n📝 Sample Login Credentials:")
        print("=" * 50)
        print("CUSTOMER ACCOUNTS:")
        print("  Username: demo_customer")
        print("  Password: password123")
        print("\n  Username: art_lover")
        print("  Password: password123")
        print("\nSELLER/ARTISAN ACCOUNTS:")
        print("  Username: sanjay_potter")
        print("  Password: seller123")
        print("\n  Username: priya_woodcraft")
        print("  Password: seller123")
        print("\n  Username: lakshmi_painter")
        print("  Password: seller123")
        print("=" * 50)
        print("\n🚀 You can now run the application with: python app.py")

if __name__ == '__main__':
    init_database()
