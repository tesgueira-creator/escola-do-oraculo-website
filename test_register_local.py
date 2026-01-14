#!/usr/bin/env python3
"""
Teste de registro no servidor LOCAL (não produção)
"""

import requests
import json
from datetime import datetime
import random
import string

# Desabilitar aviso de SSL
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL da API local (NÃO produção)
API_URL = "http://localhost:8000"

# Gerar um email único de teste
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f"teste_local_{timestamp}_{random_suffix}@teste.com"

test_user = {
    "full_name": f"Teste Local {timestamp}",
    "email": test_email,
    "password": "LocalTestPassword123!",
}

print("=" * 80)
print("🧪 TESTE DE REGISTRO - SERVIDOR LOCAL")
print("=" * 80)
print(f"📧 Email: {test_email}")
print(f"👤 Nome: {test_user['full_name']}")
print(f"🔐 Senha: {test_user['password']}")
print(f"🌐 API: {API_URL}")

print("\n" + "-" * 80)
print("PASSO 1: Verificando se a API local está acessível")
print("-" * 80)

try:
    health_response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"Status health check: {health_response.status_code}")
    print(f"Resposta: {health_response.text}")
    if health_response.status_code != 200:
        print("⚠️  API pode estar com problemas")
except Exception as e:
    print(f"❌ Erro ao conectar: {str(e)}")
    exit(1)

print("\n" + "-" * 80)
print("PASSO 2: Enviando dados de registro")
print("-" * 80)

payload = {
    "email": test_user["email"],
    "password": test_user["password"],
    "full_name": test_user["full_name"],
}

print(f"Payload enviado: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(
        f"{API_URL}/auth/register",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10,
        allow_redirects=False,
    )

    print(f"\nStatus HTTP: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Resposta: {response.text}")

    # Tentar fazer parse do JSON
    try:
        response_json = response.json()
        print(f"\nJSON: {json.dumps(response_json, indent=2, ensure_ascii=False)}")

        if response.status_code == 201:
            print("\n✅ SUCESSO! Utilizador registado!")

            # Testar login
            print("\n" + "-" * 80)
            print("PASSO 3: Testando login")
            print("-" * 80)

            login_response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": test_user["email"], "password": test_user["password"]},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            print(f"Status HTTP: {login_response.status_code}")
            print(f"Resposta: {login_response.text}")

            if login_response.status_code == 200:
                login_data = login_response.json()
                print(f"\n✅ LOGIN SUCESSO!")
                token = login_data.get("access_token")
                print(f"Token: {token[:50]}...")

                # Obter dados do utilizador
                print("\n" + "-" * 80)
                print("PASSO 4: Obtendo dados do utilizador logado")
                print("-" * 80)

                user_response = requests.get(
                    f"{API_URL}/users/me",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    timeout=10,
                )

                print(f"Status HTTP: {user_response.status_code}")
                print(f"Resposta: {user_response.text}")

                if user_response.status_code == 200:
                    user_data = user_response.json()
                    print(f"\n✅ DADOS DO UTILIZADOR:")
                    print(f"   - ID: {user_data.get('id')}")
                    print(f"   - Email: {user_data.get('email')}")
                    print(f"   - Nome: {user_data.get('full_name')}")
                    print(f"   - Ativo: {user_data.get('is_active')}")
                    print(f"   - Subscrição: {user_data.get('subscription_status')}")
            else:
                print(f"\n❌ Erro no login: {login_response.text}")
    except json.JSONDecodeError as e:
        print(f"\n⚠️  Não conseguiu fazer parse do JSON: {str(e)}")

except requests.exceptions.RequestException as e:
    print(f"❌ Erro na requisição: {str(e)}")

print("\n" + "=" * 80)
