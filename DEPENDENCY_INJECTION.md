# Dependency Injection در FastAPI

این مستند توضیح می‌دهد که چگونه Dependency Injection در پروژه پیاده‌سازی شده است.

## ساختار Dependency Injection

### 1. Database Session Management

#### فایل: `app/db/session.py`

این فایل شامل:
- **Engine**: اتصال اصلی به PostgreSQL
- **SessionLocal**: Factory برای ایجاد sessionهای جدید
- **get_db()**: Context manager برای CLI (غیر FastAPI)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # بررسی اتصال قبل از استفاده
    pool_recycle=3600,   # بازیابی اتصال بعد از 1 ساعت
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### فایل: `app/api/dependencies.py`

این فایل شامل dependencyهای FastAPI است:

**get_db()** - Dependency اصلی برای database session:
```python
def get_db() -> Session:
    """
    Dependency برای دریافت database session
    
    این dependency:
    - یک session جدید ایجاد می‌کند
    - آن را به endpoint می‌دهد
    - بعد از اتمام درخواست، session را می‌بندد
    - در صورت خطا، rollback می‌کند
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(...)
    finally:
        db.close()
```

**get_project_service()** - Dependency برای ProjectService:
```python
def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """
    Dependency برای دریافت ProjectService
    
    این dependency:
    - یک session از get_db دریافت می‌کند
    - ProjectRepository را با این session ایجاد می‌کند
    - ProjectService را با repository ایجاد می‌کند
    - Service را به endpoint می‌دهد
    """
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)
```

**get_task_service()** - Dependency برای TaskService:
```python
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """
    Dependency برای دریافت TaskService
    
    این dependency:
    - یک session از get_db دریافت می‌کند
    - Repositoryها را با این session ایجاد می‌کند
    - Service را با repositoryها ایجاد می‌کند
    - Service را به endpoint می‌دهد
    """
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TaskService(task_repo, project_repo)
```

## استفاده در Endpointها

### مثال: ایجاد پروژه

```python
@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    ایجاد پروژه جدید
    
    FastAPI به صورت خودکار:
    1. get_project_service را صدا می‌زند
    2. get_project_service، get_db را صدا می‌زند
    3. get_db یک session جدید ایجاد می‌کند
    4. session به repository داده می‌شود
    5. repository به service داده می‌شود
    6. service به endpoint داده می‌شود
    7. بعد از اتمام endpoint، session بسته می‌شود
    """
    created_project = project_service.create_project(
        name=project.name,
        description=project.description
    )
    return created_project
```

## Lifecycle Events

### Startup Event

در `api.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    check_db_connection()  # بررسی اتصال به دیتابیس
    yield
    # Shutdown
    engine.dispose()  # بستن تمام اتصالات
```

این lifecycle:
- **در startup**: اتصال دیتابیس را بررسی می‌کند
- **در shutdown**: تمام اتصالات را می‌بندد

## مزایای این معماری

### 1. جداسازی Concerns
- **Session Management**: در `dependencies.py`
- **Business Logic**: در `services/`
- **Data Access**: در `repositories/`
- **API Layer**: در `api/v1/`

### 2. قابلیت تست
```python
# در تست می‌توانید dependency را override کنید
def override_get_db():
    # استفاده از test database
    pass

app.dependency_overrides[get_db] = override_get_db
```

### 3. مدیریت خودکار Session
- FastAPI به صورت خودکار session را ایجاد و می‌بندد
- در صورت خطا، rollback انجام می‌شود
- نیازی به مدیریت دستی session نیست

### 4. Performance
- Connection pooling با SQLAlchemy
- `pool_pre_ping`: بررسی اتصال قبل از استفاده
- `pool_recycle`: بازیابی اتصالات قدیمی

## Flow Diagram

```
Request → FastAPI
    ↓
Endpoint (create_project)
    ↓
Depends(get_project_service)
    ↓
Depends(get_db)
    ↓
SessionLocal() → New Session
    ↓
ProjectRepository(session)
    ↓
ProjectService(repository)
    ↓
Business Logic Execution
    ↓
Repository.commit() (یا rollback در صورت خطا)
    ↓
Session.close()
    ↓
Response
```

## بررسی اتصال دیتابیس

### Endpoint: `/health/db`

```bash
curl http://localhost:8000/health/db
```

این endpoint اتصال دیتابیس را بررسی می‌کند.

## نکات مهم

1. **هر درخواست یک session جدید**: هر HTTP request یک session جدید دریافت می‌کند
2. **Transaction Management**: Repositoryها خودشان commit می‌کنند
3. **Error Handling**: در صورت خطا، rollback انجام می‌شود
4. **Connection Pooling**: Engine از connection pooling استفاده می‌کند
5. **Lifecycle Management**: Startup/Shutdown events برای مدیریت اتصالات

## مثال کامل

```python
# 1. Dependency تعریف می‌شود
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

# 2. Service dependency تعریف می‌شود
def get_project_service(db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    return ProjectService(repo)

# 3. در endpoint استفاده می‌شود
@router.post("/projects/")
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    return service.create_project(...)
```

## تست Dependency Injection

```python
from fastapi.testclient import TestClient
from app.api.dependencies import get_db
from app.db.session import SessionLocal

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
response = client.post("/api/v1/projects/", json={"name": "Test"})
```

