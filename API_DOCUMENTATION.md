# مستندات API - TodoList Project

این مستندات به صورت خودکار از Schemaهای Pydantic و docstringهای endpointها تولید شده است.

## دسترسی به مستندات

پس از اجرای سرور، می‌توانید از طریق مرورگر به مستندات دسترسی داشته باشید:

### Swagger UI
**آدرس**: http://localhost:8000/docs

- رابط کاربری تعاملی
- امکان تست مستقیم endpointها
- نمایش Schemaها و مثال‌ها
- امکان ارسال درخواست و مشاهده پاسخ

### ReDoc
**آدرس**: http://localhost:8000/redoc

- مستندات زیبا و خوانا
- مناسب برای خواندن و درک API
- نمایش کامل Schemaها

### OpenAPI Schema (JSON)
**آدرس**: http://localhost:8000/openapi.json

- Schema کامل API در فرمت JSON
- قابل استفاده برای تولید کد client
- قابل import در Postman یا ابزارهای دیگر

## ساختار API

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
در حال حاضر API بدون authentication است. (برای production باید اضافه شود)

## Endpoints

### Projects

#### ایجاد پروژه
```http
POST /api/v1/projects/
Content-Type: application/json

{
  "name": "string (required, min: 1, max: 100)",
  "description": "string (optional)"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "پروژه تست",
  "description": "توضیحات",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

#### لیست پروژه‌ها
```http
GET /api/v1/projects/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "پروژه 1",
    "description": "توضیحات",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

#### دریافت پروژه
```http
GET /api/v1/projects/{project_id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "پروژه تست",
  "description": "توضیحات",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Project with ID 1 not found."
}
```

#### به‌روزرسانی پروژه
```http
PUT /api/v1/projects/{project_id}
Content-Type: application/json

{
  "name": "string (optional)",
  "description": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "نام جدید",
  "description": "توضیحات جدید",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T01:00:00"
}
```

#### حذف پروژه
```http
DELETE /api/v1/projects/{project_id}
```

**Response (204 No Content)**

**نکته**: با حذف پروژه، تمام تسک‌های مرتبط نیز حذف می‌شوند (Cascade Delete)

### Tasks

#### ایجاد تسک
```http
POST /api/v1/tasks/
Content-Type: application/json

{
  "title": "string (required, min: 1, max: 200)",
  "project_id": "integer (required, > 0)",
  "description": "string (optional)",
  "deadline": "datetime (optional, ISO 8601 format)"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "تسک تست",
  "description": "توضیحات",
  "project_id": 1,
  "status": "todo",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "closed_at": null
}
```

#### لیست تسک‌ها
```http
GET /api/v1/tasks/
GET /api/v1/tasks/?project_id=1
```

**Query Parameters:**
- `project_id` (optional): فیلتر بر اساس پروژه

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "تسک تست",
    "description": "توضیحات",
    "project_id": 1,
    "status": "todo",
    "deadline": "2025-12-31T23:59:59",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00",
    "closed_at": null
  }
]
```

#### دریافت تسک
```http
GET /api/v1/tasks/{task_id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "تسک تست",
  "description": "توضیحات",
  "project_id": 1,
  "status": "todo",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "closed_at": null
}
```

#### به‌روزرسانی تسک
```http
PUT /api/v1/tasks/{task_id}
Content-Type: application/json

{
  "title": "string (optional)",
  "description": "string (optional)",
  "deadline": "datetime (optional)",
  "status": "todo | doing | done (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "عنوان جدید",
  "description": "توضیحات جدید",
  "project_id": 1,
  "status": "doing",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T01:00:00",
  "closed_at": null
}
```

#### به‌روزرسانی وضعیت تسک
```http
PATCH /api/v1/tasks/{task_id}/status
Content-Type: application/json

{
  "new_status": "todo | doing | done"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "تسک تست",
  "description": "توضیحات",
  "project_id": 1,
  "status": "done",
  "deadline": "2025-12-31T23:59:59",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T01:00:00",
  "closed_at": "2025-01-01T01:00:00"
}
```

**نکته**: وقتی status به `done` تغییر می‌کند، `closed_at` به صورت خودکار تنظیم می‌شود.

#### حذف تسک
```http
DELETE /api/v1/tasks/{task_id}
```

**Response (204 No Content)**

### Health Check

#### بررسی سلامت API
```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### بررسی اتصال دیتابیس
```http
GET /health/db
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Database connection is OK"
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "message": "Database connection failed: ..."
}
```

## کدهای وضعیت HTTP

- `200 OK`: درخواست موفق
- `201 Created`: منبع جدید ایجاد شد
- `204 No Content`: درخواست موفق، بدون محتوا (حذف)
- `400 Bad Request`: خطا در داده‌های ورودی
- `404 Not Found`: منبع یافت نشد
- `500 Internal Server Error`: خطای سرور
- `503 Service Unavailable`: سرویس در دسترس نیست (مثلاً دیتابیس)

## اعتبارسنجی داده‌ها

API به صورت خودکار داده‌های ورودی را بررسی می‌کند:

### Project
- `name`: اجباری، حداقل 1 کاراکتر، حداکثر 100 کاراکتر
- `description`: اختیاری

### Task
- `title`: اجباری، حداقل 1 کاراکتر، حداکثر 200 کاراکتر
- `project_id`: اجباری، باید بزرگتر از 0 باشد
- `description`: اختیاری
- `deadline`: اختیاری، فرمت ISO 8601
- `status`: اختیاری، فقط `todo`, `doing`, یا `done`

## مثال‌های خطا

### خطای اعتبارسنجی
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### خطای یافت نشدن
```json
{
  "detail": "Project with ID 999 not found."
}
```

### خطای دیتابیس
```json
{
  "detail": "Database error: ..."
}
```

## نکات مهم

1. **فرمت تاریخ**: از ISO 8601 استفاده کنید: `YYYY-MM-DDTHH:MM:SS`
2. **Content-Type**: همیشه `application/json` را در header قرار دهید
3. **وضعیت تسک**: فقط می‌تواند `todo`, `doing`, یا `done` باشد
4. **Cascade Delete**: حذف پروژه، تمام تسک‌های مرتبط را نیز حذف می‌کند
5. **Auto-close**: وقتی status تسک به `done` تغییر می‌کند، `closed_at` تنظیم می‌شود

## تولید Client Code

می‌توانید از OpenAPI Schema برای تولید کد client استفاده کنید:

```bash
# دریافت Schema
curl http://localhost:8000/openapi.json > openapi.json

# استفاده با openapi-generator
openapi-generator generate -i openapi.json -g python -o ./client
```

## منابع

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

