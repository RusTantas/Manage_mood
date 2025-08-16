# 🚀 Быстрый запуск Day Tracker

## Шаг 1: Запуск бэкенда

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic requests
python -m uvicorn main:app --reload --port 8000
```

✅ Бэкенд запущен: http://localhost:8000
📚 API документация: http://localhost:8000/docs

## Шаг 2: Запуск фронтенда

```bash
cd frontend
npm install
npm run dev
```

✅ Фронтенд запущен: http://localhost:3000

## Шаг 3: Тестирование

```bash
python test_backend.py
```

## 🎯 Что дальше?

1. Откройте http://localhost:3000
2. Создайте первую запись дня
3. Посмотрите аналитику
4. Изучите API документацию

## 🆘 Если что-то не работает

- Проверьте, что порты 8000 и 3000 свободны
- Убедитесь, что Python 3.8+ и Node.js 18+ установлены
- Перезапустите серверы при необходимости

---

**Удачного использования! 🌟**
