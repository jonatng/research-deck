import streamlit as st
from auth import authenticate_user, create_user, update_last_login, is_logged_in, get_current_user, logout

def show_login_page():
    """Display the login/registration page"""
    
    # Custom CSS for login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-tabs {
            display: flex;
            margin-bottom: 2rem;
        }
        
        .demo-credentials {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="login-header">
        <h1>🔐 AI Research Deck</h1>
        <p>Please log in to access your personalized research dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_registration_form()
    
    # Demo credentials info
    st.markdown("""
    <div class="demo-credentials">
        <h4>🧪 Demo Credentials</h4>
        <p><strong>Username:</strong> testuser</p>
        <p><strong>Password:</strong> testpass123</p>
        <p><em>Use these credentials to test the application</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_login_form():
    """Display the login form"""
    with st.form("login_form"):
        st.subheader("Welcome Back!")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🔑 Login", use_container_width=True)
        with col2:
            demo_login = st.form_submit_button("🧪 Demo Login", use_container_width=True)
        
        if login_button:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    update_last_login(username)
                    st.success(f"✅ Welcome back, {user['username']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        if demo_login:
            user = authenticate_user("testuser", "testpass123")
            if user:
                st.session_state.user = user
                update_last_login("testuser")
                st.success("✅ Logged in with demo account!")
                st.rerun()
            else:
                st.error("❌ Demo account not available. Please create it first.")

def show_registration_form():
    """Display the registration form"""
    with st.form("registration_form"):
        st.subheader("Create New Account")
        
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if register_button:
            if not all([username, email, password, confirm_password]):
                st.warning("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            else:
                if create_user(username, email, password):
                    st.success("✅ Account created successfully! You can now log in.")
                    st.balloons()
                else:
                    st.error("❌ Failed to create account. Username or email may already exist.")

def show_user_header():
    """Display user info and logout button in the sidebar"""
    if is_logged_in():
        user = get_current_user()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 User Info")
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Email:** {user['email']}")
            
            if user.get('last_login'):
                st.write(f"**Last Login:** {user['last_login'][:19]}")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()

def require_login():
    """Check if user is logged in, show login page if not"""
    if not is_logged_in():
        show_login_page()
        st.stop()
    else:
        show_user_header() 