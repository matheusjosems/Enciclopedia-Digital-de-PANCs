"""
Script de teste automatizado do fluxo de Receitas e Culinária PANC (Dia 05).
Testa:
1. Listagem de receitas por planta existente (GET /plantas/{id}/receitas - RF07)
2. Retorno 404 ao buscar receitas de planta inexistente (GET /plantas/99999/receitas)
3. Consulta de detalhe de receita por ID (GET /receitas/{id} - RF13)
4. Retorno 404 ao buscar receita inexistente (GET /receitas/99999)
5. Listagem geral de receitas (GET /receitas)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models.planta import Planta

client = TestClient(app)


def test_modulo_receitas():
    print("🍳 Iniciando testes do módulo de receitas e culinária PANC (Dia 05)...")

    db = SessionLocal()
    # Busca uma planta de teste que possua receitas cadastradas (ex: Ora-pro-nóbis)
    planta = db.query(Planta).filter(Planta.nome_popular.ilike("%ora-pro-nóbis%")).first()
    if not planta:
        planta = db.query(Planta).first()
    assert planta is not None, "Nenhuma planta encontrada no banco!"
    id_planta = planta.id_planta
    db.close()

    # 1. Testar GET /plantas/{id}/receitas (RF07)
    print(f"\n1️⃣ Testando GET /plantas/{id_planta}/receitas ({planta.nome_popular} - RF07)...")
    resp = client.get(f"/plantas/{id_planta}/receitas")
    assert resp.status_code == 200, f"Erro: {resp.text}"
    receitas = resp.json()
    assert len(receitas) >= 1, f"Esperado ao menos 1 receita para {planta.nome_popular}"
    rec = receitas[0]
    assert "titulo" in rec
    assert "ingredientes" in rec
    assert "modo_preparo" in rec
    print(f"   ✅ Retornada(s) {len(receitas)} receita(s): '{rec['titulo']}'")
    print(f"      - Ingredientes: {rec['ingredientes'][:50]}...")
    print(f"      - Modo de preparo: {rec['modo_preparo'][:50]}...")

    # 2. Testar GET /plantas/99999/receitas (Planta inexistente)
    print("\n2️⃣ Testando GET /plantas/99999/receitas (Planta inexistente)...")
    resp_404_planta = client.get("/plantas/99999/receitas")
    assert resp_404_planta.status_code == 404
    print("   ✅ Retorno 404 correto para planta inexistente.")

    # 3. Testar GET /receitas/{id} (RF13)
    id_receita = rec["id_receita"]
    print(f"\n3️⃣ Testando GET /receitas/{id_receita} (Ficha da Receita - RF13)...")
    resp_detalhe = client.get(f"/receitas/{id_receita}")
    assert resp_detalhe.status_code == 200
    detalhe = resp_detalhe.json()
    assert detalhe["id_receita"] == id_receita
    assert detalhe["titulo"] == rec["titulo"]
    assert detalhe["tempo_preparo"]
    assert detalhe["rendimento"]
    assert detalhe["nome_popular_planta"]
    print(f"   ✅ Detalhe completo da receita verificado:")
    print(f"      - Prato: {detalhe['titulo']}")
    print(f"      - PANC utilizada: {detalhe['nome_popular_planta']} ({detalhe['nome_cientifico_planta']})")
    print(f"      - Tempo estimado: {detalhe['tempo_preparo']} | Rendimento: {detalhe['rendimento']}")

    # 4. Testar GET /receitas/99999 (Receita inexistente)
    print("\n4️⃣ Testando GET /receitas/99999 (Receita inexistente)...")
    resp_404_rec = client.get("/receitas/99999")
    assert resp_404_rec.status_code == 404
    print("   ✅ Retorno 404 correto para receita inexistente.")

    # 5. Testar GET /receitas (Catálogo geral de receitas)
    print("\n5️⃣ Testando GET /receitas (Catálogo geral)...")
    resp_todas = client.get("/receitas")
    assert resp_todas.status_code == 200
    todas = resp_todas.json()
    assert len(todas) >= 60
    print(f"   ✅ Total de {len(todas)} receitas catalogadas acessíveis na API.")

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 05 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_modulo_receitas()
