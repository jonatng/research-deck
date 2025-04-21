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

🧠 AI Researcher: Website Summarizer & PowerPoint Generator
A Streamlit-based app that summarizes articles from URLs using either a local transformer model or the Hugging Face API, then exports the results into a PowerPoint presentation. Summaries are also saved to Supabase.

🚀 Features
📰 Summarize multiple URLs at once

🤖 Choose between:

Local model (facebook/bart-large-cnn)

Hugging Face API

📊 Export summaries to PowerPoint (new or append to existing)

☁️ Save summaries to Supabase

🐳 Fully containerized via Docker

🧱 Tech Stack
Python (Streamlit, Transformers, Requests, python-pptx)

Supabase (PostgreSQL storage)

Docker & Docker Compose

📦 Setup
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/yourusername/research-deck.git
cd research-deck
2. Configure environment
Create a .env file in the root directory:

env
Copy
Edit
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
HUGGINGFACE_TOKEN=your_huggingface_api_key
ENV=local
🔐 Never commit your .env file!

3. Install dependencies (local dev)
bash
Copy
Edit
pip install -r requirements.txt
4. Run the app locally
bash
Copy
Edit
streamlit run app.py
🐳 Docker Setup
1. Build and run with Docker Compose
bash
Copy
Edit
docker-compose up --build
2. Access the app
Visit: http://localhost:8501

🛠 Kubernetes Deployment
Optional for production

Prereqs
Supabase URL/key and Hugging Face token stored in Kubernetes ConfigMap and Secret

Deploy
bash
Copy
Edit
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml  # Optional: Autoscaling
📂 File Structure
bash
Copy
Edit
.
├── app.py                 # Streamlit app
├── db.py                 # Supabase DB logic
├── extractor.py          # Web article scraper
├── ppt_handler.py        # PowerPoint creation
├── summarize.py          # Summarization logic
├── config.py             # .env validation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── k8s/                  # (Optional) Kubernetes YAMLs
✅ Todo / Improvements
 Add title + date extraction from URL

 UI enhancements (loading states, URL validation)

 SQLite fallback if Supabase is down

 Allow markdown or PDF exports

📘 License
MIT License.
Built with 💡 and ☕ by @jonatngu