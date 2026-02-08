import requests
import os
import json

FASTAPI_URL = "http://localhost:8000"

print("--- Manual Task Listing Check ---")
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

# --- Test 1: List Tasks for the user ---
print(f"\n--- Listing tasks for user {user_id} ---")
try:
    response = requests.get(f"{FASTAPI_URL}/api/{user_id}/tasks", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Test 1 Failed: Expected 200 OK"
    print("Test 1 Passed: Tasks listed successfully.")
except Exception as e:
    print(f"Test 1 Failed: An error occurred - {e}")

# --- Test 2: List Tasks for a DIFFERENT user (should fail) ---
print(f"\n--- Listing tasks for a DIFFERENT user (expect 403 Forbidden) ---")
other_user_id = input("Enter a DIFFERENT user ID (or leave blank to skip): ")
if other_user_id:
    try:
        response = requests.get(f"{FASTAPI_URL}/api/{other_user_id}/tasks", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 403, "Test 2 Failed: Expected 403 Forbidden"
        print("Test 2 Passed: Correctly denied access to other user's tasks.")
    except Exception as e:
        print(f"Test 2 Failed: An error occurred - {e}")
