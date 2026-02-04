import requests
import os
import json

# Ensure your FastAPI server is running (e.g., uvicorn src.main:app --reload)
# Ensure your Next.js frontend is running (e.g., npm run dev)

FASTAPI_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# --- Helper to get a token (requires manual signup/login via frontend first) ---
# In a real test, you'd automate this, but for manual check, assume a user exists
# and we can simulate getting a token. This part requires manual interaction
# or a more advanced setup to extract the token from browser storage.
# For simplicity, you can manually copy a token after logging in via the frontend
# and paste it here.
#
# Example of how you might *try* to get it (won't work directly due to browser security):
# You'd need a browser automation tool like Playwright or Selenium to extract it.
#
# For now, placeholder:
# AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # REPLACE WITH YOUR ACTUAL JWT TOKEN


print("--- Manual Authentication Check ---")
print("1. Ensure FastAPI backend is running at:", FASTAPI_URL)
print("2. Ensure Next.js frontend is running at:", FRONTEND_URL)
print("3. Manually sign up and log in via the frontend.")
print("4. IMPORTANT: Copy the JWT token from your browser's Local Storage or Cookie (if HttpOnly not set).")
print("   Paste it below in the AUTH_TOKEN variable.")
print("\n--- Waiting for manual token input ---")

# Manual input for the token
AUTH_TOKEN = input("Enter JWT Token (copy from browser after login): ")

if not AUTH_TOKEN:
    print("No token entered. Exiting.")
    exit()

print(f"\nUsing token: {AUTH_TOKEN[:30]}...")

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

# --- Test 1: Access protected route with valid token ---
print("\n--- Testing protected route with VALID token ---")
try:
    response = requests.get(f"{FASTAPI_URL}/api/protected", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Test 1 Failed: Expected 200 OK"
    print("Test 1 Passed: Successfully accessed protected route.")
except Exception as e:
    print(f"Test 1 Failed: An error occurred - {e}")

# --- Test 2: Access protected route WITHOUT token ---
print("\n--- Testing protected route WITHOUT token ---")
try:
    response = requests.get(f"{FASTAPI_URL}/api/protected")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 401, "Test 2 Failed: Expected 401 Unauthorized"
    print("Test 2 Passed: Correctly denied access without token.")
except Exception as e:
    print(f"Test 2 Failed: An error occurred - {e}")

# --- Test 3: Access protected route with INVALID/EXPIRED token (manual step) ---
print("\n--- Test 3: Manually test with an invalid/expired token ---")
print("   (Modify AUTH_TOKEN above with an invalid one and re-run, or wait for it to expire)")
print("   Expected: 401 Unauthorized")
