/**
 * Funções compartilhadas de autenticação, API e interface
 */

const API_BASE = "";

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

  // Se o body não for FormData, envia JSON
  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  return response;
}

// Renderiza a barra de navegação responsiva dinamicamente
function renderNavbar() {
  const navContainer = document.getElementById("navbar-container");
  if (!navContainer) return;

  const token = getToken();
  const user = getUsuarioLogado();

  navContainer.innerHTML = `
    <nav class="bg-emerald-800 text-white shadow-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <!-- Logo & Título -->
          <div class="flex items-center space-x-3">
            <a href="/" class="flex items-center space-x-2 text-xl font-bold tracking-tight text-white hover:text-emerald-100 transition">
              <span class="text-2xl">🌿</span>
              <span>Enciclopédia de PANCs</span>
            </a>
          </div>

          <!-- Links Desktop -->
          <div class="hidden md:flex items-center space-x-6 text-sm font-medium">
            <a href="/" class="hover:text-emerald-200 transition py-2 border-b-2 border-transparent hover:border-emerald-300">Catálogo</a>
            <a href="/identificar" class="hover:text-emerald-200 transition py-2 flex items-center space-x-1">
              <span>📷</span>
              <span>Identificar IA</span>
            </a>
            <a href="/colecao" class="hover:text-emerald-200 transition py-2 flex items-center space-x-1">
              <span>📖</span>
              <span>Minha Coleção</span>
            </a>
          </div>

          <!-- Área do Usuário / Login -->
          <div class="hidden md:flex items-center space-x-4">
            ${
              token && user
                ? `
                  <div class="flex items-center space-x-3">
                    <a href="/perfil" class="text-sm bg-emerald-700 hover:bg-emerald-600 px-3 py-1.5 rounded-full flex items-center space-x-2 transition">
                      <span>👤</span>
                      <span class="font-semibold">${user.nome.split(" ")[0]}</span>
                    </a>
                    <button onclick="logout()" class="text-xs text-emerald-200 hover:text-white underline">Sair</button>
                  </div>
                `
                : `
                  <a href="/login" class="bg-emerald-500 hover:bg-emerald-400 text-white text-sm font-semibold px-4 py-2 rounded-lg shadow-sm transition">
                    Entrar / Cadastrar
                  </a>
                `
            }
          </div>

          <!-- Botão Mobile Menu -->
          <div class="md:hidden flex items-center">
            <button id="mobile-menu-btn" class="text-emerald-100 hover:text-white focus:outline-none p-2">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Menu Mobile -->
      <div id="mobile-menu" class="hidden md:hidden bg-emerald-900 border-t border-emerald-700 px-4 pt-3 pb-4 space-y-2 text-sm font-medium">
        <a href="/" class="block text-emerald-100 hover:text-white py-2">Catálogo Geral</a>
        <a href="/identificar" class="block text-emerald-100 hover:text-white py-2">📷 Identificar por Foto</a>
        <a href="/colecao" class="block text-emerald-100 hover:text-white py-2">📖 Minha Coleção</a>
        <div class="pt-2 border-t border-emerald-800">
          ${
            token && user
              ? `
                <div class="flex justify-between items-center py-2">
                  <a href="/perfil" class="text-emerald-200">👤 Olá, ${user.nome}</a>
                  <button onclick="logout()" class="text-xs bg-red-600/80 px-2 py-1 rounded text-white">Sair</button>
                </div>
              `
              : `
                <a href="/login" class="block text-center bg-emerald-500 hover:bg-emerald-400 text-white py-2 rounded-lg font-semibold mt-2">
                  Entrar / Cadastrar
                </a>
              `
          }
        </div>
      </div>
    </nav>
  `;

  // Toggle mobile menu
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }
}

// Atualiza dados do usuário logado em background
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

// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
  checarSessaoUsuario();
});
