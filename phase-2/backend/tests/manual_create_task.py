import requests
import os
import json

FASTAPI_URL = "http://localhost:8000"

print("--- Manual Task Creation Check ---")
print("1. Ensure FastAPI backend is running at:", FASTAPI_URL)
print("2. Ensure you have an AUTH_TOKEN from a logged-in user.")

AUTH_TOKEN = input("Enter JWT Token: ")

if not AUTH_TOKEN:
    print("No token entered. Exiting.")
    exit()

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

user_id = input("Enter the user ID from the JWT payload (e.g., 'sub' claim): ")

if not user_id:
    print("No user ID entered. Exiting.")
    exit()

task_title = input("Enter task title: ")
task_description = input("Enter task description (optional): ")

task_data = {
    "title": task_title,
    "description": task_description if task_description else None,
    "is_completed": False
}

# --- Test 1: Create Task ---
print(f"\n--- Creating task for user {user_id} ---")
try:
    response = requests.post(f"{FASTAPI_URL}/api/{user_id}/tasks", headers=headers, data=json.dumps(task_data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201, "Test 1 Failed: Expected 201 Created"
    print("Test 1 Passed: Task created successfully.")
except Exception as e:
    print(f"Test 1 Failed: An error occurred - {e}")
