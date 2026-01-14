#!/usr/bin/env python3
"""
QUICK START - Cópia rápida dos comandos mais importantes
"""

commands = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                        🚀 QUICK START DEBUGGING                               ║
╚════════════════════════════════════════════════════════════════════════════════╝

📌 PASSO 1: Abra DOIS terminais

═══════════════════════════════════════════════════════════════════════════════════

TERMINAL 1 - Iniciar Servidor com Logging Detalhado
─────────────────────────────────────────────────────────────────────────────────

Copie e cole:
    cd c:\\Users\\XKELU27\\Downloads\\escola-do-oraculo-website
    python run_server_debug.py

Esperado:
    🚀 INICIANDO SERVIDOR FASTAPI COM LOGGING DETALHADO
    📝 Logs serão salvos em: api_debug.log
    🌐 Servidor: http://127.0.0.1:8000
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

═══════════════════════════════════════════════════════════════════════════════════

TERMINAL 2 - Executar Teste Completo
─────────────────────────────────────────────────────────────────────────────────

Copie e cole:
    cd c:\\Users\\XKELU27\\Downloads\\escola-do-oraculo-website
    python test_complete_flow.py

Esperado:
    🧪 TESTE COMPLETO DE REGISTRO - SERVIDOR LOCAL
    ──────────────────────────────────────────────────
    PASSO 1: Verificando saúde da API
    ✅ API está pronta
    
    PASSO 2: Registrando novo utilizador
    ✅ Utilizador registado com sucesso!
    
    PASSO 3: Fazendo login com as credenciais
    ✅ Login realizado com sucesso!
    
    PASSO 4: Obtendo dados do utilizador logado
    ✅ Dados obtidos com sucesso!
    
    ══════════════════════════════════════════════════════════════════════
    ✅ TESTE COMPLETO SUCESSO!

═══════════════════════════════════════════════════════════════════════════════════

📝 PASSO 2: Verificar Logs Locais
─────────────────────────────────────────────────────────────────────────────────

Copie e cole para ver os logs detalhados:
    type api_debug.log

Procure por:
    ✅ "User registered successfully" = SUCESSO
    ❌ "Unexpected error during registration" = ERRO
    ❌ "Exception type:" = Tipo de erro
    ❌ "Exception message:" = Mensagem de erro

═══════════════════════════════════════════════════════════════════════════════════

🚀 PASSO 3: Deploy para Produção (Railway)
─────────────────────────────────────────────────────────────────────────────────

Se os testes passam, faça commit e push:

    cd c:\\Users\\XKELU27\\Downloads\\escola-do-oraculo-website
    git add -A
    git commit -m "Add detailed logging to registration endpoint"
    git push

Railway re-deploy automaticamente em ~2-3 minutos.

═══════════════════════════════════════════════════════════════════════════════════

🔍 PASSO 4: Verificar Logs em Produção (Railway)
─────────────────────────────────────────────────────────────────────────────────

OPÇÃO A - Via Dashboard Web:
1. Aceda: https://railway.app/dashboard
2. Clique no projecto "escola-do-oraculo-website"
3. Clique na aba "Logs"
4. Procure pelo seu email de teste (teste_...)

OPÇÃO B - Via Railway CLI:
Instale:
    npm install -g @railway/cli

Login:
    railway login

Ver logs:
    railway logs --follow

═══════════════════════════════════════════════════════════════════════════════════

🎯 RESUMO DOS FICHEIROS CRIADOS/MODIFICADOS
─────────────────────────────────────────────────────────────────────────────────

✨ MODIFICADO:
   └── backend_server/main.py
       (Adicionado logging detalhado)

✨ CRIADO:
   ├── run_server_debug.py          (Inicia servidor com debug)
   ├── test_complete_flow.py        (Teste completo)
   ├── DEBUGGING_STRATEGY.md        (Estratégia de debugging)
   ├── RAILWAY_LOGGING_GUIDE.txt    (Guia de logs Railway)
   └── RESUMO_DEBUGGING.md          (Este ficheiro)

📁 GERADO AUTOMATICAMENTE:
   └── api_debug.log                (Criado ao rodar servidor)

═══════════════════════════════════════════════════════════════════════════════════

💡 DICAS IMPORTANTES
─────────────────────────────────────────────────────────────────────────────────

1. Se o teste falhar localmente:
   → Ver api_debug.log para mensagem de erro
   → Corrigir no código
   → Testar novamente

2. Se tudo passa localmente mas falha em produção:
   → Verificar logs do Railway
   → Pode ser erro de configuração (DATABASE_URL, STRIPE_KEY)
   → Adicionar mais logging se necessário

3. Email de teste é único por timestamp:
   → teste_YYYYMMDD_HHMMSS_xxxxx@test.local
   → Sempre novo, sem conflitos

4. Ficheiro api_debug.log:
   → Guardado no directório raiz
   → Pode ficar grande (~1MB por 100 requisições)
   → Deletar se ficar muito grande

═══════════════════════════════════════════════════════════════════════════════════

📚 DOCUMENTAÇÃO
─────────────────────────────────────────────────────────────────────────────────

- DEBUGGING_STRATEGY.md      → Estratégia completa
- RAILWAY_LOGGING_GUIDE.txt  → Como usar Railway logs
- RESUMO_DEBUGGING.md        → Resumo executivo
- api_debug.log              → Logs detalhados

═══════════════════════════════════════════════════════════════════════════════════

✅ VOCÊ ESTÁ PRONTO PARA:

1. ✅ Testar localmente com logs detalhados
2. ✅ Identificar exactamente onde falha
3. ✅ Deploy para produção com confiança
4. ✅ Monitorar logs em tempo real
5. ✅ Debugar problemas rapidamente

═══════════════════════════════════════════════════════════════════════════════════
"""

print(commands)

# Salvar em ficheiro também
with open("QUICK_START.txt", "w", encoding="utf-8") as f:
    f.write(commands)

print("\\n✅ Salvo também em: QUICK_START.txt")
