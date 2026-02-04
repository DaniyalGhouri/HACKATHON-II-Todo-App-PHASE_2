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

def reset_auth_tables():
    print(f"Connecting to database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # List of tables to clear (Better Auth standard tables)
        # Note: We are TRUNCATING to remove data but keep structure.
        # However, if 'jwks' is the issue, we specifically target it.
        # Better Auth creates tables like 'user', 'session', 'account', 'verification', 'jwks' (if using plugins).
        
        tables = ["jwks", "session", "account", "verification"] 
        # We optionally keep 'user' if you want, but often it's cleaner to wipe all for auth reset.
        # Uncomment 'user' below to wipe users too.
        tables.append("user") 
        
        for table in tables:
            try:
                # We use quotes for safety in case of case-sensitivity or keywords
                cur.execute(f'TRUNCATE TABLE "{table}" CASCADE;')
                print(f"Cleared table: {table}")
            except psycopg2.errors.UndefinedTable:
                print(f"Table not found (skipping): {table}")
                conn.rollback() # Reset transaction
            except Exception as e:
                print(f"Error clearing {table}: {e}")
                conn.rollback()

        conn.commit()
        cur.close()
        conn.close()
        print("Success! Auth tables cleared. You can now sign up again.")

    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    confirm = input("This will DELETE ALL AUTH DATA (sessions, keys, users). Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        reset_auth_tables()
    else:
        print("Operation cancelled.")
