import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import (
    DATABASE_URL as SQLALCHEMY_DATABASE_URL,
    SUPABASE_URL,
    SUPABASE_KEY,
)

try:
    from supabase import create_client
except Exception:
    create_client = None

supabase = None
if create_client and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("Supabase client init failed:", e)
else:
    if not create_client:
        print("Supabase package not installed; skipping client initialization")
    elif not (SUPABASE_URL and SUPABASE_KEY):
        print("SUPABASE_URL or SUPABASE_KEY not set; skipping Supabase client init")


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    conn = engine.connect()
    print("Database connected successfully")
except Exception as e:
    print("Database connection failed:", e)