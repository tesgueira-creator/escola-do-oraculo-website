#!/usr/bin/env python3
"""
Script de teste completo em producao
Testa todos os endpoints e funcionalidades
"""

import requests
import json
import urllib3
from datetime import datetime

# Disable SSL warnings (Railway may have certificate issues in some networks)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://web-production-21437.up.railway.app"
VERIFY_SSL = False  # Set to True if SSL works properly
RESULTS = []


def log_result(name, success, details=""):
    status = "[OK]" if success else "[ERRO]"
    RESULTS.append({"name": name, "success": success, "details": details})
    print(f"{status} {name}: {details}")


def test_health():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=10, verify=VERIFY_SSL)
        if r.status_code == 200:
            data = r.json()
            log_result(
                "Health Check",
                True,
                f"DB: {data.get('database')}, Env: {data.get('environment')}",
            )
            return True
        else:
            log_result("Health Check", False, f"Status: {r.status_code}")
            return False
    except Exception as e:
        log_result("Health Check", False, str(e))
        return False


def test_register():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    email = f"test_prod_{timestamp}@test.local"
    try:
        data = {"email": email, "password": "TestPass123!", "full_name": "Test User"}
        r = requests.post(
            f"{BASE_URL}/auth/register", json=data, timeout=15, verify=VERIFY_SSL
        )
        if r.status_code in [200, 201]:
            user = r.json()
            log_result("Register", True, f"ID: {user.get('id')}, Email: {email}")
            return email, user
        else:
            resp = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {"detail": r.text}
            )
            log_result(
                "Register",
                False,
                f"Status: {r.status_code}, Detail: {resp.get('detail', 'Unknown')}",
            )
            return None, None
    except Exception as e:
        log_result("Register", False, str(e))
        return None, None


def test_login(email):
    if not email:
        log_result("Login", False, "No email to test")
        return None
    try:
        data = {"email": email, "password": "TestPass123!"}
        r = requests.post(
            f"{BASE_URL}/auth/login", json=data, timeout=10, verify=VERIFY_SSL
        )
        if r.status_code == 200:
            token = r.json().get("access_token")
            log_result("Login", True, f"Token: {token[:20]}...")
            return token
        else:
            resp = (
                r.json()
                if r.headers.get("content-type", "").startswith("application/json")
                else {"detail": r.text}
            )
            log_result(
                "Login",
                False,
                f"Status: {r.status_code}, Detail: {resp.get('detail', 'Unknown')}",
            )
            return None
    except Exception as e:
        log_result("Login", False, str(e))
        return None


def test_get_user(token):
    if not token:
        log_result("Get User", False, "No token")
        return
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(
            f"{BASE_URL}/user/me", headers=headers, timeout=10, verify=VERIFY_SSL
        )
        if r.status_code == 200:
            user = r.json()
            log_result(
                "Get User",
                True,
                f"Email: {user.get('email')}, Sub: {user.get('subscription_status')}",
            )
        else:
            log_result("Get User", False, f"Status: {r.status_code}")
    except Exception as e:
        log_result("Get User", False, str(e))


def test_stripe_prices():
    try:
        r = requests.get(f"{BASE_URL}/stripe/prices", timeout=10, verify=VERIFY_SSL)
        if r.status_code == 200:
            prices = r.json()
            count = len(prices) if isinstance(prices, list) else 1
            log_result("Stripe Prices", True, f"Encontrados: {count} precos")
        else:
            log_result("Stripe Prices", False, f"Status: {r.status_code}")
    except Exception as e:
        log_result("Stripe Prices", False, str(e))


def test_pages():
    pages = [
        ("/", "Home"),
        ("/pages/login.html", "Login Page"),
        ("/pages/signup.html", "Signup Page"),
        ("/pages/oraculo-app.html", "Oraculo App"),
    ]
    for path, name in pages:
        try:
            r = requests.get(f"{BASE_URL}{path}", timeout=10, verify=VERIFY_SSL)
            if r.status_code == 200:
                log_result(f"Page: {name}", True, "Acessivel")
            else:
                log_result(f"Page: {name}", False, f"Status: {r.status_code}")
        except Exception as e:
            log_result(f"Page: {name}", False, str(e))


def main():
    print("=" * 60)
    print("TESTE COMPLETO DE PRODUCAO - ESCOLA DO ORACULO")
    print(f"URL: {BASE_URL}")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Testes
    print("[1] TESTES DE API")
    print("-" * 40)
    test_health()

    print()
    print("[2] TESTES DE AUTENTICACAO")
    print("-" * 40)
    email, user = test_register()
    token = test_login(email)
    test_get_user(token)

    print()
    print("[3] TESTES DE STRIPE")
    print("-" * 40)
    test_stripe_prices()

    print()
    print("[4] TESTES DE PAGINAS")
    print("-" * 40)
    test_pages()

    # Resumo
    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    success = sum(1 for r in RESULTS if r["success"])
    total = len(RESULTS)
    print(f"Testes: {success}/{total} passaram")

    failed = [r for r in RESULTS if not r["success"]]
    if failed:
        print()
        print("Falhas:")
        for f in failed:
            print(f"  - {f['name']}: {f['details']}")
    else:
        print()
        print("[SUCCESS] Todos os testes passaram!")

    # Salvar resultados
    with open("test_production_results.txt", "w", encoding="utf-8") as f:
        f.write(f"TESTE DE PRODUCAO - {datetime.now()}\n")
        f.write("=" * 60 + "\n")
        for r in RESULTS:
            status = "[OK]" if r["success"] else "[ERRO]"
            f.write(f"{status} {r['name']}: {r['details']}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Resultado: {success}/{total} passaram\n")

    print()
    print("Resultados salvos em: test_production_results.txt")


if __name__ == "__main__":
    main()
