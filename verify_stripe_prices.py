#!/usr/bin/env python3
"""
Script para verificar se todos os preços do Stripe configurados são válidos e reais
"""

import os
import sys
import stripe
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    print("❌ ERRO: STRIPE_SECRET_KEY não configurada!")
    sys.exit(1)

stripe.api_key = STRIPE_SECRET_KEY

# Preços configurados no frontend
CONFIGURED_PRICES = {
    "pro": "price_1SpAOPHvoxa2NZ5dMc6vbBMM",
    "elite": "price_1SpAOQHvoxa2NZ5dF53uAU6W",
    "radiestesia": "price_1SpAOQHvoxa2NZ5dgts3Mso4",
    "modulo1": "price_1SpVH4Hvoxa2NZ5dFcMeOE7S",
    "modulo2": "price_1SpVH5Hvoxa2NZ5dj5yi8TCH",
    "modulo3": "price_1SpVH6Hvoxa2NZ5dUjeO5b1W",
    "kundalini": "price_1SpVH6Hvoxa2NZ5d6VPFgClM",
    "terapia-multidimensional": "price_1SpVH7Hvoxa2NZ5dF8NMEjpo",
}

print("=" * 60)
print("🔍 VERIFICANDO PREÇOS DO STRIPE")
print("=" * 60)
print(f"\n📊 Total de preços configurados: {len(CONFIGURED_PRICES)}\n")

valid_prices = []
invalid_prices = []

for name, price_id in CONFIGURED_PRICES.items():
    try:
        price = stripe.Price.retrieve(price_id)

        # Extrair informações
        product_id = price.product
        amount = price.unit_amount / 100  # Converter centavos para unidades
        currency = price.currency.upper()
        recurring = price.recurring

        # Formatar informações de recorrência
        if recurring:
            interval = recurring.get("interval", "unknown").upper()
            recurring_text = f"{interval}"
            if recurring.get("interval_count", 1) > 1:
                recurring_text = f"A CADA {recurring.get('interval_count')} {interval}S"
        else:
            recurring_text = "UMA VEZ (sem recorrência)"

        # Obter informações do produto
        product = stripe.Product.retrieve(product_id)
        product_name = product.name

        print(f"✅ {name.upper()}")
        print(f"   Price ID: {price_id}")
        print(f"   Produto: {product_name}")
        print(f"   Valor: {amount} {currency}")
        print(f"   Recorrência: {recurring_text}")
        print(f"   Ativo: {'Sim' if price.active else 'Não'}")
        print()

        valid_prices.append(
            {
                "name": name,
                "price_id": price_id,
                "product_name": product_name,
                "amount": amount,
                "currency": currency,
                "recurring": recurring_text,
                "active": price.active,
            }
        )

    except stripe.error.InvalidRequestError as e:
        print(f"❌ {name.upper()}")
        print(f"   Price ID: {price_id}")
        print(f"   ❌ ERRO: {str(e)}\n")
        invalid_prices.append({"name": name, "price_id": price_id, "error": str(e)})
    except Exception as e:
        print(f"❌ {name.upper()}")
        print(f"   Price ID: {price_id}")
        print(f"   ❌ ERRO DESCONHECIDO: {str(e)}\n")
        invalid_prices.append({"name": name, "price_id": price_id, "error": str(e)})

# Resumo
print("=" * 60)
print("📋 RESUMO")
print("=" * 60)
print(f"✅ Preços válidos: {len(valid_prices)}/{len(CONFIGURED_PRICES)}")
print(f"❌ Preços inválidos: {len(invalid_prices)}/{len(CONFIGURED_PRICES)}")

if invalid_prices:
    print("\n⚠️  PREÇOS COM PROBLEMA:")
    for item in invalid_prices:
        print(f"   - {item['name']}: {item['error']}")
else:
    print("\n✅ TODOS OS PREÇOS ESTÃO VÁLIDOS!")

# Salvar relatório
with open("STRIPE_PRICES_VERIFICATION.md", "w", encoding="utf-8") as f:
    f.write("# 💳 Verificação de Preços do Stripe\n\n")
    f.write(
        f"**Data**: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    )

    f.write("## ✅ Preços Válidos\n\n")
    for price in valid_prices:
        f.write(f"### {price['name'].upper()}\n")
        f.write(f"- **Price ID**: `{price['price_id']}`\n")
        f.write(f"- **Produto**: {price['product_name']}\n")
        f.write(f"- **Valor**: {price['amount']} {price['currency']}\n")
        f.write(f"- **Recorrência**: {price['recurring']}\n")
        f.write(f"- **Ativo**: {'Sim ✅' if price['active'] else 'Não ❌'}\n\n")

    if invalid_prices:
        f.write("## ❌ Preços Inválidos\n\n")
        for item in invalid_prices:
            f.write(f"### {item['name'].upper()}\n")
            f.write(f"- **Price ID**: `{item['price_id']}`\n")
            f.write(f"- **Erro**: {item['error']}\n\n")

    f.write(f"\n## 📊 Resumo\n")
    f.write(f"- Preços válidos: {len(valid_prices)}/{len(CONFIGURED_PRICES)}\n")
    f.write(f"- Preços inválidos: {len(invalid_prices)}/{len(CONFIGURED_PRICES)}\n")

print("\n📄 Relatório salvo em: STRIPE_PRICES_VERIFICATION.md")
print("=" * 60)

sys.exit(0 if len(invalid_prices) == 0 else 1)
