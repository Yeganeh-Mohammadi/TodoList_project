"""
Router for Project endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.dependencies import get_project_service
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    ایجاد پروژه جدید
    
    - **name**: نام پروژه (اجباری)
    - **description**: توضیحات پروژه (اختیاری)
    """
    try:
        created_project = project_service.create_project(
            name=project.name,
            description=project.description
        )
        return created_project
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    project_service: ProjectService = Depends(get_project_service)
):
    """
    دریافت لیست تمام پروژه‌ها
    """
    projects = project_service.get_all_projects()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    دریافت یک پروژه خاص با استفاده از شناسه
    
    - **project_id**: شناسه پروژه
    """
    try:
        project = project_service.get_project_by_id(project_id)
        return project
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    به‌روزرسانی پروژه
    
    - **project_id**: شناسه پروژه
    - **name**: نام جدید پروژه (اختیاری)
    - **description**: توضیحات جدید پروژه (اختیاری)
    """
    try:
        updated_project = project_service.update_project(
            project_id=project_id,
            name=project_update.name,
            description=project_update.description
        )
        return updated_project
    except ValueError as e:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code,
            detail=str(e)
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    حذف پروژه
    
    - **project_id**: شناسه پروژه
    
    توجه: با حذف پروژه، تمام تسک‌های مرتبط نیز حذف می‌شوند (Cascade Delete)
    """
    try:
        project_service.delete_project(project_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

