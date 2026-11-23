"""
Script de teste automatizado do fluxo de autenticação e segurança (Dia 03).
Testa:
1. Cadastro de usuário (POST /auth/cadastro)
2. Verificação de senha armazenada em hash bcrypt (nunca texto puro)
3. Bloqueio de e-mail e username duplicados
4. Login com credenciais válidas e inválidas (POST /auth/login)
5. Suporte a requisição JSON e Form-Data OAuth2
6. Proteção de rota privada (GET /usuarios/me)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models.usuario import Usuario

client = TestClient(app)


def test_fluxo_autenticacao():
    print("🔐 Iniciando testes do módulo de autenticação (Dia 03)...")
    
    email_teste = "matheus.teste@ceub.br"
    nome_teste = "Matheus Morais"
    senha_teste = "segredo123"
    
    # Limpa usuário de teste se já existir
    db = SessionLocal()
    u_existente = db.query(Usuario).filter(Usuario.email == email_teste).first()
    if u_existente:
        db.delete(u_existente)
        db.commit()
    db.close()
    
    # 1. Teste de Cadastro
    print("\n1️⃣ Testando POST /auth/cadastro...")
    resp_cad = client.post("/auth/cadastro", json={
        "nome": nome_teste,
        "email": email_teste,
        "senha": senha_teste
    })
    assert resp_cad.status_code == 201, f"Falha no cadastro: {resp_cad.text}"
    dados_cad = resp_cad.json()
    assert dados_cad["email"] == email_teste
    assert dados_cad["nome"] == nome_teste
    assert "senha" not in dados_cad  # Senha nunca deve ser devolvida no response
    assert "senha_hash" not in dados_cad
    print("   ✅ Usuário cadastrado com sucesso (HTTP 201).")
    
    # 2. Checklist do Usuário: Confirmar que a senha no banco pancs.db é hash bcrypt
    print("\n2️⃣ Verificando hash no banco pancs.db (Checklist do Usuário)...")
    db = SessionLocal()
    user_db = db.query(Usuario).filter(Usuario.email == email_teste).first()
    assert user_db is not None
    assert user_db.senha_hash != senha_teste, "❌ ERRO GRAVE: Senha armazenada em texto puro!"
    assert user_db.senha_hash.startswith("$2b$") or user_db.senha_hash.startswith("$2a$"), "❌ O hash não é bcrypt válido!"
    print(f"   ✅ Senha protegida no banco: {user_db.senha_hash[:20]}... (Bcrypt verificado)")
    db.close()
    
    # 3. Teste de Duplicidade
    print("\n3️⃣ Testando prevenção de e-mail duplicado...")
    resp_dup = client.post("/auth/cadastro", json={
        "nome": "Outro Nome",
        "email": email_teste,
        "senha": "outrasenha123"
    })
    assert resp_dup.status_code == 400
    print("   ✅ Duplicidade bloqueada corretamente (HTTP 400).")
    
    # 4. Teste de Login Inválido
    print("\n4️⃣ Testando POST /auth/login com senha errada...")
    resp_login_err = client.post("/auth/login", json={
        "email": email_teste,
        "senha": "senha_errada_aqui"
    })
    assert resp_login_err.status_code == 401
    print("   ✅ Credencial inválida rejeitada (HTTP 401).")
    
    # 5. Teste de Login com Sucesso (JSON)
    print("\n5️⃣ Testando POST /auth/login com sucesso (JSON)...")
    resp_login = client.post("/auth/login", json={
        "email": email_teste,
        "senha": senha_teste
    })
    assert resp_login.status_code == 200
    token_json = resp_login.json()
    assert "access_token" in token_json
    assert token_json["token_type"] == "bearer"
    token = token_json["access_token"]
    print("   ✅ Login JSON bem-sucedido e token JWT emitido.")
    
    # 6. Teste de Login via Form-Data (OAuth2 Swagger)
    print("\n6️⃣ Testando POST /auth/login via Form-Data (compatibilidade Swagger /docs)...")
    resp_login_form = client.post("/auth/login", data={
        "username": email_teste,
        "password": senha_teste
    })
    assert resp_login_form.status_code == 200
    assert "access_token" in resp_login_form.json()
    print("   ✅ Login Form-Data bem-sucedido (Authorize do Swagger compatível).")
    
    # 7. Teste de rota privada SEM token
    print("\n7️⃣ Testando GET /usuarios/me SEM token...")
    resp_sem_token = client.get("/usuarios/me")
    assert resp_sem_token.status_code == 401
    print("   ✅ Acesso não autorizado bloqueado (HTTP 401).")
    
    # 8. Teste de rota privada COM Bearer Token
    print("\n8️⃣ Testando GET /usuarios/me COM Bearer Token...")
    resp_me = client.get(
        "/usuarios/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp_me.status_code == 200
    dados_me = resp_me.json()
    assert dados_me["email"] == email_teste
    assert dados_me["nome"] == nome_teste
    assert dados_me["total_descobertas"] == 0
    print(f"   ✅ Perfil retornado: {dados_me['nome']} ({dados_me['email']}) | Descobertas: {dados_me['total_descobertas']}")
    
    # Limpeza
    db = SessionLocal()
    user_del = db.query(Usuario).filter(Usuario.email == email_teste).first()
    if user_del:
        db.delete(user_del)
        db.commit()
    db.close()
    
    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 03 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_fluxo_autenticacao()
