"""
Test script for FastAPI endpoints
اسکریپت تست برای endpointهای FastAPI
"""

import sys
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """تست import کردن ماژول‌ها"""
    try:
        from app.api.v1.router import api_router
        print("✓ Router imports OK")
        
        from app.api.dependencies import get_db, get_project_service, get_task_service
        print("✓ Dependencies imports OK")
        
        from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
        print("✓ Project schemas imports OK")
        
        from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
        print("✓ Task schemas imports OK")
        
        from app.services.project_service import ProjectService
        from app.services.task_service import TaskService
        print("✓ Services imports OK")
        
        from api import app
        print("✓ FastAPI app imports OK")
        
        print("\n✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_schema_validation():
    """تست validation در Schemaها"""
    try:
        from app.schemas.project import ProjectCreate, ProjectUpdate
        from app.schemas.task import TaskCreate, TaskUpdate, TaskStatus
        from datetime import datetime
        
        # تست ProjectCreate
        project = ProjectCreate(name="Test Project", description="Test Description")
        assert project.name == "Test Project"
        print("✓ ProjectCreate validation OK")
        
        # تست TaskCreate
        task = TaskCreate(
            title="Test Task",
            project_id=1,
            description="Test Description",
            deadline=datetime(2025, 12, 31)
        )
        assert task.title == "Test Task"
        assert task.project_id == 1
        print("✓ TaskCreate validation OK")
        
        # تست TaskStatus enum
        assert TaskStatus.TODO.value == "todo"
        assert TaskStatus.DOING.value == "doing"
        assert TaskStatus.DONE.value == "done"
        print("✓ TaskStatus enum OK")
        
        print("\n✅ All schema validations successful!")
        return True
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_routes():
    """تست routes در FastAPI app"""
    try:
        from api import app
        
        # بررسی routes
        routes = [route.path for route in app.routes]
        
        expected_routes = [
            "/",
            "/health",
            "/api/v1/projects/",
            "/api/v1/tasks/",
        ]
        
        print("\nRegistered routes:")
        for route in routes:
            print(f"  - {route}")
        
        # بررسی وجود routes اصلی
        has_projects = any("/projects" in route for route in routes)
        has_tasks = any("/tasks" in route for route in routes)
        
        if has_projects and has_tasks:
            print("\n✅ All main routes registered!")
            return True
        else:
            print(f"\n⚠️  Missing routes - Projects: {has_projects}, Tasks: {has_tasks}")
            return False
            
    except Exception as e:
        print(f"❌ Route test error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Testing FastAPI Application")
    print("=" * 50)
    
    results = []
    
    print("\n1. Testing imports...")
    results.append(test_imports())
    
    print("\n2. Testing schema validation...")
    results.append(test_schema_validation())
    
    print("\n3. Testing app routes...")
    results.append(test_app_routes())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed!")
        print("\nYou can now run the server with:")
        print("  uvicorn api:app --reload")
        print("\nThen visit:")
        print("  - http://localhost:8000/docs (Swagger UI)")
        print("  - http://localhost:8000/redoc (ReDoc)")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
    print("=" * 50)

