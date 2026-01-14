#!/usr/bin/env python3
"""
Script para iniciar o servidor FastAPI com logging detalhado
Mostra todos os logs de debug
"""

import os
import sys
import logging
from pathlib import Path

# Carregar variáveis de ambiente
from dotenv import load_dotenv

load_dotenv()

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar logging antes de importar o app
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

print("=" * 80)
print("🚀 INICIANDO SERVIDOR FASTAPI COM LOGGING DETALHADO")
print("=" * 80)
print(f"📝 Logs serão salvos em: api_debug.log")
print(f"🌐 Servidor: http://127.0.0.1:8000")
print(f"📚 Docs: http://127.0.0.1:8000/docs")
print(f"📊 Environment: {os.getenv('ENVIRONMENT', 'development')}")
print("=" * 80)
print()

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend_server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
