@echo off
echo 🚀 Starting AI Research Deck...
echo This will start the application with Streamlit.
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    echo 💡 Tip: Start Docker Desktop from your Applications folder or system tray
    echo 💡 Wait for Docker Desktop to fully load before running this script again
    pause
    exit /b 1
)

REM Start the services
echo 📦 Starting services...
docker compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo ✅ Setup complete!
echo 🌐 Open your browser and go to: http://localhost:8501
echo.
echo 📝 Features available:
echo   • 🤖 OpenAI GPT support (requires API key)
echo   • 📄 Basic text extraction (no API required)
echo   • 📊 PowerPoint export
echo   • 💾 Database storage (optional)
echo.
echo 💡 For AI summaries, set OPENAI_API_KEY in your environment
echo To stop the application, run: stop.bat
pause 