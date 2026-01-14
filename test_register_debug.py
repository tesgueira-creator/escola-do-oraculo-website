#!/usr/bin/env python3
"""
Script para testar o registro de um novo utilizador com tratamento detalhado de erros
"""

import requests
import json
from datetime import datetime
import random
import string

# Desabilitar aviso de SSL
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL da API
API_URL = "https://web-production-21437.up.railway.app"

# Gerar um email único de teste
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f"teste_{timestamp}_{random_suffix}@teste.com"

test_user = {
    "full_name": f"Teste {timestamp}",
    "email": test_email,
    "password": "TestPassword123!",
}

print("=" * 80)
print("🧪 TESTE DE REGISTRO - NOVO UTILIZADOR")
print("=" * 80)
print(f"📧 Email: {test_email}")
print(f"👤 Nome: {test_user['full_name']}")
print(f"🔐 Senha: {test_user['password']}")
print(f"🌐 API: {API_URL}")

print("\n" + "-" * 80)
print("PASSO 1: Verificando se a API está acessível")
print("-" * 80)

try:
    health_response = requests.get(f"{API_URL}/health", verify=False, timeout=10)
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
        verify=False,
        timeout=10,
        allow_redirects=False,
    )

    print(f"\nStatus HTTP: {response.status_code}")
    print(f"Headers de resposta: {dict(response.headers)}")
    print(f"\nRaw Response Text:")
    print(response.text)
    print(f"\nRaw Response Content:")
    print(response.content)

    # Tentar fazer parse do JSON
    try:
        response_json = response.json()
        print(f"\nJSON Parsed:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"\n⚠️  Não conseguiu fazer parse do JSON: {str(e)}")

    if response.status_code == 201:
        print("\n✅ SUCESSO! Utilizador registado!")
        response_data = response.json()

        # Testar login
        print("\n" + "-" * 80)
        print("PASSO 3: Testando login do novo utilizador")
        print("-" * 80)

        login_response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
            headers={"Content-Type": "application/json"},
            verify=False,
            timeout=10,
        )

        print(f"Status HTTP: {login_response.status_code}")
        print(f"Resposta: {login_response.text}")

        if login_response.status_code == 200:
            login_data = login_response.json()
            print(f"✅ LOGIN SUCESSO!")
            token = login_data.get("access_token")
            print(f"Token obtido: {token[:50]}...")

            # Obter dados do utilizador
            print("\n" + "-" * 80)
            print("PASSO 4: Obtendo dados do utilizador")
            print("-" * 80)

            user_response = requests.get(
                f"{API_URL}/users/me",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                verify=False,
                timeout=10,
            )

            print(f"Status HTTP: {user_response.status_code}")
            print(f"Resposta: {user_response.text}")

            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"✅ Dados obtidos com sucesso!")
                print(f"   - Email: {user_data.get('email')}")
                print(f"   - Nome: {user_data.get('full_name')}")
                print(f"   - Status: {user_data.get('subscription_status')}")
    else:
        print(f"\n❌ ERRO {response.status_code}")

        # Tentar extrair mensagem de erro
        try:
            error_data = response.json()
            if "detail" in error_data:
                print(f"Detalhe do erro: {error_data['detail']}")
        except:
            pass

except requests.exceptions.RequestException as e:
    print(f"❌ Erro na requisição: {str(e)}")

print("\n" + "=" * 80)
