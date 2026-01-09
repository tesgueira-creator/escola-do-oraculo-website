# Escola do Oráculo - Website

Plataforma web completa para a **Escola do Oráculo**, oferecendo cursos de tarot online, leituras interativas e comunidade exclusiva.

## 🎯 Sobre o Projeto

Este é um website estático desenvolvido em **HTML, CSS e JavaScript** (sem dependências externas) para uma escola de tarot online. Oferece:

- **3 Módulos de Cursos** com conteúdo detalhado
- **Leitura Interativa de Tarot** com deck completo de 78 cartas
- **Comunidade Exclusiva** (Círculo do Oráculo)
- **Sistema de Inscrição** com carrinho de compras simplificado
- **Design Responsivo** e elegante
- **Totalmente Customizável**

## 📁 Estrutura de Ficheiros

```
escola-do-oraculo-website/
├── index.html                 # Página principal (antiga "Escola do Oráculo Website (1).html")
├── modulo-1.html              # Módulo 1: A Base do Oráculo
├── modulo-2.html              # Módulo 2: O Método Kally
├── modulo-3.html              # Módulo 3: Profissionalização
├── circulo.html               # Círculo do Oráculo (comunidade)
├── checkout.html              # Página de inscrição/checkout
├── Tarot_Real_Cards.html      # Leitor de tarot standalone
├── README.md                  # Este ficheiro
├── .gitignore                 # Ficheiros a ignorar no Git
└── assets/                    # (Opcional) Pasta para imagens/recursos
```

## 🚀 Como Usar

### Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/escola-do-oraculo-website.git
   cd escola-do-oraculo-website
   ```

2. Abra qualquer ficheiro `.html` diretamente no browser:
   - `index.html` – Página principal
   - `modulo-1.html`, `modulo-2.html`, `modulo-3.html` – Módulos individuais
   - `circulo.html` – Comunidade
   - `checkout.html` – Inscrição para o bundle

### Hospedagem Online

Hospede num serviço gratuito como:
- **GitHub Pages** (configure no repositório)
- **Netlify** (drag-and-drop)
- **Vercel** (deployment automático)
- **Hostinger, Bluehost**, etc.

## 🎨 Características Principais

### 1. **Página Principal (index.html)**
- Hero section inspirador
- Leitor de tarot interativo com múltiplas spreads (Diária, 3 Cartas, Cruz Celta)
- Showcase dos 3 módulos
- Testimoniais de alunos
- FAQ completo
- Secção de contacto
- Rodapé com links sociais (Instagram)

### 2. **Páginas de Módulos (modulo-1.html, modulo-2.html, modulo-3.html)**
- Descrição detalhada do conteúdo
- Duração e formato
- Preço com desconto
- Benefícios inclusos
- Botão de inscrição por email

### 3. **Página do Círculo (circulo.html)**
- Descrição da comunidade exclusiva
- 6 principais benefícios
- Preço de subscrição mensal
- Critérios de adesão

### 4. **Página de Checkout (checkout.html)**
- Formulário de inscrição completo
- Resumo da encomenda em tempo real
- Itens inclusos do bundle
- Redirecionamento para email ou payment gateway

### 5. **Leitor de Tarot (Tarot_Real_Cards.html)**
- Deck completo com 78 cartas reais (Rider–Waite–Smith)
- Múltiplas spreads (Diária, 3 Cartas, Cruz Celta, Amor, 5 Cartas, Ferradura)
- Histórico de leituras (localStorage)
- Imagens de qualidade via Wikimedia Commons

## 🎨 Design & Cores

O website usa um esquema de cores elegante e profissional:

- **Roxo Escuro** (#4b0082) – Cor primária, mística
- **Ouro** (#c5a059) – Acentos, destaque
- **Creme** (#f5f5f0) – Fundo principal
- **Tipografia**: Georgia (serif) para títulos, Segoe UI (sans-serif) para corpo

## 🔧 Tecnologias

- **HTML5** – Estrutura semântica
- **CSS3** – Responsive design, gradientes, animações
- **JavaScript Vanilla** – Sem dependências externas
- **localStorage** – Persistência de dados (histórico de tarot)

## 📱 Responsividade

- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

## 💳 Sistema de Inscrição

O website usa **email para inscrições** (fallback simples). Para implementar pagamento real:

1. Integre um gateway: **Stripe**, **PayPal**, **Wise**, **2Checkout**
2. Modifique o formulário em `checkout.html`
3. Adicione validação no backend (opcional)

## 📧 Email de Contacto

Atualize o email de contacto em todos os ficheiros. Procure por:
```html
contacto@rafaellakally.com
```

E substitua pelo seu email real.

## 🔐 Segurança & Privacidade

- Sem armazenamento de dados sensíveis
- Histórico do tarot armazenado localmente (browser)
- GDPR-compliant (sem cookies de rastreamento)
- Política de privacidade disponível em `index.html#politica`

## 📝 Customização

### Alterar Cores
Abra qualquer ficheiro e procure por:
```css
:root {
  --color-cream: #f5f5f0;
  --color-dark-purple: #4b0082;
  --color-gold: #c5a059;
  ...
}
```

### Alterar Conteúdo
Edite o texto diretamente nos ficheiros `.html`. Não há base de dados – tudo é estático.

### Adicionar Imagens
Crie pasta `assets/` e insira imagens:
```html
<img src="assets/minha-imagem.jpg" alt="Descrição" />
```

## 🚀 Deploy Recomendado

### GitHub Pages (Grátis)

1. Push para GitHub
2. Vá para **Configurações → Pages**
3. Escolha **Branch: main**
4. O site estará disponível em: `https://seu-usuario.github.io/escola-do-oraculo-website/`

### Netlify (Grátis + Automático)

1. Conecte seu repositório GitHub
2. Escolha branch `main`
3. Deploy automático em cada push

## 📞 Suporte

Para dúvidas sobre este website, contacte através de `contacto@rafaellakally.com`.

## 📜 Licença

Este projecto é propriedade intelectual da **Escola do Oráculo por Rafaella Kally** (2026).

---

**Desenvolvido com ✨ e dedicação ao tarot profissional.**
