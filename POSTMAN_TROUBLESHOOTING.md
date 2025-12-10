# عیب‌یابی Postman - حل مشکل 404 Not Found

## مشکل: 404 Not Found

اگر پیام `404 Not Found` دریافت می‌کنید، احتمالاً یکی از مشکلات زیر است:

## ✅ راه حل ۱: بررسی URL

### URL اشتباه ❌
```
http://127.0.0.1:8000/projects/list_projects_api_v1_proj...
```

### URL درست ✅
```
http://localhost:8000/api/v1/projects/
```

**نکته مهم**: باید `/api/v1/` در URL باشد!

## ✅ راه حل ۲: استفاده از Collection

به جای ایجاد Request دستی، از Collection استفاده کنید:

### مراحل:

1. **Import Collection**:
   - روی دکمه **Import** (گوشه بالا سمت چپ) کلیک کنید
   - فایل `postman/TodoList_API.postman_collection.json` را انتخاب کنید
   - Import کنید

2. **استفاده از Collection**:
   - در سمت چپ، Collection "TodoList API" را پیدا کنید
   - روی **Projects** → **List Projects** کلیک کنید
   - این Request از قبل URL درست دارد

## ✅ راه حل ۳: بررسی سرور

مطمئن شوید سرور در حال اجرا است:

```bash
cd TodoList_project
uvicorn api:app --reload
```

باید پیام زیر را ببینید:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## ✅ راه حل ۴: تست Health Check

قبل از تست endpointهای دیگر، Health Check را تست کنید:

1. در Collection، به **Health Check** → **API Health** بروید
2. روی **Send** کلیک کنید
3. باید پاسخ زیر را ببینید:
   ```json
   {
     "status": "healthy",
     "message": "API is running"
   }
   ```

## 📋 لیست URLهای درست

### Health Check
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/health/db`

### Projects
- `POST http://localhost:8000/api/v1/projects/`
- `GET http://localhost:8000/api/v1/projects/`
- `GET http://localhost:8000/api/v1/projects/{id}`
- `PUT http://localhost:8000/api/v1/projects/{id}`
- `DELETE http://localhost:8000/api/v1/projects/{id}`

### Tasks
- `POST http://localhost:8000/api/v1/tasks/`
- `GET http://localhost:8000/api/v1/tasks/`
- `GET http://localhost:8000/api/v1/tasks/?project_id=1`
- `GET http://localhost:8000/api/v1/tasks/{id}`
- `PUT http://localhost:8000/api/v1/tasks/{id}`
- `PATCH http://localhost:8000/api/v1/tasks/{id}/status`
- `DELETE http://localhost:8000/api/v1/tasks/{id}`

## 🔧 مراحل تصحیح Request فعلی

اگر می‌خواهید Request فعلی را اصلاح کنید:

1. **Method**: مطمئن شوید `GET` است
2. **URL**: باید این باشد:
   ```
   http://localhost:8000/api/v1/projects/
   ```
   یا
   ```
   {{base_url}}/api/v1/projects/
   ```
   (اگر Environment را import کرده‌اید)

3. **Headers**: نیازی به Header خاصی نیست (برای GET)

4. **Body**: برای GET request، Body نباید چیزی داشته باشد

## 🎯 پیشنهاد: استفاده از Collection

بهترین روش این است که:

1. **Collection را Import کنید** (همانطور که در `POSTMAN_SETUP.md` توضیح دادم)
2. **Environment را Import کنید**
3. **از Requestهای آماده Collection استفاده کنید**

این کار از خطاهای URL جلوگیری می‌کند.

## ✅ تست سریع

بعد از Import Collection:

1. **Health Check** → **API Health** → **Send**
   - باید `200 OK` ببینید

2. **Projects** → **List Projects** → **Send**
   - باید لیست پروژه‌ها را ببینید (حتی اگر خالی باشد)

3. **Projects** → **Create Project** → **Send**
   - باید `201 Created` ببینید

## 🐛 مشکلات رایج دیگر

### Connection Refused
- سرور در حال اجرا نیست
- Port اشتباه است

### 422 Validation Error
- Body JSON اشتباه است
- فیلدهای اجباری وجود ندارد

### 500 Internal Server Error
- مشکل در دیتابیس
- جداول وجود ندارند

---

**نکته**: همیشه از Collection استفاده کنید تا از خطاهای URL جلوگیری کنید!

