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

# 📰 AI Research Deck

A secure, intelligent article summarization platform with user authentication, AI-powered content extraction, and dark mode UI. Transform web articles into professional PowerPoint presentations with advanced anti-bot web scraping.

## ✨ Key Features

- 🔐 **User Authentication**: Secure login system with bcrypt password hashing and user-specific data storage
- 🌙 **Dark Mode Interface**: Modern, eye-friendly dark theme throughout the entire application
- 🛡️ **Advanced Web Scraping**: Hybrid extraction with anti-bot evasion techniques and cloud optimization
- 🤖 **Enhanced AI Summaries**: Structured summaries with key points, analysis, and professional formatting
- 📊 **Smart PowerPoint Export**: Professional presentations with organized content and metadata
- ☁️ **Streamlit Cloud Optimized**: Reliable deployment without heavy dependencies or browser automation
- 💾 **Supabase Integration**: Secure user data storage with PostgreSQL backend
- 🔒 **Enterprise Security**: Row-level security, data isolation, and secure session management

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
# Supabase Database (Required for authentication and data storage)
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"

# OpenAI API (Optional - enables AI summaries)
OPENAI_API_KEY = "your-openai-api-key"
```

### Local Development (.streamlit/secrets.toml)

```toml
# Supabase Configuration
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"

# OpenAI Configuration (Optional)
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

-- Create indexes for performance
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
Users can create new accounts through the registration interface with:
- Unique username and email validation
- Secure password hashing with bcrypt + salt
- Email format validation
- Password strength requirements (minimum 6 characters)

### Security Features
- ✅ Bcrypt password hashing with salt rounds
- ✅ Secure session management with Streamlit
- ✅ User-specific data isolation
- ✅ Row-level security policies in database
- ✅ Input validation and sanitization
- ✅ Automatic test user creation on startup

## 🕷️ Enhanced Web Scraping

### Cloud-Optimized Architecture
The scraping system automatically adapts to the deployment environment:

- **Streamlit Cloud**: Uses lightweight, cloud-optimized requests with advanced anti-bot techniques
- **Local Development**: Full browser automation with Playwright for complex sites
- **Automatic Detection**: Intelligently selects the best extraction method

### Anti-Bot Evasion Techniques
- **Randomized User Agents**: Rotation of real browser signatures
- **Stealth Headers**: Realistic browser fingerprints and request patterns
- **Session Management**: Persistent cookies and intelligent retry mechanisms
- **Smart Delays**: Human-like timing patterns to avoid detection
- **Multiple Request Strategies**: Fallback approaches for different site types

### Content Extraction Strategies
1. **Semantic HTML Analysis**: Target `<article>`, `<main>`, content-specific classes
2. **Largest Text Block Detection**: Statistical analysis for main content identification
3. **Multiple CSS Selectors**: Comprehensive coverage of content patterns
4. **Clean Content Filtering**: Remove navigation, ads, and boilerplate content
5. **OCR Fallback**: Optional image text extraction for local environments

## 🤖 AI-Powered Summarization

### Enhanced Summary Format
```
1. **Main Topic/Title**: Clear article identification
2. **Key Points**: Bullet-pointed main ideas with explanations
3. **Important Details**: Specific facts, numbers, and notable mentions
4. **Summary**: Concluding analysis and insights
```

### AI Configuration
- **Model**: GPT-4o-mini for cost-effective, high-quality summaries
- **Temperature**: 0.3 for consistent, factual output
- **Max Tokens**: 1000 for detailed analysis
- **System Prompt**: Expert content analyst persona with structured formatting
- **Fallback**: Basic text extraction when AI is unavailable

## 📊 PowerPoint Integration

### Features
- **Professional Formatting**: Clean, readable slide layouts with metadata
- **Batch Processing**: Multiple articles in one presentation
- **Append Mode**: Add summaries to existing PowerPoint files
- **Timestamp Integration**: Automatic dating and URL tracking
- **Custom Layouts**: Optimized slide designs for readability

## 🎨 Dark Mode Design

