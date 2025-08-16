@echo off
echo ========================================
echo    Day Tracker Project - Запуск с venv
echo ========================================
echo.

echo [1/4] Проверка виртуального окружения...
cd backend
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Виртуальное окружение не найдено
    echo Создаю виртуальное окружение...
    python -m venv venv
    echo ✅ Виртуальное окружение создано
)

echo.
echo [2/4] Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo [3/4] Проверка зависимостей...
python -c "import fastapi, uvicorn, sqlalchemy, pandas, sklearn" 2>nul
if errorlevel 1 (
    echo ❌ Не все зависимости установлены
    echo Устанавливаю зависимости...
    pip install -r requirements.txt
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости установлены
)

echo.
echo [4/4] Запуск бэкенда (порт 8000)...
start "Backend Server (venv)" cmd /k "cd /d %CD% && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --port 8000"

echo.
echo [5/5] Запуск фронтенда (порт 3000)...
cd ..\frontend
start "Frontend Server" cmd /k "cd /d %CD% && npm run dev"

echo.
echo ========================================
echo    Проект запущен с виртуальным окружением!
echo ========================================
echo.
echo 🌐 Фронтенд: http://localhost:3000
echo 🔧 Бэкенд API: http://localhost:8000
echo 📚 Документация API: http://localhost:8000/docs
echo.
echo 💡 Для ручной отладки используйте:
echo    activate_venv.bat - активация venv
echo    activate_venv.ps1  - активация venv (PowerShell)
echo.
echo Нажмите любую клавишу для выхода...
pause > nul
