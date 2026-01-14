#!/usr/bin/env python3
import subprocess
import time
import requests
import json
from datetime import datetime
import sys
import os

# Mudar para o diretório
os.chdir("c:\\Users\\XKELU27\\Downloads\\escola-do-oraculo-website")

# Iniciar servidor em background
print("Iniciando servidor...")
server_proc = subprocess.Popen(
    [sys.executable, "run_server_debug.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# Aguardar que o servidor inicie
time.sleep(8)

try:
    BASE_URL = "http://127.0.0.1:8000"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_email = f"test_{timestamp}@test.local"

    # Test 1: Health
    print("1. Verificando saúde da API...")
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status: {r.status_code}")

    if r.status_code != 200:
        print("ERRO: API não está respondendo")
        sys.exit(1)

    # Test 2: Register
    print("2. Registrando novo utilizador...")
    data = {
        "email": test_email,
        "password": "TestPassword123!",
        "full_name": "Test User",
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=data, timeout=10)
    print(f"   Status: {r.status_code}")

    if r.status_code not in [200, 201]:
        resp = r.json()
        print(f"   ERRO: {resp.get('detail', 'Unknown error')}")
        sys.exit(1)

    user = r.json()
    print(f"   ID: {user.get('id')}")

    # Test 3: Login
    print("3. Fazendo login...")
    login_data = {"email": test_email, "password": "TestPassword123!"}
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
    print(f"   Status: {r.status_code}")

    if r.status_code != 200:
        resp = r.json()
        print(f"   ERRO: {resp.get('detail', 'Unknown error')}")
        sys.exit(1)

    token = r.json().get("access_token")

    # Test 4: Get user
    print("4. Obtendo dados do utilizador...")
    r = requests.get(
        f"{BASE_URL}/user/me", headers={"Authorization": f"Bearer {token}"}, timeout=10
    )
    print(f"   Status: {r.status_code}")

    if r.status_code != 200:
        resp = r.json()
        print(f"   ERRO: {resp.get('detail', 'Unknown error')}")
        sys.exit(1)

    print("\n✅ TODOS OS TESTES PASSARAM!")
    print("\n📊 Resumo:")
    print("   ✅ Health: OK")
    print("   ✅ Registro: OK")
    print("   ✅ Login: OK")
    print("   ✅ Get User: OK")

finally:
    # Parar o servidor
    print("\nParando servidor...")
    server_proc.terminate()
    try:
        server_proc.wait(timeout=5)
    except:
        server_proc.kill()
