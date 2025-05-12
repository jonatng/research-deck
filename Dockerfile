# Use official Playwright image with Python 3.11 and browsers pre-installed
FROM mcr.microsoft.com/playwright/python:v1.52.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]