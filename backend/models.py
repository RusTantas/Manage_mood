from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    daily_records = relationship("DailyRecord", back_populates="user")
    meals = relationship("Meal", back_populates="user")
    activities = relationship("Activity", back_populates="user")
    mood_trackings = relationship("MoodTracking", back_populates="user")

class DailyRecord(Base):
    __tablename__ = "daily_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    
    # Sleep data
    wake_up_time = Column(DateTime)
    sleep_time = Column(DateTime)
    sleep_quality = Column(Integer)  # 1-10
    
    # Mood and wellness
    overall_mood = Column(Integer)  # 1-10
    physical_wellness = Column(Integer)  # 1-10
    mental_wellness = Column(Integer)  # 1-10
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="daily_records")
    meals = relationship("Meal", back_populates="daily_record")
    activities = relationship("Activity", back_populates="daily_record")
    mood_trackings = relationship("MoodTracking", back_populates="daily_record")

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_record_id = Column(Integer, ForeignKey("daily_records.id"))
    
    meal_time = Column(DateTime)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    food_items = Column(Text)  # JSON string of food items
    portion_size = Column(String)  # small, medium, large
    taste_rating = Column(Integer)  # 1-10
    health_rating = Column(Integer)  # 1-10
    
    # Relationships
    user = relationship("User", back_populates="meals")
    daily_record = relationship("DailyRecord", back_populates="meals")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_record_id = Column(Integer, ForeignKey("daily_records.id"))
    
    activity_type = Column(String)  # sport, walk, social, work, hobby
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    intensity = Column(Integer)  # 1-10
    location = Column(String)
    description = Column(Text)
    enjoyment_rating = Column(Integer)  # 1-10
    
    # Relationships
    user = relationship("User", back_populates="activities")
    daily_record = relationship("DailyRecord", back_populates="activities")

class MoodTracking(Base):
    __tablename__ = "mood_trackings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_record_id = Column(Integer, ForeignKey("daily_records.id"))
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotion = Column(String)  # joy, sadness, anger, calm, anxiety, excitement
    intensity = Column(Integer)  # 1-10
    triggers = Column(Text)  # What caused this mood
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="mood_trackings")
    daily_record = relationship("DailyRecord", back_populates="mood_trackings")

