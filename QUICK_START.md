# راهنمای سریع اجرا - TodoList API

این راهنما به شما کمک می‌کند تا سریع API را اجرا و تست کنید.

## پیش‌نیازها

1. **Python 3.8+** نصب شده باشد
2. **PostgreSQL** در حال اجرا باشد
3. **فایل `.env`** با `DATABASE_URL` تنظیم شده باشد

## مراحل اجرا

### 1. نصب وابستگی‌ها

```bash
cd TodoList_project
pip install -r requirements.txt
```

### 2. تنظیم دیتابیس

مطمئن شوید که فایل `.env` وجود دارد:

```bash
# کپی کردن فایل نمونه
cp env.example .env

# ویرایش .env و تنظیم DATABASE_URL
# DATABASE_URL=postgresql://username:password@localhost:5432/todolist_db
```

ایجاد جداول:

```bash
python app/db/init_db.py
```

### 3. اجرای سرور

```bash
uvicorn api:app --reload
```

یا با پورت مشخص:

```bash
uvicorn api:app --reload --port 8000
```

### 4. مشاهده مستندات

پس از اجرای سرور، به آدرس‌های زیر بروید:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Database Health**: http://localhost:8000/health/db

## تست سریع

### با Swagger UI (ساده‌ترین روش)

1. به http://localhost:8000/docs بروید
2. روی `POST /api/v1/projects/` کلیک کنید
3. روی "Try it out" کلیک کنید
4. داده‌ها را وارد کنید:
   ```json
   {
     "name": "پروژه تست",
     "description": "توضیحات پروژه"
   }
   ```
5. روی "Execute" کلیک کنید
6. پاسخ را مشاهده کنید

### با curl

```bash
# ایجاد پروژه
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{"name": "پروژه تست", "description": "توضیحات"}'

# لیست پروژه‌ها
curl -X GET "http://localhost:8000/api/v1/projects/"

# ایجاد تسک
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "تسک تست",
    "project_id": 1,
    "description": "توضیحات تسک"
  }'
```

### با Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# ایجاد پروژه
response = requests.post(
    f"{BASE_URL}/projects/",
    json={"name": "پروژه تست", "description": "توضیحات"}
)
print(response.json())

# لیست پروژه‌ها
response = requests.get(f"{BASE_URL}/projects/")
print(response.json())
```

## ساختار API

### Projects Endpoints

- `POST /api/v1/projects/` - ایجاد پروژه
- `GET /api/v1/projects/` - لیست پروژه‌ها
- `GET /api/v1/projects/{id}` - دریافت پروژه
- `PUT /api/v1/projects/{id}` - به‌روزرسانی پروژه
- `DELETE /api/v1/projects/{id}` - حذف پروژه

### Tasks Endpoints

- `POST /api/v1/tasks/` - ایجاد تسک
- `GET /api/v1/tasks/` - لیست تسک‌ها
- `GET /api/v1/tasks/?project_id=1` - لیست تسک‌های یک پروژه
- `GET /api/v1/tasks/{id}` - دریافت تسک
- `PUT /api/v1/tasks/{id}` - به‌روزرسانی تسک
- `PATCH /api/v1/tasks/{id}/status` - به‌روزرسانی وضعیت
- `DELETE /api/v1/tasks/{id}` - حذف تسک

## عیب‌یابی

### خطای اتصال به دیتابیس

```
❌ Database connection failed
```

**راه حل:**
1. مطمئن شوید PostgreSQL در حال اجرا است
2. فایل `.env` را بررسی کنید
3. `DATABASE_URL` را بررسی کنید

### خطای Import

```
ModuleNotFoundError: No module named 'app'
```

**راه حل:**
```bash
# مطمئن شوید که در پوشه TodoList_project هستید
cd TodoList_project

# مطمئن شوید که وابستگی‌ها نصب شده‌اند
pip install -r requirements.txt
```

### خطای جداول

```
relation "projects" does not exist
```

**راه حل:**
```bash
python app/db/init_db.py
```

## نکات مهم

1. **مستندات خودکار**: FastAPI به صورت خودکار مستندات را از Schemaهای Pydantic تولید می‌کند
2. **اعتبارسنجی خودکار**: داده‌های ورودی به صورت خودکار بررسی می‌شوند
3. **کدهای وضعیت HTTP**: API از کدهای استاندارد HTTP استفاده می‌کند
4. **JSON Response**: همه پاسخ‌ها در فرمت JSON هستند

## منابع بیشتر

- `API_EXAMPLES.md` - مثال‌های کامل استفاده از API
- `TEST_API.md` - راهنمای تست
- `DEPENDENCY_INJECTION.md` - توضیحات Dependency Injection

