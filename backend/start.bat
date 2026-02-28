@echo off
echo Setting up Manny Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Checking for .env file...
if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo Please edit .env file with your database URL and AI API endpoint
    pause
)

echo Starting Manny Backend Server...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python main.py
