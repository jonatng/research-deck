#!/bin/bash

# Add Docker to PATH if it's not already available
if ! command -v docker &> /dev/null; then
    export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
fi

echo "🛑 Stopping AI Research Deck..."
docker compose down

echo "✅ Application stopped successfully!"
echo "💾 Your data and models are preserved for next time." 