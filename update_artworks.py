"""
Script to add artisan story videos and analytics data to all artworks
"""

# Additional data for each artwork
additional_data = {
    3: {
        "state": "Assam",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "video_thumbnail": "https://placehold.co/400x300/8B7355/ffffff?text=Bamboo+Weaving",
        "making_process": "Traditional bamboo weaving technique from the tribes of Northeast India",
        "views": 1534,
        "favorites": 112,
        "ar_tries": 201
    },
    4: {
        "state": "Gujarat",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "video_thumbnail": "https://placehold.co/400x300/3c5a77/ffffff?text=Indigo+Dyeing",
        "making_process": "Natural indigo dyeing with traditional block printing methods",
        "views": 987,
        "favorites": 78,
        "ar_tries": 145
    },
    5: {
        "state": "Tamil Nadu",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "video_thumbnail": "https://placehold.co/400x300/8B4513/ffffff?text=Bronze+Casting",
        "making_process": "Ancient lost-wax bronze casting technique from Thanjavur",
        "views": 2156,
        "favorites": 198,
        "ar_tries": 312
    },
    6: {
        "state": "Bihar",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        "video_thumbnail": "https://placehold.co/400x300/FF6347/ffffff?text=Madhubani+Art",
        "making_process": "Traditional Madhubani painting using natural dyes and bamboo sticks",
        "views": 1678,
        "favorites": 145,
        "ar_tries": 223
    },
    7: {
        "state": "Jammu & Kashmir",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
        "video_thumbnail": "https://placehold.co/400x300/DAA520/000000?text=Papier+Mache",
        "making_process": "Kashmiri papier-mâché with hand-painted floral motifs",
        "views": 1234,
        "favorites": 92,
        "ar_tries": 167
    },
    8: {
        "state": "Kerala",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
        "video_thumbnail": "https://placehold.co/400x300/FFD700/000000?text=Metal+Casting",
        "making_process": "Traditional bell metal casting from Kerala's Aranmula region",
        "views": 1456,
        "favorites": 104,
        "ar_tries": 189
    },
    9: {
        "state": "Maharashtra",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
        "video_thumbnail": "https://placehold.co/400x300/8B7355/ffffff?text=Warli+Art",
        "making_process": "Ancient Warli tribal art using rice paste and natural pigments",
        "views": 1789,
        "favorites": 134,
        "ar_tries": 245
    },
    10: {
        "state": "Rajasthan",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
        "video_thumbnail": "https://placehold.co/400x300/C0C0C0/000000?text=Silver+Craft",
        "making_process": "Traditional Rajasthani silver crafting with gemstone inlay work",
        "views": 2345,
        "favorites": 223,
        "ar_tries": 389
    },
    11: {
        "state": "Rajasthan",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/VolkswagenGTIReview.mp4",
        "video_thumbnail": "https://placehold.co/400x300/4169E1/ffffff?text=Blue+Pottery",
        "making_process": "Jaipur blue pottery with Persian-inspired glazing techniques",
        "views": 1923,
        "favorites": 156,
        "ar_tries": 278
    },
    12: {
        "state": "Goa",
        "artisan_video": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4",
        "video_thumbnail": "https://placehold.co/400x300/D2691E/ffffff?text=Cane+Craft",
        "making_process": "Traditional cane and bamboo furniture making from Goa",
        "views": 876,
        "favorites": 67,
        "ar_tries": 123
    }
}

print("Additional artwork data prepared for integration")
print(f"Total artworks with story data: {len(additional_data)}")
