#!/usr/bin/env python3
"""
Script to create Stripe products and prices for Escola do Oráculo courses.
"""
import stripe
import os
import sys

# Use your Stripe secret key from environment variable
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    print("❌ Error: STRIPE_SECRET_KEY environment variable not set")
    print("Please set it with: $env:STRIPE_SECRET_KEY='sk_test_...'")
    sys.exit(1)

stripe.api_key = STRIPE_SECRET_KEY

# Define the courses
courses = [
    {
        "name": "Módulo 1: A Base do Oráculo",
        "description": "Domine os 22 Arcanos Maiores e os 4 Naipes. Curso completo com 8-10 horas de conteúdo em vídeo + Certificado.",
        "amount": 2900,  # €29.00 in cents
        "currency": "eur",
        "metadata": {"type": "course", "module": "1"},
    },
    {
        "name": "Módulo 2: O Método Kally",
        "description": "Prática Intensiva e Desenvolvimento da Intuição. 10-12 horas de conteúdo + Comunidade + Certificado.",
        "amount": 4900,  # €49.00 in cents
        "currency": "eur",
        "metadata": {"type": "course", "module": "2"},
    },
    {
        "name": "Módulo 3: Profissionalização",
        "description": "Como Estruturar e Monetizar Seu Negócio de Tarot. 12-14 horas + Templates + Certificado.",
        "amount": 6900,  # €69.00 in cents
        "currency": "eur",
        "metadata": {"type": "course", "module": "3"},
    },
    {
        "name": "Kundalini Reiki - Curso Completo",
        "description": "Níveis 1, 2 e 3 (Mestrado). Inclui as 3 sintonizações à distância + Certificado.",
        "amount": 15000,  # €150.00 in cents
        "currency": "eur",
        "metadata": {"type": "course", "specialty": "kundalini"},
    },
    {
        "name": "Terapia Multidimensional",
        "description": "Formação de Terapeuta Multidimensional. A Cura pelo Coração + Certificado.",
        "amount": 18000,  # €180.00 in cents
        "currency": "eur",
        "metadata": {"type": "course", "specialty": "terapia"},
    },
]


def create_products_and_prices():
    """Create products and one-time payment prices in Stripe."""
    results = {}

    print("🔄 Creating Stripe products and prices...\n")

    for course in courses:
        try:
            # Create product
            product = stripe.Product.create(
                name=course["name"],
                description=course["description"],
                metadata=course["metadata"],
            )

            print(f"✅ Product created: {product.name}")
            print(f"   Product ID: {product.id}")

            # Create price (one-time payment)
            price = stripe.Price.create(
                product=product.id,
                unit_amount=course["amount"],
                currency=course["currency"],
                metadata=course["metadata"],
            )

            print(f"✅ Price created: €{course['amount']/100:.2f}")
            print(f"   Price ID: {price.id}\n")

            # Determine the key name for checkout.html
            if "module" in course["metadata"]:
                key = f"modulo{course['metadata']['module']}"
            elif course["metadata"]["specialty"] == "kundalini":
                key = "kundalini"
            elif course["metadata"]["specialty"] == "terapia":
                key = "terapia-multidimensional"

            results[key] = price.id

        except stripe.error.StripeError as e:
            print(f"❌ Error creating {course['name']}: {e}")
            sys.exit(1)

    return results


def print_checkout_config(results):
    """Print the configuration for checkout.html"""
    print("\n" + "=" * 70)
    print("📝 Update checkout.html with these Price IDs:")
    print("=" * 70 + "\n")

    print("const PRICE_IDS = {")
    print("  // Subscrições")
    print('  pro: "price_1SpAOPHvoxa2NZ5dMc6vbBMM", // Círculo do Oráculo - €9.90/mês')
    print(
        '  elite: "price_1SpAOQHvoxa2NZ5dF53uAU6W", // Pack Completo Tarot - €97 (anual)'
    )
    print("  // Cursos individuais")
    print('  radiestesia: "price_1SpAOQHvoxa2NZ5dgts3Mso4", // Mesa Radiónica - €120')
    print("  // Módulos de Tarot")
    print(f'  modulo1: "{results["modulo1"]}", // Módulo 1 - €29')
    print(f'  modulo2: "{results["modulo2"]}", // Módulo 2 - €49')
    print(f'  modulo3: "{results["modulo3"]}", // Módulo 3 - €69')
    print("  // Outros cursos")
    print(f'  kundalini: "{results["kundalini"]}", // Kundalini Reiki - €150')
    print(
        f'  "terapia-multidimensional": "{results["terapia-multidimensional"]}", // Terapia Multidimensional - €180'
    )
    print("};")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("🚀 Escola do Oráculo - Stripe Product & Price Creator\n")

    try:
        results = create_products_and_prices()
        print_checkout_config(results)

        # Save results to a file
        with open("stripe_price_ids.txt", "w", encoding="utf-8") as f:
            f.write("STRIPE PRICE IDS - Escola do Oráculo\n")
            f.write("=" * 50 + "\n\n")
            for key, price_id in results.items():
                f.write(f"{key}: {price_id}\n")

        print("\n✅ Price IDs saved to stripe_price_ids.txt")
        print("\n🎉 All done! Copy the PRICE_IDS object above into checkout.html")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
