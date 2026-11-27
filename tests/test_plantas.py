"""
Testes automatizados do grupo de Plantas & Catálogo (APIs 5 e 6).
Requisitos: RF06, RF12.
"""


def test_listar_todas_plantas(client):
    resp = client.get("/plantas")
    assert resp.status_code == 200
    plantas = resp.json()
    assert len(plantas) >= 3


def test_buscar_planta_por_nome_popular(client):
    resp = client.get("/plantas?nome=ora")
    assert resp.status_code == 200
    plantas = resp.json()
    assert len(plantas) >= 1
    nomes = [p["nome_popular"] for p in plantas]
    assert any("Ora-pro-nóbis" in n for n in nomes)


def test_buscar_planta_por_nome_cientifico(client):
    resp = client.get("/plantas?nome=Stachys")
    assert resp.status_code == 200
    plantas = resp.json()
    assert len(plantas) >= 1
    assert "Stachys byzantina" in plantas[0]["nome_cientifico"]


def test_filtrar_plantas_por_regiao(client):
    resp = client.get("/plantas?regiao=Cerrado")
    assert resp.status_code == 200
    plantas = resp.json()
    assert len(plantas) >= 2


def test_detalhar_planta_sucesso(client):
    # Obtém a primeira planta
    plantas = client.get("/plantas").json()
    p_id = plantas[0]["id_planta"]
    
    resp = client.get(f"/plantas/{p_id}")
    assert resp.status_code == 200
    p = resp.json()
    assert p["id_planta"] == p_id
    assert p["nome_popular"]
    assert p["nome_cientifico"]
    assert p["partes_comestiveis"]
    assert p["cuidados"]
    assert "regioes" in p
    assert "sazonalidades" in p


def test_detalhar_planta_inexistente_404(client):
    resp = client.get("/plantas/99999")
    assert resp.status_code == 404
    assert "não encontrada" in resp.json()["detail"].lower()


def test_paginacao_plantas(client):
    resp = client.get("/plantas?skip=0&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
