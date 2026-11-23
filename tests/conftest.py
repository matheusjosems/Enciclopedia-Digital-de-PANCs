import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app
from models import Usuario, Planta, Regiao, Receita, Colecao, PlantaSazonalidade

# Cria banco de dados SQLite isolado em memória para a suíte de testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Cria o schema do banco em memória e popula com dados semente para testes."""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    
    # Regiões
    r_cerrado = Regiao(nome="Cerrado", tipo="Bioma")
    r_mata = Regiao(nome="Mata Atlântica", tipo="Bioma")
    r_sudeste = Regiao(nome="Sudeste", tipo="Região Geográfica")
    db.add_all([r_cerrado, r_mata, r_sudeste])
    db.commit()

    # Plantas base
    p1 = Planta(
        nome_popular="Ora-pro-nóbis",
        nome_cientifico="Pereskia aculeata Mill",
        familia="Cactaceae",
        descricao="Trepadeira rica em proteínas, folhas verdes carnosas.",
        partes_comestiveis="Folhas e flores",
        cuidados="Possui espinhos no caule.",
        sabor="Neutro e suave",
        foto_url="https://exemplo.com/ora.jpg"
    )
    p1.regioes.extend([r_cerrado, r_mata])

    p2 = Planta(
        nome_popular="Peixinho da Horta",
        nome_cientifico="Stachys byzantina K.Koch",
        familia="Lamiaceae",
        descricao="Erva aveludada com folhas prateadas em formato de peixinho.",
        partes_comestiveis="Folhas",
        cuidados="Consumir preferencialmente empanada ou refogada.",
        sabor="Herbáceo e levemente amargo",
        foto_url="https://exemplo.com/peixinho.jpg"
    )
    p2.regioes.append(r_sudeste)

    p3 = Planta(
        nome_popular="Taioba",
        nome_cientifico="Xanthosoma taioba",
        familia="Araceae",
        descricao="Planta com folhas cordatas grandes parecidas com orelha de elefante.",
        partes_comestiveis="Folhas jovens",
        cuidados="ATENÇÃO: Deve ser cozida ou refogada antes do consumo para eliminar oxalato de cálcio.",
        sabor="Similar ao espinafre",
        foto_url="https://exemplo.com/taioba.jpg"
    )
    p3.regioes.append(r_cerrado)

    db.add_all([p1, p2, p3])
    db.commit()

    # Receitas
    rec1 = Receita(
        id_planta=p1.id_planta,
        titulo="Massa Fresca com Ora-pro-nóbis",
        ingredientes="Farinha de trigo, ovos e folhas frescas de ora-pro-nóbis",
        modo_preparo="Bata as folhas com os ovos, misture à farinha e abra a massa.",
        tempo_preparo="20 min",
        rendimento="4 porções"
    )
    rec2 = Receita(
        id_planta=p2.id_planta,
        titulo="Peixinho Empanado Crocante",
        ingredientes="Folhas de peixinho, farinha de trigo, água com gás e sal",
        modo_preparo="Empane as folhas na massa e frite em óleo quente até dourar.",
        tempo_preparo="15 min",
        rendimento="2 porções"
    )
    db.add_all([rec1, rec2])
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_alice(client):
    """Cria e autentica a usuária Alice, retornando o cabeçalho Authorization."""
    email = "alice.pytest@ceub.br"
    senha = "senhaSegura123"
    client.post("/auth/cadastro", json={
        "nome": "Alice Pytest",
        "email": email,
        "senha": senha
    })
    resp = client.post("/auth/login", json={"email": email, "senha": senha})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "email": email}


@pytest.fixture
def auth_bob(client):
    """Cria e autentica o usuário Bob, retornando o cabeçalho Authorization."""
    email = "bob.pytest@ceub.br"
    senha = "senhaSegura456"
    client.post("/auth/cadastro", json={
        "nome": "Bob Pytest",
        "email": email,
        "senha": senha
    })
    resp = client.post("/auth/login", json={"email": email, "senha": senha})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "email": email}
