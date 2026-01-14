#!/usr/bin/env python3
"""
Script para testar o fluxo local sem exigir servidor separado
Simula requisições HTTP para os endpoints
"""

import subprocess
import time
import os
import sys
import requests
import json
from datetime import datetime

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Carregar variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 80)
print("🧪 TESTE COMPLETO DE REGISTRO - SERVIDOR LOCAL")
print("=" * 80)

# Configuração
BASE_URL = "http://127.0.0.1:8000"
HEALTH_URL = f"{BASE_URL}/health"

# Email único baseado em timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
test_email = f"teste_local_{timestamp}_xyz@test.local"
test_password = "TestPassword123!"
test_name = "Test User Local"

print(f"\n📧 Email de teste: {test_email}")
print(f"🔐 Senha: {test_password}")
print(f"👤 Nome: {test_name}")
print()

try:
    # PASSO 1: Verificar saúde da API
    print("─" * 80)
    print("PASSO 1: Verificando saúde da API...")
    print("─" * 80)

    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print("✅ API está pronta")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Erro na saúde: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"❌ Não consigo conectar a {BASE_URL}")
        print("   Certifique-se que o servidor está correndo:")
        print("   Terminal 1: python run_server_debug.py")
        sys.exit(1)

    # PASSO 2: Registrar novo utilizador
    print("\n" + "─" * 80)
    print("PASSO 2: Registrando novo utilizador...")
    print("─" * 80)

    register_url = f"{BASE_URL}/auth/register"
    register_data = {
        "email": test_email,
        "password": test_password,
        "full_name": test_name,
    }

    print(f"📍 URL: {register_url}")
    print(f"📤 Dados: {json.dumps(register_data, indent=2)}")

    response = requests.post(register_url, json=register_data, timeout=10)

    print(f"\n📊 Status: {response.status_code}")
    print(f"📝 Response:")

    try:
        response_data = response.json()
        print(json.dumps(response_data, indent=2))

        if response.status_code == 200:
            print("✅ Utilizador registado com sucesso!")
            user_id = response_data.get("id")
        else:
            print(
                f"❌ Erro no registro: {response_data.get('detail', 'Unknown error')}"
            )
            print("\n📋 Verificar logs:")
            print("   Terminal 1: Verifique a saída do servidor")
            print("   Ficheiro: type api_debug.log")
            sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Resposta não é JSON: {response.text}")
        sys.exit(1)

    # PASSO 3: Fazer login
    print("\n" + "─" * 80)
    print("PASSO 3: Fazendo login...")
    print("─" * 80)

    login_url = f"{BASE_URL}/auth/login"
    login_data = {"email": test_email, "password": test_password}

    print(f"📍 URL: {login_url}")
    print(f"📤 Dados: {json.dumps(login_data, indent=2)}")

    response = requests.post(login_url, json=login_data, timeout=10)

    print(f"\n📊 Status: {response.status_code}")

    try:
        response_data = response.json()
        print(f"📝 Response: {json.dumps(response_data, indent=2)}")

        if response.status_code == 200:
            print("✅ Login realizado com sucesso!")
            token = response_data.get("access_token")
        else:
            print(f"❌ Erro no login: {response_data.get('detail', 'Unknown error')}")
            sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Resposta não é JSON: {response.text}")
        sys.exit(1)

    # PASSO 4: Obter dados do utilizador
    print("\n" + "─" * 80)
    print("PASSO 4: Obtendo dados do utilizador...")
    print("─" * 80)

    get_user_url = f"{BASE_URL}/user/me"
    headers = {"Authorization": f"Bearer {token}"}

    print(f"📍 URL: {get_user_url}")
    print(f"📤 Headers: Authorization: Bearer {token[:20]}...")

    response = requests.get(get_user_url, headers=headers, timeout=10)

    print(f"\n📊 Status: {response.status_code}")

    try:
        response_data = response.json()
        print(f"📝 Response: {json.dumps(response_data, indent=2)}")

        if response.status_code == 200:
            print("✅ Dados obtidos com sucesso!")
        else:
            print(
                f"❌ Erro ao obter dados: {response_data.get('detail', 'Unknown error')}"
            )
            sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Resposta não é JSON: {response.text}")
        sys.exit(1)

    # SUCESSO
    print("\n" + "=" * 80)
    print("✅ TESTE COMPLETO SUCESSO!")
    print("=" * 80)
    print("\n📊 Resumo:")
    print(f"   ✅ Health check: OK")
    print(f"   ✅ Registro: OK (ID: {user_id})")
    print(f"   ✅ Login: OK")
    print(f"   ✅ Get User: OK")
    print("\n🎉 Todos os testes passaram!")
    print("\n📋 Próximos passos:")
    print("   1. Verifique os logs em api_debug.log")
    print("   2. Se tudo está OK, faça deploy para produção:")
    print("      git add -A")
    print("      git commit -m 'Add detailed logging to registration endpoint'")
    print("      git push")

except Exception as e:
    print(f"\n❌ Erro inesperado: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
