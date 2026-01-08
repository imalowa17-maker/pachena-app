import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Admin Credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Contact Information
CONTACT_EMAIL = "pachenaresort@gmail.com"
CONTACT_PHONE = "+263 775 387 683 / 0786 714 774"
LOGO_PATH = "LOGO2.svg"

# Pricing Configuration
PRICING = {
    "Adult Package": 30,
    "Child Package (Under 12)": 15,
    "Wellness Day (Spa & Massage)": 25,
    "Individual Activities": 5,
    "Braai Package (Starting)": 5,
    "Own Cooler Box Fee": 10
}

# Package Inclusions
PACKAGE_INCLUSIONS = [
    "Comfortable Tented Accommodation",
    "Bed & Breakfast (Morning meal included)",
    "Guided Farm Tour",
    "Classic Farm Games",
    "Bonfire Chats",
    "Scenic Nature Walks"
]

# Gallery Images with Descriptions
GALLERY_IMAGES = [
    {"file": "1.jpg", "caption": "Scenic Farm Landscape"},
    {"file": "2.jpg", "caption": "Peaceful Natural Surroundings"},
    {"file": "4.jpg", "caption": "Outdoor Relaxation Area"},
    {"file": "18.jpg", "caption": "Comfortable Tented Accommodation"},
    {"file": "19.jpg", "caption": "Farm Tour Experience"},
    {"file": "21.jpeg", "caption": "Nature Walking Trails"},
    {"file": "28.jpg", "caption": "Resort Grounds & Gardens"},
    {"file": "29.jpg", "caption": "Outdoor Dining Area"},
    {"file": "34.jpg", "caption": "Cozy Accommodation Interior"},
    {"file": "42.jpg", "caption": "Bonfire & Social Spaces"},
    {"file": "86.jpeg", "caption": "Spa & Wellness Facilities"},
    {"file": "87.jpeg", "caption": "Farm Animals & Activities"},
    {"file": "88.jpeg", "caption": "Tranquil Resort Views"},
    {"file": "89.jpeg", "caption": "Recreation & Games Area"},
    {"file": "90.jpeg", "caption": "Outdoor Adventure Spaces"},
    {"file": "91.jpeg", "caption": "Scenic Nature Spots"},
    {"file": "92.jpeg", "caption": "Braai & BBQ Facilities"},
    {"file": "NEW 81.jpeg", "caption": "Resort Amenities"},
    {"file": "NEW 86.jpg", "caption": "Beautiful Resort Setting"}
]

# Activities
ACTIVITIES = [
    {
        "name": "Guided Farm Tour",
        "icon": "🚜",
        "description": "Explore our beautiful farm and learn about sustainable farming practices"
    },
    {
        "name": "Scenic Nature Walks",
        "icon": "🥾",
        "description": "Walk through picturesque trails and enjoy the natural beauty"
    },
    {
        "name": "Bonfire Chats",
        "icon": "🔥",
        "description": "Share stories around a cozy bonfire under the stars"
    },
    {
        "name": "Classic Farm Games",
        "icon": "🎯",
        "description": "Enjoy traditional games and family-friendly activities"
    },
    {
        "name": "Spa & Wellness",
        "icon": "💆",
        "description": "Relax with professional spa treatments and massages"
    },
    {
        "name": "Braai Experience",
        "icon": "🍖",
        "description": "Authentic braai packages for the perfect outdoor cooking experience"
    }
]
