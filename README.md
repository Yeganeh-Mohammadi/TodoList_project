# TodoList Project - Phase 2 (RDB Version)

یک پروژه TodoList کامل با استفاده از PostgreSQL، SQLAlchemy، و معماری Repository Pattern.

## ویژگی‌ها

- ✅ استفاده از PostgreSQL و Docker
- ✅ مدل‌سازی Project و Task با SQLAlchemy
- ✅ روابط یک‌به‌چند بین Project و Task
- ✅ Repository Pattern کامل
- ✅ Service Layer کامل
- ✅ CLI با تمام دستورات
- ✅ دستور HELP
- ✅ Scheduled Command برای بستن تسک‌های overdue
- ✅ Migration با Alembic
- ✅ ساختار پوشه دقیق و منظم

## پیش‌نیازها

- Python 3.14+
- Docker و Docker Compose
- PostgreSQL (یا استفاده از Docker)

## نصب و راه‌اندازی

### 1. کلون کردن پروژه

```bash
git clone <repository-url>
cd TodoList_project
```

### 2. راه‌اندازی Docker و PostgreSQL

```bash
# از پوشه root پروژه
docker-compose up -d
```

این دستور یک container PostgreSQL را راه‌اندازی می‌کند.

### 3. تنظیم فایل .env

فایل `env.example` را کپی کرده و به `.env` تغییر نام دهید:

```bash
cp env.example .env
```

سپس مقادیر را در `.env` تنظیم کنید:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todolist_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todolist_db
```

### 4. نصب وابستگی‌ها

```bash
# با pip
pip install -r requirements.txt

# یا با poetry
poetry install
```

### 5. اجرای Migration

```bash
cd TodoList_project
alembic upgrade head
```

یا برای ایجاد جداول بدون migration:

```bash
python -m app.db.init_db
```

## ساختار پروژه

```
TodoList_project/
├── app/
│   ├── cli/              # CLI Console
│   ├── commands/         # دستورات CLI
│   │   ├── project.py    # دستورات پروژه
│   │   ├── task.py       # دستورات تسک
│   │   ├── help.py       # دستور help
│   │   └── autoclose_overdue.py  # بستن خودکار تسک‌های overdue
│   ├── db/               # تنظیمات دیتابیس
│   │   ├── base.py       # Base برای SQLAlchemy
│   │   ├── session.py    # Session Management
│   │   └── init_db.py    # ایجاد جداول
│   ├── models/           # مدل‌های SQLAlchemy
│   │   ├── project.py    # مدل Project
│   │   └── task.py       # مدل Task
│   ├── repositories/     # Repository Pattern
│   │   ├── base_repository.py
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   └── services/         # Service Layer
│       ├── project_service.py
│       └── task_service.py
├── alembic/              # Migration Files
│   └── versions/
├── alembic.ini           # تنظیمات Alembic
├── main.py               # Entry Point
├── requirements.txt      # وابستگی‌ها
└── env.example           # نمونه فایل .env
```

## استفاده از CLI

### دستورات Project

```bash
# ایجاد پروژه جدید
python main.py project create <name> [description]

# لیست تمام پروژه‌ها
python main.py project list

# نمایش جزئیات پروژه
python main.py project show <project_id>

# حذف پروژه
python main.py project delete <project_id>
```

### دستورات Task

```bash
# ایجاد تسک جدید
python main.py task create <title> <project_id> [description] [deadline]
# مثال: python main.py task create "Buy groceries" 1 "Buy milk and bread" "2025-12-10"

# لیست تمام تسک‌ها (یا تسک‌های یک پروژه)
python main.py task list [project_id]

# به‌روزرسانی وضعیت تسک
python main.py task update-status <task_id> <status>
# status می‌تواند: todo, doing, done

# تنظیم deadline برای تسک
python main.py task schedule <task_id> <deadline>
# deadline format: YYYY-MM-DD or YYYY-MM-DD HH:MM

# نمایش جزئیات تسک
python main.py task show <task_id>

# حذف تسک
python main.py task delete <task_id>
```

### دستورات دیگر

```bash
# نمایش راهنما
python main.py help

# بستن خودکار تسک‌های overdue
python main.py tasks:autoclose-overdue

# اجرای CLI تست
python main.py run:cli
```

## Migration

### ایجاد Migration جدید

```bash
alembic revision -m "description"
```

### اجرای Migration

```bash
# اجرای تمام migration‌ها
alembic upgrade head

# بازگشت به یک revision خاص
alembic downgrade <revision_id>
```

### Migration‌های موجود

1. `f7e5bcaaf966` - ایجاد جداول اولیه projects و tasks
2. `a1b2c3d4e5f6` - اضافه کردن ستون closed_at به جدول tasks

## جداول دیتابیس

### جدول `projects`

- `id` (Integer, Primary Key)
- `name` (String(100), Unique, Not Null)
- `description` (Text)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### جدول `tasks`

- `id` (Integer, Primary Key)
- `title` (String(200), Not Null)
- `description` (Text)
- `deadline` (DateTime, Nullable)
- `status` (Enum: TODO, DOING, DONE)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `closed_at` (DateTime, Nullable)
- `project_id` (Integer, Foreign Key → projects.id, CASCADE DELETE)

## معماری

### Repository Pattern

Repository ها مسئول دسترسی به داده هستند و از SQLAlchemy Session استفاده می‌کنند.

### Service Layer

Service ها شامل Business Logic هستند و از Repository ها استفاده می‌کنند (Dependency Injection).

### CLI Commands

دستورات CLI از Service Layer استفاده می‌کنند و رابط کاربری را فراهم می‌کنند.

## تست

برای تست دستورات:

```bash
# اجرای CLI تست
python main.py run:cli
```

## مشاهده جداول در VS Code

برای مشاهده جداول دیتابیس در VS Code:

1. نصب Extension: "PostgreSQL" یا "SQLTools"
2. اتصال به دیتابیس با استفاده از اطلاعات `.env`
3. مشاهده جداول `projects` و `tasks`

یا استفاده از `init_db.py` برای مشاهده ساختار جداول:

```bash
python -m app.db.init_db
```

## مشکلات رایج

### خطای اتصال به دیتابیس

- مطمئن شوید Docker container در حال اجرا است: `docker-compose ps`
- بررسی کنید `.env` به درستی تنظیم شده باشد
- بررسی کنید پورت 5432 در دسترس است

### خطای Migration

- مطمئن شوید Alembic به درستی کانفیگ شده است
- بررسی کنید `alembic.ini` و `alembic/env.py` درست هستند

## مجوز

MIT License
