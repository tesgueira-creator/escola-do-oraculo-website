"""
Script de Verificação Completa - Escola do Oráculo
Testa todos os aspectos da aplicação: endpoints, formulários, conexões
"""

import requests
import json
import random
import string
import urllib3

# Desabilitar warnings de SSL para testes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URLs de teste
PRODUCTION_URL = "https://web-production-21437.up.railway.app"
LOCAL_URL = "http://127.0.0.1:8000"

# Flag para verificação SSL (False para debug)
VERIFY_SSL = False


def generate_random_email():
    """Gera email aleatório para testes"""
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@teste.com"


class APITester:
    def __init__(self, base_url, name="API"):
        self.base_url = base_url
        self.name = name
        self.results = []

    def test(
        self, endpoint, method="GET", data=None, expected_status=200, description=""
    ):
        """Executa um teste e registra resultado"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=15, verify=VERIFY_SSL)
            elif method == "POST":
                response = requests.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=15,
                    verify=VERIFY_SSL,
                )

            success = response.status_code == expected_status
            self.results.append(
                {
                    "description": description,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "success": success,
                    "response": response.text[:200] if not success else None,
                }
            )
            return success, response
        except requests.exceptions.ConnectionError:
            self.results.append(
                {
                    "description": description,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": "Connection Error",
                    "success": False,
                    "response": "Server not reachable",
                }
            )
            return False, None
        except Exception as e:
            self.results.append(
                {
                    "description": description,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": str(e),
                    "success": False,
                    "response": str(e),
                }
            )
            return False, None

    def print_summary(self):
        """Imprime resumo dos testes"""
        print(f"\n{'='*60}")
        print(f"📊 RESUMO: {self.name}")
        print(f"{'='*60}")

        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)

        for r in self.results:
            status = "✅" if r["success"] else "❌"
            print(f"  {status} {r['description']}")
            if not r["success"]:
                print(f"      Expected: {r['expected']}, Got: {r['actual']}")
                if r.get("response"):
                    print(f"      Response: {r['response'][:100]}")

        print(f"\n  Total: {passed}/{total} passaram")
        return passed, total


def test_production():
    """Testa a API de produção"""
    print("\n🌐 TESTANDO API DE PRODUÇÃO (Railway)")
    print("=" * 60)

    tester = APITester(PRODUCTION_URL, "Produção (Railway)")

    # 1. Health Check
    tester.test("/health", "GET", description="Health Check")

    # 2. Root Endpoint
    tester.test("/", "GET", description="Root Endpoint")

    # 3. Register (novo usuário)
    test_email = generate_random_email()
    success, response = tester.test(
        "/auth/register",
        "POST",
        {"email": test_email, "password": "Test123!", "full_name": "Test User"},
        expected_status=201,
        description="Registrar Novo Usuário",
    )

    # 4. Login com usuário criado
    if success:
        tester.test(
            "/auth/login",
            "POST",
            {"email": test_email, "password": "Test123!"},
            expected_status=200,
            description="Login com Novo Usuário",
        )

    # 5. Login inválido
    tester.test(
        "/auth/login",
        "POST",
        {"email": "nonexistent@test.com", "password": "wrong"},
        expected_status=401,
        description="Login Inválido (deve falhar)",
    )

    # 6. Forgot Password
    tester.test(
        "/auth/forgot-password",
        "POST",
        {"email": test_email},
        expected_status=200,
        description="Forgot Password",
    )

    return tester.print_summary()


def test_frontend_pages():
    """Testa se as páginas frontend estão acessíveis via backend"""
    print("\n📄 TESTANDO PÁGINAS FRONTEND (via Backend)")
    print("=" * 60)

    tester = APITester(PRODUCTION_URL, "Páginas Frontend")

    pages = [
        ("/", "Homepage"),
        ("/pages/login.html", "Login Page"),
        ("/pages/signup.html", "Signup Page"),
        ("/pages/checkout.html", "Checkout Page"),
        ("/pages/forgot-password.html", "Forgot Password Page"),
    ]

    for endpoint, description in pages:
        tester.test(endpoint, "GET", description=description)

    return tester.print_summary()


def check_stripe_integration():
    """Verifica se a integração Stripe está configurada"""
    print("\n💳 VERIFICANDO INTEGRAÇÃO STRIPE")
    print("=" * 60)

    # Tenta criar uma sessão de checkout (vai falhar sem Stripe key válida, mas testa o endpoint)
    try:
        response = requests.post(
            f"{PRODUCTION_URL}/payments/create-checkout-session",
            json={"price_id": "price_test", "user_email": "test@test.com"},
            headers={"Content-Type": "application/json"},
            timeout=15,
            verify=VERIFY_SSL,
        )

        if response.status_code == 400:
            error_detail = response.json().get("detail", "")
            if "Invalid API Key" in error_detail or "api_key" in error_detail.lower():
                print(
                    "  ⚠️  Stripe API Key não está configurada corretamente no Railway"
                )
                print("     Configure STRIPE_SECRET_KEY nas variáveis de ambiente")
            else:
                print(f"  ⚠️  Erro ao criar checkout: {error_detail[:100]}")
        elif response.status_code == 200:
            print("  ✅ Stripe está configurado e funcionando!")
        else:
            print(f"  ❌ Status inesperado: {response.status_code}")

    except Exception as e:
        print(f"  ❌ Erro de conexão: {e}")

    return 0, 0  # Não contamos como teste formal


def check_database_connection():
    """Verifica conexão com banco de dados"""
    print("\n🗄️  VERIFICANDO BANCO DE DADOS")
    print("=" * 60)

    try:
        response = requests.get(
            f"{PRODUCTION_URL}/health", timeout=15, verify=VERIFY_SSL
        )
        data = response.json()

        if data.get("database") == "connected":
            print("  ✅ Banco de dados conectado")
            print(f"     Ambiente: {data.get('environment', 'N/A')}")
            return 1, 1
        else:
            print("  ❌ Banco de dados não conectado")
            return 0, 1
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return 0, 1


def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("🚀 VERIFICAÇÃO COMPLETA - ESCOLA DO ORÁCULO")
    print("=" * 60)

    total_passed = 0
    total_tests = 0

    # 1. Database
    p, t = check_database_connection()
    total_passed += p
    total_tests += t

    # 2. Production API
    p, t = test_production()
    total_passed += p
    total_tests += t

    # 3. Frontend Pages
    p, t = test_frontend_pages()
    total_passed += p
    total_tests += t

    # 4. Stripe (informativo)
    check_stripe_integration()

    # Resumo Final
    print("\n" + "=" * 60)
    print("🎯 RESULTADO FINAL")
    print("=" * 60)
    print(f"  Total: {total_passed}/{total_tests} testes passaram")

    if total_passed == total_tests:
        print("\n✅ TODOS OS TESTES PASSARAM! Sistema funcionando corretamente.")
    else:
        print(
            f"\n⚠️  {total_tests - total_passed} testes falharam. Verifique os erros acima."
        )

    return total_passed == total_tests


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
