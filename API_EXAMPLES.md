# مثال‌های استفاده از API

این فایل شامل مثال‌های عملی برای استفاده از API است که معادل دستورات CLI هستند.

## مقایسه CLI و API

### ایجاد پروژه

**CLI:**
```bash
python main.py project create "پروژه جدید" "توضیحات پروژه"
```

**API (با curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "پروژه جدید",
    "description": "توضیحات پروژه"
  }'
```

**API (با Python requests):**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/projects/",
    json={
        "name": "پروژه جدید",
        "description": "توضیحات پروژه"
    }
)
print(response.json())
```

**API (با Swagger UI):**
1. به آدرس http://localhost:8000/docs بروید
2. روی `POST /api/v1/projects/` کلیک کنید
3. روی "Try it out" کلیک کنید
4. داده‌ها را وارد کنید و "Execute" را بزنید

---

### لیست پروژه‌ها

**CLI:**
```bash
python main.py project list
```

**API (با curl):**
```bash
curl -X GET "http://localhost:8000/api/v1/projects/"
```

**API (با Python):**
```python
import requests

response = requests.get("http://localhost:8000/api/v1/projects/")
projects = response.json()
for project in projects:
    print(f"ID: {project['id']}, Name: {project['name']}")
```

---

### نمایش یک پروژه

**CLI:**
```bash
python main.py project show 1
```

**API (با curl):**
```bash
curl -X GET "http://localhost:8000/api/v1/projects/1"
```

**API (با Python):**
```python
import requests

response = requests.get("http://localhost:8000/api/v1/projects/1")
project = response.json()
print(project)
```

---

### به‌روزرسانی پروژه

**CLI:**
```bash
# در CLI این قابلیت وجود ندارد، اما در API داریم!
```

**API (با curl):**
```bash
curl -X PUT "http://localhost:8000/api/v1/projects/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "نام جدید",
    "description": "توضیحات جدید"
  }'
```

**API (با Python):**
```python
import requests

response = requests.put(
    "http://localhost:8000/api/v1/projects/1",
    json={
        "name": "نام جدید",
        "description": "توضیحات جدید"
    }
)
print(response.json())
```

---

### حذف پروژه

**CLI:**
```bash
python main.py project delete 1
```

**API (با curl):**
```bash
curl -X DELETE "http://localhost:8000/api/v1/projects/1"
```

**API (با Python):**
```python
import requests

response = requests.delete("http://localhost:8000/api/v1/projects/1")
# کد 204 یعنی موفقیت‌آمیز بود
print(f"Status: {response.status_code}")
```

---

### ایجاد تسک

**CLI:**
```bash
python main.py task create "عنوان تسک" 1 "توضیحات" "2025-12-31"
```

**API (با curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "عنوان تسک",
    "project_id": 1,
    "description": "توضیحات",
    "deadline": "2025-12-31T23:59:59"
  }'
```

**API (با Python):**
```python
import requests
from datetime import datetime

response = requests.post(
    "http://localhost:8000/api/v1/tasks/",
    json={
        "title": "عنوان تسک",
        "project_id": 1,
        "description": "توضیحات",
        "deadline": "2025-12-31T23:59:59"
    }
)
print(response.json())
```

---

### لیست تسک‌ها

**CLI:**
```bash
python main.py task list          # همه تسک‌ها
python main.py task list 1        # تسک‌های پروژه 1
```

**API (با curl):**
```bash
# همه تسک‌ها
curl -X GET "http://localhost:8000/api/v1/tasks/"

# تسک‌های یک پروژه خاص
curl -X GET "http://localhost:8000/api/v1/tasks/?project_id=1"
```

**API (با Python):**
```python
import requests

# همه تسک‌ها
response = requests.get("http://localhost:8000/api/v1/tasks/")
tasks = response.json()

# تسک‌های یک پروژه
response = requests.get("http://localhost:8000/api/v1/tasks/", params={"project_id": 1})
project_tasks = response.json()
```

---

### به‌روزرسانی وضعیت تسک

**CLI:**
```bash
python main.py task update-status 1 done
```

**API (با curl):**
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"new_status": "done"}'
```

**API (با Python):**
```python
import requests

response = requests.patch(
    "http://localhost:8000/api/v1/tasks/1/status",
    json={"new_status": "done"}
)
print(response.json())
```

---

### به‌روزرسانی کامل تسک

**CLI:**
```bash
# در CLI این قابلیت وجود ندارد، اما در API داریم!
```

**API (با curl):**
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "عنوان جدید",
    "description": "توضیحات جدید",
    "status": "doing"
  }'
```

---

### حذف تسک

**CLI:**
```bash
python main.py task delete 1
```

**API (با curl):**
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

---

## مثال کامل: ایجاد پروژه و تسک

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. ایجاد پروژه
project_response = requests.post(
    f"{BASE_URL}/projects/",
    json={
        "name": "پروژه وب سایت",
        "description": "توسعه وب سایت جدید"
    }
)
project = project_response.json()
project_id = project["id"]
print(f"✅ پروژه ایجاد شد: {project['name']} (ID: {project_id})")

# 2. ایجاد تسک‌ها
tasks_data = [
    {
        "title": "طراحی UI",
        "project_id": project_id,
        "description": "طراحی رابط کاربری",
        "status": "todo"
    },
    {
        "title": "پیاده‌سازی Backend",
        "project_id": project_id,
        "description": "توسعه API",
        "status": "doing"
    }
]

for task_data in tasks_data:
    task_response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
    task = task_response.json()
    print(f"✅ تسک ایجاد شد: {task['title']} (ID: {task['id']})")

# 3. دریافت لیست تسک‌های پروژه
tasks_response = requests.get(f"{BASE_URL}/tasks/", params={"project_id": project_id})
tasks = tasks_response.json()
print(f"\n📋 تعداد تسک‌ها: {len(tasks)}")

# 4. به‌روزرسانی وضعیت یک تسک
if tasks:
    task_id = tasks[0]["id"]
    update_response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}/status",
        json={"new_status": "done"}
    )
    updated_task = update_response.json()
    print(f"✅ تسک به‌روزرسانی شد: {updated_task['title']} -> {updated_task['status']}")
```

---

## مزایای استفاده از API نسبت به CLI

1. **قابل استفاده از هر زبان برنامه‌نویسی**: Python, JavaScript, Java, C#, و...
2. **قابل استفاده در وب**: می‌توانید از frontend (React, Vue, Angular) استفاده کنید
3. **قابل استفاده در موبایل**: Android, iOS
4. **مستندسازی خودکار**: Swagger UI و ReDoc
5. **اعتبارسنجی خودکار**: Pydantic داده‌ها را بررسی می‌کند
6. **قابل استفاده از راه دور**: می‌توانید API را در سرور قرار دهید و از هر جا استفاده کنید

---

## نکات مهم

1. **Content-Type**: همیشه `Content-Type: application/json` را در header قرار دهید
2. **کدهای وضعیت HTTP**:
   - `200 OK`: موفقیت‌آمیز
   - `201 Created`: ایجاد موفق
   - `204 No Content`: حذف موفق
   - `400 Bad Request`: خطا در داده‌های ورودی
   - `404 Not Found`: مورد یافت نشد
3. **فرمت تاریخ**: برای deadline از فرمت ISO 8601 استفاده کنید: `YYYY-MM-DDTHH:MM:SS`
4. **وضعیت تسک**: فقط می‌تواند `todo`, `doing`, یا `done` باشد

