# راهنمای تست API

## مراحل تست

### 1. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 2. اجرای سرور FastAPI
```bash
uvicorn api:app --reload
```

یا با پورت مشخص:
```bash
uvicorn api:app --reload --port 8000
```

### 3. دسترسی به مستندات API

پس از اجرای سرور، می‌توانید از طریق مرورگر به آدرس‌های زیر دسترسی داشته باشید:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### 4. تست Endpointها

#### تست با curl:

**ایجاد پروژه:**
```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{"name": "پروژه تست", "description": "توضیحات پروژه"}'
```

**دریافت لیست پروژه‌ها:**
```bash
curl -X GET "http://localhost:8000/api/v1/projects/"
```

**دریافت یک پروژه:**
```bash
curl -X GET "http://localhost:8000/api/v1/projects/1"
```

**به‌روزرسانی پروژه:**
```bash
curl -X PUT "http://localhost:8000/api/v1/projects/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "پروژه به‌روز شده", "description": "توضیحات جدید"}'
```

**حذف پروژه:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/projects/1"
```

**ایجاد تسک:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "تسک تست",
    "project_id": 1,
    "description": "توضیحات تسک",
    "deadline": "2025-12-31T23:59:59"
  }'
```

**دریافت لیست تسک‌ها:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/"
```

**دریافت تسک‌های یک پروژه:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?project_id=1"
```

**به‌روزرسانی وضعیت تسک:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"new_status": "done"}'
```

#### تست با Python (requests):

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# ایجاد پروژه
response = requests.post(
    f"{BASE_URL}/projects/",
    json={"name": "پروژه تست", "description": "توضیحات"}
)
print(response.json())

# دریافت لیست پروژه‌ها
response = requests.get(f"{BASE_URL}/projects/")
print(response.json())

# ایجاد تسک
response = requests.post(
    f"{BASE_URL}/tasks/",
    json={
        "title": "تسک تست",
        "project_id": 1,
        "description": "توضیحات تسک"
    }
)
print(response.json())
```

### 5. اجرای تست خودکار

```bash
python test_api.py
```

## نکات مهم

1. **دیتابیس**: مطمئن شوید که PostgreSQL در حال اجرا است و فایل `.env` با `DATABASE_URL` صحیح تنظیم شده است.

2. **جداول**: اگر جداول وجود ندارند، ابتدا آنها را ایجاد کنید:
   ```bash
   python app/db/init_db.py
   ```

3. **خطاها**: اگر خطایی رخ داد، لاگ‌های uvicorn را بررسی کنید.

## Endpointهای موجود

### Projects:
- `POST /api/v1/projects/` - ایجاد پروژه
- `GET /api/v1/projects/` - لیست پروژه‌ها
- `GET /api/v1/projects/{project_id}` - دریافت پروژه
- `PUT /api/v1/projects/{project_id}` - به‌روزرسانی پروژه
- `DELETE /api/v1/projects/{project_id}` - حذف پروژه

### Tasks:
- `POST /api/v1/tasks/` - ایجاد تسک
- `GET /api/v1/tasks/` - لیست تسک‌ها (با فیلتر اختیاری project_id)
- `GET /api/v1/tasks/{task_id}` - دریافت تسک
- `PUT /api/v1/tasks/{task_id}` - به‌روزرسانی تسک
- `PATCH /api/v1/tasks/{task_id}/status` - به‌روزرسانی وضعیت
- `DELETE /api/v1/tasks/{task_id}` - حذف تسک

