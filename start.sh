#!/bin/bash

echo "🚀 Starting AI Research Deck..."
echo "This will take a few minutes on first run to download the AI model."
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
sleep 15

# Check if ollama container is running
if docker compose ps | grep -q "ollama.*Up"; then
    echo "🤖 Setting up AI model (this may take a few minutes on first run)..."
    # Download the model if it doesn't exist
    docker compose exec ollama ollama pull llama2
    
    echo ""
    echo "✅ Setup complete!"
    echo "🌐 Open your browser and go to: http://localhost:7860"
    echo ""
    echo "📝 Features available:"
    echo "  • 🤖 Local Ollama AI model (free, private)"
    echo "  • 🚀 OpenAI GPT support (requires API key)"
    echo "  • 📊 PowerPoint export"
    echo "  • 💾 Database storage (optional)"
    echo ""
    echo "To stop the application, run: ./stop.sh"
else
    echo "❌ Failed to start Ollama container. Please check Docker logs:"
    echo "   docker compose logs ollama"
fi 