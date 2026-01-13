import stripe
import os

# Configurar a chave API (fornecida pelo utilizador)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_catalog():
    print("🚀 A iniciar configuração automática do Stripe...")

    products_to_create = [
        {
            "name": "Curso PRO - Acesso Completo",
            "description": "Acesso a todos os cursos + suporte",
            "amount": 999,  # €9.99
            "currency": "eur",
            "interval": "month",
        },
        {
            "name": "Curso ELITE - Premium + Mentoria",
            "description": "Premium + acesso a mentoria exclusiva",
            "amount": 2999,  # €29.99
            "currency": "eur",
            "interval": "month",
        },
        {
            "name": "Radiestesia - Especializado",
            "description": "Curso completo de Radiestesia",
            "amount": 1499,  # €14.99
            "currency": "eur",
            "interval": "month",
        },
    ]

    generated_env_content = f"STRIPE_SECRET_KEY={stripe.api_key}\nSTRIPE_PUBLISHABLE_KEY=pk_test_51SpAFIHvoxa2NZ5dTkjFDoDVcno97EaJTVy0mHU4TIheB8380bIPfoOBGVCV4u4eEYiCn3bMJpFfSMqTQDs5pSYb00ATRq3XLz\n\n"

    for p in products_to_create:
        try:
            print(f"📦 A criar produto: {p['name']}...")

            # 1. criar produto
            product = stripe.Product.create(
                name=p["name"], description=p["description"]
            )

            # 2. criar preço
            price = stripe.Price.create(
                product=product.id,
                unit_amount=p["amount"],
                currency=p["currency"],
                recurring={"interval": p["interval"]},
            )

            print(f"   ✅ Sucesso! Price ID: {price.id}")

            # Adicionar ao conteúdo do .env
            env_var_name = (
                "STRIPE_PRICE_" + p["name"].split()[1].upper()
            )  # ex: STRIPE_PRICE_PRO
            if "Radiestesia" in p["name"]:
                env_var_name = "STRIPE_PRICE_RADIESTESIA"

            generated_env_content += f"{env_var_name}={price.id}\n"

        except Exception as e:
            print(f"   ❌ Erro ao criar {p['name']}: {str(e)}")

    print("\n📝 A gerar ficheiro .env com as chaves...")

    with open(".env", "w", encoding="utf-8") as f:
        f.write(generated_env_content)
        f.write("ENVIRONMENT=production\n")
        # Placeholder para o URL do Railway
        f.write("FRONTEND_URL=https://seu-projeto.railway.app\n")

    print("✅ Configuração concluída! Verifique o ficheiro .env")
    print(
        "\n⚠️ IMPORTANTE: O Webhook deve ser configurado manualmente após o deploy no Railway,"
    )
    print(
        "   pois precisamos do URL final (ex: https://projeto.railway.app/webhooks/stripe)."
    )


if __name__ == "__main__":
    create_stripe_catalog()
