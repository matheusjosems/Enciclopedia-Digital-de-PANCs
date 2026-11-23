from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./pancs.db"

# connect_args={"check_same_thread": False} é necessário para o SQLite funcionar com requisições concorrentes no FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependência FastAPI que fornece uma sessão do banco de dados por requisição
    e garante o fechamento ao finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
