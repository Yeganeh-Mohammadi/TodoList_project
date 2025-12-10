# راهنمای تنظیم Postman برای TodoList API

این راهنما به شما کمک می‌کند تا Postman را برای تست API تنظیم کنید.

## پیش‌نیازها

1. **Postman** نصب شده باشد ([دانلود Postman](https://www.postman.com/downloads/))
2. **API سرور** در حال اجرا باشد (`uvicorn api:app --reload`)

## گام ۱: ایجاد Workspace

### روش ۱: از نوار بالای Postman

1. در نوار بالای برنامه روی **Workspaces** کلیک کنید
2. از فهرست بازشده، **Create Workspace** را انتخاب کنید
3. یک نام برای Workspace خود وارد کنید (مثلاً: `TodoList API`)
4. نوع آن را روی **Personal** بگذارید
5. روی دکمه **Create Workspace** کلیک کنید

### روش ۲: از منوی Workspace

1. روی آیکون Workspace در سمت چپ بالای صفحه کلیک کنید
2. روی **Create Workspace** کلیک کنید
3. نام و نوع را وارد کنید
4. **Create Workspace** را بزنید

## گام ۲: Import کردن Collection

### روش ۱: Import از فایل

1. در Postman، روی دکمه **Import** (در گوشه بالا سمت چپ) کلیک کنید
2. روی تب **File** کلیک کنید
3. فایل `postman/TodoList_API.postman_collection.json` را انتخاب کنید
4. روی **Import** کلیک کنید

### روش ۲: Drag & Drop

1. فایل `TodoList_API.postman_collection.json` را باز کنید
2. آن را به پنجره Postman بکشید و رها کنید
3. روی **Import** کلیک کنید

## گام ۳: Import کردن Environment

1. روی دکمه **Import** کلیک کنید
2. فایل `postman/TodoList_API.postman_environment.json` را انتخاب کنید
3. روی **Import** کلیک کنید

## گام ۴: انتخاب Environment

1. در گوشه بالا سمت راست، روی dropdown **Environments** کلیک کنید
2. **TodoList API - Local** را انتخاب کنید

## گام ۵: تست API

### ۱. بررسی Health Check

1. در Collection، به **Health Check** بروید
2. **API Health** را انتخاب کنید
3. روی **Send** کلیک کنید
4. باید پاسخ زیر را ببینید:
   ```json
   {
     "status": "healthy",
     "message": "API is running"
   }
   ```

### ۲. ایجاد پروژه

1. به **Projects** → **Create Project** بروید
2. در Body، داده‌ها را ویرایش کنید:
   ```json
   {
     "name": "پروژه تست",
     "description": "توضیحات پروژه"
   }
   ```
3. روی **Send** کلیک کنید
4. پاسخ را مشاهده کنید و `id` پروژه را یادداشت کنید

### ۳. ایجاد تسک

1. به **Tasks** → **Create Task** بروید
2. در Body، `project_id` را با ID پروژه ایجاد شده جایگزین کنید:
   ```json
   {
     "title": "تسک تست",
     "project_id": 1,
     "description": "توضیحات تسک",
     "deadline": "2025-12-31T23:59:59"
   }
   ```
3. روی **Send** کلیک کنید

### ۴. استفاده از Variables

برای استفاده از متغیرها:

1. در Environment، `project_id` و `task_id` را تنظیم کنید
2. در Collection، از `{{project_id}}` و `{{task_id}}` استفاده کنید
3. Postman به صورت خودکار این متغیرها را جایگزین می‌کند

## ساختار Collection

### Health Check
- API Health
- Database Health

### Projects
- Create Project
- List Projects
- Get Project
- Update Project
- Delete Project

### Tasks
- Create Task
- List All Tasks
- List Tasks by Project
- Get Task
- Update Task
- Update Task Status
- Delete Task

## Variables موجود

### Environment Variables

- `base_url`: آدرس پایه API (پیش‌فرض: `http://localhost:8000`)
- `project_id`: شناسه پروژه (پیش‌فرض: `1`)
- `task_id`: شناسه تسک (پیش‌فرض: `1`)

### نحوه استفاده

در URL یا Body می‌توانید از متغیرها استفاده کنید:
```
{{base_url}}/api/v1/projects/{{project_id}}
```

## نکات مهم

### ۱. تغییر Port

اگر سرور روی پورت دیگری اجرا می‌شود:

1. در Environment، `base_url` را ویرایش کنید
2. مثلاً: `http://localhost:8080`

### ۲. ذخیره Response

برای ذخیره `id` از Response:

1. در **Tests** tab، کد زیر را اضافه کنید:
   ```javascript
   if (pm.response.code === 201) {
       const response = pm.response.json();
       pm.environment.set("project_id", response.id);
   }
   ```

### ۳. Pre-request Scripts

برای تنظیم خودکار متغیرها:

1. در **Pre-request Script** tab، کد زیر را اضافه کنید:
   ```javascript
   // تنظیم خودکار project_id
   pm.environment.set("project_id", "1");
   ```

### ۴. Tests

برای تست خودکار Response:

1. در **Tests** tab، کد زیر را اضافه کنید:
   ```javascript
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   
   pm.test("Response has data", function () {
       const jsonData = pm.response.json();
       pm.expect(jsonData).to.have.property('id');
   });
   ```

## مثال کامل: Workflow

### ۱. ایجاد پروژه و ذخیره ID

**Create Project** → **Tests**:
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("project_id", response.id);
    console.log("Project ID saved:", response.id);
}
```

### ۲. ایجاد تسک با استفاده از project_id

**Create Task** → Body:
```json
{
    "title": "تسک تست",
    "project_id": {{project_id}},
    "description": "توضیحات"
}
```

### ۳. ذخیره task_id

**Create Task** → **Tests**:
```javascript
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("task_id", response.id);
    console.log("Task ID saved:", response.id);
}
```

## Export و Share

### Export Collection

1. روی Collection کلیک راست کنید
2. **Export** را انتخاب کنید
3. فرمت را انتخاب کنید (v2.1 توصیه می‌شود)
4. فایل را ذخیره کنید

### Share Collection

1. روی Collection کلیک راست کنید
2. **Share** را انتخاب کنید
3. روش share را انتخاب کنید (Link, Team, و...)

## عیب‌یابی

### خطای Connection Refused

**مشکل**: `Error: connect ECONNREFUSED`

**راه حل**:
1. مطمئن شوید سرور در حال اجرا است
2. `base_url` را در Environment بررسی کنید
3. Port را بررسی کنید

### خطای 404 Not Found

**مشکل**: `404 Not Found`

**راه حل**:
1. URL را بررسی کنید
2. مطمئن شوید که `/api/v1` در URL وجود دارد
3. Environment variables را بررسی کنید

### خطای 422 Validation Error

**مشکل**: `422 Unprocessable Entity`

**راه حل**:
1. Body را بررسی کنید
2. مطمئن شوید که `Content-Type: application/json` در Header است
3. فرمت JSON را بررسی کنید

## منابع بیشتر

- [Postman Documentation](https://learning.postman.com/docs/)
- [Postman Variables](https://learning.postman.com/docs/sending-requests/variables/)
- [Postman Tests](https://learning.postman.com/docs/writing-scripts/test-scripts/)

---

**نکته**: این Collection برای تست محلی طراحی شده است. برای production، Environment را تغییر دهید.

