from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.usuario import Usuario
from models.colecao import Colecao
from schemas.usuario import UsuarioResponse
from core.deps import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Perfil e Estatísticas do Usuário (RF03)",
    description="Retorna os dados do usuário autenticado e o total de PANCs descobertas na sua coleção pessoal."
)
def obter_perfil_usuario_atual(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calcula o número total de plantas na coleção pessoal do usuário
    total_descobertas = (
        db.query(func.count(Colecao.id_colecao))
        .filter(Colecao.id_usuario == current_user.id_usuario)
        .scalar()
    ) or 0

    return UsuarioResponse(
        id_usuario=current_user.id_usuario,
        nome=current_user.nome,
        email=current_user.email,
        criado_em=current_user.criado_em,
        total_descobertas=total_descobertas
    )
