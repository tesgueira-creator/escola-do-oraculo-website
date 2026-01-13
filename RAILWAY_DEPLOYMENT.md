# 🚀 Guia de Deployment no Railway

## Pré-requisitos
- ✅ Conta no Railway (railway.app)
- ✅ Projeto Git (GitHub, GitLab, ou local)
- ✅ Stripe API Keys (sk_test_...)

---

## 📋 Passo 1: Preparar o Repositório Git

Se ainda não tiver Git inicializado:

```bash
cd c:\Users\XKELU27\Downloads\escola-do-oraculo-website
git init
git add .
git commit -m "Preparado para Railway deployment"
```

Se já tem no GitHub, pule para o Passo 2.

---

## 🔐 Passo 2: Configurar Variáveis de Ambiente no Railway

1. **Crie uma conta** em https://railway.app (grátis)
2. **Crie um novo projeto**
3. **Adicione um serviço PostgreSQL:**
   - Clique em "New" → "Database" → "PostgreSQL"
   - Railway cria automaticamente a variável `DATABASE_URL`

4. **Configure as Variáveis:**
   - Vá para "Project" → "Settings" → "Variables"
   - Adicione:

```
STRIPE_SECRET_KEY=sk_test_seu_key_aqui
ENVIRONMENT=production
FRONTEND_URL=https://seu-projeto.railway.app
```

---

## 📦 Passo 3: Deploiar via Railway CLI

### Opção A: Usar Railway CLI (Recomendado)

```bash
# 1. Instale Railway CLI (Windows)
npm install -g @railway/cli

# 2. Faça login
railway login

# 3. Crie um novo projeto
railway init

# 4. Ligue a base de dados PostgreSQL
railway add postgresql

# 5. Deploie
railway up
```

### Opção B: Conectar via GitHub (Mais Fácil)

1. Faça push do repositório para GitHub
2. No Railway, clique em "New" → "GitHub Repo"
3. Selecione seu repositório
4. Railway faz deploy automaticamente
5. Configure as variáveis de ambiente (Passo 2)

---

## 📱 Passo 4: Testar

Após o deploy:

```
Frontend:  https://seu-projeto.railway.app
API:       https://seu-projeto.railway.app/auth/login
Docs:      https://seu-projeto.railway.app/docs
```

Teste o login em:
```
https://seu-projeto.railway.app/frontend/pages/login.html
```

---

## 🔄 Passo 5: Atualizações Futuras

Quando quiser fazer atualizações:

```bash
git add .
git commit -m "Nova feature"
git push

# Railway faz deploy automaticamente (se via GitHub)
```

---

## ⚠️ Importante

### Stripe Webhooks no Railway

Para receber notificações de pagamentos:

1. Vá para https://dashboard.stripe.com/webhooks
2. Adicione endpoint: `https://seu-projeto.railway.app/webhooks/stripe`
3. Selecione eventos: `checkout.session.completed`
4. Copie o **Signing Secret** e adicione como variável:

```
STRIPE_WEBHOOK_SECRET=whsec_seu_secret
```

---

## 💰 Custos

- **Free tier**: $5/mês em créditos (suficiente para começar)
- **PostgreSQL**: Incluído nos créditos
- **Depois**: Conforme o uso

---

## 🐛 Troubleshooting

**Erro: "Port already in use"**
- Railway atribui porta automaticamente (não use 8000 em produção)

**Erro: "Database connection failed"**
- Certifique-se que `DATABASE_URL` está configurada
- Verifique se PostgreSQL foi adicionado

**Erro: "Stripe key not found"**
- Configure `STRIPE_SECRET_KEY` nas Variables do Railway

**Logs:**
```bash
railway logs
```

---

## ✅ Checklist Final

- [ ] Git repositório criado
- [ ] Railway account criada
- [ ] PostgreSQL adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy bem-sucedido
- [ ] Frontend acessa a API
- [ ] Login funciona
- [ ] Stripe keys configuradas

---

**Suporte Railway:** https://docs.railway.app
