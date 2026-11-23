"""
Testes automatizados do grupo de Coleção Pessoal do Usuário (APIs 7, 8, 9 e 10).
Requisitos: RF08, RF09, RF10, RF11, RNF03, RNF04.
"""


def test_adicionar_colecao_sucesso(client, auth_alice):
    headers = {"Authorization": auth_alice["Authorization"]}
    plantas = client.get("/plantas?nome=ora").json()
    id_planta = plantas[0]["id_planta"]

    resp = client.post("/colecao", headers=headers, json={
        "id_planta": id_planta,
        "data_descoberta": "2026-11-23",
        "foto_usuario": "https://exemplo.com/minha_ora.jpg"
    })
    assert resp.status_code == 201
    dados = resp.json()
    assert dados["id_planta"] == id_planta
    assert dados["data_descoberta"] == "2026-11-23"


def test_adicionar_colecao_duplicada_bloqueada(client, auth_alice):
    headers = {"Authorization": auth_alice["Authorization"]}
    plantas = client.get("/plantas?nome=ora").json()
    id_planta = plantas[0]["id_planta"]

    # Tenta adicionar novamente a mesma planta
    resp = client.post("/colecao", headers=headers, json={"id_planta": id_planta})
    assert resp.status_code == 400
    assert "já está cadastrada" in resp.json()["detail"].lower()


def test_adicionar_colecao_planta_inexistente_404(client, auth_alice):
    headers = {"Authorization": auth_alice["Authorization"]}
    resp = client.post("/colecao", headers=headers, json={"id_planta": 99999})
    assert resp.status_code == 404


def test_listar_colecao_isolamento_entre_usuarios(client, auth_alice, auth_bob):
    headers_alice = {"Authorization": auth_alice["Authorization"]}
    headers_bob = {"Authorization": auth_bob["Authorization"]}

    # Alice tem 1 planta salva
    resp_alice = client.get("/colecao", headers=headers_alice)
    assert resp_alice.status_code == 200
    assert len(resp_alice.json()) >= 1

    # Bob não adicionou nada, deve estar vazia (isolamento RNF03)
    resp_bob = client.get("/colecao", headers=headers_bob)
    assert resp_bob.status_code == 200
    assert len(resp_bob.json()) == 0


def test_detalhar_descoberta_com_receitas(client, auth_alice):
    headers_alice = {"Authorization": auth_alice["Authorization"]}
    colecao = client.get("/colecao", headers=headers_alice).json()
    id_colecao = colecao[0]["id_colecao"]

    resp = client.get(f"/colecao/{id_colecao}", headers=headers_alice)
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["id_colecao"] == id_colecao
    assert dados["planta"]["nome_popular"]
    assert "receitas" in dados


def test_detalhar_descoberta_outro_usuario_bloqueada_403(client, auth_alice, auth_bob):
    headers_alice = {"Authorization": auth_alice["Authorization"]}
    headers_bob = {"Authorization": auth_bob["Authorization"]}

    colecao_alice = client.get("/colecao", headers=headers_alice).json()
    id_alice = colecao_alice[0]["id_colecao"]

    # Bob tenta acessar a descoberta de Alice
    resp = client.get(f"/colecao/{id_alice}", headers=headers_bob)
    assert resp.status_code == 403


def test_remover_descoberta_outro_usuario_bloqueada_403(client, auth_alice, auth_bob):
    headers_alice = {"Authorization": auth_alice["Authorization"]}
    headers_bob = {"Authorization": auth_bob["Authorization"]}

    colecao_alice = client.get("/colecao", headers=headers_alice).json()
    id_alice = colecao_alice[0]["id_colecao"]

    # Bob tenta remover item de Alice
    resp = client.delete(f"/colecao/{id_alice}", headers=headers_bob)
    assert resp.status_code == 403


def test_remover_descoberta_sucesso(client, auth_alice):
    headers_alice = {"Authorization": auth_alice["Authorization"]}
    colecao = client.get("/colecao", headers=headers_alice).json()
    id_colecao = colecao[0]["id_colecao"]

    resp = client.delete(f"/colecao/{id_colecao}", headers=headers_alice)
    assert resp.status_code == 200

    # Confirma que foi removida
    resp_check = client.get(f"/colecao/{id_colecao}", headers=headers_alice)
    assert resp_check.status_code == 404
