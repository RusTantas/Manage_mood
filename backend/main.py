from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db, engine
import models
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Day Tracker API",
    description="API для отслеживания ежедневной активности и настроения",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Day Tracker API!"}

# Daily Records endpoints
@app.post("/daily-records/", response_model=schemas.DailyRecord)
def create_daily_record(
    daily_record: schemas.DailyRecordCreate,
    db: Session = Depends(get_db)
):
    # For now, we'll use a default user_id of 1
    # In a real app, you'd get this from authentication
    db_daily_record = models.DailyRecord(
        user_id=1,
        **daily_record.dict()
    )
    db.add(db_daily_record)
    db.commit()
    db.refresh(db_daily_record)
    return db_daily_record

@app.get("/daily-records/", response_model=List[schemas.DailyRecord])
def get_daily_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    daily_records = db.query(models.DailyRecord).offset(skip).limit(limit).all()
    return daily_records

@app.get("/daily-records/{record_id}", response_model=schemas.DailyRecord)
def get_daily_record(record_id: int, db: Session = Depends(get_db)):
    daily_record = db.query(models.DailyRecord).filter(models.DailyRecord.id == record_id).first()
    if daily_record is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return daily_record

# Meals endpoints
@app.post("/meals/", response_model=schemas.Meal)
def create_meal(
    meal: schemas.MealCreate,
    daily_record_id: int,
    db: Session = Depends(get_db)
):
    db_meal = models.Meal(
        user_id=1,
        daily_record_id=daily_record_id,
        **meal.dict()
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

@app.get("/meals/", response_model=List[schemas.Meal])
def get_meals(
    daily_record_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Meal)
    if daily_record_id:
        query = query.filter(models.Meal.daily_record_id == daily_record_id)
    meals = query.offset(skip).limit(limit).all()
    return meals

# Activities endpoints
@app.post("/activities/", response_model=schemas.Activity)
def create_activity(
    activity: schemas.ActivityCreate,
    daily_record_id: int,
    db: Session = Depends(get_db)
):
    db_activity = models.Activity(
        user_id=1,
        daily_record_id=daily_record_id,
        **activity.dict()
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.get("/activities/", response_model=List[schemas.Activity])
def get_activities(
    daily_record_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Activity)
    if daily_record_id:
        query = query.filter(models.Activity.daily_record_id == daily_record_id)
    activities = query.offset(skip).limit(limit).all()
    return activities

# Mood Tracking endpoints
@app.post("/mood-tracking/", response_model=schemas.MoodTracking)
def create_mood_tracking(
    mood_tracking: schemas.MoodTrackingCreate,
    daily_record_id: int,
    db: Session = Depends(get_db)
):
    db_mood_tracking = models.MoodTracking(
        user_id=1,
        daily_record_id=daily_record_id,
        **mood_tracking.dict()
    )
    db.add(db_mood_tracking)
    db.commit()
    db.refresh(db_mood_tracking)
    return db_mood_tracking

@app.get("/mood-tracking/", response_model=List[schemas.MoodTracking])
def get_mood_tracking(
    daily_record_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.MoodTracking)
    if daily_record_id:
        query = query.filter(models.MoodTracking.daily_record_id == daily_record_id)
    mood_trackings = query.offset(skip).limit(limit).all()
    return mood_trackings

# Analytics endpoints
@app.get("/analytics/daily/{date}")
def get_daily_analytics(date: str, db: Session = Depends(get_db)):
    """Get analytics for a specific date"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    
    # Get daily record for the date
    daily_record = db.query(models.DailyRecord).filter(
        models.DailyRecord.date >= target_date,
        models.DailyRecord.date < target_date + timedelta(days=1)
    ).first()
    
    if not daily_record:
        return {
            "date": target_date,
            "sleep_hours": None,
            "average_mood": None,
            "activities_count": 0,
            "meals_count": 0,
            "mood_entries_count": 0
        }
    
    # Calculate sleep hours
    sleep_hours = None
    if daily_record.wake_up_time and daily_record.sleep_time:
        sleep_duration = daily_record.sleep_time - daily_record.wake_up_time
        sleep_hours = sleep_duration.total_seconds() / 3600
    
    # Count related records
    activities_count = db.query(models.Activity).filter(
        models.Activity.daily_record_id == daily_record.id
    ).count()
    
    meals_count = db.query(models.Meal).filter(
        models.Meal.daily_record_id == daily_record.id
    ).count()
    
    mood_entries_count = db.query(models.MoodTracking).filter(
        models.MoodTracking.daily_record_id == daily_record.id
    ).count()
    
    return {
        "date": target_date,
        "sleep_hours": sleep_hours,
        "average_mood": daily_record.overall_mood,
        "activities_count": activities_count,
        "meals_count": meals_count,
        "mood_entries_count": mood_entries_count
    }

@app.get("/analytics/weekly/{start_date}")
def get_weekly_analytics(start_date: str, db: Session = Depends(get_db)):
    """Get analytics for a week starting from the given date"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = start + timedelta(days=7)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    
    daily_records = db.query(models.DailyRecord).filter(
        models.DailyRecord.date >= start,
        models.DailyRecord.date < end
    ).all()
    
    analytics = []
    for record in daily_records:
        # Calculate sleep hours
        sleep_hours = None
        if record.wake_up_time and record.sleep_time:
            sleep_duration = record.sleep_time - record.wake_up_time
            sleep_hours = sleep_duration.total_seconds() / 3600
        
        # Count related records
        activities_count = db.query(models.Activity).filter(
            models.Activity.daily_record_id == record.id
        ).count()
        
        meals_count = db.query(models.Meal).filter(
            models.Meal.daily_record_id == record.id
        ).count()
        
        mood_entries_count = db.query(models.MoodTracking).filter(
            models.MoodTracking.daily_record_id == record.id
        ).count()
        
        analytics.append({
            "date": record.date,
            "sleep_hours": sleep_hours,
            "average_mood": record.overall_mood,
            "activities_count": activities_count,
            "meals_count": meals_count,
            "mood_entries_count": mood_entries_count
        })
    
    return analytics
