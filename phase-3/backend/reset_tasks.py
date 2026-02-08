import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env")
    exit(1)

def reset_tasks_table():
    print(f"Connecting to database to reset 'task' table...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Drop task table
        print("Dropping 'task' table...")
        cur.execute('DROP TABLE IF EXISTS "task" CASCADE;')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Success! 'task' table dropped. Restart the backend to recreate it with the new schema.")

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    confirm = input("This will DELETE ALL TASKS. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        reset_tasks_table()
    else:
        print("Operation cancelled.")
