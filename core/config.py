import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://royal_admin:123456@localhost/royal_fitness_db"
)

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "ROYALFITNESSSL2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# API
API_TITLE = "Royal Fitness SL API"
API_VERSION = "1.0.0"
