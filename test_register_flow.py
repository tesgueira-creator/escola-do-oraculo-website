#!/usr/bin/env python3
"""
Script para testar o registro de um novo usuário através do fluxo normal
Simula exatamente o que o frontend faz quando um utilizador cria uma conta
"""

import requests
import json
from datetime import datetime
import random
import string

# URL da API (Railway em produção)
API_URL = "https://web-production-21437.up.railway.app"

# Gerar um email único de teste
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
test_email = f"teste_{timestamp}_{random_suffix}@escola-test.com"

# Dados de teste
test_user = {
    "full_name": f"Teste User {timestamp}",
    "email": test_email,
    "password": "TestPassword123!",
}

print("=" * 70)
print("🧪 TESTE DE REGISTRO DE NOVO UTILIZADOR")
print("=" * 70)
print(f"\n📧 Email de teste: {test_email}")
print(f"👤 Nome: {test_user['full_name']}")
print(f"🔐 Senha: {test_user['password']}")
print(f"🌐 API: {API_URL}")

print("\n" + "-" * 70)
print("📝 PASSO 1: Tentando registar novo utilizador")
print("-" * 70)

try:
    # Fazer a requisição de registro (exatamente como o frontend faz)
    response = requests.post(
        f"{API_URL}/auth/register",
        json={
            "email": test_user["email"],
            "password": test_user["password"],
            "full_name": test_user["full_name"],
        },
        headers={"Content-Type": "application/json"},
        verify=False,  # Desabilitar verificação SSL para testes
        timeout=10,
    )

    print(f"Status HTTP: {response.status_code}")
    print(f"Resposta: {response.text}")

    if response.status_code == 201:
        print("\n✅ SUCESSO! Utilizador registado com sucesso!")
        response_data = response.json()
        print(
            f"Dados retornados: {json.dumps(response_data, indent=2, ensure_ascii=False)}"
        )

        # Agora testar se conseguimos fazer login
        print("\n" + "-" * 70)
        print("🔐 PASSO 2: Testando login do novo utilizador")
        print("-" * 70)

        login_response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
            headers={"Content-Type": "application/json"},
            verify=False,
            timeout=10,
        )

        print(f"Status HTTP: {login_response.status_code}")

        if login_response.status_code == 200:
            login_data = login_response.json()
            print(f"✅ LOGIN SUCESSO!")
            print(f"Token: {login_data.get('access_token', 'N/A')[:50]}...")
            print(f"Tipo: {login_data.get('token_type', 'N/A')}")

            # Testar obter dados do utilizador
            print("\n" + "-" * 70)
            print("👤 PASSO 3: Obtendo dados do utilizador logado")
            print("-" * 70)

            token = login_data.get("access_token")
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

            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"✅ DADOS DO UTILIZADOR:")
                print(f"   - ID: {user_data.get('id')}")
                print(f"   - Email: {user_data.get('email')}")
                print(f"   - Nome: {user_data.get('full_name')}")
                print(f"   - Ativo: {user_data.get('is_active')}")
                print(f"   - Subscrição: {user_data.get('subscription_status')}")
            else:
                print(f"❌ Erro ao obter dados: {user_response.text}")

        else:
            print(f"❌ ERRO NO LOGIN!")
            print(f"Resposta: {login_response.text}")

    elif response.status_code == 400:
        error_data = response.json()
        if "already registered" in str(error_data):
            print("⚠️  Email já estava registado (como esperado)")
        else:
            print(f"❌ ERRO 400 (Requisição Inválida)")
            print(f"Detalhes: {error_data}")

    elif response.status_code == 500:
        print("❌ ERRO 500 (Erro no Servidor)")
        print(f"Resposta: {response.text}")
        error_data = response.json()
        if "detail" in error_data:
            print(f"Detalhes do erro: {error_data['detail']}")

    else:
        print(f"⚠️  Status inesperado: {response.status_code}")
        print(f"Resposta: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ ERRO: Não conseguiu conectar à API")
    print(f"URL: {API_URL}")
except requests.exceptions.Timeout:
    print("❌ ERRO: Timeout na requisição")
except Exception as e:
    print(f"❌ ERRO: {str(e)}")

print("\n" + "=" * 70)
print("📋 RESUMO")
print("=" * 70)
print(
    f"""
O teste tentou:
1. ✅ Registar um novo utilizador com email: {test_email}
2. ✅ Fazer login com as credenciais
3. ✅ Obter dados do utilizador logado

Se todos os passos tiveram sucesso, o fluxo de registro está funcionando perfeitamente!
"""
)
print("=" * 70)
