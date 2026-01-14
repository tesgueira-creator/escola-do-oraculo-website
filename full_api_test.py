#!/usr/bin/env python3
"""
Script de Teste Completo da API - Escola do Oráculo
Testa todos os endpoints em produção
"""

import requests
import json
import time
import random
import string
import urllib3

# Desativar avisos de SSL para testes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://web-production-21437.up.railway.app"

# Configuração para desativar verificação SSL
VERIFY_SSL = False

def random_email():
    """Gera um email aleatório para testes"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@test.local"

def random_password():
    """Gera uma password aleatória"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def test_with_result(name, method, url, expected_status=None, **kwargs):
    """Executa um teste e retorna o resultado formatado"""
    try:
        response = method(url, timeout=30, verify=VERIFY_SSL, **kwargs)
        status = response.status_code
        
        if expected_status:
            success = status == expected_status
        else:
            success = 200 <= status < 300
            
        return {
            "name": name,
            "url": url,
            "status": status,
            "success": success,
            "expected": expected_status,
            "response": response.text[:500] if len(response.text) < 500 else response.text[:500] + "..."
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "status": None,
            "success": False,
            "error": str(e)
        }

def print_result(result):
    """Imprime resultado formatado"""
    icon = "✅" if result["success"] else "❌"
    print(f"\n{icon} {result['name']}")
    print(f"   URL: {result['url']}")
    print(f"   Status: {result['status']}")
    if result.get('expected'):
        print(f"   Expected: {result['expected']}")
    if result.get('error'):
        print(f"   Error: {result['error']}")
    else:
        try:
            data = json.loads(result['response'])
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)[:300]}")
        except:
            print(f"   Response: {result['response'][:200]}")

def main():
    print("=" * 60)
    print("🔮 TESTE COMPLETO DA API - ESCOLA DO ORÁCULO")
    print("=" * 60)
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    # ========== TESTES DE INFRAESTRUTURA ==========
    print("\n📊 TESTES DE INFRAESTRUTURA")
    print("-" * 40)
    
    # 1. Health Check
    r = test_with_result("Health Check", requests.get, f"{BASE_URL}/health", 200)
    print_result(r)
    results.append(r)
    
    # 2. Version
    r = test_with_result("API Version", requests.get, f"{BASE_URL}/version", 200)
    print_result(r)
    results.append(r)
    
    # 3. API Root
    r = test_with_result("API Root", requests.get, f"{BASE_URL}/", 200)
    print_result(r)
    results.append(r)
    
    # 4. OpenAPI Docs
    r = test_with_result("OpenAPI Docs", requests.get, f"{BASE_URL}/docs", 200)
    print_result(r)
    results.append(r)
    
    # 5. ReDoc
    r = test_with_result("ReDoc", requests.get, f"{BASE_URL}/redoc", 200)
    print_result(r)
    results.append(r)
    
    # ========== TESTES DE AUTENTICAÇÃO ==========
    print("\n🔐 TESTES DE AUTENTICAÇÃO")
    print("-" * 40)
    
    # 6. Registo - Password Normal
    email1 = random_email()
    pwd1 = random_password()
    r = test_with_result(
        "Register (Normal Password)", 
        requests.post, 
        f"{BASE_URL}/auth/register", 
        201,
        json={"email": email1, "password": pwd1, "full_name": "Test User Normal"}
    )
    print_result(r)
    results.append(r)
    
    # 7. Registo - Password Longa (teste bcrypt 72-byte)
    email2 = random_email()
    long_pwd = "a" * 100  # 100 caracteres - mais que 72 bytes
    r = test_with_result(
        "Register (Long Password - 100 chars)", 
        requests.post, 
        f"{BASE_URL}/auth/register", 
        201,
        json={"email": email2, "password": long_pwd, "full_name": "Test User Long Password"}
    )
    print_result(r)
    results.append(r)
    
    # 8. Registo - Email Duplicado
    r = test_with_result(
        "Register (Duplicate Email)", 
        requests.post, 
        f"{BASE_URL}/auth/register", 
        400,
        json={"email": email1, "password": "test123", "full_name": "Duplicate Test"}
    )
    print_result(r)
    results.append(r)
    
    # 9. Registo - Email Inválido
    r = test_with_result(
        "Register (Invalid Email)", 
        requests.post, 
        f"{BASE_URL}/auth/register", 
        422,
        json={"email": "notanemail", "password": "test123", "full_name": "Invalid Email Test"}
    )
    print_result(r)
    results.append(r)
    
    # 10. Login - Credenciais Válidas
    r = test_with_result(
        "Login (Valid Credentials)", 
        requests.post, 
        f"{BASE_URL}/auth/login", 
        200,
        json={"email": email1, "password": pwd1}
    )
    print_result(r)
    results.append(r)
    
    # Guardar token se login bem sucedido
    auth_token = None
    if r["success"]:
        try:
            data = json.loads(r["response"])
            auth_token = data.get("access_token")
        except:
            pass
    
    # 11. Login - Credenciais Inválidas
    r = test_with_result(
        "Login (Invalid Credentials)", 
        requests.post, 
        f"{BASE_URL}/auth/login", 
        401,
        json={"email": email1, "password": "wrongpassword"}
    )
    print_result(r)
    results.append(r)
    
    # 12. Login - Utilizador Inexistente
    r = test_with_result(
        "Login (Non-existent User)", 
        requests.post, 
        f"{BASE_URL}/auth/login", 
        401,
        json={"email": "nonexistent@test.com", "password": "test123"}
    )
    print_result(r)
    results.append(r)
    
    # 13. Get User Profile
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    r = test_with_result(
        "Get User Profile (/auth/me)", 
        requests.get, 
        f"{BASE_URL}/auth/me", 
        200 if auth_token else 401,
        headers=headers
    )
    print_result(r)
    results.append(r)
    
    # ========== TESTES DE STRIPE ==========
    print("\n💳 TESTES DE STRIPE")
    print("-" * 40)
    
    # 14. Listar Preços
    r = test_with_result(
        "Stripe Prices List", 
        requests.get, 
        f"{BASE_URL}/stripe/prices", 
        200
    )
    print_result(r)
    results.append(r)
    
    # 15. Criar Checkout Session (sem autenticação)
    r = test_with_result(
        "Stripe Checkout (PRO Plan)", 
        requests.post, 
        f"{BASE_URL}/stripe/create-checkout-session", 
        None,  # Pode ser 200 ou 401/500 dependendo da config
        json={"price_id": "price_1RSH9BFrSqH6HiMTtawWKf4B"}
    )
    print_result(r)
    results.append(r)
    
    # ========== TESTES DE DEBUG ==========
    print("\n🔧 TESTES DE DEBUG")
    print("-" * 40)
    
    # 16. Debug Hash Test
    r = test_with_result(
        "Debug Hash Test", 
        requests.get, 
        f"{BASE_URL}/debug/hash-test", 
        200
    )
    print_result(r)
    results.append(r)
    
    # ========== RESUMO FINAL ==========
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL")
    print("=" * 60)
    
    passed = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    total = len(results)
    
    print(f"✅ Passados: {passed}/{total}")
    print(f"❌ Falhados: {failed}/{total}")
    print(f"📈 Taxa de Sucesso: {(passed/total)*100:.1f}%")
    
    if failed > 0:
        print("\n❌ TESTES FALHADOS:")
        for r in results:
            if not r["success"]:
                print(f"   - {r['name']}: {r.get('error') or f'Status {r['status']} (expected {r.get('expected', '2xx')}'}")
    
    print("\n" + "=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
