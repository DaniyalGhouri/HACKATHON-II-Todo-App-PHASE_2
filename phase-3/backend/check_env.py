from dotenv import load_dotenv
import os

# Explicitly load .env file from the current directory
load_dotenv(dotenv_path=".env")

better_auth_secret = os.getenv("BETTER_AUTH_SECRET")
database_url = os.getenv("DATABASE_URL")

print(f"BETTER_AUTH_SECRET: {better_auth_secret}")
print(f"DATABASE_URL: {database_url}")
