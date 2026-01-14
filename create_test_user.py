#!/usr/bin/env python3
"""
Script para criar utilizador de teste na Escola do Oráculo
"""
import requests
import json

# API Configuration
API_URL = "https://web-production-21437.up.railway.app"

# Test User Credentials
TEST_USER = {
    "full_name": "Tomas Esgueira",
    "email": "tomas.teste@teste.com",
    "password": "Teste123!",
}


def create_test_user():
    """Cria utilizador de teste via API"""
    print("🔄 Criando utilizador de teste...\n")

    try:
        # Register user
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "full_name": TEST_USER["full_name"],
                "email": TEST_USER["email"],
                "password": TEST_USER["password"],
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200 or response.status_code == 201:
            print("✅ Utilizador criado com sucesso!\n")
            print("=" * 60)
            print("🔐 CREDENCIAIS DE TESTE - ESCOLA DO ORÁCULO")
            print("=" * 60)
            print(f"📧 Email:    {TEST_USER['email']}")
            print(f"🔑 Password: {TEST_USER['password']}")
            print(f"👤 Nome:     {TEST_USER['full_name']}")
            print("=" * 60)
            print("\n✨ Use estas credenciais em:")
            print(f"   Login: http://localhost:8000/login.html")
            print(f"   ou:    https://escola-do-oraculo-website.vercel.app/login.html")
            print("\n")

            # Try to login to verify
            print("🔄 Verificando login...\n")
            login_response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": TEST_USER["email"], "password": TEST_USER["password"]},
                headers={"Content-Type": "application/json"},
            )

            if login_response.status_code == 200:
                token_data = login_response.json()
                print("✅ Login verificado! Token gerado com sucesso.")
                print(f"🎫 Token: {token_data.get('access_token', 'N/A')[:50]}...")
            else:
                print(f"⚠️  Login falhou: {login_response.status_code}")
                print(f"   Resposta: {login_response.text}")

        elif response.status_code == 400:
            error_detail = response.json().get("detail", "")
            if (
                "already registered" in error_detail.lower()
                or "já existe" in error_detail.lower()
            ):
                print("⚠️  Utilizador já existe! Use as credenciais abaixo:\n")
                print("=" * 60)
                print("🔐 CREDENCIAIS DE TESTE - ESCOLA DO ORÁCULO")
                print("=" * 60)
                print(f"📧 Email:    {TEST_USER['email']}")
                print(f"🔑 Password: {TEST_USER['password']}")
                print(f"👤 Nome:     {TEST_USER['full_name']}")
                print("=" * 60)
                print("\n✨ Use estas credenciais em:")
                print(f"   Login: http://localhost:8000/login.html")
                print("\n")
            else:
                print(f"❌ Erro ao criar utilizador: {response.status_code}")
                print(f"   Detalhes: {response.text}")
        else:
            print(f"❌ Erro ao criar utilizador: {response.status_code}")
            print(f"   Resposta: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        print("\n⚠️  API pode estar offline. Use as credenciais para testar localmente:")
        print("=" * 60)
        print("🔐 CREDENCIAIS DE TESTE")
        print("=" * 60)
        print(f"📧 Email:    {TEST_USER['email']}")
        print(f"🔑 Password: {TEST_USER['password']}")
        print("=" * 60)


if __name__ == "__main__":
    create_test_user()
