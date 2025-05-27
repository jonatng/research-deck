@echo off
echo 🚀 Starting AI Research Deck...
echo This will take a few minutes on first run to download the AI model.
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
docker compose up -d

REM Wait for ollama to be ready
echo ⏳ Waiting for AI model to be ready...
timeout /t 10 /nobreak >nul

REM Download the model if it doesn't exist
echo 🤖 Setting up AI model (this may take a few minutes on first run)...
docker compose exec ollama ollama pull llama2

echo.
echo ✅ Setup complete!
echo 🌐 Open your browser and go to: http://localhost:7860
echo.
echo To stop the application, run: stop.bat
pause 