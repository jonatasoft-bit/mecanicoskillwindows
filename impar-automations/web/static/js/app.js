/**
 * Impar Automations - Dashboard App
 * Lógica do frontend para o dashboard
 */

// Estados globais
let appState = {
    authenticated: false,
    cookies_valid: false,
    has_credentials: false,
    days_until_expiry: 0
};

// Inicializar app ao carregar página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard iniciado');
    reloadStatus();
    loadHistory();

    // Atualizar status a cada 30 segundos
    setInterval(reloadStatus, 30000);
    setInterval(loadHistory, 60000);
});

/**
 * Recarrega status do sistema
 */
function reloadStatus() {
    console.log('Recarregando status...');

    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateStatusDisplay(data);
            appState = {
                authenticated: data.authenticated,
                cookies_valid: data.cookies.valid,
                has_credentials: data.has_credentials,
                days_until_expiry: data.cookies.days_until_expiry
            };
        })
        .catch(error => {
            console.error('Erro ao carregar status:', error);
            showError('Erro ao conectar ao servidor');
        });
}

/**
 * Atualiza exibição de status na tela
 */
function updateStatusDisplay(data) {
    // Autenticação
    const authElement = document.getElementById('auth-status');
    if (data.authenticated) {
        authElement.innerHTML = '<span class="badge success">✓ Autenticado</span>';
    } else {
        authElement.innerHTML = '<span class="badge error">✗ Não Autenticado</span>';
    }

    // Cookies
    const cookiesElement = document.getElementById('cookies-status');
    if (data.cookies.valid) {
        const refreshNeeded = data.cookies.needs_refresh ? ' (Renovação em breve)' : '';
        cookiesElement.innerHTML = `<span class="badge success">✓ Válidos${refreshNeeded}</span>`;
    } else {
        cookiesElement.innerHTML = '<span class="badge error">✗ Inválidos/Expirados</span>';
    }

    // Dias até expiração
    const expiryElement = document.getElementById('expiry-status');
    if (data.cookies.valid) {
        const days = data.cookies.days_until_expiry;
        if (days > 30) {
            expiryElement.innerHTML = `<span class="badge success">${days} dias</span>`;
        } else if (days > 0) {
            expiryElement.innerHTML = `<span class="badge warning">${days} dias</span>`;
        } else {
            expiryElement.innerHTML = '<span class="badge error">Expirado</span>';
        }
    } else {
        expiryElement.innerHTML = '<span class="badge neutral">-</span>';
    }

    // Automação
    const automationElement = document.getElementById('automation-status');
    if (data.authenticated && data.has_credentials) {
        automationElement.innerHTML = '<span class="badge success">✓ Pronto</span>';
    } else if (data.authenticated) {
        automationElement.innerHTML = '<span class="badge warning">⚠ Parcial</span>';
    } else {
        automationElement.innerHTML = '<span class="badge error">✗ Desativada</span>';
    }

    // Mensagem de status
    const messageElement = document.getElementById('status-message');
    messageElement.textContent = data.system.message;

    // Atualizar estado dos botões
    const refreshBtn = document.getElementById('refresh-btn');
    if (data.authenticated && data.has_credentials) {
        refreshBtn.disabled = false;
    } else {
        refreshBtn.disabled = true;
    }
}

/**
 * Carrega histórico de tentativas
 */
function loadHistory() {
    console.log('Carregando histórico...');

    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            displayHistory(data);
        })
        .catch(error => {
            console.error('Erro ao carregar histórico:', error);
        });
}

/**
 * Exibe histórico na tela
 */
function displayHistory(history) {
    const historyList = document.getElementById('history-list');

    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="text-center text-muted">Nenhum histórico disponível</p>';
        return;
    }

    let html = '';
    history.reverse().forEach(item => {
        const time = new Date(item.timestamp).toLocaleString('pt-BR');
        const message = item.message || item.status || 'Ação registrada';

        html += `
            <div class="history-item">
                <div class="history-time">${time}</div>
                <div class="history-message">${message}</div>
            </div>
        `;
    });

    historyList.innerHTML = html;
}

/**
 * Inicia login interativo
 */
function startLogin() {
    console.log('Iniciando login...');

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        openLoginModal();
    })
    .catch(error => {
        console.error('Erro:', error);
        showError('Erro ao iniciar login');
    });
}

/**
 * Abre modal de login
 */
function openLoginModal() {
    const modal = document.getElementById('login-modal');
    modal.classList.remove('hidden');
}

/**
 * Fecha modal de login
 */
function closeLoginModal() {
    const modal = document.getElementById('login-modal');
    modal.classList.add('hidden');
    reloadStatus();
}

/**
 * Tenta renovar cookies automaticamente
 */
function refreshCookies() {
    console.log('Renovando cookies...');

    const btn = document.getElementById('refresh-btn');
    btn.disabled = true;
    const originalText = btn.textContent;
    btn.textContent = '⏳ Renovando...';

    fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Renovação iniciada com sucesso!');
            setTimeout(reloadStatus, 2000);
        } else {
            showError(data.error || 'Erro ao renovar cookies');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showError('Erro ao renovar cookies');
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = originalText;
    });
}

/**
 * Configura scheduler do Windows
 */
function setupScheduler() {
    console.log('Configurando Task Scheduler...');

    if (!appState.authenticated || !appState.has_credentials) {
        showError('Faça login primeiro antes de ativar automação');
        return;
    }

    fetch('/api/setup-scheduler')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'not_implemented') {
                showInfo(data.message + '\n' + data.note);
                return;
            }
            showSuccess('Automação ativada!');
            reloadStatus();
        })
        .catch(error => {
            console.error('Erro:', error);
            showError('Erro ao configurar automação');
        });
}

/**
 * Mostra mensagem de sucesso
 */
function showSuccess(message) {
    alert('✅ ' + message);
}

/**
 * Mostra mensagem de erro
 */
function showError(message) {
    alert('❌ ' + message);
}

/**
 * Mostra mensagem de info
 */
function showInfo(message) {
    alert('ℹ️ ' + message);
}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {
    const modal = document.getElementById('login-modal');
    if (event.target === modal) {
        closeLoginModal();
    }
});
