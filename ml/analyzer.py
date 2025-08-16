import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

class DayAnalyzer:
    def __init__(self):
        self.mood_model = None
        self.correlation_matrix = None
        self.feature_importance = None
        
    def prepare_data(self, daily_records: List[Dict], meals: List[Dict], 
                    activities: List[Dict], mood_trackings: List[Dict]) -> pd.DataFrame:
        """Подготовка данных для анализа"""
        
        # Создаем DataFrame из записей дня
        df_records = pd.DataFrame(daily_records)
        df_meals = pd.DataFrame(meals)
        df_activities = pd.DataFrame(activities)
        df_moods = pd.DataFrame(mood_trackings)
        
        # Обработка записей дня
        if not df_records.empty:
            df_records['date'] = pd.to_datetime(df_records['date'])
            df_records['wake_up_time'] = pd.to_datetime(df_records['wake_up_time'])
            df_records['sleep_time'] = pd.to_datetime(df_records['sleep_time'])
            
            # Вычисляем продолжительность сна
            df_records['sleep_duration_hours'] = (
                df_records['sleep_time'] - df_records['wake_up_time']
            ).dt.total_seconds() / 3600
            
            # Время пробуждения (час)
            df_records['wake_up_hour'] = df_records['wake_up_time'].dt.hour
            
        # Обработка приемов пищи
        if not df_meals.empty:
            df_meals['meal_time'] = pd.to_datetime(df_meals['meal_time'])
            df_meals['meal_hour'] = df_meals['meal_time'].dt.hour
            
            # Группируем по дням
            daily_meals = df_meals.groupby('daily_record_id').agg({
                'taste_rating': 'mean',
                'health_rating': 'mean',
                'meal_hour': ['count', 'mean'],
                'portion_size': lambda x: x.value_counts().index[0] if len(x) > 0 else 'medium'
            }).reset_index()
            
            daily_meals.columns = [
                'daily_record_id', 'avg_taste_rating', 'avg_health_rating',
                'meals_count', 'avg_meal_hour', 'most_common_portion'
            ]
        
        # Обработка активностей
        if not df_activities.empty:
            df_activities['start_time'] = pd.to_datetime(df_activities['start_time'])
            df_activities['end_time'] = pd.to_datetime(df_activities['end_time'])
            
            # Вычисляем продолжительность активности
            df_activities['activity_duration_hours'] = (
                df_activities['end_time'] - df_activities['start_time']
            ).dt.total_seconds() / 3600
            
            # Группируем по дням
            daily_activities = df_activities.groupby('daily_record_id').agg({
                'activity_type': 'count',
                'intensity': 'mean',
                'enjoyment_rating': 'mean',
                'activity_duration_hours': 'sum'
            }).reset_index()
            
            daily_activities.columns = [
                'daily_record_id', 'activities_count', 'avg_intensity',
                'avg_enjoyment', 'total_activity_hours'
            ]
        
        # Обработка настроения
        if not df_moods.empty:
            df_moods['timestamp'] = pd.to_datetime(df_moods['timestamp'])
            
            # Группируем по дням
            daily_moods = df_moods.groupby('daily_record_id').agg({
                'emotion': lambda x: x.value_counts().index[0] if len(x) > 0 else 'neutral',
                'intensity': 'mean',
                'timestamp': 'count'
            }).reset_index()
            
            daily_moods.columns = [
                'daily_record_id', 'dominant_emotion', 'avg_mood_intensity', 'mood_entries_count'
            ]
        
        # Объединяем все данные
        df_combined = df_records.copy()
        
        if not df_meals.empty:
            df_combined = df_combined.merge(daily_meals, on='daily_record_id', how='left')
        
        if not df_activities.empty:
            df_combined = df_combined.merge(daily_activities, on='daily_record_id', how='left')
        
        if not df_moods.empty:
            df_combined = df_combined.merge(daily_moods, on='daily_record_id', how='left')
        
        # Заполняем пропущенные значения
        df_combined = df_combined.fillna({
            'sleep_duration_hours': 8.0,
            'avg_taste_rating': 5.0,
            'avg_health_rating': 5.0,
            'meals_count': 3,
            'avg_meal_hour': 12,
            'activities_count': 0,
            'avg_intensity': 5.0,
            'avg_enjoyment': 5.0,
            'total_activity_hours': 0,
            'avg_mood_intensity': 5.0,
            'mood_entries_count': 0
        })
        
        return df_combined
    
    def analyze_correlations(self, df: pd.DataFrame) -> Dict:
        """Анализ корреляций между факторами и настроением"""
        
        # Выбираем числовые колонки для корреляционного анализа
        numeric_columns = [
            'sleep_quality', 'sleep_duration_hours', 'wake_up_hour',
            'overall_mood', 'physical_wellness', 'mental_wellness',
            'avg_taste_rating', 'avg_health_rating', 'meals_count',
            'avg_meal_hour', 'activities_count', 'avg_intensity',
            'avg_enjoyment', 'total_activity_hours', 'avg_mood_intensity'
        ]
        
        # Фильтруем только существующие колонки
        available_columns = [col for col in numeric_columns if col in df.columns]
        
        if len(available_columns) < 2:
            return {"error": "Недостаточно данных для анализа корреляций"}
        
        correlation_matrix = df[available_columns].corr()
        
        # Находим корреляции с настроением
        mood_correlations = {}
        if 'overall_mood' in correlation_matrix.columns:
            mood_corr = correlation_matrix['overall_mood'].abs().sort_values(ascending=False)
            mood_correlations = {
                factor: {
                    'correlation': float(corr),
                    'strength': self._get_correlation_strength(corr)
                }
                for factor, corr in mood_corr.items()
                if factor != 'overall_mood' and not pd.isna(corr)
            }
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'mood_correlations': mood_correlations
        }
    
    def _get_correlation_strength(self, correlation: float) -> str:
        """Определение силы корреляции"""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return "сильная"
        elif abs_corr >= 0.5:
            return "средняя"
        elif abs_corr >= 0.3:
            return "слабая"
        else:
            return "очень слабая"
    
    def train_mood_prediction_model(self, df: pd.DataFrame) -> Dict:
        """Обучение модели для предсказания настроения"""
        
        # Подготавливаем признаки
        feature_columns = [
            'sleep_quality', 'sleep_duration_hours', 'wake_up_hour',
            'avg_taste_rating', 'avg_health_rating', 'meals_count',
            'activities_count', 'avg_intensity', 'avg_enjoyment',
            'total_activity_hours'
        ]
        
        # Фильтруем только существующие колонки
        available_features = [col for col in feature_columns if col in df.columns]
        
        if 'overall_mood' not in df.columns or len(available_features) < 3:
            return {"error": "Недостаточно данных для обучения модели"}
        
        # Удаляем строки с пропущенными значениями
        df_clean = df[available_features + ['overall_mood']].dropna()
        
        if len(df_clean) < 10:
            return {"error": "Недостаточно данных для обучения модели"}
        
        X = df_clean[available_features]
        y = df_clean['overall_mood']
        
        # Разделяем данные
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Обучаем модель
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Оцениваем модель
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Важность признаков
        feature_importance = dict(zip(available_features, model.feature_importances_))
        
        self.mood_model = model
        self.feature_importance = feature_importance
        
        return {
            'model_performance': {
                'mse': float(mse),
                'r2_score': float(r2),
                'rmse': float(np.sqrt(mse))
            },
            'feature_importance': feature_importance
        }
    
    def generate_recommendations(self, df: pd.DataFrame, user_id: int = 1) -> List[Dict]:
        """Генерация персонализированных рекомендаций"""
        
        recommendations = []
        
        if df.empty:
            return [{
                'type': 'general',
                'title': 'Начните отслеживать данные',
                'description': 'Для получения персонализированных рекомендаций начните записывать данные о своем дне.',
                'confidence': 0.8,
                'priority': 5
            }]
        
        # Анализ сна
        if 'sleep_quality' in df.columns and 'sleep_duration_hours' in df.columns:
            avg_sleep_quality = df['sleep_quality'].mean()
            avg_sleep_duration = df['sleep_duration_hours'].mean()
            
            if avg_sleep_quality < 6:
                recommendations.append({
                    'type': 'sleep',
                    'title': 'Улучшите качество сна',
                    'description': f'Ваше среднее качество сна: {avg_sleep_quality:.1f}/10. Попробуйте создать вечерний ритуал и избегать экранов перед сном.',
                    'confidence': 0.9,
                    'priority': 4
                })
            
            if avg_sleep_duration < 7:
                recommendations.append({
                    'type': 'sleep',
                    'title': 'Увеличьте продолжительность сна',
                    'description': f'Вы спите в среднем {avg_sleep_duration:.1f} часов. Рекомендуется 7-9 часов сна.',
                    'confidence': 0.8,
                    'priority': 3
                })
        
        # Анализ питания
        if 'avg_health_rating' in df.columns:
            avg_health_rating = df['avg_health_rating'].mean()
            if avg_health_rating < 6:
                recommendations.append({
                    'type': 'nutrition',
                    'title': 'Улучшите качество питания',
                    'description': f'Средняя оценка полезности питания: {avg_health_rating:.1f}/10. Попробуйте добавить больше овощей и фруктов.',
                    'confidence': 0.8,
                    'priority': 3
                })
        
        # Анализ активности
        if 'activities_count' in df.columns and 'avg_enjoyment' in df.columns:
            avg_activities = df['activities_count'].mean()
            avg_enjoyment = df['avg_enjoyment'].mean()
            
            if avg_activities < 2:
                recommendations.append({
                    'type': 'activity',
                    'title': 'Увеличьте активность',
                    'description': f'В среднем у вас {avg_activities:.1f} активностей в день. Попробуйте добавить прогулки или спорт.',
                    'confidence': 0.7,
                    'priority': 2
                })
            
            if avg_enjoyment < 6:
                recommendations.append({
                    'type': 'activity',
                    'title': 'Найдите более приятные активности',
                    'description': f'Средняя оценка удовольствия от активностей: {avg_enjoyment:.1f}/10. Попробуйте новые хобби.',
                    'confidence': 0.7,
                    'priority': 2
                })
        
        # Сортируем по приоритету
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations
    
    def predict_mood(self, features: Dict) -> Optional[float]:
        """Предсказание настроения на основе факторов"""
        
        if self.mood_model is None:
            return None
        
        # Подготавливаем признаки
        feature_names = list(self.feature_importance.keys())
        feature_values = []
        
        for feature in feature_names:
            feature_values.append(features.get(feature, 5.0))  # Значение по умолчанию
        
        # Делаем предсказание
        prediction = self.mood_model.predict([feature_values])[0]
        return float(prediction)
