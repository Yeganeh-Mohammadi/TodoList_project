import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

print("Loading .env ...")
load_dotenv()
print("Loaded.")

database_url = os.getenv("DATABASE_URL")
print("DATABASE_URL =", database_url)

try:
    engine = create_engine(database_url)
    conn = engine.connect()
    print("CONNECTED SUCCESSFULLY ✔")
    conn.close()
except Exception as e:
    print("ERROR:", e)
