"""
Script de teste automatizado do fluxo de Catálogo de Plantas & Busca Avançada (Dia 04).
Testa:
1. Listagem completa do catálogo (GET /plantas)
2. Busca textual por nome popular (ex: 'ora')
3. Busca textual por nome científico (ex: 'Pereskia')
4. Filtro por região/bioma (ex: 'Cerrado')
5. Consulta de detalhes por ID válido (GET /plantas/{id})
6. Consulta de ID inexistente com retorno amigável 404 (GET /plantas/99999)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_catalogo_plantas():
    print("🌿 Iniciando testes do catálogo de plantas e busca avançada (Dia 04)...")

    # 1. Listagem geral
    print("\n1️⃣ Testando GET /plantas (listagem padrão com paginação)...")
    resp = client.get("/plantas?limit=100")
    assert resp.status_code == 200, f"Erro: {resp.text}"
    plantas = resp.json()
    assert len(plantas) >= 60, f"Esperado >= 60 plantas, obtido {len(plantas)}"
    print(f"   ✅ Retornadas {len(plantas)} plantas cadastradas no banco SQLite.")

    # 2. Busca por nome popular parcial ("ora")
    print("\n2️⃣ Testando GET /plantas?nome=ora (busca por nome popular)...")
    resp_ora = client.get("/plantas?nome=ora")
    assert resp_ora.status_code == 200
    dados_ora = resp_ora.json()
    assert len(dados_ora) >= 1
    nomes = [p["nome_popular"].lower() for p in dados_ora]
    assert any("ora-pro-nóbis" in n or "ora" in n for n in nomes)
    ora = dados_ora[0]
    print(f"   ✅ Encontrada: {ora['nome_popular']} ({ora['nome_cientifico']})")

    # 3. Busca por nome científico ("Pereskia")
    print("\n3️⃣ Testando GET /plantas?nome=Pereskia (busca por nome científico)...")
    resp_sci = client.get("/plantas?nome=Pereskia")
    assert resp_sci.status_code == 200
    dados_sci = resp_sci.json()
    assert len(dados_sci) >= 1
    assert "pereskia" in dados_sci[0]["nome_cientifico"].lower()
    print(f"   ✅ Busca científica confirmada: {dados_sci[0]['nome_cientifico']}")

    # 4. Filtro por região ("Cerrado")
    print("\n4️⃣ Testando GET /plantas?regiao=Cerrado (filtro por bioma)...")
    resp_reg = client.get("/plantas?regiao=Cerrado&limit=10")
    assert resp_reg.status_code == 200
    dados_reg = resp_reg.json()
    assert len(dados_reg) > 0
    print(f"   ✅ Retornadas {len(dados_reg)} plantas filtradas pelo bioma Cerrado.")

    # 5. Detalhes completos por ID válido
    id_teste = ora["id_planta"]
    print(f"\n5️⃣ Testando GET /plantas/{id_teste} (ficha completa da planta - RF06)...")
    resp_detalhe = client.get(f"/plantas/{id_teste}")
    assert resp_detalhe.status_code == 200
    detalhe = resp_detalhe.json()
    assert detalhe["id_planta"] == id_teste
    assert detalhe["nome_popular"]
    assert detalhe["nome_cientifico"]
    assert detalhe["partes_comestiveis"]
    assert detalhe["cuidados"]
    assert "regioes" in detalhe
    print("   ✅ Ficha técnica completa verificada:")
    print(f"      - Nome: {detalhe['nome_popular']} ({detalhe['nome_cientifico']})")
    print(f"      - Família: {detalhe['familia']}")
    print(f"      - Partes comestíveis: {detalhe['partes_comestiveis'][:40]}...")
    print(f"      - Cuidados: {detalhe['cuidados'][:40]}...")
    print(f"      - Regiões vinculadas: {[r['nome'] for r in detalhe['regioes']]}")

    # 6. ID inexistente deve retornar 404
    print("\n6️⃣ Testando GET /plantas/99999 (ID inexistente)...")
    resp_404 = client.get("/plantas/99999")
    assert resp_404.status_code == 404
    assert "não encontrada" in resp_404.json()["detail"].lower()
    print("   ✅ Erro 404 retornado corretamente com mensagem amigável.")

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 04 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_catalogo_plantas()
