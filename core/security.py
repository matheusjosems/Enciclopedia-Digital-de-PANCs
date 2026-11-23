import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt

# Chave secreta e algoritmo para assinatura dos tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY", "edpancs-super-secret-key-2026-ceub-desenvolvimento-sistemas")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas de validade


def hash_senha(senha: str) -> str:
    """Gera um hash seguro da senha usando bcrypt com salt aleatório."""
    pwd_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara uma senha em texto puro com o hash bcrypt armazenado."""
    try:
        return bcrypt.checkpw(senha_plana.encode("utf-8"), senha_hash.encode("utf-8"))
    except Exception:
        return False


def criar_token_acesso(dados: dict, tempo_expiracao: Optional[timedelta] = None) -> str:
    """Gera um novo token JWT com payload e tempo de expiração."""
    to_encode = dados.copy()
    if tempo_expiracao:
        expire = datetime.now(timezone.utc) + tempo_expiracao
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> dict:
    """Decodifica e valida a assinatura e expiração de um token JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return {}
