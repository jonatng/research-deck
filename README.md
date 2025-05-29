---
title: AI Research Deck
emoji: 📰
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.45.1
app_file: app.py
pinned: false
license: mit
---

# �� AI Research Deck

A secure, intelligent article summarization platform with user authentication, AI-powered content extraction, and dark mode UI. Transform web articles into professional PowerPoint presentations with advanced anti-bot web scraping.

## ✨ Key Features

- 🔐 **User Authentication**: Secure login system with user-specific data storage
- 🌙 **Dark Mode Interface**: Modern, eye-friendly dark theme throughout
- 🛡️ **Advanced Web Scraping**: Hybrid extraction with anti-bot evasion techniques
- 🤖 **Enhanced AI Summaries**: Structured summaries with key points and analysis
- 📊 **Smart PowerPoint Export**: Professional presentations with organized content
- ☁️ **Streamlit Cloud Optimized**: Reliable deployment without heavy dependencies
- 💾 **Supabase Integration**: Secure user data and summary storage

## 🚀 Quick Start

### Streamlit Cloud Deployment (Recommended)

1. **Fork this repository**
2. **Connect to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Deploy your fork**
4. **Configure secrets** in Streamlit Cloud settings (see Configuration section)
5. **Set up Supabase database** (see Database Setup section)

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/research-deck.git
cd research-deck

# Install dependencies
pip install -r requirements.txt

# Create .streamlit/secrets.toml with your credentials
# Run the application
streamlit run app.py
```

## 🔧 Configuration

### Required Streamlit Cloud Secrets

Configure these in your Streamlit Cloud app settings → Secrets:

```toml
# Supabase Database (Required)
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"

# OpenAI API (Required for AI summaries)
OPENAI_API_KEY = "your-openai-api-key"
```

### Local Development (.streamlit/secrets.toml)

```toml
# Supabase Configuration
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"

# OpenAI Configuration
OPENAI_API_KEY = "your-openai-api-key"
```

## 🗄️ Database Setup

### 1. Create Supabase Project
1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Set Up Database Tables
Run this SQL in your Supabase SQL Editor:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_summaries_user_id ON summaries(user_id);

-- Insert demo user (password: testpass123)
INSERT INTO users (username, email, password_hash, is_active) 
VALUES (
    'testuser', 
    'test@example.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.e',
    TRUE
) ON CONFLICT (username) DO NOTHING;
```

## 👤 User Authentication

### Demo Account
- **Username**: `testuser`
- **Password**: `testpass123`

### User Registration
Users can create new accounts through the registration tab with:
- Unique username and email
- Secure password hashing with bcrypt
- Email validation

### Security Features
- ✅ Bcrypt password hashing with salt
- ✅ User session management
- ✅ Data isolation per user
- ✅ Secure database policies

## 🕷️ Enhanced Web Scraping

### Anti-Bot Evasion Techniques
- **Multiple User Agents**: Random selection from real browser signatures
- **Stealth Headers**: Realistic browser fingerprints and request patterns
- **Session Management**: Persistent cookies and retry mechanisms
- **Smart Fallbacks**: Cloud-optimized requests when browser automation fails

### Content Extraction Strategies
1. **Semantic HTML Analysis**: Target `<article>`, `<main>`, content-specific classes
2. **Largest Text Block Detection**: Statistical analysis for main content
3. **Multiple CSS Selectors**: Comprehensive coverage of content patterns
4. **Clean Content Filtering**: Remove navigation, ads, and boilerplate

### Environment Adaptation
- **Streamlit Cloud**: Uses lightweight, cloud-optimized requests
- **Local Development**: Full browser automation with Playwright
- **Automatic Detection**: Adapts strategy based on deployment environment

## 🤖 AI-Powered Summarization

### Enhanced Summary Format
```
1. **Main Topic/Title**: Clear article identification
2. **Key Points**: Bullet-pointed main ideas
3. **Important Details**: Specific facts and numbers  
4. **Summary**: Concluding analysis
```

### AI Configuration
- **Model**: GPT-4o-mini for cost-effective, high-quality summaries
- **Temperature**: 0.3 for consistent, factual output
- **Max Tokens**: 1000 for detailed analysis
- **System Prompt**: Expert content analyst persona

## 📊 PowerPoint Integration

### Features
- **Professional Formatting**: Clean, readable slide layouts
- **Metadata Integration**: Titles, URLs, and timestamps
- **Batch Processing**: Multiple articles in one presentation
- **Append Mode**: Add to existing PowerPoint files

