# فاز ۴: تست API با Postman

این فاز شامل تنظیم و استفاده از Postman برای تست کامل API است.

## 📋 اهداف فاز ۴

1. ✅ ایجاد Workspace در Postman
2. ✅ Import کردن Collection
3. ✅ Import کردن Environment
4. ✅ تست تمام Endpointها
5. ✅ استفاده از Variables
6. ✅ نوشتن Tests

## 📁 فایل‌های ایجاد شده

```
TodoList_project/
├── postman/
│   ├── TodoList_API.postman_collection.json    # Collection کامل
│   └── TodoList_API.postman_environment.json   # Environment variables
├── POSTMAN_SETUP.md                            # راهنمای کامل تنظیم
└── PHASE4_POSTMAN.md                           # این فایل
```

## 🚀 مراحل تنظیم

### گام ۱: نصب Postman

1. Postman را دانلود و نصب کنید: https://www.postman.com/downloads/
2. Postman را باز کنید

### گام ۲: ایجاد Workspace

#### روش ۱: از نوار بالای Postman

1. در نوار بالای برنامه روی **Workspaces** کلیک کنید
2. از فهرست بازشده، **Create Workspace** را انتخاب کنید
3. یک نام برای Workspace خود وارد کنید (مثلاً: `TodoList API`)
4. نوع آن را روی **Personal** بگذارید
5. روی دکمه **Create Workspace** کلیک کنید

#### روش ۲: از منوی Workspace

1. روی آیکون Workspace در سمت چپ بالای صفحه کلیک کنید
2. روی **Create Workspace** کلیک کنید
3. نام و نوع را وارد کنید
4. **Create Workspace** را بزنید

### گام ۳: Import کردن Collection

1. در Postman، روی دکمه **Import** (در گوشه بالا سمت چپ) کلیک کنید
2. روی تب **File** کلیک کنید
3. فایل `postman/TodoList_API.postman_collection.json` را انتخاب کنید
4. روی **Import** کلیک کنید

### گام ۴: Import کردن Environment

1. روی دکمه **Import** کلیک کنید
2. فایل `postman/TodoList_API.postman_environment.json` را انتخاب کنید
3. روی **Import** کلیک کنید

### گام ۵: انتخاب Environment

1. در گوشه بالا سمت راست، روی dropdown **Environments** کلیک کنید
2. **TodoList API - Local** را انتخاب کنید

## ✅ تست API

### ۱. Health Check

**API Health**:
- Method: `GET`
- URL: `{{base_url}}/health`
- Expected: `200 OK` با پیام "API is running"

**Database Health**:
- Method: `GET`
- URL: `{{base_url}}/health/db`
- Expected: `200 OK` با پیام "Database connection is OK"

### ۲. Projects

**Create Project**:
```json
{
    "name": "پروژه تست",
    "description": "توضیحات پروژه"
}
```
- Expected: `201 Created`
- Response شامل `id` پروژه

**List Projects**:
- Expected: `200 OK`
- Response شامل لیست پروژه‌ها

**Get Project**:
- URL: `{{base_url}}/api/v1/projects/{{project_id}}`
- Expected: `200 OK`

**Update Project**:
```json
{
    "name": "نام جدید",
    "description": "توضیحات جدید"
}
```
- Expected: `200 OK`

**Delete Project**:
- Expected: `204 No Content`

### ۳. Tasks

**Create Task**:
```json
{
    "title": "تسک تست",
    "project_id": {{project_id}},
    "description": "توضیحات تسک",
    "deadline": "2025-12-31T23:59:59"
}
```
- Expected: `201 Created`

**List Tasks**:
- URL: `{{base_url}}/api/v1/tasks/`
- Expected: `200 OK`

**List Tasks by Project**:
- URL: `{{base_url}}/api/v1/tasks/?project_id={{project_id}}`
- Expected: `200 OK`

**Update Task Status**:
```json
{
    "new_status": "done"
}
```
- Expected: `200 OK`
- `closed_at` باید تنظیم شود

## 🔧 استفاده از Variables

### Environment Variables

- `base_url`: `http://localhost:8000`
- `project_id`: `1`
- `task_id`: `1`

### نحوه استفاده

در URL:
```
{{base_url}}/api/v1/projects/{{project_id}}
```

در Body:
```json
{
    "project_id": {{project_id}}
}
```

## 📝 نوشتن Tests

### مثال: Test برای Create Project

در **Tests** tab:
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response has project data", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
});

// ذخیره project_id
if (pm.response.code === 201) {
    const response = pm.response.json();
    pm.environment.set("project_id", response.id);
}
```

### مثال: Test برای List Projects

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is an array", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

## 🎯 Workflow پیشنهادی

### ۱. Setup
1. Health Check را تست کنید
2. Database Health را تست کنید

### ۲. Create
1. یک پروژه ایجاد کنید
2. `project_id` را ذخیره کنید
3. یک تسک برای آن پروژه ایجاد کنید
4. `task_id` را ذخیره کنید

### ۳. Read
1. لیست پروژه‌ها را دریافت کنید
2. پروژه خاص را دریافت کنید
3. لیست تسک‌ها را دریافت کنید
4. تسک خاص را دریافت کنید

### ۴. Update
1. پروژه را به‌روزرسانی کنید
2. تسک را به‌روزرسانی کنید
3. وضعیت تسک را تغییر دهید

### ۵. Delete
1. تسک را حذف کنید
2. پروژه را حذف کنید (تمام تسک‌ها نیز حذف می‌شوند)

## 📊 Collection Structure

```
TodoList API
├── Health Check
│   ├── API Health
│   └── Database Health
├── Projects
│   ├── Create Project
│   ├── List Projects
│   ├── Get Project
│   ├── Update Project
│   └── Delete Project
└── Tasks
    ├── Create Task
    ├── List All Tasks
    ├── List Tasks by Project
    ├── Get Task
    ├── Update Task
    ├── Update Task Status
    └── Delete Task
```

## 🐛 عیب‌یابی

### Connection Refused
- مطمئن شوید سرور در حال اجرا است
- `base_url` را بررسی کنید

### 404 Not Found
- URL را بررسی کنید
- Environment variables را بررسی کنید

### 422 Validation Error
- Body را بررسی کنید
- `Content-Type: application/json` را بررسی کنید

## 📚 منابع

- `POSTMAN_SETUP.md` - راهنمای کامل تنظیم
- `API_DOCUMENTATION.md` - مستندات API
- `API_EXAMPLES.md` - مثال‌های استفاده

---

**نکته**: این Collection برای تست محلی طراحی شده است. برای production، Environment را تغییر دهید.

