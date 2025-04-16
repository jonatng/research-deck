#!/bin/bash

echo "🔧 Setting up your local summarization environment..."

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl https://ollama.com/install.sh | sh
else
    echo "✅ Ollama already installed"
fi

# Pull desired model (you can change this)
MODEL_NAME="mistral"
ollama pull $MODEL_NAME

# Install Cloudflare tunnel (assumes cloudflared is in PATH)
if ! command -v cloudflared &> /dev/null; then
    echo "Installing Cloudflare tunnel..."
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
fi

echo "✅ Setup complete!"
echo "Next, run: ./cloudflare_tunnel.sh"
