"""
Main router for API v1
"""

from fastapi import APIRouter
from app.api.v1 import projects, tasks

api_router = APIRouter()

# اضافه کردن routerهای مختلف
api_router.include_router(projects.router)
api_router.include_router(tasks.router)

