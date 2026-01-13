# Análise Completa e Planeamento de Backend (Escola do Oráculo)

## 1. Visão Geral
O website atual é um Frontend estático (HTML/JS) que simula interatividade. Para tornar o projeto funcional ("Real"), é necessário implementar um Backend (Servidor + Base de Dados) que gerencie Identidade (Quem é o usuário), Permissões (O que ele pagou) e Dados (O histórico dele).

---

## 2. Auditoria e Correções Necessárias no Frontend
Para conectar ao Backend, os formulários HTML precisam de atributos `name` e `id` corretos.

### A. Página de Login (`frontend/pages/login.html`)
*   **Estado Atual:** Inputs genéricos sem identificação.
*   **Ação Necessária:**
    *   Adicionar `name="email"` e `id="email"` ao campo de email.
    *   Adicionar `name="password"` e `id="password"` ao campo de senha.
    *   Mudar o formulário para enviar dados via AJAX (Fetch API) para `/api/auth/login`.

### B. Página de Planos/Checkout (`frontend/pages/checkout-pro.html`)
*   **Estado Atual:** Funções JS simuladas (`subscribe('monthly')`).
*   **Ação Necessária:**
    *   Integrar **Stripe Payment Links** reais ou botão de redirecionamento.
    *   Criar lógica de callback: Se o pagamento for sucesso, o Stripe avisa o Backend (Webhook), e o Backend atualiza o status do usuário.

### C. Aplicação Principal (`frontend/pages/oraculo-app.html`)
*   **Estado Atual:** Verificação de acesso via `localStorage` (inseguro, qualquer um pode editar).
*   **Ação Necessária:**
    *   Validar token JWT real no carregamento (`GET /api/users/me`).
    *   Adicionar botão "Salvar Leitura" que chama `POST /api/readings`.
    *   Adicionar secção "Meu Histórico" que chama `GET /api/readings`.

### D. Formulários de Captura (Proposto)
*   Criar `frontend/components/newsletter-form.html` para capturar leads na Home Page.

---

## 3. Planeamento da Arquitetura Backend

Recomenda-se uma arquitetura **Python (FastAPI)** ou **Node.js (Express)** pela facilidade de manutenção e integração com o sistema atual. Abaixo, detalho a estrutura de dados.

### A. Base de Dados (Schema Simplificado)

**Tabela: Users (Utilizadores)**
| Campo                   | Tipo   | Descrição                            |
| :---------------------- | :----- | :----------------------------------- |
| `id`                    | UUID   | Identificador único                  |
| `email`                 | String | Email de login                       |
| `password_hash`         | String | Senha criptografada                  |
| `subscription_status`   | Enum   | `FREE`, `MONTHLY`, `YEARLY`, `ADMIN` |
| `subscription_end_date` | Date   | Validade do acesso                   |

**Tabela: Readings (Histórico de Leituras)**
| Campo         | Tipo     | Descrição                        |
| :------------ | :------- | :------------------------------- |
| `id`          | UUID     | ID da leitura                    |
| `user_id`     | UUID     | Quem fez a leitura               |
| `spread_type` | String   | Tipo (Cruz Celta, 3 Cartas, etc) |
| `cards_drawn` | JSON     | Lista das cartas (IDs)           |
| `notes`       | Text     | Diário/Anotações do usuário      |
| `created_at`  | DateTime | Data da leitura                  |

---

## 4. API Endpoints (Mapa de Funcionalidades)

### Autenticação
*   `POST /auth/register` - Criar conta nova.
*   `POST /auth/login` - Receber Token de Acesso (JWT).
*   `POST /auth/refresh` - Manter sessão ativa.
*   `POST /auth/forgot-password` - Disparar email de recuperação.

### Pagamentos (Stripe)
*   `POST /payments/create-checkout-session` - Iniciar pagamento.
*   `POST /payments/webhook` - Receber confirmação automática do Stripe.

### Funcionalidades do Oráculo
*   `GET /users/me` - Perfil e Status da Subscrição.
*   `POST /readings` - Salvar uma tiragem no histórico.
*   `GET /readings` - Listar minhas tiragens passadas.

---

## 5. Próximos Passos de Implementação (Roadmap)

1.  **Fase 1 (Estrutura):** Criar pastas do servidor python (`backend_api/`).
2.  **Fase 2 (Login):** Implementar Registo e Login real com base de dados SQLite local.
3.  **Fase 3 (Frontend Wiring):** Modificar o HTML para falar com esse servidor local.
4.  **Fase 4 (Pagamentos):** Conectar com conta Stripe de teste.

Este documento serve como guia mestre para o desenvolvimento do backend.
