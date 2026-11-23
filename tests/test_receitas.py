"""
Testes automatizados do grupo de Receitas & Culinária PANC (APIs 11 e 12).
Requisitos: RF07, RF13.
"""


def test_listar_receitas_por_planta(client):
    # Planta 1 tem receita
    plantas = client.get("/plantas?nome=ora").json()
    id_planta = plantas[0]["id_planta"]

    resp = client.get(f"/plantas/{id_planta}/receitas")
    assert resp.status_code == 200
    receitas = resp.json()
    assert len(receitas) >= 1
    rec = receitas[0]
    assert "titulo" in rec
    assert "ingredientes" in rec
    assert "modo_preparo" in rec


def test_listar_receitas_planta_inexistente_404(client):
    resp = client.get("/plantas/99999/receitas")
    assert resp.status_code == 404
    assert "não encontrada" in resp.json()["detail"].lower()


def test_detalhar_receita_sucesso(client):
    todas = client.get("/receitas").json()
    assert len(todas) >= 1
    id_receita = todas[0]["id_receita"]

    resp = client.get(f"/receitas/{id_receita}")
    assert resp.status_code == 200
    detalhes = resp.json()
    assert detalhes["id_receita"] == id_receita
    assert detalhes["titulo"]
    assert detalhes["modo_preparo"]
    assert detalhes["tempo_preparo"]
    assert detalhes["rendimento"]


def test_detalhar_receita_inexistente_404(client):
    resp = client.get("/receitas/99999")
    assert resp.status_code == 404
    assert "não encontrada" in resp.json()["detail"].lower()


def test_catalogo_todas_receitas(client):
    resp = client.get("/receitas")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2
