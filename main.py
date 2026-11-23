from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine, Base
import models
from routers.auth import router as auth_router
from routers.usuarios import router as usuarios_router
from routers.plantas import router as plantas_router
from routers.receitas import router as receitas_router
from routers.colecao import router as colecao_router
from routers.upload import router as upload_router

# Garante a criação de tabelas na inicialização da aplicação
Base.metadata.create_all(bind=engine)

# Garante que a pasta de uploads local exista
UPLOADS_DIR = Path(__file__).resolve().parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Enciclopédia Digital de PANCs",
    description="Sistema web inteligente para identificação botânica, catálogo e receitas de PANCs do Cerrado.",
    version="1.0.0"
)

# Monta o servidor de arquivos estáticos para acesso às fotos salvas (/uploads/<nome>.jpg)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Inclusão dos roteadores da API
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(plantas_router)
app.include_router(receitas_router)
app.include_router(colecao_router)
app.include_router(upload_router)
