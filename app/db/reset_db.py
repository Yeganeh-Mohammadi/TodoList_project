"""
Reset database: Drop and recreate all tables with Integer IDs
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.db.base import Base
from app.models.project import Project  # noqa: F401
from app.models.task import Task  # noqa: F401


def reset_database():
    """
    Drop all existing tables and recreate them with Integer IDs.
    WARNING: This will delete all existing data!
    """
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set. Please set it in .env or the environment.")

    engine = create_engine(database_url)
    
    print("Dropping existing tables and sequences...")
    with engine.begin() as conn:
        # Drop tables in correct order (tasks first due to foreign key)
        # CASCADE will also drop sequences and constraints
        conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS projects CASCADE"))
        
        # Drop sequences if they exist (PostgreSQL sequences)
        conn.execute(text("DROP SEQUENCE IF EXISTS projects_id_seq CASCADE"))
        conn.execute(text("DROP SEQUENCE IF EXISTS tasks_id_seq CASCADE"))
    
    print("Creating new tables with Integer IDs...")
    Base.metadata.create_all(bind=engine)
    
    # Verify tables were created correctly
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'projects' AND column_name = 'id'
        """))
        row = result.fetchone()
        if row:
            print(f"✓ Projects table: id column type = {row[1]}")
        
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'tasks' AND column_name = 'id'
        """))
        row = result.fetchone()
        if row:
            print(f"✓ Tasks table: id column type = {row[1]}")
    
    print("✓ Database reset successfully!")
    print("✓ Tables created with Integer autoincrement IDs starting from 1")


if __name__ == "__main__":
    reset_database()

