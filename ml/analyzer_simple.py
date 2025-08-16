import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class SimpleDayAnalyzer:
    def __init__(self):
        self.mood_data = []
        self.meal_data = []
        self.activity_data = []
        
    def analyze_daily_records(self, daily_records: List[Dict]) -> Dict:
        """Простой анализ записей дня без ML"""
        
        if not daily_records:
            return {"message": "Нет данных для анализа"}
        
        # Базовые статистики
        total_records = len(daily_records)
        avg_sleep_quality = sum(r.get('sleep_quality', 0) for r in daily_records) / total_records
        avg_mood = sum(r.get('mood_rating', 0) for r in daily_records) / total_records
        avg_wellness = sum(r.get('wellness_rating', 0) for r in daily_records) / total_records
        
        # Анализ времени сна
        sleep_times = []
        wake_times = []
        
        for record in daily_records:
            if record.get('sleep_time'):
                try:
                    sleep_time = datetime.fromisoformat(record['sleep_time'].replace('Z', '+00:00'))
                    sleep_times.append(sleep_time.hour)
                except:
                    pass
                    
            if record.get('wake_up_time'):
                try:
                    wake_time = datetime.fromisoformat(record['wake_up_time'].replace('Z', '+00:00'))
                    wake_times.append(wake_time.hour)
                except:
                    pass
        
        # Рекомендации
        recommendations = []
        
        if avg_sleep_quality < 6:
            recommendations.append("Попробуйте улучшить качество сна: установите режим сна, избегайте экранов перед сном")
        
        if avg_mood < 6:
            recommendations.append("Ваше настроение ниже среднего. Попробуйте добавить больше физической активности")
        
        if avg_wellness < 6:
            recommendations.append("Обратите внимание на общее самочувствие. Возможно, стоит пересмотреть режим дня")
        
        if sleep_times and wake_times:
            avg_sleep_hour = sum(sleep_times) / len(sleep_times)
            avg_wake_hour = sum(wake_times) / len(wake_times)
            
            if avg_sleep_hour > 23 or avg_sleep_hour < 22:
                recommendations.append("Попробуйте ложиться спать в 22:00-23:00 для лучшего качества сна")
            
            if avg_wake_hour > 8:
                recommendations.append("Ранний подъем может улучшить продуктивность дня")
        
        return {
            "total_records": total_records,
            "average_sleep_quality": round(avg_sleep_quality, 2),
            "average_mood": round(avg_mood, 2),
            "average_wellness": round(avg_wellness, 2),
            "recommendations": recommendations,
            "analysis_date": datetime.now().isoformat()
        }
    
    def analyze_meals(self, meals: List[Dict]) -> Dict:
        """Анализ приемов пищи"""
        
        if not meals:
            return {"message": "Нет данных о приемах пищи"}
        
        # Статистики по приемам пищи
        total_meals = len(meals)
        avg_taste = sum(m.get('taste_rating', 0) for m in meals) / total_meals
        avg_health = sum(m.get('health_rating', 0) for m in meals) / total_meals
        
        # Популярные размеры порций
        portion_sizes = [m.get('portion_size', 'medium') for m in meals]
        portion_counter = Counter(portion_sizes)
        most_common_portion = portion_counter.most_common(1)[0][0] if portion_counter else 'medium'
        
        # Рекомендации по питанию
        recommendations = []
        
        if avg_health < 6:
            recommendations.append("Попробуйте включить больше овощей и фруктов в рацион")
        
        if avg_taste < 6:
            recommendations.append("Экспериментируйте с новыми рецептами для улучшения вкусовых ощущений")
        
        if most_common_portion == 'large':
            recommendations.append("Попробуйте уменьшить размер порций для лучшего пищеварения")
        
        return {
            "total_meals": total_meals,
            "average_taste_rating": round(avg_taste, 2),
            "average_health_rating": round(avg_health, 2),
            "most_common_portion_size": most_common_portion,
            "recommendations": recommendations
        }
    
    def analyze_activities(self, activities: List[Dict]) -> Dict:
        """Анализ активностей"""
        
        if not activities:
            return {"message": "Нет данных об активностях"}
        
        # Статистики по активностям
        total_activities = len(activities)
        avg_intensity = sum(a.get('intensity', 0) for a in activities) / total_activities
        avg_enjoyment = sum(a.get('enjoyment_rating', 0) for a in activities) / total_activities
        
        # Популярные типы активностей
        activity_types = [a.get('activity_type', 'other') for a in activities]
        activity_counter = Counter(activity_types)
        most_popular_activity = activity_counter.most_common(1)[0][0] if activity_counter else 'other'
        
        # Рекомендации по активностям
        recommendations = []
        
        if avg_enjoyment < 6:
            recommendations.append("Попробуйте найти новые виды активностей, которые приносят больше удовольствия")
        
        if avg_intensity < 5:
            recommendations.append("Увеличьте интенсивность физических нагрузок для лучшего самочувствия")
        
        if total_activities < 3:
            recommendations.append("Попробуйте добавить больше разнообразных активностей в день")
        
        return {
            "total_activities": total_activities,
            "average_intensity": round(avg_intensity, 2),
            "average_enjoyment": round(avg_enjoyment, 2),
            "most_popular_activity": most_popular_activity,
            "recommendations": recommendations
        }
    
    def generate_daily_summary(self, daily_records: List[Dict], 
                             meals: List[Dict], activities: List[Dict]) -> Dict:
        """Генерация ежедневного отчета"""
        
        daily_analysis = self.analyze_daily_records(daily_records)
        meal_analysis = self.analyze_meals(meals)
        activity_analysis = self.analyze_activities(activities)
        
        # Общие рекомендации
        all_recommendations = []
        all_recommendations.extend(daily_analysis.get('recommendations', []))
        all_recommendations.extend(meal_analysis.get('recommendations', []))
        all_recommendations.extend(activity_analysis.get('recommendations', []))
        
        return {
            "daily_analysis": daily_analysis,
            "meal_analysis": meal_analysis,
            "activity_analysis": activity_analysis,
            "all_recommendations": all_recommendations,
            "summary": {
                "total_records": daily_analysis.get('total_records', 0),
                "overall_mood": daily_analysis.get('average_mood', 0),
                "overall_wellness": daily_analysis.get('average_wellness', 0),
                "recommendations_count": len(all_recommendations)
            }
        }
