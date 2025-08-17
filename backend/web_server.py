#!/usr/bin/env python3
"""
FastAPI веб-сервер для системы управления пользователями
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from pydantic import BaseModel

# Импортируем наш менеджер пользователей
from user_manager import UserManager

# Создаем FastAPI приложение
app = FastAPI(title="Система оценки дня", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Базовое аутентификация
security = HTTPBasic()

# Инициализируем менеджер пользователей
user_manager = UserManager()

# Модели данных
class UserRegistration(BaseModel):
    username: str
    password: str
    email: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class DataRecord(BaseModel):
    kol_sna: float
    kolichestvo_sna_0: int
    nalichee_zarydki: int
    zavrrak_koloriy: int
    obed_koloriy: int
    chteniy: int
    sostavlenye_rasporydka: int
    ocenka_dny: int
    date: Optional[str] = None

class FieldDefinition(BaseModel):
    name: str
    display_name: str
    field_type: str  # "number", "boolean", "integer"
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: str = ""

# Файл для хранения определений полей
FIELDS_CONFIG_FILE = "fields_config.json"

def load_fields_config() -> Dict:
    """Загружает конфигурацию полей"""
    if os.path.exists(FIELDS_CONFIG_FILE):
        with open(FIELDS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Стандартные поля
        default_fields = {
            "fields": [
                {
                    "name": "kol_sna",
                    "display_name": "Количество сна (часы)",
                    "field_type": "number",
                    "min_value": 4.0,
                    "max_value": 12.0,
                    "description": "Количество часов сна"
                },
                {
                    "name": "kolichestvo_sna_0",
                    "display_name": "Качество сна после 00:00",
                    "field_type": "integer",
                    "min_value": 0,
                    "max_value": 10,
                    "description": "Оценка качества сна после полуночи"
                },
                {
                    "name": "nalichee_zarydki",
                    "display_name": "Наличие зарядки",
                    "field_type": "boolean",
                    "description": "Делали ли зарядку"
                },
                {
                    "name": "zavrrak_koloriy",
                    "display_name": "Калорийный завтрак",
                    "field_type": "boolean",
                    "description": "Был ли калорийный завтрак"
                },
                {
                    "name": "obed_koloriy",
                    "display_name": "Калорийный обед",
                    "field_type": "boolean",
                    "description": "Был ли калорийный обед"
                },
                {
                    "name": "chteniy",
                    "display_name": "Чтение",
                    "field_type": "boolean",
                    "description": "Читали ли сегодня"
                },
                {
                    "name": "sostavlenye_rasporydka",
                    "display_name": "Составление распорядка",
                    "field_type": "boolean",
                    "description": "Составляли ли распорядок дня"
                },
                {
                    "name": "ocenka_dny",
                    "display_name": "Оценка дня",
                    "field_type": "integer",
                    "min_value": 1,
                    "max_value": 10,
                    "description": "Общая оценка дня"
                }
            ]
        }
        save_fields_config(default_fields)
        return default_fields

def save_fields_config(config: Dict):
    """Сохраняет конфигурацию полей"""
    with open(FIELDS_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Получает текущего пользователя"""
    result = user_manager.authenticate_user(credentials.username, credentials.password)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def calculate_correlations(df: pd.DataFrame) -> List[Dict]:
    """Вычисляет корреляции с оценкой дня"""
    if df.empty or 'ocenka_dny' not in df.columns:
        return []
    
    correlations = df.corr()['ocenka_dny'].drop('ocenka_dny').sort_values(ascending=False)
    
    top_features = []
    for feature, corr in correlations.head(3).items():
        top_features.append({
            "feature": feature,
            "correlation": round(corr, 3),
            "impact": "положительное" if corr > 0 else "отрицательное"
        })
    
    return top_features

# API endpoints

