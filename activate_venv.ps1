# Активация виртуального окружения для Day Tracker
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Активация виртуального окружения" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Переходим в папку backend
Set-Location backend

# Активируем виртуальное окружение
Write-Host "Активирую виртуальное окружение..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "✅ Виртуальное окружение активировано!" -ForegroundColor Green
Write-Host ""
Write-Host "Доступные команды:" -ForegroundColor White
Write-Host "  python -m uvicorn main:app --reload --port 8000  - запуск бэкенда" -ForegroundColor Gray
Write-Host "  python test_backend.py                          - тестирование API" -ForegroundColor Gray
Write-Host "  pip install <package>                           - установка пакетов" -ForegroundColor Gray
Write-Host "  pip list                                        - список установленных пакетов" -ForegroundColor Gray
Write-Host ""
Write-Host "Для деактивации введите: deactivate" -ForegroundColor Yellow
Write-Host ""
