from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.workout import Workout

from schemas.workout import WorkoutCreate, WorkoutResponse

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.post("/", response_model=WorkoutResponse)
def create_workout(
    workout: WorkoutCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new workout"""
    new_workout = Workout(
        workout_name=workout.workout_name,
        duration=workout.duration,
        calories_burned=workout.calories_burned,
        user_id=user_id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific workout"""
    workout = db.query(Workout).filter(
        Workout.id == workout_id
    ).first()
    
    if not workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    
    return workout


@router.get("/user/{user_id}", response_model=List[WorkoutResponse])
def get_user_workouts(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all workouts for a user"""
    workouts = db.query(Workout).filter(
        Workout.user_id == user_id
    ).all()
    
    return workouts


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):
    """Update a workout"""
    db_workout = db.query(Workout).filter(
        Workout.id == workout_id
    ).first()
    
    if not db_workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    
    db_workout.workout_name = workout.workout_name
    db_workout.duration = workout.duration
    db_workout.calories_burned = workout.calories_burned
    
    db.commit()
    db.refresh(db_workout)
    
    return db_workout


@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):
    """Delete a workout"""
    db_workout = db.query(Workout).filter(
        Workout.id == workout_id
    ).first()
    
    if not db_workout:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )
    
    db.delete(db_workout)
    db.commit()
    
    return {"message": "Workout deleted successfully"}
