/**
 * Funções compartilhadas de autenticação, API e interface
 * Identidade visual baseada no fluxo do usuário da Enciclopédia Digital de PANCs
 */

const API_BASE = "";

// Escapa caracteres HTML para evitar injeção ao renderizar dados dinâmicos
function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Gerenciamento de Token JWT no LocalStorage
function getToken() {
  return localStorage.getItem("pancs_token");
}

function setToken(token) {
  localStorage.setItem("pancs_token", token);
}

function removeToken() {
  localStorage.removeItem("pancs_token");
}

function getUsuarioLogado() {
  const user = localStorage.getItem("pancs_user");
  try {
    return user ? JSON.parse(user) : null;
  } catch (e) {
    return null;
  }
}

function setUsuarioLogado(user) {
  localStorage.setItem("pancs_user", JSON.stringify(user));
}

// Wrapper para requisições Fetch autenticadas
async function apiFetch(endpoint, options = {}) {
  const headers = options.headers || {};
  const token = getToken();

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  return await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });
}

// Renderiza a barra de navegação responsiva no estilo do guia de campo
function renderNavbar() {
  const navContainer = document.getElementById("navbar-container");
  if (!navContainer) return;

  const token = getToken();
  const user = getUsuarioLogado();
  const inicial = user && user.nome ? user.nome.trim().charAt(0).toUpperCase() : "E";
  const primeiroNome = user && user.nome ? user.nome.trim().split(/\s+/)[0] : "Perfil";

  navContainer.innerHTML = `
    <nav class="bg-[#036934]/95 text-white border-b border-emerald-300/25 sticky top-0 z-50 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center space-x-3">
            <a href="/" class="flex items-center space-x-2 text-base sm:text-lg font-bold tracking-tight text-white hover:text-emerald-100 transition">
              <span class="text-xl">🌿</span>
              <span>Enciclopédia Digital de PANCs</span>
            </a>
          </div>

          <div class="hidden md:flex items-center space-x-6 text-xs lg:text-sm font-semibold">
            <a href="/#biblioteca" class="hover:text-emerald-200 transition py-1">Biblioteca</a>
            <a href="/identificar" class="hover:text-emerald-200 transition py-1">📷 Identificar</a>
            <a href="/minha-colecao" class="hover:text-emerald-200 transition py-1">📖 Minha enciclopédia</a>
          </div>

          <div class="hidden md:flex items-center space-x-3">
            ${
              token && user
                ? `
                  <a href="/perfil" class="flex items-center space-x-2 hover:opacity-90 transition">
                    <span class="w-9 h-9 rounded-full bg-[#EEFAEF] text-[#0F291E] font-bold flex items-center justify-center shadow-sm">
                      ${escapeHtml(inicial)}
                    </span>
                    <span class="text-sm font-semibold">${escapeHtml(primeiroNome)}</span>
                  </a>
                  <button onclick="logout()" class="text-xs text-emerald-100 hover:text-white underline ml-2">Sair</button>
                `
                : `
                  <a href="/login" class="btn-caramel text-xs sm:text-sm px-4 py-2">
                    Entrar
                  </a>
                  <a href="/login?modo=cadastro" class="bg-white text-[#0F291E] hover:bg-emerald-50 text-xs sm:text-sm font-semibold px-4 py-2 rounded-xl transition">
                    Criar conta
                  </a>
                `
            }
          </div>

          <div class="md:hidden flex items-center">
            <button id="mobile-menu-btn" class="text-white hover:text-emerald-200 focus:outline-none p-2" aria-label="Menu">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div id="mobile-menu" class="hidden md:hidden bg-[#025429] border-t border-emerald-300/20 px-4 pt-3 pb-4 space-y-2 text-sm font-medium">
        <a href="/#biblioteca" class="block text-emerald-50 hover:text-white py-2">Biblioteca de PANCs</a>
        <a href="/identificar" class="block text-emerald-50 hover:text-white py-2">📷 Identificar uma planta</a>
        <a href="/minha-colecao" class="block text-emerald-50 hover:text-white py-2">📖 Minha enciclopédia</a>
        <div class="pt-2 border-t border-emerald-300/20">
          ${
            token && user
              ? `
                <div class="flex justify-between items-center py-2">
                  <a href="/perfil" class="text-emerald-100 font-semibold">👤 ${escapeHtml(user.nome)}</a>
                  <button onclick="logout()" class="text-xs bg-[#B85A00] px-3 py-1.5 rounded-lg text-white font-semibold">Sair</button>
                </div>
              `
              : `
                <div class="grid grid-cols-2 gap-2 pt-2">
                  <a href="/login" class="btn-caramel text-center py-2 text-xs">Entrar</a>
                  <a href="/login?modo=cadastro" class="bg-white text-[#0F291E] text-center py-2 rounded-xl text-xs font-semibold">Criar conta</a>
                </div>
              `
          }
        </div>
      </div>
    </nav>
  `;

  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }
}

async function checarSessaoUsuario() {
  const token = getToken();
  if (!token) return;

  try {
    const res = await apiFetch("/usuarios/me");
    if (res.ok) {
      const usuario = await res.json();
      setUsuarioLogado(usuario);
      renderNavbar();
    } else if (res.status === 401) {
      removeToken();
      localStorage.removeItem("pancs_user");
      renderNavbar();
    }
  } catch (err) {
    console.warn("Não foi possível verificar sessão:", err);
  }
}

function logout() {
  removeToken();
  localStorage.removeItem("pancs_user");
  window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
  checarSessaoUsuario();
});
