import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
print(f"Testing connection with DATABASE_URL: {db_url}")

try:
    conn = psycopg2.connect(db_url)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
