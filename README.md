---
title: Research Deck
emoji: 🦀
colorFrom: gray
colorTo: red
sdk: streamlit
sdk_version: 1.44.1
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 🧠 AI Researcher

Summarize articles from any franchise-related website and export the insights directly into PowerPoint presentations. Perfect for consultants, analysts, and researchers.

---

## 🚀 Features

- 🔗 Input article URLs
- 📄 Extract content using `trafilatura`
- 🤖 Summarize using local LLM (via Ollama & Cloudflare Tunnel)
- 📊 Export summaries to PowerPoint slides
- ☁️ Store all results in Supabase for tracking and analytics

---

## 💻 Running Locally

This Hugging Face Space hosts only the **Streamlit frontend**.
To run your own summarization model securely and locally:

### 1. Clone the Repo

```bash
git clone https://huggingface.co/spaces/your-username/franchise-consultant-ai
cd franchise-consultant-ai

## 🐳 Docker Deployment

1. Copy `.env.example` to `.env` and update with your credentials:

   ```bash
   cp .env.example .env

