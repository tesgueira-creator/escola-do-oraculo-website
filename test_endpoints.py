"""
Teste completo de todos os endpoints da API Escola do Oráculo
"""

import requests
import json
import time
import random
import string

# Configuração
BASE_URL = "http://127.0.0.1:8000"
PRODUCTION_URL = "https://web-production-21437.up.railway.app"


def generate_random_email():
    """Gera email aleatório para testes"""
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@teste.com"


def test_endpoint(name, method, url, data=None, expected_status=200, headers=None):
    """Testa um endpoint e retorna resultado"""
    try:
        if headers is None:
            headers = {"Content-Type": "application/json"}

        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)

        status = (
            "✅ PASS"
            if response.status_code == expected_status
            else f"❌ FAIL (expected {expected_status})"
        )
        print(f"\n{status} - {name}")
        print(f"  URL: {url}")
        print(f"  Status: {response.status_code}")

        try:
            response_json = response.json()
            print(f"  Response: {json.dumps(response_json, indent=2)[:500]}")
        except:
            print(f"  Response: {response.text[:200]}")

        return response.status_code == expected_status, response
    except requests.exceptions.ConnectionError:
        print(f"\n❌ FAIL - {name}")
        print(f"  URL: {url}")
        print(f"  Error: Connection refused - server not running?")
        return False, None
    except Exception as e:
        print(f"\n❌ FAIL - {name}")
        print(f"  URL: {url}")
        print(f"  Error: {str(e)}")
        return False, None


def run_local_tests():
    """Testa endpoints locais"""
    print("=" * 60)
    print("🔬 TESTES DE ENDPOINTS LOCAIS (http://127.0.0.1:8000)")
    print("=" * 60)

    results = []

    # 1. Health Check
    success, _ = test_endpoint("Health Check", "GET", f"{BASE_URL}/health")
    results.append(("Health Check", success))

    # 2. Root Endpoint
    success, _ = test_endpoint("Root Endpoint", "GET", f"{BASE_URL}/")
    results.append(("Root Endpoint", success))

    # 3. Register New User
    test_email = generate_random_email()
    test_password = "TestPassword123!"

    success, register_response = test_endpoint(
        "Register New User",
        "POST",
        f"{BASE_URL}/auth/register",
        data={"email": test_email, "password": test_password, "full_name": "Test User"},
        expected_status=201,
    )
    results.append(("Register New User", success))

    # 4. Register Duplicate User (should fail)
    success, _ = test_endpoint(
        "Register Duplicate User (should fail with 400)",
        "POST",
        f"{BASE_URL}/auth/register",
        data={"email": test_email, "password": test_password, "full_name": "Test User"},
        expected_status=400,
    )
    results.append(("Register Duplicate", success))

    # 5. Login Valid User
    success, login_response = test_endpoint(
        "Login Valid User",
        "POST",
        f"{BASE_URL}/auth/login",
        data={"email": test_email, "password": test_password},
    )
    results.append(("Login Valid User", success))

    # 6. Login Invalid Password
    success, _ = test_endpoint(
        "Login Invalid Password (should fail with 401)",
        "POST",
        f"{BASE_URL}/auth/login",
        data={"email": test_email, "password": "wrongpassword"},
        expected_status=401,
    )
    results.append(("Login Invalid Password", success))

    # 7. Login Non-existent User
    success, _ = test_endpoint(
        "Login Non-existent User (should fail with 401)",
        "POST",
        f"{BASE_URL}/auth/login",
        data={"email": "nonexistent@test.com", "password": "anypassword"},
        expected_status=401,
    )
    results.append(("Login Non-existent", success))

    # 8. Forgot Password
    success, _ = test_endpoint(
        "Forgot Password",
        "POST",
        f"{BASE_URL}/auth/forgot-password",
        data={"email": test_email},
    )
    results.append(("Forgot Password", success))

    # 9. Get User Info (with token)
    if login_response and login_response.status_code == 200:
        token = login_response.json().get("access_token", "")
        success, _ = test_endpoint(
            "Get User Info", "GET", f"{BASE_URL}/users/me?token={token}"
        )
        results.append(("Get User Info", success))

    # 10. Create Checkout Session (will fail without valid Stripe key but tests endpoint)
    success, _ = test_endpoint(
        "Create Checkout Session (may fail without valid Stripe key)",
        "POST",
        f"{BASE_URL}/payments/create-checkout-session",
        data={"price_id": "price_1SpAOPHvoxa2NZ5dMc6vbBMM", "user_email": test_email},
        expected_status=400,  # Expected to fail without valid Stripe key
    )
    results.append(("Checkout Session", success))

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES LOCAIS")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")

    print(f"\n  Total: {passed}/{total} testes passaram")
    return passed, total


def run_production_tests():
    """Testa endpoints de produção (Railway)"""
    print("\n" + "=" * 60)
    print("🌐 TESTES DE ENDPOINTS PRODUÇÃO (Railway)")
    print("=" * 60)

    results = []

    # 1. Health Check
    success, _ = test_endpoint(
        "Production Health Check", "GET", f"{PRODUCTION_URL}/health"
    )
    results.append(("Health Check", success))

    # 2. Root Endpoint
    success, _ = test_endpoint("Production Root", "GET", f"{PRODUCTION_URL}/")
    results.append(("Root Endpoint", success))

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES PRODUÇÃO")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")

    print(f"\n  Total: {passed}/{total} testes passaram")
    return passed, total


def test_frontend_files():
    """Testa se arquivos frontend são servidos corretamente"""
    print("\n" + "=" * 60)
    print("📄 TESTES DE ARQUIVOS FRONTEND")
    print("=" * 60)

    files_to_test = [
        "/index.html",
        "/pages/login.html",
        "/pages/signup.html",
        "/pages/checkout.html",
        "/pages/forgot-password.html",
        "/pages/oraculo-app.html",
    ]

    results = []

    for file_path in files_to_test:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=10)
            success = response.status_code == 200
            status = "✅" if success else f"❌ ({response.status_code})"
            print(f"  {status} {file_path}")
            results.append((file_path, success))
        except Exception as e:
            print(f"  ❌ {file_path} - Error: {str(e)}")
            results.append((file_path, False))

    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n  Total: {passed}/{total} arquivos acessíveis")
    return passed, total


if __name__ == "__main__":
    print("\n🚀 TESTE COMPLETO DA API ESCOLA DO ORÁCULO\n")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Testes Locais
    local_passed, local_total = run_local_tests()

    # Testes de arquivos frontend
    frontend_passed, frontend_total = test_frontend_files()

    # Testes de Produção
    prod_passed, prod_total = run_production_tests()

    # Resumo Final
    print("\n" + "=" * 60)
    print("🎯 RESUMO FINAL")
    print("=" * 60)

    total_passed = local_passed + frontend_passed + prod_passed
    total_tests = local_total + frontend_total + prod_total

    print(f"  Local:      {local_passed}/{local_total}")
    print(f"  Frontend:   {frontend_passed}/{frontend_total}")
    print(f"  Produção:   {prod_passed}/{prod_total}")
    print(f"  ────────────────────")
    print(f"  TOTAL:      {total_passed}/{total_tests}")

    if total_passed == total_tests:
        print("\n✅ TODOS OS TESTES PASSARAM!")
    else:
        print(f"\n⚠️  {total_tests - total_passed} testes falharam")
