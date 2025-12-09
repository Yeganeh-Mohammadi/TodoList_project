"""
Router for Task endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.api.dependencies import get_task_service
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
from app.models.task import TaskStatus as TaskStatusEnum

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    """
    ایجاد تسک جدید
    
    - **title**: عنوان تسک (اجباری)
    - **project_id**: شناسه پروژه (اجباری)
    - **description**: توضیحات تسک (اختیاری)
    - **deadline**: مهلت انجام تسک (اختیاری)
    """
    try:
        created_task = task_service.create_task(
            title=task.title,
            project_id=task.project_id,
            description=task.description,
            deadline=task.deadline
        )
        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    project_id: Optional[int] = Query(None, description="فیلتر بر اساس شناسه پروژه"),
    task_service: TaskService = Depends(get_task_service)
):
    """
    دریافت لیست تمام تسک‌ها
    
    - **project_id**: (اختیاری) اگر مشخص شود، فقط تسک‌های این پروژه برگردانده می‌شود
    """
    if project_id:
        tasks = task_service.get_tasks_by_project(project_id)
    else:
        tasks = task_service.get_all_tasks()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    دریافت یک تسک خاص با استفاده از شناسه
    
    - **task_id**: شناسه تسک
    """
    try:
        task = task_service.get_task_by_id(task_id)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """
    به‌روزرسانی تسک
    
    - **task_id**: شناسه تسک
    - **title**: عنوان جدید تسک (اختیاری)
    - **description**: توضیحات جدید تسک (اختیاری)
    - **deadline**: مهلت جدید تسک (اختیاری)
    - **status**: وضعیت جدید تسک (اختیاری) - مقادیر: todo, doing, done
    """
    try:
        # تبدیل TaskStatus از Pydantic schema به TaskStatusEnum از model (اگر وجود داشته باشد)
        status_enum = None
        if task_update.status is not None:
            status_enum = TaskStatusEnum(task_update.status.value)
        
        updated_task = task_service.update_task(
            task_id=task_id,
            title=task_update.title,
            description=task_update.description,
            deadline=task_update.deadline,
            status=status_enum
        )
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    new_status: TaskStatus,
    task_service: TaskService = Depends(get_task_service)
):
    """
    به‌روزرسانی فقط وضعیت تسک
    
    - **task_id**: شناسه تسک
    - **new_status**: وضعیت جدید (todo, doing, done)
    """
    try:
        # تبدیل TaskStatus از Pydantic schema به TaskStatusEnum از model
        status_enum = TaskStatusEnum(new_status.value)
        updated_task = task_service.update_task_status(task_id, status_enum)
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    حذف تسک
    
    - **task_id**: شناسه تسک
    """
    try:
        task_service.delete_task(task_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
