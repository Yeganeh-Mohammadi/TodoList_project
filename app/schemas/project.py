"""
Pydantic Schemas for Project entity
Schemaهای Pydantic برای موجودیت Project
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    """Schema پایه برای Project"""
    name: str = Field(..., min_length=1, max_length=100, description="نام پروژه")
    description: Optional[str] = Field(None, description="توضیحات پروژه")


class ProjectCreate(ProjectBase):
    """
    Schema برای ایجاد پروژه جدید (Input)
    """
    pass


class ProjectUpdate(BaseModel):
    """
    Schema برای به‌روزرسانی پروژه (Input)
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="نام پروژه")
    description: Optional[str] = Field(None, description="توضیحات پروژه")


class ProjectResponse(ProjectBase):
    """
    Schema برای پاسخ API (Output)
    """
    id: int = Field(..., description="شناسه پروژه")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ آخرین به‌روزرسانی")
    
    model_config = ConfigDict(from_attributes=True)  # برای تبدیل از SQLAlchemy model

