@echo off
echo ========================================
echo    Day Tracker Project - Запуск
echo ========================================
echo.

echo [1/3] Проверка зависимостей...
cd backend
python -c "import fastapi, uvicorn, sqlalchemy, pandas, sklearn" 2>nul
if errorlevel 1 (
    echo ❌ Ошибка: Не все зависимости установлены
    echo Установите зависимости: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Зависимости установлены

echo.
echo [2/3] Запуск бэкенда (порт 8000)...
start "Backend Server" cmd /k "cd /d %CD% && python -m uvicorn main:app --reload --port 8000"

echo.
echo [3/3] Запуск фронтенда (порт 3000)...
cd ..\frontend
start "Frontend Server" cmd /k "cd /d %CD% && npm run dev"

echo.
echo ========================================
echo    Проект запущен!
echo ========================================
echo.
echo 🌐 Фронтенд: http://localhost:3000
echo 🔧 Бэкенд API: http://localhost:8000
echo 📚 Документация API: http://localhost:8000/docs
echo.
echo Нажмите любую клавишу для выхода...
pause > nul
