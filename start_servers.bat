@echo off
echo Starting Scholarship Portal with Email Verification...

echo.
echo Starting Django Backend Server...
cd /d "d:\ScholarshipPortal\scholarship-backend"
start "Django Backend" cmd /k "python manage.py runserver 8000"

echo.
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting Next.js Frontend Server...
cd /d "d:\ScholarshipPortal\scholarship-portal"
start "Next.js Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
