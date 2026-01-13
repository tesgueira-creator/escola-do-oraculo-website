# 🔐 STRIPE SETUP COMPLETO - INSTRUÇÕES PASSO-A-PASSO

## 📋 PASSO 1: Abrir Dashboard do Stripe

1. Vá a: https://dashboard.stripe.com
2. Login com a sua conta
3. Clique no seu nome (canto superior direito) → **Developers**

---

## 🔑 PASSO 2: Obter API Keys (Test Mode)

### Localização:
Developers → **API Keys**

### O que vai ver:
- **Publishable Key** (começa com `pk_test_`)
- **Secret Key** (começa com `sk_test_`)

### O que fazer:
1. Copie a **Secret Key** (`sk_test_...`)
2. Coloque no Railway em: **Variables** → `STRIPE_SECRET_KEY`

**⚠️ IMPORTANTE:** Use sempre `sk_test_` no desenvolvimento!

---

## 💳 PASSO 3: Criar Produtos e Preços

### Localização:
Home → **Products** (ou Products → Catalogs)

### O que fazer:

#### **Produto 1: Assinatura PRO**
1. Clique **+ Add Product**
2. **Name:** `Curso PRO - Acesso Completo`
3. **Description:** `Acesso a todos os cursos + suporte`
4. Clique **Create Product**

#### **Agora adicione um Preço:**
1. Na página do produto, clique **Add pricing option**
2. **Billing period:** `Monthly` (mensalmente)
3. **Price:** `9.99` (EUR)
4. **Recurring:** `Yes`
5. Clique **Save price**
6. **Copie o Price ID** (começa com `price_`) → Guarde num ficheiro

#### **Produto 2: Assinatura ELITE**
1. Repita o processo
2. **Name:** `Curso ELITE - Premium + Mentoria`
3. **Price:** `29.99` EUR/mês
4. **Copie o Price ID**

#### **Produto 3: Assinatura RADIESTESIA**
1. **Name:** `Radiestesia - Especializado`
2. **Price:** `14.99` EUR/mês
3. **Copie o Price ID**

---

## 🎫 PASSO 4: Configurar Restricted API Key (Segurança)

### Localização:
Developers → **API Keys** → Scroll down → **Restricted Keys**

### Crie uma Restricted Key:
1. Clique **Create Restricted Key**
2. **Name:** `Railway Backend`
3. **Permissions:**
   - ✅ `checkout.session.create` (criar pagamentos)
   - ✅ `checkout.session.read` (ler status)
   - ✅ `customer.create` (criar clientes)
   - ✅ `customer.read` (ler cliente)
   - ✅ `billing_portal.session.create` (criar portal)
4. Clique **Create**
5. **Copie a chave** (`rk_test_...`)
6. **Use esta no Railway em:** `STRIPE_SECRET_KEY`

---

## 🌐 PASSO 5: Webhooks (Notificações)

### O que são?
Avisos que o Stripe envia quando um pagamento é confirmado.

### Localização:
Developers → **Webhooks**

### Crie um Webhook:
1. Clique **+ Add an endpoint**
2. **URL:** `https://seu-projeto.railway.app/webhooks/stripe`
3. **Events to send:**
   - ✅ `checkout.session.completed` (pagamento confirmado)
   - ✅ `customer.subscription.updated` (subscrição alterada)
   - ✅ `customer.subscription.deleted` (cancelada)
4. Clique **Add endpoint**

### Obtenha o Webhook Secret:
1. Clique no endpoint criado
2. Scroll até **Signing secret**
3. Clique **Reveal** e **Copie** (começa com `whsec_test_`)
4. **Coloque no Railway em:** `STRIPE_WEBHOOK_SECRET`

---

## 🧪 PASSO 6: Modo Teste (Test Data)

### Cartões para Testar:

| Cenário            | Cartão                | Expiração | CVC   |
| ------------------ | --------------------- | --------- | ----- |
| ✅ Sucesso          | `4242 4242 4242 4242` | `12/50`   | `123` |
| ❌ Falha            | `4000 0000 0000 0002` | `12/50`   | `123` |
| ⚠️ Requer 3D Secure | `4000 0025 0000 3155` | `12/50`   | `123` |

**Use estes para testar!**

---

## 📊 PASSO 7: Visualizar Transações

### Localização:
Home → **Payments**

Aqui verá:
- ✅ Pagamentos completados
- ❌ Falhas
- ⏳ Pagamentos pendentes

---

## 💾 RESUMO: VALORES A GUARDAR

Crie um ficheiro `.env` com:

```
# Stripe Keys
STRIPE_SECRET_KEY=sk_test_... (ou rk_test_ se restricted)
STRIPE_WEBHOOK_SECRET=whsec_test_...

# Stripe Product IDs (Price IDs)
STRIPE_PRICE_PRO=price_... (de Assinatura PRO)
STRIPE_PRICE_ELITE=price_... (de Assinatura ELITE)
STRIPE_PRICE_RADIESTESIA=price_... (de Radiestesia)

# Railway
FRONTEND_URL=https://seu-projeto.railway.app
ENVIRONMENT=production
```

---

## ✅ CHECKLIST STRIPE

- [ ] API Keys copiadas
- [ ] Restricted Key criada
- [ ] 3 Produtos criados (PRO, ELITE, RADIESTESIA)
- [ ] 3 Price IDs guardados
- [ ] Webhook configurado
- [ ] Webhook Secret guardado
- [ ] Cartões de teste memo

---

## 🎯 PRÓXIMO PASSO

Quando tiver tudo guardado, diga-me e eu:
1. ✅ Atualizo o `main.py` com Customer Portal
2. ✅ Adiciono os endpoints de pagamento
3. ✅ Testo tudo localmente
4. ✅ Deploy no Railway

**Quer que comece com o código agora?**
