from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from database.database import engine
from database.database import Base

from routers.auth import router as auth_router
from routers.workouts import router as workout_router
from routers.nutrition import router as nutrition_router
from routers.progress import router as progress_router
from routers.users import router as users_router

from models.user import User
from models.workout import Workout
from models.nutrition import Nutrition
from models.progress import Progress

app = FastAPI(
    title="Royal Fitness SL API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logging.warning(f"Could not create database tables: {e}")
    logging.info("Make sure your PostgreSQL database is properly configured and has necessary permissions")

app.include_router(auth_router)
app.include_router(workout_router)
app.include_router(nutrition_router)
app.include_router(progress_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Royal Fitness SL API"
    }
