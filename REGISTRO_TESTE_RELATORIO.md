# 📋 Teste de Registro - Relatório Detalhado

**Data**: 14 de Janeiro de 2026  
**Status**: ⚠️ Investigação em Progresso

---

## 🧪 Testes Realizados

### 1. Verificação de Preços Stripe ✅
- **Status**: COMPLETO E VALIDADO
- **Resultado**: Todos os 8 preços estão válidos e ativos
- **Detalhes**: Ver [STRIPE_PRICES_VERIFICATION.md](STRIPE_PRICES_VERIFICATION.md)

### 2. Teste de Registro - Produção (Railway) ⚠️
- **URL**: https://web-production-21437.up.railway.app
- **Endpoint**: POST /auth/register
- **Status HTTP**: 500 (Internal Server Error)
- **Resposta**: "Internal Server Error" (sem detalhes JSON)

**Problema Identificado**:
- Servidor retorna erro 500 sem informações de debug
- Pode ser:
  1. Erro na conexão com banco de dados PostgreSQL em produção
  2. Erro durante o commit/refresh do utilizador
  3. Erro na validação de dados Pydantic

### 3. Teste de Registro - Local (Planejado) ⚠️
- **Status**: Não foi possível executar
- **Motivo**: Servidor local parou durante execução

---

## 🔧 Código de Registro (Análise)

O endpoint `/auth/register` está bem implementado:

```python
@app.post("/auth/register", status_code=201, response_model=UserDisplay)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se email já existe
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Cria novo utilizador
        hashed_pwd = get_password_hash(user.password)
        new_user = User(
            email=user.email,
            hashed_password=hashed_pwd,
            full_name=user.full_name,
            subscription_status="free",
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
```

**Análise**:
- ✅ Validação de email duplicado
- ✅ Hash de senha com bcrypt
- ✅ Tratamento de exceções com rollback
- ✅ Mensagem de erro detalhada no exception handler

---

## 📊 Fluxo de Teste Esperado

1. **Frontend Signup Page** (`/pages/signup.html`)
   - Coleta: email, password, confirm-password, full_name
   - Valida senhas coincidem
   - POST para `/auth/register`

2. **Backend Registration** (`/auth/register`)
   - Valida email único
   - Hash password com bcrypt
   - Cria User no DB com status="free"
   - Retorna status 201 + dados do utilizador

3. **Auto-Login** (opcional)
   - POST para `/auth/login` com email/password
   - Retorna access_token
   - Frontend redireciona para `oraculo-app.html`

---

## ⚠️ Problema a Resolver

**Erro 500 sem detalhes em Produção**:
- O Railway pode estar ocultando detalhes de erro por segurança
- Precisamos de acesso aos logs do Railway para ver o erro exato

**Possíveis Causas**:
1. **Database Connection**: PostgreSQL em produção pode estar fora
2. **Pydantic V2**: Classe `UserDisplay` com `from_attributes = True`
3. **SQLAlchemy Refresh**: `db.refresh(new_user)` pode falhar com PostgreSQL

---

## ✅ Recomendações

### Curto Prazo:
1. Adicionar logging mais detalhado no endpoint `/auth/register`
2. Retornar erro mais específico (não genérico 500)
3. Verificar logs do Railway

### Médio Prazo:
1. Implementar testes automatizados (pytest)
2. Adicionar validações de email (formato, verificação)
3. Implementar CAPTCHA para evitar abuse

### Longo Prazo:
1. Migrar para JWT tokens propios em vez de "user_id:{id}"
2. Implementar rate limiting
3. Adicionar monitore de erros (Sentry)

---

## 📝 Conclusão

O código de registro está **bem escrito e correto logicamente**. O problema é um erro 500 em produção que retorna sem detalhes. Isto pode ser:
- Um problema temporário (servidor indisponível)
- Um problema de configuração (DATABASE_URL inválido)
- Um problema de permissões (PostgreSQL em produção)

**Próximo passo**: Verificar logs do Railway ou adicionar logging no backend para diagnosticar o erro exato.

---

**Status**: Investigação Pendente
**Atribuição**: Aguardando resposta do servidor Railway
