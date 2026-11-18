@echo off
title SIH26034 - Legal Metrology AI Inspection Platform
color 0B

echo ===============================================================================
echo      DEPARTMENT OF CONSUMER AFFAIRS - LEGAL METROLOGY DIVISION (GOI)
echo      AI-Powered Legal Metrology Compliance & Inspection Platform (SIH26034)
echo ===============================================================================
echo.

cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH! Please install Python 3.10+
    pause
    exit /b 1
)

:: Check Node
node --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH! Please install Node.js 18+
    pause
    exit /b 1
)

echo [1/3] Setting up Python Environment and paths...
set PYTHONPATH=%cd%\backend

echo [2/3] Starting FastAPI Backend on port 8000...
start "SIH26034 - Backend API (Port 8000)" cmd /k "cd /d "%~dp0backend" && set PYTHONPATH=%~dp0backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [3/3] Starting Next.js Frontend on port 3000...
start "SIH26034 - Frontend UI (Port 3000)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ===============================================================================
echo  Platform is starting!
echo  Frontend UI:           http://localhost:3000
echo  Officer Login:         http://localhost:3000/login
echo  Inspection Dashboard:  http://localhost:3000/dashboard
echo  FastAPI Swagger Docs:  http://localhost:8000/docs
echo  Backend Health Check:  http://localhost:8000/api/health
echo ===============================================================================
echo.
echo Waiting 4 seconds before launching browser...
timeout /t 4 /nobreak >nul
start http://localhost:3000
echo Application launched. Keep this window or minimize it.
pause
