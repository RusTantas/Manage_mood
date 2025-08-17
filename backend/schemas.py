from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Daily Record schemas
class DailyRecordBase(BaseModel):
    wake_up_time: Optional[datetime] = None
    sleep_time: Optional[datetime] = None
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    overall_mood: Optional[int] = Field(None, ge=1, le=10)
    physical_wellness: Optional[int] = Field(None, ge=1, le=10)
    mental_wellness: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class DailyRecordCreate(DailyRecordBase):
    pass

class DailyRecord(DailyRecordBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True

# Meal schemas
class MealBase(BaseModel):
    meal_time: datetime
    meal_type: str  # breakfast, lunch, dinner, snack
    food_items: str  # JSON string
    portion_size: str  # small, medium, large
    taste_rating: Optional[int] = Field(None, ge=1, le=10)
    health_rating: Optional[int] = Field(None, ge=1, le=10)

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int
    user_id: int
    daily_record_id: int
    
    class Config:
        from_attributes = True

# Activity schemas
class ActivityBase(BaseModel):
    activity_type: str  # sport, walk, social, work, hobby
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    intensity: Optional[int] = Field(None, ge=1, le=10)
    location: Optional[str] = None
    description: Optional[str] = None
    enjoyment_rating: Optional[int] = Field(None, ge=1, le=10)

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    user_id: int
    daily_record_id: int
    
    class Config:
        from_attributes = True

# Mood Tracking schemas
class MoodTrackingBase(BaseModel):
    emotion: str  # joy, sadness, anger, calm, anxiety, excitement
    intensity: int = Field(..., ge=1, le=10)
    triggers: Optional[str] = None
    notes: Optional[str] = None

class MoodTrackingCreate(MoodTrackingBase):
    pass

class MoodTracking(MoodTrackingBase):
    id: int
    user_id: int
    daily_record_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class DailyAnalytics(BaseModel):
    date: datetime
    sleep_hours: Optional[float] = None
    average_mood: Optional[float] = None
    activities_count: int
    meals_count: int
    mood_entries_count: int

class CorrelationAnalysis(BaseModel):
    factor: str
    correlation_with_mood: float
    sample_size: int
    confidence_level: float

class Recommendation(BaseModel):
    type: str  # sleep, nutrition, activity, general
    title: str
    description: str
    confidence: float
    priority: int  # 1-5, where 5 is highest priority

