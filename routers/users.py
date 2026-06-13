from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.user import User

from schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user"""
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):
    """Get all users"""
    users = db.query(User).all()
    return users
