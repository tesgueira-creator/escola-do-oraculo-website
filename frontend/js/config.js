/**
 * Configuração centralizada da Escola do Oráculo
 * Use este arquivo para configurar URLs e constantes globais
 */

const EscolaConfig = {
    // URLs da API
    API_URL: (function () {
        // Auto-detecta baseado no ambiente
        if (window.location.hostname === 'localhost' ||
            window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000';
        } else if (window.location.protocol === 'file:') {
            // Se estiver abrindo como arquivo local, usa produção
            return 'https://web-production-21437.up.railway.app';
        } else {
            // Em produção, usa a mesma origem
            return window.location.origin;
        }
    })(),

    // IDs de preços do Stripe
    PRICE_IDS: {
        // Subscrições
        pro: 'price_1SpAOPHvoxa2NZ5dMc6vbBMM',       // Círculo do Oráculo - €9.90/mês
        elite: 'price_1SpAOQHvoxa2NZ5dF53uAU6W',     // Pack Completo Tarot - €97 (anual)

        // Cursos individuais
        radiestesia: 'price_1SpAOQHvoxa2NZ5dgts3Mso4', // Mesa Radiónica - €120

        // Módulos de Tarot
        modulo1: 'price_1SpVH4Hvoxa2NZ5dFcMeOE7S',   // Módulo 1 - €29
        modulo2: 'price_1SpVH5Hvoxa2NZ5dj5yi8TCH',   // Módulo 2 - €49
        modulo3: 'price_1SpVH6Hvoxa2NZ5dUjeO5b1W',   // Módulo 3 - €69

        // Outros cursos
        kundalini: 'price_1SpVH6Hvoxa2NZ5d6VPFgClM', // Kundalini Reiki - €150
        'terapia-multidimensional': 'price_1SpVH7Hvoxa2NZ5dF8NMEjpo' // Terapia Multidimensional - €180
    },

    // Métodos utilitários
    isLocalhost() {
        return window.location.hostname === 'localhost' ||
            window.location.hostname === '127.0.0.1';
    },

    isDevelopment() {
        return this.isLocalhost() || window.location.protocol === 'file:';
    },

    getToken() {
        return localStorage.getItem('user_token');
    },

    getUserEmail() {
        return localStorage.getItem('user_email');
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    logout() {
        localStorage.removeItem('user_token');
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_name');
        window.location.href = this.isLocalhost() ?
            '/pages/login.html' :
            '/pages/login.html';
    },

    // Função para fazer chamadas à API
    async api(endpoint, options = {}) {
        const url = `${this.API_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    },

    // Verifica se o usuário está autenticado antes de acessar área protegida
    requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = '/pages/login.html?redirect=' + encodeURIComponent(window.location.pathname);
            return false;
        }
        return true;
    }
};

// Disponibiliza globalmente
window.EscolaConfig = EscolaConfig;

// Log para debug em desenvolvimento
if (EscolaConfig.isDevelopment()) {
    console.log('🔧 EscolaConfig loaded:', {
        API_URL: EscolaConfig.API_URL,
        isLocalhost: EscolaConfig.isLocalhost(),
        isLoggedIn: EscolaConfig.isLoggedIn()
    });
}
