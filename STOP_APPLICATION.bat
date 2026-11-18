@echo off
title Stop SIH26034 Platform
echo Stopping Legal Metrology Backend and Frontend processes...
taskkill /F /IM uvicorn.exe >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq SIH26034*" >nul 2>&1
echo Done. Services stopped.
timeout /t 2 >nul
