import streamlit as st
from datetime import datetime, date
import pandas as pd
from PIL import Image
import os
from config import (
    ACTIVITIES, PRICING, ADMIN_USERNAME, ADMIN_PASSWORD,
    CONTACT_EMAIL, CONTACT_PHONE, LOGO_PATH, PACKAGE_INCLUSIONS, GALLERY_IMAGES
)
from database import (
    insert_enquiry, 
    fetch_all_enquiries, 
    update_follow_up_notes, 
    update_enquiry_status,
    calculate_quotation
)

# Page configuration
st.set_page_config(
    page_title="Pachena Eco-Tourism Resort",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Dark Mode Support
st.markdown("""
<style>
    /* Light Mode (Default) */
    .main {
        background: linear-gradient(to bottom, #faf9f6 0%, #e8f5e9 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 50%, #81c784 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(27, 94, 32, 0.3);
    }
    
    /* Activity Card */
    .activity-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #66bb6a;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        color: #424242;
    }
    .activity-card h2 {
        color: #1b5e20;
    }
    .activity-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        border-left-color: #4caf50;
    }
    
    /* Price Table */
    .price-table {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .price-row {
        display: flex;
        justify-content: space-between;
        padding: 1rem;
        border-bottom: 1px solid #f0f0f0;
        transition: all 0.2s;
    }
    
    .price-row:hover {
        background: #f1f8e9;
        border-radius: 6px;
    }
    
    .price-row:last-child {
        border-bottom: none;
    }
    
    .service-name {
        font-size: 1.1rem;
        color: #2e7d32;
        font-weight: 500;
    }
    
    .price-amount {
        font-size: 1.3rem;
        color: #1b5e20;
        font-weight: bold;
    }
    
    /* Package Inclusion Card */
    .inclusion-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #66bb6a;
        margin-bottom: 1.5rem;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.2);
    }
    
    .inclusion-item {
        padding: 0.5rem 0;
        font-size: 1.05rem;
        color: #1b5e20;
        font-weight: 500;
    }
    
    .inclusion-item:before {
        content: "✓ ";
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.3rem;
        margin-right: 0.3rem;
    }
    
    /* Gallery Container */
    .gallery-container {
        margin: 1rem 0;
    }
    
    /* Gallery Image Caption */
    .gallery-caption {
        text-align: center;
        color: #2e7d32;
        font-weight: 500;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(46, 125, 50, 0.4);
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 100%);
    }
    
    /* Section Headers */
    .section-header {
        color: #1b5e20;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        border-bottom: 4px solid #66bb6a;
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #e8f5e9;
    }
    
    /* Sidebar Text Elements - Light Mode */
    [data-testid="stSidebar"] .stMarkdown {
        color: #212121;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1b5e20 !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #1b5e20 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stInfo, 
    [data-testid="stSidebar"] .stSuccess {
        background-color: #ffffff !important;
        border: 1px solid #c8e6c9;
        color: #212121 !important;
    }
    
    [data-testid="stSidebar"] .stInfo p,
    [data-testid="stSidebar"] .stSuccess p {
        color: #212121 !important;
        font-weight: 500;
    }
    
    /* Logo Container */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
    }
    
    .logo-container svg {
        max-width: 100%;
        height: auto;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    /* Dark Mode Styles */
    @media (prefers-color-scheme: dark) {
        .main {
            background: linear-gradient(to bottom, #1a1a1a 0%, #0d2818 100%);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #1b4d20 0%, #2d6e32 50%, #3d7d43 100%);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        }
        
        .activity-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #1e3d25 100%);
            border-left: 5px solid #66bb6a;
            box-shadow: 0 3px 10px rgba(0,0,0,0.4);
            color: #e0e0e0;
        }
        
        .activity-card h2 {
            color: #81c784 !important;
        }
        
        .activity-card p {
            color: #c8c8c8 !important;
        }
        
        .price-table {
            background: #2a2a2a;
            border: 1px solid #3d3d3d;
            box-shadow: 0 3px 10px rgba(0,0,0,0.4);
        }
        
        .price-row {
            border-bottom: 1px solid #3d3d3d;
        }
        
        .price-row:hover {
            background: #1e3d25;
        }
        
        .service-name {
            color: #81c784;
        }
        
        .price-amount {
            color: #a5d6a7;
        }
        
        .inclusion-card {
            background: linear-gradient(135deg, #1e3d25 0%, #2d4f32 100%);
            border: 2px solid #4caf50;
            box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
        }
        
        .inclusion-item {
            color: #c8e6c9;
        }
        
        .inclusion-item:before {
            color: #81c784;
        }
        
        .gallery-caption {
            color: #81c784;
            background: rgba(0, 0, 0, 0.5);
            padding: 0.5rem;
            border-radius: 4px;
        }
        
        .section-header {
            color: #81c784;
            border-bottom: 4px solid #4caf50;
        }
        
        [data-testid="stSidebar"] {
            background: #1e3d25;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #e0e0e0;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #81c784 !important;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            color: #81c784 !important;
        }
        
        [data-testid="stSidebar"] .stInfo, 
        [data-testid="stSidebar"] .stSuccess {
            background-color: #2a2a2a !important;
            border: 1px solid #4caf50;
            color: #e0e0e0 !important;
        }
        
        [data-testid="stSidebar"] .stInfo p,
        [data-testid="stSidebar"] .stSuccess p {
            color: #e0e0e0 !important;
        }
        
        .logo-container svg {
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.6)) brightness(1.1);
        }
    }
    
    /* Force dark mode for Streamlit in dark theme */
    [data-theme="dark"] .main {
        background: linear-gradient(to bottom, #1a1a1a 0%, #0d2818 100%);
    }
    
    [data-theme="dark"] .hero-section {
        background: linear-gradient(135deg, #1b4d20 0%, #2d6e32 50%, #3d7d43 100%);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    
    [data-theme="dark"] .activity-card {
        background: linear-gradient(135deg, #2a2a2a 0%, #1e3d25 100%);
        color: #e0e0e0;
    }
    
    [data-theme="dark"] .activity-card h2 {
        color: #81c784 !important;
    }
    
    [data-theme="dark"] .activity-card p {
        color: #c8c8c8 !important;
    }
    
    [data-theme="dark"] .price-table {
        background: #2a2a2a;
        border: 1px solid #3d3d3d;
    }
    
    [data-theme="dark"] .price-row {
        border-bottom: 1px solid #3d3d3d;
    }
    
    [data-theme="dark"] .price-row:hover {
        background: #1e3d25;
    }
    
    [data-theme="dark"] .service-name {
        color: #81c784;
    }
    
    [data-theme="dark"] .price-amount {
        color: #a5d6a7;
    }
    
    [data-theme="dark"] .inclusion-card {
        background: linear-gradient(135deg, #1e3d25 0%, #2d4f32 100%);
        border: 2px solid #4caf50;
    }
    
    [data-theme="dark"] .inclusion-item {
        color: #c8e6c9;
    }
    
    [data-theme="dark"] .inclusion-item:before {
        color: #81c784;
    }
    
    [data-theme="dark"] .gallery-caption {
        color: #81c784;
        background: rgba(0, 0, 0, 0.5);
        padding: 0.5rem;
        border-radius: 4px;
    }
    
    [data-theme="dark"] .section-header {
        color: #81c784;
        border-bottom: 4px solid #4caf50;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] {
        background: #1e3d25;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] h3 {
        color: #81c784 !important;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] .stInfo, 
    [data-theme="dark"] [data-testid="stSidebar"] .stSuccess {
        background-color: #2a2a2a !important;
        border: 1px solid #4caf50;
        color: #e0e0e0 !important;
    }
    
    [data-theme="dark"] [data-testid="stSidebar"] .stInfo p,
    [data-theme="dark"] [data-testid="stSidebar"] .stSuccess p {
        color: #e0e0e0 !important;
    }
    
    [data-theme="dark"] .logo-container svg {
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.6)) brightness(1.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'


def render_hero_section():
    """Render the hero section with resort description and logo"""
    # Display logo - optimized for 1366x768 landscape SVG
    if os.path.exists(LOGO_PATH):
        # Handle SVG or image files
        if LOGO_PATH.endswith('.svg'):
            with open(LOGO_PATH, 'r') as f:
                svg_content = f.read()
            st.markdown(f'''
            <div class="logo-container">
                <div style="max-width: 900px; width: 100%;">
                    {svg_content}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                logo = Image.open(LOGO_PATH)
                st.image(logo, use_container_width=True)
    
    st.markdown("""
    <div class="hero-section">
        <h1 style="text-align: center; font-size: 2.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">Welcome to Pachena Resort</h1>
        <h3 style="text-align: center; margin-top: 0.5rem; font-size: 1.5rem;">Your Gateway to Nature & Relaxation</h3>
        <p style="font-size: 1.15rem; margin-top: 1.5rem; text-align: center; line-height: 1.6;">
            Escape to the tranquility of Pachena Resort, where comfortable tented accommodation meets 
            authentic farm experiences. Nestled in nature's embrace, we offer the perfect blend of 
            adventure, relaxation, and genuine hospitality.
        </p>
        <p style="font-size: 1.1rem; text-align: center; margin-top: 1rem; line-height: 1.6;">
            From guided farm tours and bonfire chats to spa treatments and nature walks, 
            every moment at Pachena is designed to reconnect you with the beauty of the outdoors.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_gallery_section():
    """Render photo gallery with captions"""
    st.markdown('<h2 class="section-header">📸 Resort Gallery</h2>', unsafe_allow_html=True)
    st.markdown("Discover the beauty and charm of Pachena Resort through our photo collection")
    
    # Display images in a grid (4 columns)
    cols_per_row = 4
    
    for i in range(0, len(GALLERY_IMAGES), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(GALLERY_IMAGES):
                img_data = GALLERY_IMAGES[idx]
                img_file = img_data["file"]
                caption = img_data["caption"]
                
                if os.path.exists(img_file):
                    with cols[j]:
                        try:
                            img = Image.open(img_file)
                            st.image(img, use_container_width=True)
                            st.markdown(f'<p class="gallery-caption">{caption}</p>', unsafe_allow_html=True)
                        except Exception as e:
                            st.warning(f"Could not load {img_file}")


def render_activities_section():
    """Render the activities section in a grid layout"""
    st.markdown('<h2 class="section-header">🌟 Our Experiences</h2>', unsafe_allow_html=True)
    st.markdown("Immerse yourself in a variety of activities designed for relaxation and adventure")
    
    # Create a 3-column grid for activities
    cols = st.columns(3)
    
    for idx, activity in enumerate(ACTIVITIES):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="activity-card">
                <h2 style="margin: 0; color: #1b5e20;">{activity['icon']} {activity['name']}</h2>
                <p style="margin-top: 0.5rem; color: #424242; line-height: 1.5;">{activity['description']}</p>
            </div>
            """, unsafe_allow_html=True)


def render_pricing_section():
    """Render the pricing section with clear service-price layout"""
    st.markdown('<h2 class="section-header">💰 Rates & Pricing</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Pachena Resort Rates (Per Person)")
        st.markdown("""
        <div class="price-table">
        """, unsafe_allow_html=True)
        
        # Display each price item
        for service, price in PRICING.items():
            price_text = f"${price}" if "Starting" not in service else f"Starting at ${price}"
            st.markdown(f"""
            <div class="price-row">
                <span class="service-name">{service}</span>
                <span class="price-amount">{price_text}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### What's Included")
        st.markdown('<div class="inclusion-card">', unsafe_allow_html=True)
        
        for inclusion in PACKAGE_INCLUSIONS:
            st.markdown(f'<div class="inclusion-item">{inclusion}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.info("💡 **Note:** Child packages apply to children under 12 years old")


def render_booking_form():
    """Render the booking enquiry form"""
    st.markdown('<h2 class="section-header">📝 Book Your Stay</h2>', unsafe_allow_html=True)
    st.markdown("Complete the form below and our team will contact you to confirm your booking")
    
    with st.form("booking_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            phone = st.text_input("Phone Number *", placeholder="+263 775 387 683")
            booking_date = st.date_input("Preferred Date *", min_value=date.today())
        
        with col2:
            num_adults = st.number_input("Number of Adults *", min_value=0, max_value=20, value=1)
            num_children = st.number_input("Number of Children (Under 12)", min_value=0, max_value=20, value=0)
            
            package_options = list(PRICING.keys())
            package = st.selectbox("Select Package/Service *", options=package_options)
        
        # Additional comments
        comments = st.text_area("Special Requests or Questions", placeholder="Any dietary requirements, special occasions, or questions?")
        
        submitted = st.form_submit_button("Submit Booking Enquiry", use_container_width=True)
        
        if submitted:
            # Validation
            if not name or not phone:
                st.error("❌ Please fill in all required fields (Name and Phone)")
            elif num_adults == 0 and num_children == 0:
                st.error("❌ Please specify at least one adult or child")
            else:
                # Insert into database
                result = insert_enquiry(
                    name=name,
                    phone=phone,
                    date=str(booking_date),
                    num_adults=num_adults,
                    num_children=num_children,
                    package=package
                )
                
                if result.get("success"):
                    st.success("🎉 Thank you for your booking enquiry! Our team will contact you shortly to confirm your reservation.")
                    st.balloons()
                    st.info(f"📧 You can also reach us directly at {CONTACT_EMAIL} or call {CONTACT_PHONE}")
                else:
                    st.error(f"❌ Error submitting enquiry: {result.get('error')}")


def render_public_page():
    """Render the complete public landing page"""
    render_hero_section()
    st.divider()
    render_gallery_section()
    st.divider()
    render_activities_section()
    st.divider()
    render_pricing_section()
    st.divider()
    render_booking_form()


def render_staff_login():
    """Render the staff login page"""
    st.header("🔐 Staff Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")


def render_admin_dashboard():
    """Render the admin dashboard"""
    st.header("📊 Admin Dashboard")
    
    # Logout button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    st.divider()
    
    # Fetch all enquiries
    enquiries_df = fetch_all_enquiries()
    
    if enquiries_df.empty:
        st.info("No enquiries found in the database.")
        return
    
    # Display summary metrics
    st.subheader("📈 Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Enquiries", len(enquiries_df))
    
    with col2:
        pending = len(enquiries_df[enquiries_df.get('status', 'pending') == 'pending'])
        st.metric("Pending", pending)
    
    with col3:
        total_adults = enquiries_df['num_adults'].sum()
        st.metric("Total Adults", int(total_adults))
    
    with col4:
        total_children = enquiries_df['num_children'].sum()
        st.metric("Total Children", int(total_children))
    
    st.divider()
    
    # Display enquiries table
    st.subheader("📋 All Enquiries")
    
    # Select columns to display
    display_columns = ['id', 'name', 'phone', 'booking_date', 'num_adults', 
                      'num_children', 'package', 'status', 'created_at']
    
    available_columns = [col for col in display_columns if col in enquiries_df.columns]
    st.dataframe(enquiries_df[available_columns], use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Section for adding follow-up notes and generating quotations
    st.subheader("🔧 Manage Enquiry")
    
    enquiry_ids = enquiries_df['id'].tolist()
    selected_id = st.selectbox("Select Enquiry ID", options=enquiry_ids)
    
    if selected_id:
        selected_enquiry = enquiries_df[enquiries_df['id'] == selected_id].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Customer Details:**")
            st.write(f"Name: {selected_enquiry['name']}")
            st.write(f"Phone: {selected_enquiry['phone']}")
            st.write(f"Date: {selected_enquiry['booking_date']}")
            st.write(f"Adults: {selected_enquiry['num_adults']}")
            st.write(f"Children: {selected_enquiry['num_children']}")
            st.write(f"Package: {selected_enquiry['package']}")
            
            # Update status
            st.markdown("**Update Status:**")
            new_status = st.selectbox("Change Status", 
                                     options=['pending', 'confirmed', 'completed', 'cancelled'],
                                     key='status_select')
            if st.button("Update Status"):
                result = update_enquiry_status(selected_id, new_status)
                if result.get("success"):
                    st.success("Status updated successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error')}")
        
        with col2:
            # Add follow-up notes
            st.markdown("**Follow-up Notes:**")
            current_notes = selected_enquiry.get('follow_up_notes', '')
            notes = st.text_area("Add Notes", value=current_notes, height=150)
            
            if st.button("Save Notes"):
                result = update_follow_up_notes(selected_id, notes)
                if result.get("success"):
                    st.success("Notes saved successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('error')}")
            
            # Generate quotation
            st.markdown("**Generate Quotation:**")
            if st.button("Calculate Quotation"):
                quotation = calculate_quotation(
                    num_adults=int(selected_enquiry['num_adults']),
                    num_children=int(selected_enquiry['num_children']),
                    package=selected_enquiry['package']
                )
                
                st.markdown("---")
                st.markdown("**Quotation Breakdown:**")
                st.write(f"Adults: {quotation['num_adults']} × ${quotation['adult_price']} = ${quotation['adults_total']}")
                st.write(f"Children: {quotation['num_children']} × ${quotation['child_price']} = ${quotation['children_total']}")
                st.write(f"Package: {quotation['package']} = ${quotation['package_price']}")
                st.write(f"Subtotal: ${quotation['subtotal']:.2f}")
                st.write(f"Tax (12%): ${quotation['tax']:.2f}")
                st.markdown(f"**Total: ${quotation['total']:.2f}**")


def main():
    """Main application"""
    
    # Sidebar with logo - optimized for landscape SVG
    if os.path.exists(LOGO_PATH):
        try:
            if LOGO_PATH.endswith('.svg'):
                with open(LOGO_PATH, 'r') as f:
                    svg_content = f.read()
                st.sidebar.markdown(f'''
                <div style="max-width: 100%; overflow: hidden; margin-bottom: 1rem;">
                    {svg_content}
                </div>
                ''', unsafe_allow_html=True)
            else:
                logo = Image.open(LOGO_PATH)
                st.sidebar.image(logo, use_container_width=True)
        except:
            st.sidebar.title("Pachena Resort")
    else:
        st.sidebar.title("Pachena Resort")
    
    if not st.session_state.logged_in:
        page = st.sidebar.radio("Navigation", ["🏠 Home", "🔐 Staff Login"], label_visibility="collapsed")
    else:
        page = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Admin Dashboard"], label_visibility="collapsed")
    
    st.sidebar.divider()
    st.sidebar.markdown("### 📞 Contact Us")
    st.sidebar.info(f"📧 {CONTACT_EMAIL}\n\n📱 {CONTACT_PHONE}")
    
    st.sidebar.divider()
    st.sidebar.markdown("### 🕒 Operating Hours")
    st.sidebar.success("**Open Daily**\n\n🌅 8:00 AM - 6:00 PM")
    
    # Clean up page names for routing
    page_clean = page.split(" ", 1)[1] if " " in page else page
    
    # Render appropriate page
    if "Home" in page:
        render_public_page()
    elif "Staff Login" in page:
        render_staff_login()
    elif "Admin Dashboard" in page:
        if st.session_state.logged_in:
            render_admin_dashboard()
        else:
            st.warning("Please log in to access the admin dashboard")
            render_staff_login()


if __name__ == "__main__":
    main()
