import os
import bcrypt
import streamlit as st
from datetime import datetime
from db import supabase

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username: str, email: str, password: str) -> bool:
    """Create a new user in the database"""
    if not supabase:
        print("⚠️ Database not available - cannot create user")
        return False
    
    try:
        # Check if user already exists
        existing_user = supabase.table("users").select("*").eq("username", username).execute()
        if existing_user.data:
            print(f"❌ User {username} already exists")
            return False
        
        # Check if email already exists
        existing_email = supabase.table("users").select("*").eq("email", email).execute()
        if existing_email.data:
            print(f"❌ Email {email} already exists")
            return False
        
        # Hash password and create user
        hashed_password = hash_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        result = supabase.table("users").insert(user_data).execute()
        print(f"✅ User {username} created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return False

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user and return user data if successful"""
    if not supabase:
        print("⚠️ Database not available - cannot authenticate")
        return None
    
    try:
        # Get user from database
        result = supabase.table("users").select("*").eq("username", username).execute()
        
        if not result.data:
            print(f"❌ User {username} not found")
            return None
        
        user = result.data[0]
        
        # Check if user is active
        if not user.get("is_active", True):
            print(f"❌ User {username} is deactivated")
            return None
        
        # Verify password
        if verify_password(password, user["password_hash"]):
            print(f"✅ User {username} authenticated successfully")
            # Remove password hash from returned data
            user_data = {k: v for k, v in user.items() if k != "password_hash"}
            return user_data
        else:
            print(f"❌ Invalid password for user {username}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def update_last_login(username: str) -> bool:
    """Update the last login timestamp for a user"""
    if not supabase:
        return False
    
    try:
        result = supabase.table("users").update({
            "last_login": datetime.now().isoformat()
        }).eq("username", username).execute()
        return True
    except Exception as e:
        print(f"❌ Failed to update last login: {e}")
        return False

def get_user_summaries(user_id: int):
    """Get summaries for a specific user"""
    if not supabase:
        return []
    
    try:
        result = supabase.table("summaries").select("*").eq("user_id", user_id).execute()
        return result.data
    except Exception as e:
        print(f"❌ Failed to get user summaries: {e}")
        return []

def is_logged_in() -> bool:
    """Check if user is logged in"""
    return "user" in st.session_state and st.session_state.user is not None

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get("user", None)

def logout():
    """Log out the current user"""
    if "user" in st.session_state:
        del st.session_state.user
    st.rerun()

def require_auth():
    """Decorator function to require authentication"""
    if not is_logged_in():
        st.error("🔒 Please log in to access this feature")
        st.stop()

# Initialize test user if database is available
def create_test_user():
    """Create a test user for demonstration"""
    if supabase:
        # Create test user: username=testuser, password=testpass123
        create_user("testuser", "test@example.com", "testpass123")
        print("🧪 Test user created: username=testuser, password=testpass123") 