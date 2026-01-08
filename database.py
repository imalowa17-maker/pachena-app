from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime
import pandas as pd

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Create and return a Supabase client"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_enquiry(name: str, phone: str, date: str, num_adults: int, 
                   num_children: int, package: str) -> dict:
    """
    Insert a new enquiry into the Supabase 'enquiries' table
    
    Args:
        name: Customer name
        phone: Contact phone number
        date: Booking date
        num_adults: Number of adults
        num_children: Number of children
        package: Selected package name
    
    Returns:
        dict: Response from Supabase insertion
    """
    try:
        supabase = get_supabase_client()
        
        enquiry_data = {
            "name": name,
            "phone": phone,
            "booking_date": date,
            "num_adults": num_adults,
            "num_children": num_children,
            "package": package,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "follow_up_notes": ""
        }
        
        response = supabase.table("enquiries").insert(enquiry_data).execute()
        return {"success": True, "data": response.data}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_all_enquiries() -> pd.DataFrame:
    """
    Fetch all enquiries from Supabase and return as a Pandas DataFrame
    
    Returns:
        pd.DataFrame: DataFrame containing all enquiries
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("enquiries").select("*").order("created_at", desc=True).execute()
        
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error fetching enquiries: {e}")
        return pd.DataFrame()


def update_follow_up_notes(enquiry_id: int, notes: str) -> dict:
    """
    Update follow-up notes for a specific enquiry
    
    Args:
        enquiry_id: ID of the enquiry to update
        notes: Follow-up notes to add
    
    Returns:
        dict: Response from Supabase update
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("enquiries").update({
            "follow_up_notes": notes,
            "updated_at": datetime.now().isoformat()
        }).eq("id", enquiry_id).execute()
        
        return {"success": True, "data": response.data}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_enquiry_status(enquiry_id: int, status: str) -> dict:
    """
    Update the status of a specific enquiry
    
    Args:
        enquiry_id: ID of the enquiry to update
        status: New status (e.g., 'pending', 'confirmed', 'completed')
    
    Returns:
        dict: Response from Supabase update
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("enquiries").update({
            "status": status,
            "updated_at": datetime.now().isoformat()
        }).eq("id", enquiry_id).execute()
        
        return {"success": True, "data": response.data}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def calculate_quotation(num_adults: int, num_children: int, package: str) -> dict:
    """
    Calculate quotation based on pricing
    
    Args:
        num_adults: Number of adults
        num_children: Number of children
        package: Package name
    
    Returns:
        dict: Quotation details with breakdown
    """
    from config import PRICING
    
    adult_price = PRICING["Adult"]
    child_price = PRICING["Child"]
    
    # Base calculation
    adults_total = num_adults * adult_price
    children_total = num_children * child_price
    
    # Package pricing
    package_price = PRICING.get(package, 0)
    
    subtotal = adults_total + children_total + package_price
    tax = subtotal * 0.12  # 12% tax
    total = subtotal + tax
    
    return {
        "num_adults": num_adults,
        "num_children": num_children,
        "adult_price": adult_price,
        "child_price": child_price,
        "adults_total": adults_total,
        "children_total": children_total,
        "package": package,
        "package_price": package_price,
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    }
