"""
Pydantic Schemas for Task entity
Schemaهای Pydantic برای موجودیت Task
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """وضعیت تسک"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskBase(BaseModel):
    """Schema پایه برای Task"""
    title: str = Field(..., min_length=1, max_length=200, description="عنوان تسک")
    description: Optional[str] = Field(None, description="توضیحات تسک")
    deadline: Optional[datetime] = Field(None, description="مهلت انجام تسک")


class TaskCreate(TaskBase):
    """
    Schema برای ایجاد تسک جدید (Input)
    """
    project_id: int = Field(..., gt=0, description="شناسه پروژه")


class TaskUpdate(BaseModel):
    """
    Schema برای به‌روزرسانی تسک (Input)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="عنوان تسک")
    description: Optional[str] = Field(None, description="توضیحات تسک")
    deadline: Optional[datetime] = Field(None, description="مهلت انجام تسک")
    status: Optional[TaskStatus] = Field(None, description="وضعیت تسک")


class TaskResponse(TaskBase):
    """
    Schema برای پاسخ API (Output)
    """
    id: int = Field(..., description="شناسه تسک")
    project_id: int = Field(..., description="شناسه پروژه")
    status: TaskStatus = Field(..., description="وضعیت تسک")
    created_at: datetime = Field(..., description="تاریخ ایجاد")
    updated_at: datetime = Field(..., description="تاریخ آخرین به‌روزرسانی")
    closed_at: Optional[datetime] = Field(None, description="تاریخ بسته شدن تسک")
    
    model_config = ConfigDict(from_attributes=True)  # برای تبدیل از SQLAlchemy model

