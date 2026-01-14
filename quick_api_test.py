#!/usr/bin/env python3
"""Quick API test to diagnose production issues"""

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://web-production-21437.up.railway.app"

print("=" * 60)
print("DIAGNÓSTICO RÁPIDO DA API")
print("=" * 60)

# Test 0: Version
print("\n0. API Version:")
try:
    r = requests.get(f"{BASE}/version", verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 1: Health
print("\n1. Health Check:")
try:
    r = requests.get(f"{BASE}/health", verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Register with SHORT password
print("\n2. Register (senha curta 'Test123!'):")
try:
    data = {
        "email": "test_short_pwd@test.local",
        "password": "Test123!",
        "full_name": "Short Pwd Test",
    }
    r = requests.post(f"{BASE}/auth/register", json=data, verify=False, timeout=15)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:500]}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Check email column (the real issue might be email, not password)
print("\n3. Register with very simple data:")
try:
    import random

    email = f"x{random.randint(10000,99999)}@t.co"
    data = {"email": email, "password": "abc", "full_name": "X"}
    r = requests.post(f"{BASE}/auth/register", json=data, verify=False, timeout=15)
    print(f"   Email: {email}")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:500]}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 4: Stripe endpoint
print("\n4. Stripe Prices:")
try:
    r = requests.get(f"{BASE}/stripe/prices", verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   Response: {r.json()}")
    else:
        print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 5: List endpoints available
print("\n5. API Root:")
try:
    r = requests.get(f"{BASE}/", verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 6: OpenAPI docs
print("\n6. OpenAPI Docs:")
try:
    r = requests.get(f"{BASE}/docs", verify=False, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Has Swagger UI: {'swagger-ui' in r.text.lower()}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 60)
print("FIM DO DIAGNÓSTICO")
print("=" * 60)
