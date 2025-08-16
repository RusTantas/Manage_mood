# 🐍 Виртуальное окружение (venv) - Руководство

## ✅ Что такое виртуальное окружение?

Виртуальное окружение - это изолированная среда Python, которая позволяет:
- Избежать конфликтов между пакетами разных проектов
- Упростить управление зависимостями
- Обеспечить воспроизводимость окружения
- Упростить отладку и разработку

## 🚀 Быстрая активация

### Вариант 1: Автоматический запуск с venv
```bash
./start_project_with_venv.bat
```

### Вариант 2: Ручная активация

**Windows (Command Prompt):**
```bash
cd backend
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

**Или используйте готовые скрипты:**
```bash
# Command Prompt
./activate_venv.bat

# PowerShell
./activate_venv.ps1
```

## 🔧 Работа с виртуальным окружением

### Активация
После активации в командной строке появится префикс `(venv)`:
```bash
(venv) PS C:\path\to\backend>
```

### Деактивация
```bash
deactivate
```

### Проверка активного окружения
```bash
# Показать путь к Python
where python

# Показать установленные пакеты
pip list

# Показать информацию о venv
python -c "import sys; print(sys.prefix)"
```

## 📦 Управление пакетами

### Установка пакетов
```bash
# В активированном venv
pip install package_name

# Установка из requirements.txt
pip install -r requirements.txt
```

### Обновление пакетов
```bash
pip install --upgrade package_name
```

### Удаление пакетов
```bash
pip uninstall package_name
```

### Экспорт зависимостей
```bash
pip freeze > requirements.txt
```

## 🐛 Отладка в виртуальном окружении

### Запуск бэкенда для отладки
```bash
# Активируйте venv
cd backend
venv\Scripts\activate.bat

# Запустите сервер
python -m uvicorn main:app --reload --port 8000
```

### Тестирование API
```bash
# В активированном venv
python test_backend.py
```

### Интерактивная отладка
```bash
# Запуск Python в venv
python

# Импорт и тестирование модулей
>>> import main
>>> import models
>>> import schemas
```

### Отладка с VS Code
1. Откройте проект в VS Code
2. Нажмите `Ctrl+Shift+P`
3. Выберите "Python: Select Interpreter"
4. Выберите интерпретатор из `backend/venv/Scripts/python.exe`

## 🔍 Полезные команды

### Проверка зависимостей
```bash
# Проверить, что все работает
python -c "import fastapi, uvicorn, sqlalchemy, pandas, sklearn; print('✅ Все OK!')"
```

### Информация о системе
```bash
# Версия Python
python --version

# Путь к Python
which python

# Список пакетов
pip list

# Информация о venv
python -c "import sys; print(f'Python: {sys.version}'); print(f'Path: {sys.executable}')"
```

### Очистка и пересоздание
```bash
# Удалить venv (если что-то сломалось)
rmdir /s venv

# Создать заново
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 🎯 Рекомендации

### Для разработки:
1. **Всегда активируйте venv** перед работой с проектом
2. **Устанавливайте новые пакеты** только в активированном venv
3. **Обновляйте requirements.txt** при добавлении новых зависимостей
4. **Используйте `pip freeze`** для экспорта точных версий

### Для отладки:
1. **Запускайте сервер** в активированном venv
2. **Используйте интерактивный Python** для тестирования
3. **Проверяйте импорты** перед запуском
4. **Логируйте ошибки** для диагностики

## 🚨 Частые проблемы

### "Команда не найдена"
```bash
# Убедитесь, что venv активирован
# Должен быть префикс (venv)
(venv) PS C:\path\to\backend>
```

### "Модуль не найден"
```bash
# Проверьте, что пакет установлен
pip list | findstr package_name

# Переустановите пакет
pip install --force-reinstall package_name
```

### "Порт занят"
```bash
# Измените порт
python -m uvicorn main:app --reload --port 8001
```

## 📚 Дополнительные ресурсы

- [Документация venv](https://docs.python.org/3/library/venv.html)
- [Руководство по pip](https://pip.pypa.io/en/stable/)
- [FastAPI документация](https://fastapi.tiangolo.com/)

---

**💡 Совет:** Создайте алиас в PowerShell для быстрой активации:
```powershell
# Добавьте в профиль PowerShell
function activate-daytracker {
    Set-Location "C:\path\to\project\backend"
    & .\venv\Scripts\Activate.ps1
}
```
