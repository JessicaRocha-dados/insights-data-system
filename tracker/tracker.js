/**
 * ==================================================================================
 * InsightOS Tracker v1.0
 * ----------------------------------------------------------------------------------
 * Este script é responsável por coletar dados de atribuição de marketing e eventos
 * de comportamento do usuário no front-end e enviá-los para a API de coleta.
 * ==================================================================================
 */

// Usamos uma função auto-executável para não poluir o escopo global do site.
(function() {
    // --- 1. CONFIGURAÇÃO ---
    // O endereço da nossa API FastAPI. Por enquanto, aponta para um ambiente local.
    // Quando fizermos o deploy, mudaremos para a URL de produção.
    const API_ENDPOINT = 'http://127.0.0.1:8000/event';

    // --- 2. GERENCIAMENTO DE IDENTIDADE ---
    /**
     * Obtém um ID de visitante anônimo do localStorage.
     * Se não existir, cria um novo ID único (UUID v4).
     * @returns {string} O ID do visitante.
     */
    function getOrSetVisitorId() {
        let visitorId = localStorage.getItem('insightos_visitor_id');
        if (!visitorId) {
            // Gera um UUID v4 simples
            visitorId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
            localStorage.setItem('insightos_visitor_id', visitorId);
        }
        return visitorId;
    }

    // --- 3. GERENCIAMENTO DE ATRIBUIÇÃO DE MARKETING ---
    /**
     * Analisa a URL atual em busca de parâmetros de marketing (UTMs, gclid, etc.).
     * @returns {object} Um objeto com os parâmetros encontrados.
     */
    function getMarketingParams() {
        const params = new URLSearchParams(window.location.search);
        const marketingData = {};
        const paramKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];
        
        paramKeys.forEach(key => {
            if (params.has(key)) {
                marketingData[key] = params.get(key);
            }
        });
        return marketingData;
    }

    /**
     * Salva os dados de atribuição. Guarda o primeiro e o último toque.
     */
    function storeAttributionData() {
        const marketingParams = getMarketingParams();
        // Se houver algum parâmetro de marketing na URL atual...
        if (Object.keys(marketingParams).length > 0) {
            // Salva como o último toque (sobrescreve o anterior)
            localStorage.setItem('insightos_last_touch', JSON.stringify(marketingParams));

            // Salva como o primeiro toque (apenas se ainda não existir)
            if (!localStorage.getItem('insightos_first_touch')) {
                localStorage.setItem('insightos_first_touch', JSON.stringify(marketingParams));
            }
        }
    }
    
    // --- 4. NÚCLEO DE ENVIO DE EVENTOS ---
    /**
     * A função principal que envia um evento para a nossa API.
     * @param {string} eventName - O nome do evento (ex: 'page_view', 'signup').
     * @param {object} eventProperties - Um objeto com dados adicionais sobre o evento.
     */
    async function trackEvent(eventName, eventProperties = {}) {
        const visitorId = getOrSetVisitorId();
        const firstTouch = JSON.parse(localStorage.getItem('insightos_first_touch')) || {};
        const lastTouch = JSON.parse(localStorage.getItem('insightos_last_touch')) || {};

        // Monta o payload completo com todas as informações que temos
        const payload = {
            event_type: eventName,
            visitor_id: visitorId,
            timestamp: new Date().toISOString(),
            url: window.location.href,
            page_title: document.title,
            event_properties: eventProperties,
            attribution: {
                first_touch: firstTouch,
                last_touch: lastTouch
            }
        };

        console.log('Enviando evento:', payload);

        try {
            // Usa a API Fetch para enviar os dados para o nosso backend
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
                // keepalive: true permite que a requisição continue mesmo se o usuário sair da página
                keepalive: true 
            });

            if (!response.ok) {
                console.error('Erro ao enviar evento:', response.statusText);
            }
        } catch (error) {
            console.error('Falha na requisição de tracking:', error);
        }
    }

    // --- 5. INICIALIZAÇÃO E TRACKING AUTOMÁTICO ---
    /**
     * Função que inicializa o tracker.
     */
    function initializeTracker() {
        console.log('InsightOS Tracker Inicializado.');
        // 1. Processa e armazena os dados de atribuição da URL atual
        storeAttributionData();
        
        // 2. Dispara automaticamente um evento 'page_view' em cada carregamento de página
        // Este foi movido para a função showPage() no index.html para lidar com a navegação SPA
    }

    // Expõe a função `trackEvent` globalmente para que possamos chamá-la de fora
    // Ex: <button onclick="InsightOS.track('cta_click')">Click Me</button>
    window.InsightOS = {
        track: trackEvent
    };

    // Inicializa o tracker assim que o script for carregado
    initializeTracker();

})();