"""
Script de teste automatizado do módulo da Coleção Pessoal do Usuário (Dia 06).
Testa:
1. Bloqueio de acesso sem token (401 Unauthorized)
2. Inclusão de descoberta na coleção (POST /colecao - RF08)
3. Prevenção de duplicatas da mesma planta na coleção do usuário
4. Isolamento estrito entre usuários (RNF03): Usuário B não vê nem altera a coleção do Usuário A
5. Consulta de detalhes da descoberta com receitas recomendadas (GET /colecao/{id} - RF10)
6. Remoção de planta da coleção (DELETE /colecao/{id} - RF11)
7. Atualização dinâmica do contador total_descobertas em GET /usuarios/me
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models.usuario import Usuario
from models.planta import Planta

client = TestClient(app)


def test_modulo_colecao():
    print("📚 Iniciando testes do módulo de Coleção Pessoal (Dia 06)...")

    # Limpeza prévia de usuários de teste
    db = SessionLocal()
    for email in ["alice.colecao@ceub.br", "bob.colecao@ceub.br"]:
        u = db.query(Usuario).filter(Usuario.email == email).first()
        if u:
            db.delete(u)
    db.commit()

    planta_teste = db.query(Planta).filter(Planta.nome_popular.ilike("%ora-pro-nóbis%")).first()
    if not planta_teste:
        planta_teste = db.query(Planta).first()
    assert planta_teste is not None, "Nenhuma planta encontrada para teste!"
    id_planta = planta_teste.id_planta
    db.close()

    # 1. Rota protegida sem token
    print("\n1️⃣ Testando POST /colecao SEM token (RNF03)...")
    resp_sem_token = client.post("/colecao", json={"id_planta": id_planta})
    assert resp_sem_token.status_code == 401
    print("   ✅ Acesso não autorizado bloqueado (HTTP 401).")

    # 2. Cadastro e login de dois usuários independentes
    print("\n2️⃣ Cadastrando e autenticando Usuária Alice e Usuário Bob...")
    client.post("/auth/cadastro", json={
        "nome": "Alice Teste",
        "email": "alice.colecao@ceub.br",
        "senha": "senhaAlice123"
    })
    client.post("/auth/cadastro", json={
        "nome": "Bob Teste",
        "email": "bob.colecao@ceub.br",
        "senha": "senhaBob123"
    })

    token_alice = client.post("/auth/login", json={
        "email": "alice.colecao@ceub.br",
        "senha": "senhaAlice123"
    }).json()["access_token"]

    token_bob = client.post("/auth/login", json={
        "email": "bob.colecao@ceub.br",
        "senha": "senhaBob123"
    }).json()["access_token"]

    auth_alice = {"Authorization": f"Bearer {token_alice}"}
    auth_bob = {"Authorization": f"Bearer {token_bob}"}
    print("   ✅ Alice e Bob autenticados com tokens JWT exclusivos.")

    # 3. Alice adiciona planta à sua coleção (RF08)
    print(f"\n3️⃣ Alice adiciona {planta_teste.nome_popular} à sua coleção (POST /colecao)...")
    resp_add = client.post(
        "/colecao",
        headers=auth_alice,
        json={
            "id_planta": id_planta,
            "data_descoberta": "2026-11-23",
            "foto_usuario": "https://meuapp.com/uploads/descoberta_alice.jpg"
        }
    )
    assert resp_add.status_code == 201, f"Erro: {resp_add.text}"
    item_alice = resp_add.json()
    id_colecao_alice = item_alice["id_colecao"]
    print(f"   ✅ Descoberta registrada com ID {id_colecao_alice} (HTTP 201).")

    # 4. Prevenção de duplicata para Alice
    print("\n4️⃣ Alice tenta adicionar a mesma planta novamente (prevenção de duplicata)...")
    resp_dup = client.post(
        "/colecao",
        headers=auth_alice,
        json={"id_planta": id_planta}
    )
    assert resp_dup.status_code == 400
    print("   ✅ Duplicata prevenida com sucesso (HTTP 400).")

    # 5. Isolamento: Bob lista sua coleção (deve estar vazia)
    print("\n5️⃣ Verificando isolamento: Bob lista sua coleção (GET /colecao)...")
    resp_bob_list = client.get("/colecao", headers=auth_bob)
    assert resp_bob_list.status_code == 200
    assert len(resp_bob_list.json()) == 0
    print("   ✅ Coleção de Bob está vazia (Bob não vê itens de Alice).")

    # 6. Alice lista sua coleção (deve conter 1 item)
    print("\n6️⃣ Alice lista sua coleção (GET /colecao - RF09)...")
    resp_alice_list = client.get("/colecao", headers=auth_alice)
    assert resp_alice_list.status_code == 200
    itens_alice = resp_alice_list.json()
    assert len(itens_alice) == 1
    assert itens_alice[0]["id_planta"] == id_planta
    print(f"   ✅ Alice visualiza sua planta: {itens_alice[0]['planta']['nome_popular']}")

    # 7. Bob tenta visualizar a descoberta de Alice (GET /colecao/{id}) -> deve ser 403 Forbidden
    print(f"\n7️⃣ Bob tenta acessar a descoberta de Alice ID {id_colecao_alice} (GET /colecao/{id_colecao_alice})...")
    resp_bob_spy = client.get(f"/colecao/{id_colecao_alice}", headers=auth_bob)
    assert resp_bob_spy.status_code == 403, f"Esperado 403, obtido {resp_bob_spy.status_code}"
    print("   ✅ Acesso indevido de Bob bloqueado com HTTP 403 Forbidden.")

    # 8. Bob tenta excluir a descoberta de Alice (DELETE /colecao/{id}) -> deve ser 403 Forbidden
    print(f"\n8️⃣ Bob tenta excluir a descoberta de Alice ID {id_colecao_alice} (DELETE /colecao/{id_colecao_alice})...")
    resp_bob_hack = client.delete(f"/colecao/{id_colecao_alice}", headers=auth_bob)
    assert resp_bob_hack.status_code == 403
    print("   ✅ Exclusão indevida de Bob bloqueada com HTTP 403 Forbidden.")

    # 9. Alice visualiza sua própria descoberta com receitas (RF10)
    print(f"\n9️⃣ Alice consulta os detalhes da sua descoberta (GET /colecao/{id_colecao_alice} - RF10)...")
    resp_alice_detail = client.get(f"/colecao/{id_colecao_alice}", headers=auth_alice)
    assert resp_alice_detail.status_code == 200
    detalhes = resp_alice_detail.json()
    assert detalhes["id_colecao"] == id_colecao_alice
    assert detalhes["planta"]["nome_popular"]
    assert "receitas" in detalhes
    print("   ✅ Detalhes exibidos:")
    print(f"      - Planta: {detalhes['planta']['nome_popular']}")
    print(f"      - Data descoberta: {detalhes['data_descoberta']}")
    print(f"      - Receitas recomendadas: {len(detalhes['receitas'])} encontrada(s)")

    # 10. Verificar contador total_descobertas em GET /usuarios/me
    print("\n🔟 Alice consulta suas estatísticas em GET /usuarios/me (RF03)...")
    me_antes = client.get("/usuarios/me", headers=auth_alice).json()
    assert me_antes["total_descobertas"] == 1
    print(f"   ✅ total_descobertas atualizado: {me_antes['total_descobertas']}")

    # 11. Alice remove a planta de sua coleção (DELETE /colecao/{id} - RF11)
    print(f"\n1️⃣1️⃣ Alice remove a planta de sua coleção (DELETE /colecao/{id_colecao_alice} - RF11)...")
    resp_del = client.delete(f"/colecao/{id_colecao_alice}", headers=auth_alice)
    assert resp_del.status_code == 200
    print("   ✅ Planta removida com sucesso (HTTP 200).")

    # 12. Verificar que contador retornou a 0
    me_depois = client.get("/usuarios/me", headers=auth_alice).json()
    assert me_depois["total_descobertas"] == 0
    print(f"   ✅ total_descobertas após exclusão: {me_depois['total_descobertas']}")

    # Limpeza dos usuários de teste
    db = SessionLocal()
    for email in ["alice.colecao@ceub.br", "bob.colecao@ceub.br"]:
        u = db.query(Usuario).filter(Usuario.email == email).first()
        if u:
            db.delete(u)
    db.commit()
    db.close()

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 06 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_modulo_colecao()
