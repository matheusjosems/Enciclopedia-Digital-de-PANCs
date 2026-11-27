"""
Testes automatizados do grupo de Autenticação e Usuários (APIs 1, 2 e 3).
Requisitos: RF01, RF02, RF03, RNF02, RNF03, RNF04.
"""


def test_cadastro_sucesso(client):
    resp = client.post("/auth/cadastro", json={
        "nome": "Carlos Silva",
        "email": "carlos@ceub.br",
        "senha": "senhaCarlos123"
    })
    assert resp.status_code == 201
    dados = resp.json()
    assert dados["email"] == "carlos@ceub.br"
    assert dados["nome"] == "Carlos Silva"
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_cadastro_email_duplicado(client):
    client.post("/auth/cadastro", json={
        "nome": "User Original",
        "email": "duplicado@ceub.br",
        "senha": "senha123456"
    })
    resp = client.post("/auth/cadastro", json={
        "nome": "User Copia",
        "email": "duplicado@ceub.br",
        "senha": "outrasenha123"
    })
    assert resp.status_code == 400
    assert "já existe" in resp.json()["detail"].lower() or "e-mail" in resp.json()["detail"].lower()


def test_cadastro_senha_curta(client):
    resp = client.post("/auth/cadastro", json={
        "nome": "Senha Fraca",
        "email": "fraca@ceub.br",
        "senha": "123"
    })
    assert resp.status_code == 400
    assert "mínimo 6" in resp.json()["detail"].lower()


def test_login_sucesso_json(client):
    client.post("/auth/cadastro", json={
        "nome": "Login JSON",
        "email": "login.json@ceub.br",
        "senha": "minhasenha123"
    })
    resp = client.post("/auth/login", json={
        "email": "login.json@ceub.br",
        "senha": "minhasenha123"
    })
    assert resp.status_code == 200
    dados = resp.json()
    assert "access_token" in dados
    assert dados["token_type"] == "bearer"


def test_login_sucesso_form_data(client):
    client.post("/auth/cadastro", json={
        "nome": "Login Form",
        "email": "login.form@ceub.br",
        "senha": "minhasenha123"
    })
    resp = client.post("/auth/login", data={
        "username": "login.form@ceub.br",
        "password": "minhasenha123"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_senha_incorreta(client):
    resp = client.post("/auth/login", json={
        "email": "carlos@ceub.br",
        "senha": "senhaErradaInvalida"
    })
    assert resp.status_code == 401
    assert "incorretos" in resp.json()["detail"].lower()


def test_usuario_me_sem_token(client):
    resp = client.get("/usuarios/me")
    assert resp.status_code == 401


def test_usuario_me_autenticado(client, auth_alice):
    headers = {"Authorization": auth_alice["Authorization"]}
    resp = client.get("/usuarios/me", headers=headers)
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["email"] == auth_alice["email"]
    assert "total_descobertas" in dados
    assert isinstance(dados["total_descobertas"], int)


def test_cadastro_nome_duplicado(client):
    client.post("/auth/cadastro", json={
        "nome": "Nome Unico Pytest",
        "email": "nome.unico1@ceub.br",
        "senha": "senha123456"
    })
    resp = client.post("/auth/cadastro", json={
        "nome": "Nome Unico Pytest",
        "email": "nome.unico2@ceub.br",
        "senha": "senha123456"
    })
    assert resp.status_code == 400
    assert "nome" in resp.json()["detail"].lower()


def test_usuario_me_token_invalido(client):
    resp = client.get("/usuarios/me", headers={"Authorization": "Bearer token-falso-invalido"})
    assert resp.status_code == 401
