"""
FastAPI Application - TodoList Project
فایل اصلی برنامه FastAPI برای پروژه TodoList
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# ایجاد نمونه FastAPI
app = FastAPI(
    title="TodoList API",
    description="API برای مدیریت پروژه‌ها و تسک‌ها",
    version="1.0.0"
)


@app.get("/")
async def root():
    """
    Endpoint اصلی برای تست
    """
    return JSONResponse(
        content={
            "message": "خوش آمدید به TodoList API",
            "status": "success",
            "version": "1.0.0"
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

