# Инструкции по настройке проекта Day Tracker

## 🚀 Быстрый старт

### Предварительные требования

1. **Python 3.8+**
2. **Node.js 18+**
3. **npm или yarn**

### 1. Настройка бэкенда

```bash
# Переходим в папку бэкенда
cd backend

# Создаем виртуальное окружение
python -m venv venv

# Активируем виртуальное окружение
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем сервер
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Бэкенд будет доступен по адресу: http://localhost:8000
API документация: http://localhost:8000/docs

### 2. Настройка фронтенда

```bash
# Открываем новый терминал и переходим в папку фронтенда
cd frontend

# Устанавливаем зависимости
npm install

# Запускаем приложение
npm run dev
```

Фронтенд будет доступен по адресу: http://localhost:3000

## 📁 Структура проекта

```
project/
├── backend/                 # FastAPI сервер
│   ├── main.py             # Основной файл приложения
│   ├── models.py           # Модели базы данных
│   ├── schemas.py          # Pydantic схемы
│   ├── database.py         # Конфигурация БД
│   └── requirements.txt    # Python зависимости
├── frontend/               # Next.js приложение
│   ├── app/                # App Router
│   ├── components/         # React компоненты
│   ├── package.json        # Node.js зависимости
│   └── tailwind.config.js  # Конфигурация Tailwind
├── ml/                     # ML модули
│   └── analyzer.py         # Анализ данных
└── README.md               # Документация
```

## 🔧 Конфигурация

### База данных

По умолчанию используется SQLite для разработки. База данных создается автоматически в файле `backend/day_tracker.db`.

Для продакшена рекомендуется использовать PostgreSQL:

```python
# В backend/database.py
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/daytracker"
```

### Переменные окружения

Создайте файл `.env` в папке `backend/`:

```env
DATABASE_URL=sqlite:///./day_tracker.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 📊 API Endpoints

### Основные эндпоинты:

- `GET /` - Главная страница API
- `GET /docs` - Swagger документация
- `POST /daily-records/` - Создание записи дня
- `GET /daily-records/` - Получение всех записей
- `GET /daily-records/{id}` - Получение конкретной записи
- `POST /meals/` - Создание записи о приеме пищи
- `POST /activities/` - Создание записи об активности
- `POST /mood-tracking/` - Создание записи настроения
- `GET /analytics/daily/{date}` - Аналитика за день
- `GET /analytics/weekly/{start_date}` - Аналитика за неделю

## 🎯 Функциональность

### Текущая реализация:

✅ **Базовый функционал:**
- Создание записей о дне
- Отслеживание сна, настроения, самочувствия
- История записей
- Базовая аналитика с графиками

✅ **UI/UX:**
- Современный дизайн с Tailwind CSS
- Адаптивная верстка
- Интуитивные формы ввода
- Визуализация данных

✅ **Backend:**
- RESTful API на FastAPI
- Валидация данных с Pydantic
- SQLAlchemy ORM
- Автоматическая документация

### Планируемые улучшения:

🔄 **В разработке:**
- Система аутентификации
- Расширенная аналитика
- ML рекомендации
- Экспорт данных

🔄 **Будущие версии:**
- Мобильное приложение
- Уведомления
- Социальные функции
- Интеграция с фитнес-трекерами

## 🐛 Устранение неполадок

### Частые проблемы:

1. **Ошибка подключения к базе данных:**
   ```bash
   # Удалите файл базы данных и перезапустите сервер
   rm backend/day_tracker.db
   uvicorn main:app --reload
   ```

2. **Ошибки CORS:**
   - Убедитесь, что фронтенд запущен на порту 3000
   - Проверьте настройки CORS в `backend/main.py`

3. **Проблемы с зависимостями:**
   ```bash
   # Переустановите зависимости
   pip install -r requirements.txt --force-reinstall
   npm install --force
   ```

## 📈 Разработка

### Добавление новых функций:

1. **Новый эндпоинт:**
   - Добавьте в `backend/main.py`
   - Создайте схему в `backend/schemas.py`
   - Обновите модель в `backend/models.py`

2. **Новый компонент:**
   - Создайте в `frontend/components/`
   - Добавьте в нужную страницу
   - Обновите типы TypeScript

3. **Новая аналитика:**
   - Добавьте в `ml/analyzer.py`
   - Создайте эндпоинт в API
   - Добавьте визуализацию на фронтенде

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте документацию API: http://localhost:8000/docs
2. Посмотрите логи сервера
3. Создайте Issue в репозитории

---

**Удачной разработки! 🚀**
