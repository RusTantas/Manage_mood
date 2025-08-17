import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import secrets

class UserManager:
    """Менеджер пользователей с индивидуальными CSV таблицами"""
    
    def __init__(self, users_file: str = "users.json", data_dir: str = "user_data"):
        self.users_file = users_file
        self.data_dir = data_dir
        self.users = self._load_users()
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Создает папку для данных пользователей если её нет"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Создана папка: {self.data_dir}")
    
    def _load_users(self) -> Dict:
        """Загружает список пользователей из JSON файла"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки пользователей: {e}")
                return {}
        return {}
    
    def _save_users(self):
        """Сохраняет список пользователей в JSON файл"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения пользователей: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Хеширует пароль"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_user_id(self) -> str:
        """Генерирует уникальный ID пользователя"""
        return secrets.token_hex(8)
    
    def register_user(self, username: str, password: str, email: str = "") -> Dict:
        """Регистрирует нового пользователя"""
        
        # Проверяем, что пользователь не существует
        if username in self.users:
            return {"success": False, "message": "Пользователь уже существует"}
        
        # Создаем нового пользователя
        user_id = self._generate_user_id()
        hashed_password = self._hash_password(password)
        
        user_data = {
            "user_id": user_id,
            "username": username,
            "password_hash": hashed_password,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "data_file": f"{user_id}_data.csv"
        }
        
        # Добавляем пользователя
        self.users[username] = user_data
        self._save_users()
        
        # Создаем пустую таблицу данных для пользователя
        self._create_user_data_table(user_id)
        
        return {
            "success": True, 
            "message": "Пользователь успешно зарегистрирован",
            "user_id": user_id
        }
    
    def _create_user_data_table(self, user_id: str):
        """Создает пустую таблицу данных для пользователя"""
        filename = os.path.join(self.data_dir, f"{user_id}_data.csv")
        
        # Загружаем конфигурацию полей
        fields_config = self._load_fields_config()
        columns = ['date'] + [field['name'] for field in fields_config['fields']]
        
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        print(f"Создана таблица данных: {filename}")
    
    def _load_fields_config(self) -> Dict:
        """Загружает конфигурацию полей"""
        fields_config_file = "fields_config.json"
        if os.path.exists(fields_config_file):
            try:
                with open(fields_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации полей: {e}")
        
        # Возвращаем стандартные поля если файл не найден
        return {
            "fields": [
                {"name": "kol_sna"},
                {"name": "kolichestvo_sna_0"},
                {"name": "nalichee_zarydki"},
                {"name": "zavrrak_koloriy"},
                {"name": "obed_koloriy"},
                {"name": "chteniy"},
                {"name": "sostavlenye_rasporydka"},
                {"name": "ocenka_dny"}
            ]
        }
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """Аутентифицирует пользователя"""
        
        if username not in self.users:
            return {"success": False, "message": "Пользователь не найден"}
        
        user = self.users[username]
        hashed_password = self._hash_password(password)
        
        if user["password_hash"] != hashed_password:
            return {"success": False, "message": "Неверный пароль"}
        
        # Обновляем время последнего входа
        user["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        return {
            "success": True,
            "message": "Успешная аутентификация",
            "user_id": user["user_id"],
            "username": username
        }
    
    def get_user_data(self, username: str) -> Optional[pd.DataFrame]:
        """Получает данные пользователя"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        filename = os.path.join(self.data_dir, user["data_file"])
        
        if os.path.exists(filename):
            return pd.read_csv(filename)
        else:
            # Создаем таблицу если её нет
            self._create_user_data_table(user["user_id"])
            return pd.DataFrame()
    
    def save_user_data(self, username: str, data: pd.DataFrame) -> bool:
        """Сохраняет данные пользователя"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        filename = os.path.join(self.data_dir, user["data_file"])
        
        try:
            data.to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
            return False
    
    def add_user_record(self, username: str, record: Dict) -> bool:
        """Добавляет новую запись пользователю"""
        if username not in self.users:
            return False
        
        # Получаем текущие данные
        df = self.get_user_data(username)
        if df is None:
            df = pd.DataFrame()
        
        # Добавляем дату если её нет
        if 'date' not in record:
            record['date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Добавляем новую запись
        new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        
        # Сохраняем
        return self.save_user_data(username, new_df)
    
    def get_user_stats(self, username: str) -> Dict:
        """Получает статистику пользователя"""
        df = self.get_user_data(username)
        if df is None or df.empty:
            return {"message": "Нет данных"}
        
        stats = {
            "total_records": len(df),
            "average_sleep": df['kol_sna'].mean() if 'kol_sna' in df.columns else 0,
            "average_rating": df['ocenka_dny'].mean() if 'ocenka_dny' in df.columns else 0,
            "last_record": df['date'].iloc[-1] if 'date' in df.columns else None,
            "columns": list(df.columns)
        }
        
        return stats
    
    def list_users(self) -> List[Dict]:
        """Возвращает список всех пользователей (без паролей)"""
        user_list = []
        for username, user_data in self.users.items():
            user_list.append({
                "username": username,
                "user_id": user_data["user_id"],
                "email": user_data["email"],
                "created_at": user_data["created_at"],
                "last_login": user_data["last_login"]
            })
        return user_list
    
    def delete_user(self, username: str) -> bool:
        """Удаляет пользователя и его данные"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        
        # Удаляем файл данных
        filename = os.path.join(self.data_dir, user["data_file"])
        if os.path.exists(filename):
            os.remove(filename)
        
        # Удаляем из списка пользователей
        del self.users[username]
        self._save_users()
        
        return True

# Пример использования
if __name__ == "__main__":
    # Создаем менеджер пользователей
    user_manager = UserManager()
    
    # Регистрируем пользователя
    result = user_manager.register_user("test_user", "password123", "test@example.com")
    print("Регистрация:", result)
    
    # Аутентифицируем пользователя
    auth_result = user_manager.authenticate_user("test_user", "password123")
    print("Аутентификация:", auth_result)
    
    # Добавляем запись
    record = {
        'kol_sna': 8.0,
        'kolichestvo_sna_0': 7,
        'nalichee_zarydki': 1,
        'zavrrak_koloriy': 1,
        'obed_koloriy': 1,
        'chteniy': 0,
        'sostavlenye_rasporydka': 1,
        'ocenka_dny': 8
    }
    
    success = user_manager.add_user_record("test_user", record)
    print("Добавление записи:", success)
    
    # Получаем статистику
    stats = user_manager.get_user_stats("test_user")
    print("Статистика:", stats)
