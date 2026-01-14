#!/usr/bin/env python3
"""
Teste simples de registro com salva em arquivo
"""
import requests
import json
from datetime import datetime
import random
import string
import urllib3

urllib3.disable_warnings()

API_URL = "http://localhost:8000"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f"teste_{timestamp}_{random_suffix}@test.local"

test_data = {
    "email": test_email,
    "password": "Password123!",
    "full_name": f"Test User {timestamp}",
}

# Salvar em arquivo para debug
with open("register_test_log.txt", "w") as log:
    log.write(f"Testing registration at {datetime.now()}\n")
    log.write(f"Email: {test_email}\n")
    log.write(f"API: {API_URL}\n\n")

    try:
        # Health check
        health = requests.get(f"{API_URL}/health", timeout=5)
        log.write(f"Health: {health.status_code} - {health.text}\n\n")

        # Register
        reg_response = requests.post(
            f"{API_URL}/auth/register",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        log.write(f"Register Status: {reg_response.status_code}\n")
        log.write(f"Register Response: {reg_response.text}\n\n")

        if reg_response.status_code == 201:
            log.write("SUCCESS!\n")

            # Login
            login_response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": test_data["email"], "password": test_data["password"]},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            log.write(f"\nLogin Status: {login_response.status_code}\n")
            log.write(f"Login Response: {login_response.text}\n")

    except Exception as e:
        log.write(f"ERROR: {str(e)}\n")

print("✅ Teste completo! Verifique register_test_log.txt")
