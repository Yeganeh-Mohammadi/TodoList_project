"""
FastAPI Application - TodoList Project
فایل اصلی برنامه FastAPI برای پروژه TodoList
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router

# ایجاد نمونه FastAPI
app = FastAPI(
    title="TodoList API",
    description="API برای مدیریت پروژه‌ها و تسک‌ها",
    version="1.0.0"
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

