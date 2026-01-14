# 🔧 Plano de Debugging - Erro 500 no Registro

**Data**: 14 de Janeiro de 2026  
**Status**: Investigação em Progresso

---

## 📊 Problema Identificado

```
POST /auth/register
Status: 500 Internal Server Error
Response: "Internal Server Error" (sem detalhes JSON)
Ambiente: Production (Railway)
```

---

## ✅ Soluções Implementadas

### 1. ✅ Logging Detalhado no Backend

Adicionado logging em múltiplos níveis no endpoint `/auth/register`:

```python
@app.post("/auth/register", status_code=201, response_model=UserDisplay)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"📝 Registration attempt for email: {user.email}")
    
    # Step 1: Verificar se email existe
    logger.debug(f"Step 1: Checking if user {user.email} already exists")
    
    # Step 2: Hash password
    logger.debug(f"Step 2: Hashing password for {user.email}")
    
    # Step 3: Criar objeto User
    logger.debug(f"Step 3: Creating User object for {user.email}")
    
    # Step 4: Adicionar ao session
    logger.debug(f"Step 4: Adding user to database session")
    
    # Step 5: Commit
    logger.debug(f"Step 5: Committing to database")
    
    # Step 6: Refresh
    logger.debug(f"Step 6: Refreshing user object from database")
    
    # Sucesso
    logger.info(f"✅ User registered successfully: {new_user.email} (ID: {new_user.id})")
```

**Benefício**: Cada passo será registado, mostrando exactamente onde falha.

### 2. ✅ Arquivo de Log Local

- **Ficheiro**: `api_debug.log`
- **Localização**: Raiz do projecto
- **Conteúdo**: Todos os logs DEBUG, INFO, WARNING, ERROR
- **Formato**: Timestamp - Logger - Level - Mensagem

### 3. ✅ Script de Teste Local Completo

**Ficheiro**: `test_complete_flow.py`

Testa o fluxo completo:
1. Health check
2. Registro
3. Login
4. Obtenção de dados do utilizador

Com mensagens detalhadas e saída amigável.

### 4. ✅ Script para Iniciar Servidor com Debug

**Ficheiro**: `run_server_debug.py`

Inicia o servidor com:
- `--reload` ativado (auto-restart ao mudar código)
- `log_level="debug"` (máximo detalhe)
- Logging para stdout e ficheiro

---

## 🚀 Como Usar

### Teste Local Completo

**Terminal 1 - Inicia servidor:**
```bash
python run_server_debug.py
```

**Terminal 2 - Executa teste:**
```bash
python test_complete_flow.py
```

**Resultado esperado:**
- Todos os testes passam (✅)
- Arquivo `api_debug.log` criado com logs detalhados

### Verificar Logs do Railway

**Opção 1 - Dashboard Web:**
1. Aceda: https://railway.app/dashboard
2. Seleccione projecto
3. Aba "Logs"
4. Procure pelo timestamp do erro

**Opção 2 - CLI do Railway:**
```bash
npm install -g @railway/cli
railway login
railway logs --follow
```

---

## 🔍 Possíveis Causas e Soluções

| Causa                       | Sintoma               | Solução                          |
| --------------------------- | --------------------- | -------------------------------- |
| **Database desconectado**   | 500 erro imediato     | Verificar PostgreSQL em Railway  |
| **DATABASE_URL inválido**   | 500 erro imediato     | Verificar variáveis de ambiente  |
| **Erro Pydantic**           | 422 erro de validação | Verificar tipos de dados         |
| **Erro bcrypt**             | 500 erro ao hash      | Verificar permissões do servidor |
| **Erro SQLAlchemy refresh** | 500 erro após commit  | Usar `db.expunge_all()` antes    |
| **Email duplicado**         | 400 erro esperado     | Testar com novo email            |

---

## 📝 Passos de Ação

### Passo 1: Testar Localmente ✅
```bash
# Terminal 1
python run_server_debug.py

# Terminal 2
python test_complete_flow.py
```

**Resultado esperado:**
```
✅ TESTE COMPLETO SUCESSO!

🎉 Fluxo de Registro Funcionando Perfeitamente:
   1. ✅ Health Check
   2. ✅ Registro de Novo Utilizador
   3. ✅ Login
   4. ✅ Obtenção de Dados do Utilizador
```

### Passo 2: Verificar Logs Locais
```bash
# Verificar api_debug.log
type api_debug.log
```

Procurar por:
- `❌ Unexpected error during registration`
- `Exception type: ...`
- `Exception message: ...`
- Stack trace completo

### Passo 3: Deploy para Railway

Se os testes locais passam:
```bash
git add -A
git commit -m "Add detailed logging to registration endpoint"
git push
# Railway faz re-deploy automaticamente
```

### Passo 4: Verificar Logs em Produção

Acede ao Railway dashboard:
- Procura pelo novo email de teste
- Verifica a resposta do servidor
- Copia a mensagem de erro completa

### Passo 5: Corrigir e Repetir

Se encontrar erro:
1. Corrige no código
2. Testa localmente
3. Deploy para produção
4. Verifica logs

---

## 📊 Arquivos Criados

| Ficheiro                    | Propósito                           |
| --------------------------- | ----------------------------------- |
| `backend_server/main.py`    | ✨ Atualizado com logging            |
| `run_server_debug.py`       | 🚀 Inicia servidor com debug         |
| `test_complete_flow.py`     | 🧪 Teste completo do fluxo           |
| `api_debug.log`             | 📝 Logs detalhados (criado ao rodar) |
| `RAILWAY_LOGGING_GUIDE.txt` | 📖 Guia de logs do Railway           |

---

## ✨ Melhorias Futuras

1. **Monitoramento**: Integrar Sentry para capturar erros em produção
2. **Métricas**: Adicionar Prometheus para monitorar performance
3. **Testes Automatizados**: Criar suite de testes com pytest
4. **CI/CD**: Executar testes antes de deploy

---

## 🎯 Conclusão

Com estas mudanças:
1. ✅ Temos logging detalhado em cada passo
2. ✅ Podemos testar localmente antes de deploy
3. ✅ Podemos verificar logs em produção
4. ✅ Sabemos exactamente onde falha o código

**Próximo passo**: Executar `test_complete_flow.py` para confirmar que funciona localmente.
