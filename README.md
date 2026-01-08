# Pachena Resort - Booking & Management System

A beautiful, full-featured resort booking and management application built with Streamlit and Supabase.

## ✨ Features

### 🌐 Public Landing Page
- **Professional Logo Display**: Custom branding with LOGO.png
- **Photo Gallery**: Showcase resort images (1.jpg, 2.jpg, 3.jpg, 4.jpg, 18.jpg, 19.jpg, 21.jpeg)
- **Activities Showcase**: Display of resort experiences
  - Guided Farm Tour
  - Scenic Nature Walks
  - Bonfire Chats
  - Classic Farm Games
  - Spa & Wellness
  - Braai Experience
- **Clear Pricing Display**: Service-by-service pricing table
  - Adult Package: $30
  - Child Package (Under 12): $15
  - Wellness Day (Spa & Massage): $25
  - Individual Activities: $5
  - Braai Packages: Starting at $5
  - Own Cooler Box Fee: $10
- **Package Inclusions Section**: 
  - Comfortable Tented Accommodation
  - Bed & Breakfast
  - Guided Farm Tour
  - Classic Farm Games
  - Bonfire Chats
  - Scenic Nature Walks
- **Booking Enquiry Form**: Complete customer information capture

### 🗄️ Supabase Integration
- Real-time data storage
- Secure database operations
- Automatic timestamp tracking

### 🔐 Admin Dashboard
- Secure staff authentication
- View all enquiries
- Add follow-up notes
- Update booking status
- Generate quotations with tax
- Summary analytics

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account (free tier available)
- Windows/Mac/Linux

## 🚀 Installation

### Step 1: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages (use one of these methods)
pip install --only-binary :all: pandas
pip install -r requirements.txt
```

**If you encounter pandas build errors:**
```bash
pip install streamlit supabase python-dotenv Pillow
```

### Step 2: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to **SQL Editor** and run the entire [schema.sql](schema.sql) file
4. Go to **Settings** → **API** and copy:
   - Project URL
   - anon/public key

### Step 3: Configure Environment Variables

1. Copy the template:
   ```bash
   Copy-Item .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=eyJhbGc...your-key-here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_secure_password_123
   ```

### Step 4: Add Your Images

Ensure these files are in the project folder:
- `LOGO.png` - Your resort logo
- `1.jpg`, `2.jpg`, `3.jpg`, `4.jpg` - Gallery photos
- `18.jpg`, `19.jpg`, `21.jpeg` - More gallery photos

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 📱 Usage

### For Guests
1. Browse the gallery and activities
2. Check pricing and package inclusions
3. Fill out the booking enquiry form
4. Receive confirmation

### For Staff
1. Click **"Staff Login"** in sidebar
2. Enter credentials from `.env` file
3. View all enquiries in dashboard
4. Add notes and generate quotations
5. Update booking status

## 📁 Project Structure

```
Pachena/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration (pricing, activities, contact)
├── database.py            # Supabase database operations
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (DO NOT COMMIT)
├── .env.example          # Template for credentials
├── .gitignore            # Git ignore rules
├── LOGO.png              # Resort logo
├── 1.jpg, 2.jpg, etc.    # Gallery images
└── README.md             # This file
```

## 🎨 Customization

### Update Contact Information
Edit [config.py](config.py):
```python
CONTACT_EMAIL = "your@email.com"
CONTACT_PHONE = "+263 775 387 683"
```

### Modify Pricing
Edit the `PRICING` dictionary in [config.py](config.py)

### Change Activities
Update the `ACTIVITIES` list in [config.py](config.py)

### Adjust Package Inclusions
Modify `PACKAGE_INCLUSIONS` in [config.py](config.py)

### Add/Remove Gallery Images
Update `GALLERY_IMAGES` list in [config.py](config.py)

## 🔒 Security

- ✅ Environment variables for sensitive data
- ✅ `.gitignore` prevents credential commits
- ✅ Supabase Row Level Security policies
- ✅ Password-protected admin dashboard
- ⚠️ **Change default admin password immediately**
- ⚠️ Use HTTPS in production

## 🐛 Troubleshooting

### "Supabase credentials not configured"
- Check `.env` file exists and has correct values
- Verify SUPABASE_URL and SUPABASE_KEY are set

### Images not displaying
- Ensure image files are in the root project folder
- Check file names match exactly (case-sensitive)
- Verify image files aren't corrupted

### Pandas build error
- Use: `pip install --only-binary :all: pandas`
- Or install packages individually without pandas version lock

### Login not working
- Verify credentials in `.env` file
- Check for typos in username/password

## 📞 Support

**Pachena Resort**
- 📧 Email: pachenaresort@gmail.com
- 📱 Phone: +263 775 387 683

## 📄 License

MIT License - Free to use and modify

---

Built with ❤️ using Streamlit & Supabase
