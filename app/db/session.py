from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please create a .env file with DATABASE_URL.")

# ایجاد engine با تنظیمات بهینه
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # بررسی اتصال قبل از استفاده
    pool_recycle=3600,   # بازیابی اتصال بعد از 1 ساعت
    echo=False           # برای debug می‌توان True کرد
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """دیتابیس سشن رو میده (context manager)"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()