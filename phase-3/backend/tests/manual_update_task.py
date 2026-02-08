import requests
import os
import json

FASTAPI_URL = "http://localhost:8000"

print("--- Manual Task Update Check ---")
print("1. Ensure FastAPI backend is running at:", FASTAPI_URL)
print("2. Ensure you have an AUTH_TOKEN from a logged-in user.")
print("3. Ensure tasks exist for that user (use manual_create_task.py first).")

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

task_id = input("Enter the ID of the task to update: ")
if not task_id:
    print("No task ID entered. Exiting.")
    exit()

update_title = input("Enter new title (leave blank for no change): ")
update_description = input("Enter new description (leave blank for no change): ")
update_completed_str = input("Mark as completed? (true/false, leave blank for no change): ")

task_data = {}
if update_title:
    task_data["title"] = update_title
if update_description:
    task_data["description"] = update_description
if update_completed_str:
    task_data["is_completed"] = update_completed_str.lower() == "true"

if not task_data:
    print("No update data provided. Exiting.")
    exit()

# --- Test 1: Update Task ---
print(f"\n--- Updating task {task_id} for user {user_id} ---")
try:
    response = requests.patch(f"{FASTAPI_URL}/api/{user_id}/tasks/{task_id}", headers=headers, data=json.dumps(task_data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Test 1 Failed: Expected 200 OK"
    print("Test 1 Passed: Task updated successfully.")
except Exception as e:
    print(f"Test 1 Failed: An error occurred - {e}")

# --- Test 2: Try to update a non-existent task or task of another user (should fail) ---
print(f"\n--- Trying to update a task with an invalid ID or other user's ID ---")
invalid_task_id = "00000000-0000-0000-0000-000000000000" # Example invalid UUID
try:
    response = requests.patch(f"{FASTAPI_URL}/api/{user_id}/tasks/{invalid_task_id}", headers=headers, data=json.dumps({"title": "Invalid update"}))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 404, "Test 2 Failed: Expected 404 Not Found"
    print("Test 2 Passed: Correctly denied update to non-existent task.")
except Exception as e:
    print(f"Test 2 Failed: An error occurred - {e}")
