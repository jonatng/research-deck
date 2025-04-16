#!/bin/bash

echo "Launching secure Cloudflare tunnel for Ollama..."
cloudflared tunnel --url http://localhost:11434