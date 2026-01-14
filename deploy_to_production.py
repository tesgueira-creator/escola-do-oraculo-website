#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir("c:\\Users\\XKELU27\\Downloads\\escola-do-oraculo-website")

print("[DEPLOY] Iniciando deploy para producao...")
print()

# Step 1: Add files
print("1. Adicionando ficheiros ao staging...")
result = subprocess.run(
    [
        "git",
        "add",
        "backend_server/main.py",
        "run_server_debug.py",
        "FIX_REPORT_PASSWORD_BCRYPT.md",
        "SESSION_SUMMARY.py",
    ],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    print(f"Erro: {result.stderr}")
    sys.exit(1)
print("   [OK] Ficheiros adicionados")

# Step 2: Commit
print("2. Criando commit...")
commit_msg = """Fix: Handle passwords longer than 72 bytes in bcrypt

- Added hashlib import for SHA256 hashing
- Modified get_password_hash() to hash long passwords with SHA256 first
- Modified verify_password() with same pattern
- Fixed dotenv loading in run_server_debug.py
- Resolves error: 'password cannot be longer than 72 bytes'
- All tests pass locally
- Ready for production deployment"""

result = subprocess.run(
    ["git", "commit", "-m", commit_msg], capture_output=True, text=True
)
if result.returncode != 0:
    print(f"Erro: {result.stderr}")
    sys.exit(1)
print("   [OK] Commit criado")
print(f"   Mensagem: {commit_msg.split(chr(10))[0]}")

# Step 3: Push
print("3. Fazendo push para Railway...")
result = subprocess.run(["git", "push"], capture_output=True, text=True)
if result.returncode != 0:
    print(f"Erro: {result.stderr}")
    sys.exit(1)
print("   [OK] Push concluido")

print()
print("=" * 80)
print("[SUCCESS] DEPLOY CONCLUIDO COM SUCESSO!")
print("=" * 80)
print()
print("[INFO] Proximos passos:")
print("   1. Railway vai fazer re-deploy automatico (~2-3 min)")
print("   2. Verifique os logs em: https://railway.app/dashboard")
print("   3. Procure por: 'Application startup complete'")
print("   4. Teste o signup em producao")
print()
print("[COMMANDS] Comandos uteis:")
print("   Ver logs locais: type api_debug.log")
print("   Ver logs Railway: railway logs --follow")
print("   Testar localmente: python run_server_debug.py (Terminal 1)")
print("                      python test_simple_flow.py (Terminal 2)")
print()