### Visual Features
- **Consistent Dark Theme**: Throughout login, main app, and all components
- **Coral Accent Color**: Modern `#FF6B6B` highlight color with gradients
- **Smooth Transitions**: Polished hover effects and animations
- **High Contrast**: Accessibility-focused color schemes
- **Custom Components**: Styled forms, buttons, tabs, and notifications

### Component Styling
- ✅ Dark input fields with focus states
- ✅ Styled tabs and navigation elements
- ✅ Custom form validation messages
- ✅ Themed success/error notifications
- ✅ Professional login interface
- ✅ Responsive design elements

## 📁 Project Structure

```
research-deck/
├── 📱 app.py                      # Main Streamlit application with auth integration
├── 🔐 auth.py                     # Complete authentication system with bcrypt
├── 🔑 login_page.py               # Beautiful dark mode login/registration interface
├── 🌐 article_info_extractor.py   # Hybrid web scraping with cloud optimization
├── 🤖 summarize.py                # Enhanced AI summarization with structured output
├── 💾 db.py                       # Supabase integration with user-specific data
├── 📊 ppt_handler.py              # PowerPoint generation and management
├── ⚙️  config.py                  # Flexible environment configuration
├── 🧪 setup_database.py           # Database setup utilities and SQL schema
├── 🎯 llm_clients.py              # AI client initialization and management
├── 📋 requirements.txt            # Python dependencies (cloud-optimized)
├── 📦 packages.txt                # Minimal system packages for cloud deployment
├── 🐳 Dockerfile                  # Container configuration
├── 🔧 docker-compose.yaml         # Local development orchestration
├── 🎨 .streamlit/
│   ├── config.toml                # Dark theme and server configuration
│   └── secrets.toml               # Local development secrets (ignored)
├── 🚀 start.sh / start.bat        # Cross-platform startup scripts
├── 🛑 stop.sh / stop.bat          # Graceful shutdown scripts
└── 📚 README.md                   # This comprehensive documentation
```

## 🔍 How to Use

### 1. Authentication
- **Login**: Use existing account credentials
- **Register**: Create new account with unique username/email
- **Demo**: Use testuser/testpass123 for immediate testing
- **Security**: All passwords are securely hashed with bcrypt

### 2. Article Processing
- **Input URLs**: Enter article URLs (one per line, up to configurable limit)
- **Choose Processing Method**:
  - **OpenAI GPT**: Structured AI summaries with key points and analysis
  - **Basic Text Extraction**: Simple content extraction without AI
- **Upload PowerPoint**: Optional - append to existing presentations
- **Process**: Click "Start Summarization" for automated processing

### 3. Export and Management
- **Download**: Get generated PowerPoint presentation with professional formatting
- **Auto-Save**: Summaries automatically saved to your user account
- **Statistics**: View processing metrics and method used
- **History**: Access previously processed articles (user-specific)

## 🚀 Deployment

### Streamlit Cloud Benefits
- ✅ **Free hosting** with automatic deployments from GitHub
- ✅ **Built-in secrets management** for secure credential storage
- ✅ **No browser dependencies** - uses cloud-optimized extraction methods
- ✅ **Fast deployment** with minimal system requirements
- ✅ **Automatic scaling** and high availability
- ✅ **SSL certificates** and secure HTTPS by default

### Migration from Hugging Face Spaces
This project has been fully migrated from Hugging Face Spaces to Streamlit Cloud:
- ❌ Removed all HF Spaces dependencies and configurations
- ✅ Updated ports from 7860 (HF) to 8501 (Streamlit standard)
- ✅ Removed Ollama local AI dependencies for cloud compatibility
- ✅ Simplified Docker configuration for Streamlit deployment
- ✅ Updated all documentation for Streamlit Cloud focus

### Deployment Requirements
- **GitHub Repository**: Connected to Streamlit Cloud
- **Supabase Account**: For user authentication and data storage
- **OpenAI API Key**: Optional, for AI-powered summaries

## 🛠️ Troubleshooting

### Authentication Issues
**Login/Registration Fails**
- ✅ Verify Supabase credentials in Streamlit secrets
- ✅ Confirm database tables are created with proper schema
- ✅ Check network connectivity to Supabase
- ✅ Ensure demo user exists (testuser/testpass123)

