# SIH26034 - Legal Metrology AI Inspection Platform
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "     DEPARTMENT OF CONSUMER AFFAIRS - LEGAL METROLOGY DIVISION (GOI)" -ForegroundColor White
Write-Host "     AI-Powered Legal Metrology Compliance & Inspection Platform (SIH26034)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Backend
Write-Host "`n[1/3] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
$backendProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='$scriptDir\backend'; cd '$scriptDir\backend'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -PassThru

# 2. Start Frontend
Write-Host "[2/3] Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Green
$frontendProc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir\frontend'; npm run dev" -PassThru

Write-Host "`n[3/3] Opening browser at http://localhost:3000..." -ForegroundColor Yellow
Start-Sleep -Seconds 4
Start-Process "http://localhost:3000"

Write-Host "`nPlatform running successfully!" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "Frontend UI:  http://localhost:3000" -ForegroundColor Gray
