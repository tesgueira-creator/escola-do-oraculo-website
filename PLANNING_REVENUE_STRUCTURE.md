# Planeamento Estratégico: Escola do Oráculo & Método Kally

Este documento detalha a reestruturação completa do website para focar na marca pessoal "Rafaella Kally", no "Método Kally" e na implementação de um modelo de negócio baseado em subscrições e vendas de cursos.

---

## 1. Identidade e Posicionamento (O "Método Kally")

**Objetivo:** Transformar a Home Page numa vitrine de autoridade e conversão.

### Pilares do Conteúdo:
1.  **Radiestesia e Radiônica:** Foco na Mesa Radiónica de Arcanjo Miguel. Ferramenta de harmonização e limpeza energética.
2.  **Kundalini Reiki:** Rafaella Kally como Mestre. Foco em cura energética, desbloqueio de chakras e despertar espiritual.
3.  **Terapia Multidimensional:** A "Cura pelo Coração". Foco em cura emocional e kármica.
4.  **Tarot Terapêutico:** O Tarot não como adivinhação fútil, mas como ferramenta de autoconhecimento e orientação (O Oráculo).

### Estrutura da Nova Home Page (`index.html`):
*   **Hero Section:** "Desperte a sua Mestra Interior com o Método Kally." (Botão: "Começar Jornada Gratuitamente").
*   **Sobre a Rafaella Kally:** Biografia curta destacando as certificações (Mestre Kundalini, Mestre em Terapia Multidimensional e Tarot).
*   **O Método:** Explicação de como as 4 vertentes se unem.
*   **Vitrine de Cursos:** Cards para cada modalidade (Radiestesia, Reiki, Tarot).
*   **Área de Membros (Teaser):** "Acesse o Templo Virtual - Leituras diárias e Ferramentas exclusivas".

---

## 2. Modelo de Negócio e Revenue (Receita)

Implementaremos um sistema híbrido de monetização.

### A. Venda de Infoprodutos (Cursos)
*   **Produto:** Acesso vitalício ou anual a cursos específicos (ex: Curso de Tarot Módulo 1).
*   **Entrega:** Acesso a páginas protegidas (`pages/modulo-1.html`, etc.).
*   **Gateway de Pagamento Sugerido:** Stripe ou PayPal (integração via botões de checkout na página `checkout.html`).

### B. Subscrição Mensal ("Círculo do Oráculo" / "Templo Kally")
*   **Proposta de Valor:** Ferramentas digitais de uso recorrente e comunidade.
*   **Custo Sugerido:** €9,90/mês ou €97/ano.
*   **Benefícios:**
    *   **Oráculos Ilimitados:** Acesso às tiragens complexas (Cruz Celta, Chakras, Mandala Astrológica).
    *   **Limitação Diária (Gamification):** "Energia Diária" - O utilizador pode fazer 1 grande leitura por dia para manter a sacralidade, ou ilimitado conforme a estratégia.
    *   **Descontos em Consultas:** 10-20% off em consultas 1:1 com a Rafaella.

---

## 3. Arquitetura Técnica Proposta

### Estrutura de Pastas e Navegação

1.  **Público (Frontend Aberto):**
    *   `index.html`: Landing Page Principal (Vendas & Branding).
    *   `sobre.html`: História da Rafaella e Certificações.
    *   `cursos.html`: Catálogo de cursos com botões de compra.
    *   `blog.html`: Artigos SEO sobre Radiônica, Reiki, etc. (Atração de tráfego).

2.  **Área de Login / Autenticação:**
    *   `login.html`: Entrada de alunos.
    *   `register.html`: Criação de conta.
    *   *Tecnologia:* Simulação via LocalStorage (fase 1) ou Integração com Firebase/Auth0 (fase 2 profissional).

3.  **Área do Cliente (Privada - "O Templo"):**
    *   `app/dashboard.html`: Painel principal do aluno. Resumo do progresso.
    *   `app/oraculo.html`: A ferramenta de Tarot atual (migrada do index para cá).
        *   *Lógica:* Tirares Simples (Gratuito no index) vs. Tirares Avançados (Aqui).
    *   `app/mesa-radionica.html`: (Nova Funcionalidade) Um simulador visual de mesa radiônica onde o usuário clica para "enviar frequências" (uso diário).
    *   `app/meditacao.html`: Áudios de Kundalini Reiki.

### Fluxo de Conversão (Funnel)
1.  Visitante chega na Home.
2.  Lê sobre "Método Kally".
3.  Experimenta o "Tarot Diário" (Gratuito, captura email no final).
4.  Recebe sequência de emails (Automação).
5.  Compra o acesso ao "Círculo" ou um Curso.

---

## 4. Funcionalidades e Lógica

### A. Sistema de Cobranças e Forms
*   **Captura de Leads:** Integração do Formspree (já existente) para uma "Newsletter Espiritual".
*   **Checkout:** Criar página de checkout profissional (`frontend/pages/checkout-pro.html`) com, por exemplo, Stripe Payment Links.
*   **Automação de Email:**
    *   *Email 1 (Boas-vindas):* Link para o E-book gratuito ou Tiragem Grátis.
    *   *Email 2 (Nutrição):* Explicando o que é a Mesa Radiônica de Arcanjo Miguel.
    *   *Email 3 (Venda):* Convite para o curso completo.

### B. Funcionalidades da Área de Membros
1.  **Tarot Premium:**
    *   Salvar leituras no histórico (Cloud/LocalStorage).
    *   Diário (Journaling) de sentimentos pós-leitura.
2.  **Régua de Limitação:**
    *   *Lógica:* `if (user.subscription !== 'active' && dailyReadings > 1) { showPaywall(); }`

---

## 5. Próximos Passos Imediatos de Desenvolvimento

1.  **Re-design da Home (`index.html`):** Remover a ferramenta de tarot do topo. Colocar a "Promessa" e a "Biografia". Mover o Tarot para uma secção "Experimente Grátis" mais abaixo ou página dedicada.
2.  **Criar Página de Login/Registo:** Estrutura HTML/CSS.
3.  **Configurar Área de Membros:** Criar o layout (`dashboard`) que verifica se o usuário está "logado".
4.  **Implementar Lógica de Assinatura (Simulada):** Um botão "Assinar Premium" que "libera" as funcionalidades avançadas no LocalStorage para testes.

---
*Documento Gerado por GitHub Copilot - 13/01/2026*
