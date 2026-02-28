@echo off
echo Starting Manny Campus Chatbot Backend...
cd /d "D:\Coding\SIH25\backend"
echo Current directory: %CD%
D:/Coding/SIH25/.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
