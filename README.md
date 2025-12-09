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

##  معماری

### Repository Pattern

Repository ها مسئول دسترسی به داده هستند و از SQLAlchemy Session استفاده می‌کنند.

### Service Layer

Service ها شامل Business Logic هستند و از Repository ها استفاده می‌کنند (Dependency Injection).

### CLI Commands

دستورات CLI از Service Layer استفاده می‌کنند و رابط کاربری را فراهم می‌کنند.
