#!/usr/bin/env python3
"""
Teste completo de registro com detalhes
Testa: health check → register → login → get user data
"""

import requests
import json
from datetime import datetime
import random
import string
import time
import sys

# Configurações
API_URL = "http://localhost:8000"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

test_user = {
    "email": f"testlocal_{timestamp}_{random_suffix}@test.local",
    "password": "LocalPassword123!Test",
    "full_name": f"Teste Local {timestamp}",
}

print("=" * 90)
print("🧪 TESTE COMPLETO DE REGISTRO - SERVIDOR LOCAL")
print("=" * 90)
print(f"\n📋 Dados de Teste:")
print(f"   Email: {test_user['email']}")
print(f"   Nome: {test_user['full_name']}")
print(f"   Senha: {test_user['password'][:15]}...")
print(f"   API: {API_URL}\n")

# Passo 1: Health Check
print("-" * 90)
print("PASSO 1: Verificando saúde da API")
print("-" * 90)

try:
    health_resp = requests.get(f"{API_URL}/health", timeout=5)
    print(f"Status: {health_resp.status_code}")
    print(f"Resposta: {health_resp.text}\n")

    if health_resp.status_code != 200:
        print("❌ API não está pronta!")
        sys.exit(1)
    print("✅ API está pronta\n")
except requests.exceptions.ConnectionError:
    print(f"❌ Erro: Não consegui conectar a {API_URL}")
    print("   Certifique-se de que o servidor está rodando:")
    print("   python run_server_debug.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    sys.exit(1)

# Passo 2: Registrar
print("-" * 90)
print("PASSO 2: Registrando novo utilizador")
print("-" * 90)

try:
    register_resp = requests.post(
        f"{API_URL}/auth/register",
        json={
            "email": test_user["email"],
            "password": test_user["password"],
            "full_name": test_user["full_name"],
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    print(f"Status: {register_resp.status_code}")
    print(f"Resposta: {register_resp.text}\n")

    if register_resp.status_code == 201:
        print("✅ Utilizador registado com sucesso!\n")
        user_data = register_resp.json()
    elif register_resp.status_code == 400:
        try:
            error_data = register_resp.json()
            if "already registered" in error_data.get("detail", ""):
                print("⚠️ Email já estava registado (esperado)\n")
                sys.exit(0)
        except:
            pass
        print(f"❌ Erro 400: {register_resp.text}\n")
        sys.exit(1)
    else:
        print(f"❌ Erro {register_resp.status_code}: {register_resp.text}\n")
        sys.exit(1)

except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}\n")
    sys.exit(1)

# Passo 3: Login
print("-" * 90)
print("PASSO 3: Fazendo login com as credenciais")
print("-" * 90)

try:
    login_resp = requests.post(
        f"{API_URL}/auth/login",
        json={"email": test_user["email"], "password": test_user["password"]},
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    print(f"Status: {login_resp.status_code}")
    print(f"Resposta: {login_resp.text}\n")

    if login_resp.status_code == 200:
        print("✅ Login realizado com sucesso!\n")
        login_data = login_resp.json()
        token = login_data.get("access_token")
        print(f"   Token: {token[:50]}...\n")
    else:
        print(f"❌ Erro no login: {login_resp.text}\n")
        sys.exit(1)

except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}\n")
    sys.exit(1)

# Passo 4: Obter dados do utilizador
print("-" * 90)
print("PASSO 4: Obtendo dados do utilizador logado")
print("-" * 90)

try:
    user_resp = requests.get(
        f"{API_URL}/users/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=10,
    )

    print(f"Status: {user_resp.status_code}")
    print(f"Resposta: {user_resp.text}\n")

    if user_resp.status_code == 200:
        print("✅ Dados obtidos com sucesso!\n")
        user = user_resp.json()
        print("   Dados do Utilizador:")
        print(f"   - ID: {user.get('id')}")
        print(f"   - Email: {user.get('email')}")
        print(f"   - Nome: {user.get('full_name')}")
        print(f"   - Ativo: {user.get('is_active')}")
        print(f"   - Subscrição: {user.get('subscription_status')}\n")
    else:
        print(f"❌ Erro ao obter dados: {user_resp.text}\n")
        sys.exit(1)

except Exception as e:
    print(f"❌ Erro na requisição: {str(e)}\n")
    sys.exit(1)

# Resumo Final
print("=" * 90)
print("✅ TESTE COMPLETO SUCESSO!")
print("=" * 90)
print(
    f"""
🎉 Fluxo de Registro Funcionando Perfeitamente:
   1. ✅ Health Check
   2. ✅ Registro de Novo Utilizador
   3. ✅ Login
   4. ✅ Obtenção de Dados do Utilizador

📊 Resumo:
   - Utilizador: {test_user['email']}
   - ID: {user.get('id')}
   - Status: {user.get('subscription_status')}
   - Ativo: {user.get('is_active')}

✨ Sistema pronto para produção!
"""
)
print("=" * 90)
