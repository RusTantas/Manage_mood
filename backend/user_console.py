#!/usr/bin/env python3
"""
Консольное приложение для управления пользователями
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_manager import UserManager
import pandas as pd
from datetime import datetime

class UserConsole:
    """Консольное приложение для управления пользователями"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
    
    def main_menu(self):
        """Главное меню"""
        while True:
            print("\n" + "="*50)
            print("🏠 СИСТЕМА УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ")
            print("="*50)
            
            if self.current_user:
                print(f"👤 Текущий пользователь: {self.current_user}")
                print("1. 📊 Мои данные")
                print("2. ➕ Добавить запись")
                print("3. 📈 Статистика")
                print("4. 🔄 Создать тестовые данные")
                print("5. 🚪 Выйти из аккаунта")
                print("0. ❌ Выход")
            else:
                print("1. 📝 Регистрация")
                print("2. 🔐 Вход")
                print("3. 👥 Список пользователей")
                print("4. 🗑️ Удалить пользователя")
                print("0. ❌ Выход")
            
            choice = input("\nВыберите действие: ")
            
            if self.current_user:
                if choice == "1":
                    self.show_user_data()
                elif choice == "2":
                    self.add_record()
                elif choice == "3":
                    self.show_user_stats()
                elif choice == "4":
                    self.create_test_data()
                elif choice == "5":
                    self.logout()
                elif choice == "0":
                    print("👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор!")
            else:
                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    self.list_users()
                elif choice == "4":
                    self.delete_user()
                elif choice == "0":
                    print("👋 До свидания!")
                    break
                else:
                    print("❌ Неверный выбор!")
    
    def register_user(self):
        """Регистрация пользователя"""
        print("\n" + "="*30)
        print("📝 РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ")
        print("="*30)
        
        username = input("Введите имя пользователя: ").strip()
        if not username:
            print("❌ Имя пользователя не может быть пустым!")
            return
        
        password = input("Введите пароль: ").strip()
        if not password:
            print("❌ Пароль не может быть пустым!")
            return
        
        email = input("Введите email (необязательно): ").strip()
        
        result = self.user_manager.register_user(username, password, email)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"🆔 ID пользователя: {result['user_id']}")
        else:
            print(f"❌ {result['message']}")
    
    def login_user(self):
        """Вход пользователя"""
        print("\n" + "="*30)
        print("🔐 ВХОД В СИСТЕМУ")
        print("="*30)
        
        username = input("Введите имя пользователя: ").strip()
        password = input("Введите пароль: ").strip()
        
        result = self.user_manager.authenticate_user(username, password)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            self.current_user = username
        else:
            print(f"❌ {result['message']}")
    
    def logout(self):
        """Выход из аккаунта"""
        print(f"👋 До свидания, {self.current_user}!")
        self.current_user = None
    
    def show_user_data(self):
        """Показать данные пользователя"""
        print("\n" + "="*30)
        print("📊 МОИ ДАННЫЕ")
        print("="*30)
        
        df = self.user_manager.get_user_data(self.current_user)
        
        if df is None or df.empty:
            print("📭 У вас пока нет записей")
            return
        
        print(f"📋 Всего записей: {len(df)}")
        print("\nПоследние 5 записей:")
        print(df.tail().to_string(index=False))
    
    def add_record(self):
        """Добавить новую запись"""
        print("\n" + "="*30)
        print("➕ ДОБАВЛЕНИЕ ЗАПИСИ")
        print("="*30)
        
        record = {}
        
        # Количество сна
        while True:
            try:
                kol_sna = float(input("Введите количество сна (часы, 4-12): "))
                if 4 <= kol_sna <= 12:
                    record['kol_sna'] = kol_sna
                    break
                else:
                    print("❌ Количество сна должно быть от 4 до 12 часов!")
            except ValueError:
                print("❌ Введите число!")
        
        # Качество сна после 00:00
        while True:
            try:
                kolichestvo_sna_0 = int(input("Введите качество сна после 00:00 (0-10): "))
                if 0 <= kolichestvo_sna_0 <= 10:
                    record['kolichestvo_sna_0'] = kolichestvo_sna_0
                    break
                else:
                    print("❌ Качество сна должно быть от 0 до 10!")
            except ValueError:
                print("❌ Введите целое число!")
        
        # Наличие зарядки
        while True:
            zarydka = input("Делали ли зарядку? (да/нет): ").lower()
            if zarydka in ['да', 'д', 'yes', 'y', '1']:
                record['nalichee_zarydki'] = 1
                break
            elif zarydka in ['нет', 'н', 'no', 'n', '0']:
                record['nalichee_zarydki'] = 0
                break
            else:
                print("❌ Введите 'да' или 'нет'!")
        
        # Завтрак калорийный
        while True:
            zavtrak = input("Был ли калорийный завтрак? (да/нет): ").lower()
            if zavtrak in ['да', 'д', 'yes', 'y', '1']:
                record['zavrrak_koloriy'] = 1
                break
            elif zavtrak in ['нет', 'н', 'no', 'n', '0']:
                record['zavrrak_koloriy'] = 0
                break
            else:
                print("❌ Введите 'да' или 'нет'!")
        
        # Обед калорийный
        while True:
            obed = input("Был ли калорийный обед? (да/нет): ").lower()
            if obed in ['да', 'д', 'yes', 'y', '1']:
                record['obed_koloriy'] = 1
                break
            elif obed in ['нет', 'н', 'no', 'n', '0']:
                record['obed_koloriy'] = 0
                break
            else:
                print("❌ Введите 'да' или 'нет'!")
        
        # Чтение
        while True:
            chtenie = input("Читали ли сегодня? (да/нет): ").lower()
            if chtenie in ['да', 'д', 'yes', 'y', '1']:
                record['chteniy'] = 1
                break
            elif chtenie in ['нет', 'н', 'no', 'n', '0']:
                record['chteniy'] = 0
                break
            else:
                print("❌ Введите 'да' или 'нет'!")
        
        # Составление распорядка
        while True:
            rasporyadok = input("Составляли ли распорядок дня? (да/нет): ").lower()
            if rasporyadok in ['да', 'д', 'yes', 'y', '1']:
                record['sostavlenye_rasporydka'] = 1
                break
            elif rasporyadok in ['нет', 'н', 'no', 'n', '0']:
                record['sostavlenye_rasporydka'] = 0
                break
            else:
                print("❌ Введите 'да' или 'нет'!")
        
        # Оценка дня
        while True:
            try:
                ocenka = int(input("Введите оценку дня (1-10): "))
                if 1 <= ocenka <= 10:
                    record['ocenka_dny'] = ocenka
                    break
                else:
                    print("❌ Оценка должна быть от 1 до 10!")
            except ValueError:
                print("❌ Введите целое число!")
        
        # Добавляем дату
        record['date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Сохраняем запись
        success = self.user_manager.add_user_record(self.current_user, record)
        
        if success:
            print("✅ Запись успешно добавлена!")
        else:
            print("❌ Ошибка при добавлении записи!")
    
    def show_user_stats(self):
        """Показать статистику пользователя"""
        print("\n" + "="*30)
        print("📈 СТАТИСТИКА")
        print("="*30)
        
        stats = self.user_manager.get_user_stats(self.current_user)
        
        if "message" in stats:
            print(f"📭 {stats['message']}")
            return
        
        print(f"📊 Всего записей: {stats['total_records']}")
        print(f"😴 Средний сон: {stats['average_sleep']:.1f} часов")
        print(f"⭐ Средняя оценка дня: {stats['average_rating']:.1f}")
        print(f"📅 Последняя запись: {stats['last_record']}")
    
    def create_test_data(self):
        """Создать тестовые данные"""
        print("\n" + "="*30)
        print("🔄 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
        print("="*30)
        
        try:
            num_records = int(input("Сколько записей создать? (по умолчанию 10): ") or "10")
        except ValueError:
            num_records = 10
        
        import numpy as np
        
        # Создаем тестовые данные
        for i in range(num_records):
            record = {
                'kol_sna': np.random.normal(7.5, 1.5).clip(4, 12),
                'kolichestvo_sna_0': np.random.randint(0, 11),
                'nalichee_zarydki': np.random.choice([0, 1]),
                'zavrrak_koloriy': np.random.choice([0, 1]),
                'obed_koloriy': np.random.choice([0, 1]),
                'chteniy': np.random.choice([0, 1]),
                'sostavlenye_rasporydka': np.random.choice([0, 1]),
                'ocenka_dny': np.random.randint(1, 11),
                'date': (datetime.now() - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
            }
            
            success = self.user_manager.add_user_record(self.current_user, record)
            if success:
                print(f"✅ Запись {i+1}/{num_records} добавлена")
            else:
                print(f"❌ Ошибка при добавлении записи {i+1}")
        
        print(f"\n✅ Создано {num_records} тестовых записей!")
    
    def list_users(self):
        """Показать список пользователей"""
        print("\n" + "="*50)
        print("👥 СПИСОК ПОЛЬЗОВАТЕЛЕЙ")
        print("="*50)
        
        users = self.user_manager.list_users()
        
        if not users:
            print("📭 Пользователей пока нет")
            return
        
        for i, user in enumerate(users, 1):
            print(f"{i}. 👤 {user['username']}")
            print(f"   🆔 ID: {user['user_id']}")
            print(f"   📧 Email: {user['email']}")
            print(f"   📅 Создан: {user['created_at'][:10]}")
            if user['last_login']:
                print(f"   🔄 Последний вход: {user['last_login'][:10]}")
            print()
    
    def delete_user(self):
        """Удалить пользователя"""
        print("\n" + "="*30)
        print("🗑️ УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
        print("="*30)
        
        username = input("Введите имя пользователя для удаления: ").strip()
        
        if not username:
            print("❌ Имя пользователя не может быть пустым!")
            return
        
        confirm = input(f"⚠️ Вы уверены, что хотите удалить пользователя '{username}'? (да/нет): ").lower()
        
        if confirm in ['да', 'д', 'yes', 'y']:
            success = self.user_manager.delete_user(username)
            if success:
                print(f"✅ Пользователь '{username}' удален!")
                if self.current_user == username:
                    self.current_user = None
            else:
                print(f"❌ Пользователь '{username}' не найден!")
        else:
            print("❌ Удаление отменено")

if __name__ == "__main__":
    console = UserConsole()
    console.main_menu()
