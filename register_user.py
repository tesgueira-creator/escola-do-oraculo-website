#!/usr/bin/env python3
"""
Registar utilizador Tomas Esgueira no backend Railway
"""
import requests
import json

API_URL = "https://web-production-21437.up.railway.app"

user_data = {
    "full_name": "Tomas Esgueira",
    "email": "tomas.teste@teste.com",
    "password": "Teste123!",
}

print("🔄 Registando utilizador no backend Railway...")
print(f"📧 Email: {user_data['email']}")
print(f"👤 Nome: {user_data['full_name']}")

try:
    # Tentar registar
    response = requests.post(
        f"{API_URL}/auth/register",
        json=user_data,
        headers={"Content-Type": "application/json"},
        verify=False,  # Ignorar SSL certificate issues
    )

    print(f"\n📡 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text}")

    if response.status_code in [200, 201]:
        print("\n✅ UTILIZADOR REGISTADO COM SUCESSO!")
        print("\n🔐 Agora podes fazer login com:")
        print(f"   Email: {user_data['email']}")
        print(f"   Password: {user_data['password']}")

        # Tentar login imediatamente
        print("\n🔄 Testando login...")
        login_response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
            headers={"Content-Type": "application/json"},
            verify=False,
        )

        if login_response.status_code == 200:
            data = login_response.json()
            print("✅ LOGIN BEM-SUCEDIDO!")
            print(f"🎫 Token: {data.get('access_token', 'N/A')[:50]}...")
        else:
            print(f"❌ Login falhou: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")

    elif response.status_code == 400:
        print("\n⚠️  Utilizador já existe! Tenta fazer login diretamente.")

        # Tentar login
        print("\n🔄 Testando login com credenciais existentes...")
        login_response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
            headers={"Content-Type": "application/json"},
            verify=False,
        )

        if login_response.status_code == 200:
            data = login_response.json()
            print("✅ LOGIN BEM-SUCEDIDO!")
            print(f"🎫 Token: {data.get('access_token', 'N/A')[:50]}...")
        else:
            print(f"❌ Login falhou: {login_response.status_code}")
            print(f"   Resposta: {login_response.text}")
    else:
        print(f"\n❌ Erro ao registar: {response.status_code}")
        print(f"Detalhes: {response.text}")

except requests.exceptions.SSLError as e:
    print(f"\n⚠️  Erro SSL (ignorado): {e}")
    print("Tentando novamente sem verificação SSL...")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback

    traceback.print_exc()
