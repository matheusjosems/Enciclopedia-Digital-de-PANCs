"""
Testes automatizados das páginas web responsivas e arquivos estáticos (Dia 10).
Requisitos: RNF05, RNF06.
"""


def test_pagina_catalogo_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Professor Tamanduá" in resp.text
    assert "input-busca" in resp.text
    assert "grid-plantas" in resp.text

    resp_img = client.get("/static/assets/professor-tamandua.jfif")
    assert resp_img.status_code == 200


def test_pagina_login_cadastro(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "form-login" in resp.text
    assert "form-cadastro" in resp.text
    assert "cad-confirmar-senha" in resp.text


def test_pagina_ficha_planta(client):
    resp = client.get("/planta/1")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "aba-descricao" in resp.text
    assert "aba-cuidados" in resp.text
    assert "aba-receitas" in resp.text
    assert "grid-sazonalidade" in resp.text
    assert "mapa-brasil" in resp.text


def test_arquivos_estaticos_frontend(client):
    resp_css = client.get("/static/styles.css")
    assert resp_css.status_code == 200
    assert "badge-bioma" in resp_css.text

    resp_js = client.get("/static/app.js")
    assert resp_js.status_code == 200
    assert "apiFetch" in resp_js.text
    assert "escapeHtml" in resp_js.text


def test_pagina_identificar_camera_ia(client):
    resp = client.get("/identificar")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert 'capture="environment"' in resp.text
    assert "btn-salvar-colecao" in resp.text
    assert "texto-aviso-seguranca" in resp.text


def test_pagina_minha_colecao(client):
    resp = client.get("/minha-colecao")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "grid-colecao" in resp.text


def test_pagina_perfil(client):
    resp = client.get("/perfil")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "perfil-total" in resp.text
    assert "perfil-distintivo" in resp.text
