import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing API Key: {api_key[:10]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": "Hello, are you working?"}]
    }]
}

response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
