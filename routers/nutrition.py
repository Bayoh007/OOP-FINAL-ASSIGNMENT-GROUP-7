from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db

from models.nutrition import Nutrition
from models.user import User

from schemas.nutrition import NutritionCreate, NutritionResponse

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutrition"]
)


@router.post("/", response_model=NutritionResponse)
def create_nutrition(
    nutrition: NutritionCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a nutrition entry"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_nutrition = Nutrition(
        food_name=nutrition.food_name,
        calories=nutrition.calories,
        protein=nutrition.protein,
        carbs=nutrition.carbs,
        user_id=user_id
    )
    db.add(new_nutrition)
    try:
        db.commit()
        db.refresh(new_nutrition)
        return new_nutrition
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid nutrition or user data")


@router.get("/{nutrition_id}", response_model=NutritionResponse)
def get_nutrition(
    nutrition_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific nutrition entry"""
    nutrition = db.query(Nutrition).filter(
        Nutrition.id == nutrition_id
    ).first()
    
    if not nutrition:
        raise HTTPException(
            status_code=404,
            detail="Nutrition entry not found"
        )
    
    return nutrition


@router.get("/user/{user_id}", response_model=List[NutritionResponse])
def get_user_nutrition(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all nutrition entries for a user"""
    nutrition = db.query(Nutrition).filter(
        Nutrition.user_id == user_id
    ).all()
    
    return nutrition


@router.put("/{nutrition_id}", response_model=NutritionResponse)
def update_nutrition(
    nutrition_id: int,
    nutrition: NutritionCreate,
    db: Session = Depends(get_db)
):
    """Update a nutrition entry"""
    db_nutrition = db.query(Nutrition).filter(
        Nutrition.id == nutrition_id
    ).first()
    
    if not db_nutrition:
        raise HTTPException(
            status_code=404,
            detail="Nutrition entry not found"
        )
    
    db_nutrition.food_name = nutrition.food_name
    db_nutrition.calories = nutrition.calories
    db_nutrition.protein = nutrition.protein
    db_nutrition.carbs = nutrition.carbs
    
    db.commit()
    db.refresh(db_nutrition)
    
    return db_nutrition


@router.delete("/{nutrition_id}")
def delete_nutrition(
    nutrition_id: int,
    db: Session = Depends(get_db)
):
    """Delete a nutrition entry"""
    db_nutrition = db.query(Nutrition).filter(
        Nutrition.id == nutrition_id
    ).first()
    
    if not db_nutrition:
        raise HTTPException(
            status_code=404,
            detail="Nutrition entry not found"
        )
    
    db.delete(db_nutrition)
    db.commit()
    
    return {"message": "Nutrition entry deleted successfully"}
