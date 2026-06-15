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

from dotenv import load_dotenv
import os

# New main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Fitness Tracker API")

# --- ADD THIS FUNCTION TO UPDATE OPENAPI SCHEMA ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Fitness Tracker API",
        version="1.0.0",
        routes=app.routes,
    )
    # This block tells Swagger to add the Bearer Auth option
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **Bearer <YOUR_TOKEN>**"
        }
    }
    openapi_schema["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# --------------------------------------------------

# Include your routers as before
# app.include_router(auth.router)
# app.include_router(workouts.router)

# Load environment variables from .env
load_dotenv()

# Note: DATABASE_URL is loaded in core.config, not here
# Removed direct psycopg2.connect() call to prevent blocking app startup

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
