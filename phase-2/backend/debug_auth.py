import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load env variables
load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env")
    exit(1)

def debug_auth_db():
    print(f"Connecting to database...")
    print(f"URL (masked): {DATABASE_URL[:20]}...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 1. Check Tables
        print("\n--- Tables in DB ---")
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cur.fetchall()
        for t in tables:
            print(f"- {t[0]}")

        # 2. Check Session Table Content
        if any(t[0] == 'session' for t in tables):
            print("\n--- Content of 'session' table ---")
            # Select all columns
            cur.execute('SELECT * FROM "session"')
            rows = cur.fetchall()
            
            # Get column names
            col_names = [desc[0] for desc in cur.description]
            print(f"Columns: {col_names}")
            
            if not rows:
                print("Table is EMPTY.")
            else:
                for row in rows:
                    print(f"Row: {row}")
        else:
            print("\nERROR: 'session' table not found!")

        conn.close()

    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    debug_auth_db()
