import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.db.base import Base
from app.models.project import Project  # noqa: F401
from app.models.task import Task  # noqa: F401


def create_tables():
    """
    Create PostgreSQL tables based on SQLAlchemy models using Base.metadata.
    """
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set. Please set it in .env or the environment.")

    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully using Base.metadata.")


if __name__ == "__main__":
    create_tables()

