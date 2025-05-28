import streamlit as st
from auth import authenticate_user, create_user, update_last_login, is_logged_in, get_current_user, logout

def show_login_page():
    """Display the login/registration page"""
    
    # Custom CSS for dark mode login page
    st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
        }
        
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: #262730;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            border: 1px solid #3D4551;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #FAFAFA;
        }
        
        .login-header h1 {
            color: #FAFAFA;
            margin-bottom: 0.5rem;
        }
        
        .login-header p {
            color: #A6A6A6;
        }
        
        .login-tabs {
            display: flex;
            margin-bottom: 2rem;
        }
        
        .demo-credentials {
            background: #1E2329;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #FF6B6B;
            color: #FAFAFA;
        }
        
        .demo-credentials h4 {
            color: #FAFAFA;
            margin-bottom: 0.5rem;
        }
        
        .demo-credentials p {
            color: #A6A6A6;
            margin: 0.25rem 0;
        }
        
        .demo-credentials em {
            color: #8A8A8A;
        }
        
        /* Style form inputs for dark mode */
        .stTextInput > div > div > input {
            background-color: #1E2329;
            color: #FAFAFA;
            border: 1px solid #3D4551;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FF6B6B;
            box-shadow: 0 0 0 1px #FF6B6B;
        }
        
        /* Style tabs for dark mode */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #262730;
            border-radius: 8px 8px 0 0;
            border-bottom: 1px solid #3D4551;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1E2329;
            color: #A6A6A6;
            border: 1px solid #3D4551;
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            margin-right: 2px;
            padding: 12px 24px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #262730;
            color: #FAFAFA;
            border-color: #5A6270;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #262730;
            color: #FAFAFA;
            border-color: #FF6B6B;
            border-bottom: 2px solid #FF6B6B;
            box-shadow: 0 -2px 8px rgba(255, 107, 107, 0.2);
        }
        
        /* Style tab content area */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: #262730;
            border: 1px solid #3D4551;
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 2rem;
        }
        
        /* Style buttons for dark mode */
        .stButton > button {
            background-color: #FF6B6B;
            color: #FAFAFA;
            border: none;
            border-radius: 6px;
        }
        
        .stButton > button:hover {
            background-color: #FF5252;
            color: #FAFAFA;
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

def show_login_form():
    """Display the login form"""
    with st.form("login_form"):
        st.subheader("Welcome Back!")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        login_button = st.form_submit_button("🔑 Login", use_container_width=True)
        
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