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

An intelligent article summarization tool that extracts content from web URLs and generates concise summaries using AI models. Export your research directly to PowerPoint presentations.

## 🚀 Quick Start

### Option 1: Streamlit Cloud (Recommended)
Deploy directly to Streamlit Cloud for instant access:

1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy your fork
4. Configure secrets in Streamlit Cloud settings:
   - `OPENAI_API_KEY` (for AI summaries)
   - `SUPABASE_URL` and `SUPABASE_KEY` (optional, for data storage)

### Option 2: Local Installation

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

#### One-Click Setup

**For Mac/Linux users:**
```bash
git clone https://github.com/yourusername/research-deck.git
cd research-deck
./start.sh
```

**For Windows users:**
```cmd
git clone https://github.com/yourusername/research-deck.git
cd research-deck
start.bat
```

That's it! The script will:
- ✅ Check if Docker is running
- 📦 Download and start all required services
- 🌐 Open the app at http://localhost:8501

#### Manual Setup (Alternative)
```bash
git clone https://github.com/yourusername/research-deck.git
cd research-deck
docker compose up -d
```

## Features

- 🔍 **Smart Content Extraction**: Automatically extracts article content, metadata, and Open Graph data
- 🤖 **AI Processing**: Uses OpenAI GPT for high-quality summaries
- 📊 **PowerPoint Export**: Create new presentations or append to existing ones
- 💾 **Optional Database Storage**: Persistent storage of summaries using Supabase
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface
- ☁️ **Cloud Ready**: Optimized for Streamlit Cloud deployment

## How to Use

1. Enter one or more article URLs (one per line)
2. Choose your preferred processing method:
   - **OpenAI GPT**: High-quality AI summaries (requires API key)
   - **Basic Text Extraction**: Simple text extraction (no API required)
3. Click "Start Summarization"
4. Download your PowerPoint presentation

## Configuration

### Streamlit Cloud Secrets
Configure these in your Streamlit Cloud app settings → Secrets:

```toml
# Required for AI summaries
OPENAI_API_KEY = "your_openai_api_key"

# Optional for database storage
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
```

### Local Environment Variables
For local development, create a `.env` file:

```bash
# For OpenAI GPT (higher quality summaries)
OPENAI_API_KEY=your_openai_key

# For database storage (optional)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Stopping the Application (Local)

**Easy way:**
```bash
./stop.sh    # Mac/Linux
stop.bat     # Windows
```

**Manual way:**
```bash
docker compose down
```

## Project Structure

```
research-deck/
├── 🚀 start.sh / start.bat     # One-click startup scripts
├── 🛑 stop.sh / stop.bat       # Easy shutdown scripts
├── 🐳 docker-compose.yaml      # Docker services configuration
├── 📱 app.py                   # Main Streamlit application
├── 🔧 Dockerfile               # Container build instructions
├── 📋 requirements.txt         # Python dependencies
├── ⚙️  config.py               # Environment configuration
├── 🌐 article_info_extractor.py # Web scraping logic
├── 🤖 summarize.py             # AI summarization logic
├── 💾 db.py                    # Database operations
├── 📊 ppt_handler.py           # PowerPoint generation
└── 🎨 .streamlit/              # UI configuration
```

## Deployment Options

### Streamlit Cloud (Recommended)
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Built-in secrets management
- ✅ No server maintenance

### Docker Deployment
- ✅ Self-hosted control
- ✅ Custom infrastructure
- ✅ Full feature access

## Troubleshooting

**"Docker is not running"**: Start Docker Desktop and wait for it to fully load

**"Site cannot be reached"**: Wait a few minutes for services to start

**API errors**: Ensure your OpenAI API key is correctly configured in secrets

**Slow performance**: Basic text extraction is faster but less detailed than AI summaries

## Technologies Used

- **Streamlit**: Web interface and cloud hosting
- **OpenAI GPT**: AI-powered summarization
- **Playwright**: Enhanced web scraping
- **python-pptx**: PowerPoint generation
- **Docker**: Containerized deployment
- **Supabase**: Optional database storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

💳 Support this project: [Venmo @jonatng](https://venmo.com/u/jonatng)
🔗 Connect: [LinkedIn](https://www.linkedin.com/in/jonatng/)

## License

MIT License - see LICENSE file for details.

---

*Built with ❤️ for researchers and content creators | Optimized for Streamlit Cloud*