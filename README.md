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

## 🚀 Quick Start (Local Installation)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### One-Click Setup

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
- 🤖 Set up the AI model (llama2)
- 🌐 Open the app at http://localhost:7860

### Manual Setup (Alternative)
```bash
git clone https://github.com/yourusername/research-deck.git
cd research-deck
docker compose up -d
```

## Features

- 🔍 **Smart Content Extraction**: Automatically extracts article content, metadata, and Open Graph data
- 🤖 **Local AI Processing**: Uses Ollama with Llama2 model (no API keys required!)
- 📊 **PowerPoint Export**: Create new presentations or append to existing ones
- 💾 **Optional Database Storage**: Persistent storage of summaries using Supabase
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface

## How to Use

1. Enter one or more article URLs (one per line)
2. Choose your preferred AI model:
   - **Ollama Local Model**: Free, runs locally, no API required
   - **OpenAI GPT**: Requires API key, higher quality summaries
3. Click "Run Summarization"
4. Download your PowerPoint presentation

## Optional Enhancements

For enhanced features, you can set these environment variables:

```bash
# For OpenAI GPT (higher quality summaries)
export OPENAI_API_KEY=your_openai_key
export USE_OPENAI=true

# For database storage
export SUPABASE_URL=your_supabase_url
export SUPABASE_KEY=your_supabase_key
```

## Stopping the Application

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

## Troubleshooting

**"Docker is not running"**: Start Docker Desktop and wait for it to fully load

**"Site cannot be reached"**: Wait a few minutes for the AI model to download on first run

**Slow performance**: The local AI model takes time to process. For faster results, consider using OpenAI API

## Technologies Used

- **Streamlit**: Web interface
- **Ollama + Llama2**: Local AI model (no API required)
- **OpenAI GPT**: Optional enhanced AI (requires API key)
- **Playwright**: Web scraping
- **python-pptx**: PowerPoint generation
- **Docker**: Containerized deployment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

💳 Support this project: [Venmo @jonatng](https://venmo.com/u/jonatng)
🔗 Connect: [LinkedIn](https://www.linkedin.com/in/jonatng/)

## License

MIT License - see LICENSE file for details.

---

*Built with ❤️ for researchers and content creators*