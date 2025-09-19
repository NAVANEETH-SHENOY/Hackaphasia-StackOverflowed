@echo off
echo Starting AgriTech Services...
echo.

echo Starting Backend API...
start "AgriTech Backend" cmd /k "cd /d D:\kuch bhi two\final\backend && pip install -r requirements.txt && python app.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend...
start "AgriTech Frontend" cmd /k "cd /d D:\kuch bhi two\final\frontend && npm install && npm run dev"

echo.
echo ✅ Both services are starting!
echo.
echo Backend API: http://localhost:5000
echo Frontend App: http://localhost:5173
echo.
echo Press any key to exit...
pause > nul
