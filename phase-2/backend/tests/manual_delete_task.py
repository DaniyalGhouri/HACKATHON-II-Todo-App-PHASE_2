import requests
import os
import json

FASTAPI_URL = "http://localhost:8000"

print("--- Manual Task Deletion Check ---")
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

task_id = input("Enter the ID of the task to DELETE: ")
if not task_id:
    print("No task ID entered. Exiting.")
    exit()

# --- Test 1: Delete Task ---
print(f"\n--- Deleting task {task_id} for user {user_id} ---")
try:
    response = requests.delete(f"{FASTAPI_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 204, "Test 1 Failed: Expected 204 No Content"
    print("Test 1 Passed: Task deleted successfully.")
except Exception as e:
    print(f"Test 1 Failed: An error occurred - {e}")

# --- Test 2: Verify deletion by trying to get the task ---
print(f"\n--- Verifying deletion of task {task_id} ---")
try:
    response = requests.get(f"{FASTAPI_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 404, "Test 2 Failed: Expected 404 Not Found after deletion"
    print("Test 2 Passed: Task is no longer found.")
except Exception as e:
    print(f"Test 2 Failed: An error occurred - {e}")
