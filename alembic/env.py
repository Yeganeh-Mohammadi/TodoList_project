# alembic/env.py (شروع فایل)
import os
import sys
from dotenv import load_dotenv # <--- جدید

# مسیر پروژه را به PATH اضافه کنید تا ایمپورت‌های داخلی کار کنند
sys.path.append(os.path.join(os.getcwd(), 'app'))

# لود کردن متغیرهای محیطی از .env
load_dotenv() 

# ایمپورت Base و Engine از پروژه شما
from app.db.base import Base # <--- حاوی MetaData مدل‌های ORM
from app.db.session import engine # <--- حاوی Engine کانفیگ شده

# ... (بقیه ایمپورت‌های پیش‌فرض Alembic)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    This uses the configured 'engine' from app.db.session.
    """
    connectable = engine  # استفاده از Engine که قبلاً در app/db/session.py کانفیگ شده است

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # (اختیاری: برای دیدن کوئری‌های اجرا شده در کنسول)
            # include_schemas=True 
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
