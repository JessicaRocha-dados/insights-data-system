/**
 * ==================================================================================
 * InsightOS Tracker 
 * ----------------------------------------------------------------------------------
 * Autor: Jessica Rocha
 * Data: 27 de Agosto de 2025
 *
 * Objetivo:
 * Este script é o cérebro da nossa recolha de dados no front-end. As suas
 * responsabilidades são:
 * 1. Identificar cada visitante de forma anónima e persistente.
 * 2. Capturar os parâmetros de marketing (UTMs, etc.) da URL.
 * 3. Guardar os dados de primeiro e último toque para análise de atribuição.
 * 4. Fornecer uma função global (`InsightOS.track`) para enviar eventos
 * customizados para a nossa API de recolha de dados.
 * ==================================================================================
 */

// Utilizo uma "Immediately Invoked Function Expression" (IIFE).
// Isto cria um escopo privado para o meu código, evitando que as minhas variáveis
// e funções entrem em conflito com outras bibliotecas que o site possa usar.
(function() {
    // --- 1. CONFIGURAÇÃO ---

    // Defino o endereço do meu endpoint da API.
    // Durante o desenvolvimento, aponto para o meu servidor local.
    // Quando a API estiver online no Render, eu atualizarei este URL.
    const API_ENDPOINT = 'http://127.0.0.1:8000/event';

    // --- 2. GESTÃO DA IDENTIDADE DO VISITANTE ---

    /**
     * Esta função é responsável por identificar o visitante.
     * Ela verifica se já existe um ID guardado no `localStorage` do navegador.
     * Se não existir, ela cria um novo ID único (UUID v4) e guarda-o.
     * Isto garante que o mesmo visitante seja reconhecido nas suas diferentes visitas ao site.
     * @returns {string} O ID único do visitante.
     */
    function getOrSetVisitorId() {
        let visitorId = localStorage.getItem('insightos_visitor_id');
        if (!visitorId) {
            // Gero um UUID v4 simples usando uma substituição de caracteres aleatórios.
            visitorId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
            localStorage.setItem('insightos_visitor_id', visitorId);
        }
        return visitorId;
    }

    // --- 3. GESTÃO DA ATRIBUIÇÃO DE MARKETING ---

    /**
     * Esta função analisa a URL da página atual e extrai todos os parâmetros de marketing conhecidos.
     * @returns {object} Um objeto contendo os parâmetros encontrados (ex: { utm_source: 'google', utm_campaign: 'promo' }).
     */
    function getMarketingParams() {
        const params = new URLSearchParams(window.location.search);
        const marketingData = {};
        // Defino uma lista de todas as chaves de parâmetros de marketing que me interessam.
        const paramKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];
        
        paramKeys.forEach(key => {
            if (params.has(key)) {
                marketingData[key] = params.get(key);
            }
        });
        return marketingData;
    }

    /**
     * Esta função guarda os dados de atribuição no `localStorage`.
     * Ela implementa a lógica de primeiro e último toque (first and last touch).
     */
    function storeAttributionData() {
        const marketingParams = getMarketingParams();
        
        // Só executo a lógica se encontrar algum parâmetro de marketing na URL.
        if (Object.keys(marketingParams).length > 0) {
            // O "último toque" é sempre a campanha mais recente, então eu sobrescrevo-o a cada nova visita com UTMs.
            localStorage.setItem('insightos_last_touch', JSON.stringify(marketingParams));

            // O "primeiro toque" é a primeira campanha que trouxe o utilizador.
            // Por isso, só o guardo se ele ainda não existir no localStorage.
            if (!localStorage.getItem('insightos_first_touch')) {
                localStorage.setItem('insightos_first_touch', JSON.stringify(marketingParams));
            }
        }
    }
    
    // --- 4. NÚCLEO DE ENVIO DE EVENTOS ---

    /**
     * Esta é a função principal do tracker. Ela monta o pacote de dados (payload)
     * e envia-o para a minha API de recolha.
     * @param {string} eventName - O nome do evento (ex: 'page_view', 'cta_click').
     * @param {object} eventProperties - Um objeto com dados adicionais sobre o evento.
     */
    async function trackEvent(eventName, eventProperties = {}) {
        const visitorId = getOrSetVisitorId();
        // Recupero os dados de primeiro e último toque guardados, tratando o caso de não existirem (|| {}).
        const firstTouch = JSON.parse(localStorage.getItem('insightos_first_touch')) || {};
        const lastTouch = JSON.parse(localStorage.getItem('insightos_last_touch')) || {};

        // Monto o objeto 'payload' com a estrutura exata que a minha API FastAPI espera receber.
        const payload = {
            event_type: eventName,
            visitor_id: visitorId,
            timestamp: new Date().toISOString(), // Uso o formato ISO para um padrão universal de data/hora.
            url: window.location.href,
            page_title: document.title,
            event_properties: eventProperties,
            attribution: {
                first_touch: firstTouch,
                last_touch: lastTouch
            }
        };

        // Imprimo o payload na consola para fins de depuração durante o desenvolvimento.
        console.log('A enviar evento:', payload);

        try {
            // Uso a API Fetch do navegador para enviar os dados para o meu backend.
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
                // 'keepalive: true' é uma otimização importante. Garante que o pedido
                // seja concluído mesmo que o utilizador saia da página imediatamente após o evento.
                keepalive: true 
            });

            if (!response.ok) {
                console.error('Erro ao enviar evento:', response.statusText);
            }
        } catch (error) {
            console.error('Falha na requisição de tracking:', error);
        }
    }

    // --- 5. INICIALIZAÇÃO E EXPOSIÇÃO GLOBAL ---

    /**
     * Função que arranca o tracker.
     */
    function initializeTracker() {
        console.log('InsightOS Tracker Inicializado.');
        // 1. Processo e armazeno os dados de atribuição da URL atual assim que o tracker carrega.
        storeAttributionData();
        
        // 2. O evento 'page_view' inicial foi movido para a função showPage() no index.html.
        //    Isto é necessário para que ele seja disparado não apenas no primeiro carregamento,
        //    mas a cada "mudança de página" na nossa Single-Page Application.
    }

    // Exponho a minha função `trackEvent` para o mundo exterior, dentro de um objeto global 'InsightOS'.
    // Isto permite-me chamar o tracking de forma limpa a partir do meu HTML, como por exemplo:
    // <button onclick="InsightOS.track('cta_click')">Click Me</button>
    window.InsightOS = {
        track: trackEvent
    };

    // Finalmente, chamo a função de inicialização para que o tracker comece a funcionar.
    initializeTracker();

})();