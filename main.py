from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
import models
from routers.auth import router as auth_router
from routers.usuarios import router as usuarios_router
from routers.plantas import router as plantas_router
from routers.receitas import router as receitas_router
from routers.colecao import router as colecao_router
from routers.upload import router as upload_router
from routers.identificacao import router as identificacao_router

# Garante a criação de tabelas na inicialização da aplicação
Base.metadata.create_all(bind=engine)

# Diretórios estáticos
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Enciclopédia Digital de PANCs",
    description="Sistema web inteligente para identificação botânica, catálogo e receitas de PANCs do Cerrado.",
    version="1.0.0"
)

# Servidores de arquivos estáticos
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Inclusão dos roteadores da API REST
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(plantas_router)
app.include_router(receitas_router)
app.include_router(colecao_router)
app.include_router(upload_router)
app.include_router(identificacao_router)


# -------------------------------------------------------------
# Rotas Web Front-end Responsivo (HTML5)
# -------------------------------------------------------------

@app.get("/", response_class=FileResponse, tags=["Web"])
def rota_home():
    """Página inicial: Catálogo com busca em tempo real."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/login", response_class=FileResponse, tags=["Web"])
def rota_login():
    """Tela de Acesso: Login e Cadastro com JWT."""
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/planta/{id}", response_class=FileResponse, tags=["Web"])
def rota_ficha_planta(id: int):
    """Ficha completa da PANC com abas de descrição, cuidados e receitas."""
    return FileResponse(FRONTEND_DIR / "planta.html")
