"""
FastAPI Application - TodoList Project
فایل اصلی برنامه FastAPI برای پروژه TodoList
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.api.dependencies import check_db_connection
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events برای FastAPI
    
    - Startup: بررسی اتصال به دیتابیس
    - Shutdown: بستن اتصالات دیتابیس
    """
    # Startup
    print("🚀 Starting up...")
    try:
        check_db_connection()
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    engine.dispose()
    print("✅ Database connections closed")


# ایجاد نمونه FastAPI با lifecycle events
app = FastAPI(
    title="TodoList API",
    description="API برای مدیریت پروژه‌ها و تسک‌ها",
    version="1.0.0",
    lifespan=lifespan
)

# اضافه کردن Routerهای API
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Endpoint اصلی برای تست
    """
    return JSONResponse(
        content={
            "message": "خوش آمدید به TodoList API",
            "status": "success",
            "version": "1.0.0",
            "docs": "/docs",
            "api": "/api/v1"
        }
    )


@app.get("/health")
async def health_check():
    """
    بررسی سلامت API
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "message": "API is running"
        }
    )


@app.get("/health/db")
async def health_check_db():
    """
    بررسی سلامت اتصال به دیتابیس
    """
    try:
        check_db_connection()
        return JSONResponse(
            content={
                "status": "healthy",
                "database": "connected",
                "message": "Database connection is OK"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "message": f"Database connection failed: {str(e)}"
            }
        )

