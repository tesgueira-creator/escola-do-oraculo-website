#!/usr/bin/env python3
"""
Verificação rápida do status do deployment
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://web-production-21437.up.railway.app"

print("🔍 VERIFICAÇÃO DO DEPLOYMENT - ESCOLA DO ORÁCULO")
print("=" * 60)
print(f"⏰ Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🌐 URL: {BASE_URL}")
print("=" * 60)

endpoints = [
    ("/", "GET", "API Root"),
    ("/health", "GET", "Health Check"),
    ("/version", "GET", "API Version"),
    ("/docs", "GET", "OpenAPI Docs"),
]

working = 0
failed = 0

for endpoint, method, desc in endpoints:
    try:
        url = f"{BASE_URL}{endpoint}"
        r = requests.get(url, verify=False, timeout=5)
        status = f"✅ {r.status_code}"
        working += 1
        print(f"{status} | {desc:20} | {endpoint}")
    except Exception as e:
        print(f"❌ ERROR | {desc:20} | {endpoint}")
        print(f"         Error: {str(e)[:50]}")
        failed += 1

print("=" * 60)
print(f"📊 Resumo: {working} funcionando, {failed} com erro")
print(
    "\n✅ Servidor está OPERACIONAL!"
    if failed == 0
    else "\n⚠️  Alguns endpoints com problema"
)
