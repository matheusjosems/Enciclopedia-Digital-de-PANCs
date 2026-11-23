"""
Script de teste automatizado das rotas web front-end e arquivos estáticos (Dia 10).
Testa:
1. Rota raiz GET / (Catálogo responsivo com busca)
2. Rota de autenticação GET /login (Tela de login e cadastro)
3. Rota de detalhes GET /planta/{id} (Ficha da planta com abas de receitas)
4. Disponibilidade dos arquivos estáticos /static/styles.css e /static/app.js
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_frontend_rotas():
    print("🌐 Iniciando testes da interface web responsiva (Dia 10)...")

    # 1. Teste da Home / Catálogo
    print("\n1️⃣ Testando GET / (Home e Catálogo)...")
    resp_home = client.get("/")
    assert resp_home.status_code == 200
    assert "text/html" in resp_home.headers["content-type"]
    assert "Enciclopédia Digital de PANCs" in resp_home.text or "Enciclopédia de PANCs" in resp_home.text
    assert "input-busca" in resp_home.text
    assert "grid-plantas" in resp_home.text
    print("   ✅ Catálogo web renderizado com sucesso (HTTP 200).")

    # 2. Teste da Tela de Login / Cadastro
    print("\n2️⃣ Testando GET /login (Tela de Login e Cadastro)...")
    resp_login = client.get("/login")
    assert resp_login.status_code == 200
    assert "text/html" in resp_login.headers["content-type"]
    assert "form-login" in resp_login.text
    assert "form-cadastro" in resp_login.text
    assert "pancs_token" in resp_login.text or "localStorage" in resp_login.text
    print("   ✅ Tela de autenticação renderizada com sucesso (HTTP 200).")

    # 3. Teste da Ficha da Planta
    print("\n3️⃣ Testando GET /planta/1 (Ficha Completa com Receitas)...")
    resp_planta = client.get("/planta/1")
    assert resp_planta.status_code == 200
    assert "text/html" in resp_planta.headers["content-type"]
    assert "nome-popular" in resp_planta.text
    assert "aba-descricao" in resp_planta.text
    assert "aba-cuidados" in resp_planta.text
    assert "aba-receitas" in resp_planta.text
    print("   ✅ Ficha de planta renderizada com abas interativas (HTTP 200).")

    # 4. Teste dos arquivos estáticos
    print("\n4️⃣ Testando entrega de arquivos estáticos (/static/styles.css e /static/app.js)...")
    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    assert "badge-bioma" in resp_css.text

    resp_js = client.get("/static/app.js")
    assert resp_js.status_code == 200
    assert "apiFetch" in resp_js.text
    assert "renderNavbar" in resp_js.text
    print("   ✅ Arquivos CSS e JavaScript entregues com sucesso via StaticFiles.")

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 10 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_frontend_rotas()