@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница с веб-интерфейсом"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Система оценки дня</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; text-align: center; }
                .api-section { margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 5px; }
                .endpoint { background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 3px; }
                .method { font-weight: bold; color: #1976d2; }
                .url { font-family: monospace; color: #333; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏠 Система оценки дня</h1>
                <p>Добро пожаловать в веб-интерфейс системы управления пользователями!</p>
                
                <div class="api-section">
                    <h2>📋 Доступные API endpoints:</h2>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <span class="url">/register</span> - Регистрация пользователя
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <span class="url">/login</span> - Вход в систему
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <span class="url">/users</span> - Список пользователей
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <span class="url">/data</span> - Получить данные пользователя
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <span class="url">/data</span> - Добавить запись
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <span class="url">/stats</span> - Статистика пользователя
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <span class="url">/fields</span> - Получить поля данных
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <span class="url">/fields</span> - Добавить новое поле
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">DELETE</span> <span class="url">/fields/{field_name}</span> - Удалить поле
                    </div>
                </div>
                
                <div class="api-section">
                    <h2>🔧 Документация API:</h2>
                    <p><a href="/docs" target="_blank">📖 Swagger UI</a> - Интерактивная документация</p>
                    <p><a href="/redoc" target="_blank">📚 ReDoc</a> - Альтернативная документация</p>
                </div>
            </div>
        </body>
        </html>
        """

@app.post("/register")
async def register_user(user_data: UserRegistration):
    """Регистрация нового пользователя"""
    result = user_manager.register_user(user_data.username, user_data.password, user_data.email)
    if result["success"]:
        return {"message": "Пользователь успешно зарегистрирован", "user_id": result["user_id"]}
    else:
        raise HTTPException(status_code=400, detail=result["message"])

@app.post("/login")
async def login_user(user_data: UserLogin):
    """Вход в систему"""
    result = user_manager.authenticate_user(user_data.username, user_data.password)
    if result["success"]:
        return {"message": "Успешная аутентификация", "user_id": result["user_id"]}
    else:
        raise HTTPException(status_code=401, detail=result["message"])

@app.get("/users")
async def list_users():
    """Список всех пользователей"""
    return {"users": user_manager.list_users()}

@app.get("/data")
async def get_user_data(username: str = Depends(get_current_user)):
    """Получить данные пользователя"""
    df = user_manager.get_user_data(username)
    if df is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {
        "username": username,
        "data": df.to_dict('records'),
        "total_records": len(df)
    }

@app.post("/data")
async def add_data_record(record: DataRecord, username: str = Depends(get_current_user)):
    """Добавить новую запись"""
    # Преобразуем в словарь
    record_dict = record.dict()
    if record_dict.get('date') is None:
        record_dict['date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Добавляем запись
    success = user_manager.add_user_record(username, record_dict)
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении записи")
    
    # Получаем обновленные данные для анализа
    df = user_manager.get_user_data(username)
    correlations = calculate_correlations(df)
    
    return {
        "message": "Запись успешно добавлена",
        "record": record_dict,
        "top_features": correlations
    }

@app.get("/stats")
async def get_user_stats(username: str = Depends(get_current_user)):
    """Получить статистику пользователя"""
    stats = user_manager.get_user_stats(username)
    if "message" in stats:
        return {"message": stats["message"]}
    
    # Добавляем анализ корреляций
    df = user_manager.get_user_data(username)
    correlations = calculate_correlations(df)
    
    return {
        **stats,
        "top_features": correlations
    }

@app.get("/fields")
async def get_fields():
    """Получить конфигурацию полей"""
    return load_fields_config()

@app.post("/fields")
async def add_field(field: FieldDefinition):
    """Добавить новое поле"""
    config = load_fields_config()
    
    # Проверяем, что поле не существует
    existing_fields = [f["name"] for f in config["fields"]]
    if field.name in existing_fields:
        raise HTTPException(status_code=400, detail="Поле уже существует")
    
    # Добавляем новое поле
    field_dict = field.dict()
    config["fields"].append(field_dict)
    save_fields_config(config)
    
    return {"message": f"Поле '{field.display_name}' успешно добавлено", "field": field_dict}

@app.delete("/fields/{field_name}")
async def delete_field(field_name: str):
    """Удалить поле"""
    config = load_fields_config()
    
    # Находим и удаляем поле
    field_to_remove = None
    for field in config["fields"]:
        if field["name"] == field_name:
            field_to_remove = field
            break
    
    if field_to_remove is None:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    
    # Проверяем, что это не обязательное поле
    required_fields = ["date", "ocenka_dny"]
    if field_name in required_fields:
        raise HTTPException(status_code=400, detail="Нельзя удалить обязательное поле")
    
    config["fields"] = [f for f in config["fields"] if f["name"] != field_name]
    save_fields_config(config)
    
    return {"message": f"Поле '{field_to_remove['display_name']}' успешно удалено"}

@app.get("/health")
async def health_check():
    """Проверка состояния сервера"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Запуск веб-сервера на http://localhost:4000")
    print("📖 Документация: http://localhost:4000/docs")
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=True)
