@echo off
echo ========================================
echo    Активация виртуального окружения
echo ========================================
echo.

cd backend
echo Активирую виртуальное окружение...
call venv\Scripts\activate.bat

echo.
echo ✅ Виртуальное окружение активировано!
echo.
echo Доступные команды:
echo   python -m uvicorn main:app --reload --port 8000  - запуск бэкенда
echo   python test_backend.py                          - тестирование API
echo   pip install <package>                           - установка пакетов
echo   pip list                                        - список установленных пакетов
echo.
echo Для деактивации введите: deactivate
echo.
cmd /k
