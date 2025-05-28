#!/bin/bash

echo "🚀 Starting AI Research Deck..."
echo "This will start the application with Streamlit."
echo ""

# Add Docker to PATH if it's not already available
if ! command -v docker &> /dev/null; then
    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    echo "💡 Tip: You can start Docker Desktop by running: open -a Docker"
    exit 1
fi

# Start the services
echo "📦 Starting services..."
docker compose up --build -d

# Wait for containers to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if research-deck container is running
if docker compose ps | grep -q "research-deck.*Up"; then
    echo ""
    echo "✅ Setup complete!"
    echo "🌐 Open your browser and go to: http://localhost:8501"
    echo ""
    echo "📝 Features available:"
    echo "  • 🤖 OpenAI GPT support (requires API key)"
    echo "  • 📄 Basic text extraction (no API required)"
    echo "  • 📊 PowerPoint export"
    echo "  • 💾 Database storage (optional)"
    echo ""
    echo "💡 For AI summaries, set OPENAI_API_KEY in your environment"
    echo "To stop the application, run: ./stop.sh"
else
    echo "❌ Failed to start application. Please check Docker logs:"
    echo "   docker compose logs research-deck"
fi 