**User Already Exists Error**
- ✅ Try different username/email combination
- ✅ Use demo account for testing
- ✅ Check database for existing users

### Content Extraction Issues
**Poor Content Quality**
- ✅ Some sites have advanced anti-bot protection
- ✅ Cloud environment automatically uses optimized extraction
- ✅ Try different URLs or use Basic mode
- ✅ Check if site requires JavaScript (graceful fallback)

### AI Summary Errors
**OpenAI API Issues**
- ✅ Verify API key is correct and has available credits
- ✅ Check API rate limits and quotas
- ✅ Use Basic Text Extraction as fallback
- ✅ Monitor API usage in OpenAI dashboard

### Deployment Issues
**Streamlit Cloud Deployment**
- ✅ Ensure packages.txt is minimal (avoid heavy system dependencies)
- ✅ Check requirements.txt for cloud compatibility
- ✅ Verify all secrets are properly configured
- ✅ Monitor deployment logs for specific errors

## 🔗 Technologies

### Core Stack
- **Streamlit 1.45.1**: Web interface and cloud hosting platform
- **Supabase**: PostgreSQL database with authentication and real-time features
- **OpenAI GPT-4o-mini**: Cost-effective AI for high-quality content analysis
- **BeautifulSoup4**: Advanced HTML parsing and content extraction
- **Bcrypt**: Industry-standard password hashing with salt

### Enhanced Features
- **Requests**: Cloud-optimized HTTP client with anti-bot techniques
- **Python-PPTX**: Professional PowerPoint generation and manipulation
- **Random/Time**: Smart delays and human-like interaction patterns
- **Python-dotenv**: Environment variable management

### Optional (Local Development)
- **Playwright**: Browser automation for complex sites (local only)
- **Pillow/Pytesseract**: OCR capabilities for image text extraction

### Removed Dependencies
- ❌ **Hugging Face Hub**: Removed for Streamlit Cloud compatibility
- ❌ **Ollama**: Removed local AI dependencies
- ❌ **lxml**: Removed unused dependency causing deployment issues

## 🤝 Contributing

Contributions welcome! Priority areas for improvement:
- Additional content extraction strategies for difficult sites
- New export formats (PDF, Word, Markdown, etc.)
- Enhanced UI components and user experience
- Performance optimizations and caching
- Advanced authentication features (2FA, social login)
- Multi-language support and internationalization

### Development Setup
1. Fork the repository
2. Set up local Supabase instance or use cloud
3. Configure environment variables
4. Install dependencies: `pip install -r requirements.txt`
5. Run locally: `streamlit run app.py`

## 💝 Support

- 💳 **Support this project**: [Venmo @jonatng](https://venmo.com/u/jonatng)
- 🔗 **Connect**: [LinkedIn](https://www.linkedin.com/in/jonatng/)
- 🐛 **Report Issues**: GitHub Issues
- 💡 **Feature Requests**: GitHub Discussions

## 📄 License

MIT License - see LICENSE file for details.

## 🔄 Recent Updates

### v2.1 - Major Migration & Authentication (Current)
- ✅ Complete migration from Hugging Face Spaces to Streamlit Cloud
- ✅ Full user authentication system with bcrypt security
- ✅ User-specific data isolation and session management
- ✅ Enhanced web scraping with cloud optimization
- ✅ Improved AI summarization with structured output
- ✅ Professional dark mode UI throughout application
- ✅ Comprehensive error handling and fallback systems

### v2.0 - Streamlit Cloud Optimization
- ✅ Removed heavy dependencies for cloud compatibility
- ✅ Simplified deployment process
- ✅ Enhanced anti-bot web scraping techniques
- ✅ Improved PowerPoint generation

### v1.x - Initial Hugging Face Version
- ✅ Basic article summarization
- ✅ Simple web scraping
- ✅ PowerPoint export functionality

---

*Built with ❤️ for researchers and content creators | Optimized for Streamlit Cloud with enterprise-grade security and user authentication*