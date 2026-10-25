@echo off
title Adaptive Wind Power Forecasting Launcher
color 0A

echo ===============================================================================
echo     ADAPTIVE WIND POWER FORECASTING USING CONCEPT DRIFT DETECTION
echo     Final Year Engineering Project — Panimalar Engineering College
echo ===============================================================================
echo.

set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo [1/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Wind Forecasting - Backend API" cmd /k "cd /d ""%PROJECT_DIR%"" && python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/3] Starting React Vite Frontend on http://localhost:5173 ...
start "Wind Forecasting - React UI" cmd /k "cd /d ""%PROJECT_DIR%\frontend"" && npm.cmd run dev"

echo [3/3] Waiting for servers to initialize...
timeout /t 4 /nobreak >nul

echo Opening Interactive Analytics Dashboard in default browser...
start http://localhost:5173

echo.
echo ===============================================================================
echo  Application is running!
echo    - Frontend UI : http://localhost:5173
echo    - Backend API  : http://127.0.0.1:8000
echo    - Swagger Docs : http://127.0.0.1:8000/docs
echo ===============================================================================
echo.
pause
