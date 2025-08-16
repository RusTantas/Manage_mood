import requests
import json
from datetime import datetime

# URL бэкенда
BASE_URL = "http://localhost:8000"

def test_backend():
    """Тестирование основных эндпоинтов бэкенда"""
    
    print("🧪 Тестирование Day Tracker Backend")
    print("=" * 50)
    
    # Тест 1: Проверка доступности API
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API доступен")
            print(f"   Ответ: {response.json()}")
        else:
            print(f"❌ API недоступен. Статус: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что бэкенд запущен.")
        return False
    
    # Тест 2: Создание записи дня
    print("\n📝 Тест создания записи дня...")
    daily_record = {
        "wake_up_time": datetime.now().isoformat(),
        "sleep_time": datetime.now().isoformat(),
        "sleep_quality": 8,
        "overall_mood": 7,
        "physical_wellness": 8,
        "mental_wellness": 7,
        "notes": "Тестовая запись для проверки работы API"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/daily-records/",
            json=daily_record,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Запись дня создана успешно")
            record_data = response.json()
            print(f"   ID записи: {record_data['id']}")
            return record_data['id']
        else:
            print(f"❌ Ошибка создания записи. Статус: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при создании записи: {e}")
        return None

def test_analytics():
    """Тестирование аналитики"""
    print("\n📊 Тест аналитики...")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = requests.get(f"{BASE_URL}/analytics/daily/{today}")
        if response.status_code == 200:
            print("✅ Аналитика за день получена")
            analytics = response.json()
            print(f"   Дата: {analytics['date']}")
            print(f"   Записей: {analytics['mood_entries_count']}")
        else:
            print(f"❌ Ошибка получения аналитики. Статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении аналитики: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестов Day Tracker Backend")
    print("Убедитесь, что сервер запущен на http://localhost:8000")
    print()
    
    # Запускаем тесты
    record_id = test_backend()
    if record_id:
        test_analytics()
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено")
    print("\nДля просмотра API документации откройте:")
    print("http://localhost:8000/docs")
