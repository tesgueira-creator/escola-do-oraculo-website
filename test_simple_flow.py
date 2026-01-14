#!/usr/bin/env python3
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
test_email = f"test_{timestamp}@test.local"

# Test 1: Health
r = requests.get(f"{BASE_URL}/health", timeout=5)
print(f"Health: {r.status_code}")

# Test 2: Register
data = {"email": test_email, "password": "TestPassword123!", "full_name": "Test User"}
r = requests.post(f"{BASE_URL}/auth/register", json=data, timeout=10)
print(f"Register: {r.status_code}")
if r.status_code != 200 and r.status_code != 201:
    print(json.dumps(r.json(), indent=2))
else:
    user = r.json()
    print(f"User ID: {user.get('id')}")

    # Test 3: Login
    login_data = {"email": test_email, "password": "TestPassword123!"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
    print(f"Login: {r.status_code}")
    if r.status_code == 200:
        token = r.json().get("access_token")

        # Test 4: Get user
        r = requests.get(
            f"{BASE_URL}/user/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        print(f"Get User: {r.status_code}")
        print("SUCCESS!")
    else:
        print(f"Login failed: {r.json()}")