## 🎨 Dark Mode Design

### Visual Features
- **Consistent Dark Theme**: Throughout login and main application
- **Coral Accent Color**: Modern `#FF6B6B` highlight color
- **Smooth Transitions**: Polished hover effects and animations
- **Accessibility**: High contrast for better readability

### Component Styling
- ✅ Dark input fields and buttons
- ✅ Styled tabs and navigation
- ✅ Custom form elements
- ✅ Themed success/error messages

## 📁 Project Structure

```
research-deck/
├── 📱 app.py                      # Main Streamlit application
├── 🔐 auth.py                     # Authentication system
├── 🔑 login_page.py               # Login/registration interface
├── 🌐 article_info_extractor.py   # Hybrid web scraping system
├── 🤖 summarize.py                # Enhanced AI summarization
├── 💾 db.py                       # Supabase database operations
├── 📊 ppt_handler.py              # PowerPoint generation
├── ⚙️  config.py                  # Environment configuration
├── 🧪 setup_database.py           # Database setup utilities
├── 📋 requirements.txt            # Python dependencies (cloud-optimized)
├── 📦 packages.txt                # System packages (minimal for cloud)
├── 🎨 .streamlit/
│   ├── config.toml                # Dark theme configuration
│   └── secrets.toml               # Local development secrets
└── 📚 README.md                   # This file
```

## 🔍 How to Use

### 1. Authentication
- Login with existing account or register new user
- Demo account available for testing

### 2. Article Processing
- Enter article URLs (one per line)
- Choose processing method:
  - **OpenAI GPT**: Structured AI summaries with key points
  - **Basic Text Extraction**: Simple content extraction
- Click "Start Summarization"

### 3. Export Results
- Download generated PowerPoint presentation
- Summaries automatically saved to your account
- View processing statistics and method used

## 🚀 Deployment

### Streamlit Cloud Benefits
- ✅ **Free hosting** with automatic deployments
- ✅ **Built-in secrets management** for secure configuration
- ✅ **No browser dependencies** - uses cloud-optimized extraction
- ✅ **Fast deployment** with minimal system requirements
- ✅ **Automatic scaling** and reliability

### Deployment Requirements
- **Supabase account** for user data and authentication
- **OpenAI API key** for AI-powered summaries
- **GitHub repository** connected to Streamlit Cloud

## 🛠️ Troubleshooting

### Common Issues

**Login/Registration Fails**
- ✅ Check Supabase credentials in secrets
- ✅ Verify database tables are created
- ✅ Confirm internet connectivity

**Poor Content Extraction**
- ✅ Try different URLs - some sites have better anti-bot protection
- ✅ Cloud environment automatically uses optimized extraction
- ✅ Check if site requires JavaScript (will fallback gracefully)

**AI Summary Errors**
- ✅ Verify OpenAI API key is correct and has credits
- ✅ Check API rate limits
- ✅ Use Basic Text Extraction as fallback

**Deployment Issues**
- ✅ Ensure packages.txt is minimal (avoid system dependencies)
- ✅ Check requirements.txt for cloud compatibility
- ✅ Verify all secrets are properly configured

## 🔗 Technologies

### Core Stack
- **Streamlit**: Web interface and cloud hosting
- **Supabase**: PostgreSQL database with authentication
- **OpenAI GPT-4o-mini**: AI-powered content analysis
- **BeautifulSoup4**: HTML parsing and content extraction
- **Bcrypt**: Secure password hashing

### Enhanced Features
- **Requests**: Cloud-optimized HTTP client with anti-bot techniques
- **Python-PPTX**: Professional PowerPoint generation
- **Random/Time**: Smart delays and evasion patterns

### Optional (Local Development)
- **Playwright**: Browser automation for complex sites
- **Pillow/Pytesseract**: OCR capabilities (local only)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional content extraction strategies
- New export formats (PDF, Word, etc.)
- Enhanced UI components
- Performance optimizations

## 💝 Support

- 💳 **Support this project**: [Venmo @jonatng](https://venmo.com/u/jonatng)
- 🔗 **Connect**: [LinkedIn](https://www.linkedin.com/in/jonatng/)

## 📄 License

MIT License - see LICENSE file for details.

---

*Built with ❤️ for researchers and content creators | Optimized for Streamlit Cloud with enterprise-grade security*