from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UsuarioBase(BaseModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    criado_em: datetime
    total_descobertas: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
