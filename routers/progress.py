from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.progress import Progress

from schemas.progress import ProgressCreate, ProgressResponse
from services.bmi_service import calculate_bmi

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


@router.post("/", response_model=ProgressResponse)
def create_progress(
    progress: ProgressCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a progress entry"""
    bmi = calculate_bmi(progress.weight, progress.height)
    
    new_progress = Progress(
        weight=progress.weight,
        height=progress.height,
        bmi=bmi,
        user_id=user_id
    )
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return new_progress


@router.get("/{progress_id}", response_model=ProgressResponse)
def get_progress(
    progress_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific progress entry"""
    progress = db.query(Progress).filter(
        Progress.id == progress_id
    ).first()
    
    if not progress:
        raise HTTPException(
            status_code=404,
            detail="Progress entry not found"
        )
    
    return progress


@router.get("/user/{user_id}", response_model=List[ProgressResponse])
def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all progress entries for a user"""
    progress = db.query(Progress).filter(
        Progress.user_id == user_id
    ).all()
    
    return progress


@router.put("/{progress_id}", response_model=ProgressResponse)
def update_progress(
    progress_id: int,
    progress: ProgressCreate,
    db: Session = Depends(get_db)
):
    """Update a progress entry"""
    db_progress = db.query(Progress).filter(
        Progress.id == progress_id
    ).first()
    
    if not db_progress:
        raise HTTPException(
            status_code=404,
            detail="Progress entry not found"
        )
        
    
    db.commit()
    db.refresh(db_progress)
    
    return db_progress


@router.delete("/{progress_id}")
def delete_progress(
    progress_id: int,
    db: Session = Depends(get_db)
):
    """Delete a progress entry"""
    db_progress = db.query(Progress).filter(
        Progress.id == progress_id
    ).first()
    
    if not db_progress:
        raise HTTPException(
            status_code=404,
            detail="Progress entry not found"
        )
    
    db.delete(db_progress)
    db.commit()
    
    return {"message": "Progress entry deleted successfully"}
