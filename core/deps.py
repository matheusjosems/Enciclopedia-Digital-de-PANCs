from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from core.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    description="Insira o token JWT no formato: Bearer <token>"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependência de segurança FastAPI para rotas protegidas.
    Extrai e valida o token JWT do cabeçalho 'Authorization: Bearer <token>'
    e retorna o objeto Usuario correspondente do banco SQLite.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decodificar_token(token)
    if not payload:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if not email:
        raise credentials_exception
        
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise credentials_exception
        
    return usuario
