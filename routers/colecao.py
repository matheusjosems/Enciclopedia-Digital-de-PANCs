from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from models.planta import Planta
from models.colecao import Colecao
from models.receita import Receita
from schemas.colecao import ColecaoCreate, ColecaoResponse, ColecaoDetalheResponse
from schemas.receita import ReceitaResponse
from core.deps import get_current_user

router = APIRouter(prefix="/colecao", tags=["Coleção"])


@router.post(
    "",
    response_model=ColecaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Salvar Descoberta na Coleção (RF08)",
    description="Adiciona uma PANC identificada à coleção pessoal do usuário autenticado, com a foto tirada e a data da descoberta."
)
def adicionar_a_colecao(
    dados: ColecaoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Verifica se a planta existe no catálogo
    planta = db.query(Planta).filter(Planta.id_planta == dados.id_planta).first()
    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planta com ID {dados.id_planta} não encontrada no catálogo."
        )

    # 2. Verifica se a planta já foi salva anteriormente na coleção do usuário
    existente = db.query(Colecao).filter(
        Colecao.id_usuario == current_user.id_usuario,
        Colecao.id_planta == dados.id_planta
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta planta já está cadastrada na sua coleção pessoal de descobertas."
        )

    nova_descoberta = Colecao(
        id_usuario=current_user.id_usuario,
        id_planta=dados.id_planta,
        data_descoberta=dados.data_descoberta or date.today(),
        foto_usuario=dados.foto_usuario
    )
    db.add(nova_descoberta)
    db.commit()
    db.refresh(nova_descoberta)

    return nova_descoberta


@router.get(
    "",
    response_model=List[ColecaoResponse],
    summary="Listar Minhas Descobertas (RF09)",
    description="Retorna exclusivamente a lista de PANCs descobertas pelo usuário atualmente autenticado (RNF03)."
)
def listar_minha_colecao(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Isolamento estrito por usuário autenticado
    descobertas = (
        db.query(Colecao)
        .filter(Colecao.id_usuario == current_user.id_usuario)
        .order_by(Colecao.data_descoberta.desc(), Colecao.id_colecao.desc())
        .all()
    )
    return descobertas


@router.get(
    "/{id}",
    response_model=ColecaoDetalheResponse,
    summary="Detalhes da Descoberta e Receitas Sugeridas (RF10)",
    description="Exibe os detalhes de uma descoberta registrada, incluindo ficha botânica da planta e receitas recomendadas."
)
def detalhar_descoberta(
    id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Colecao).filter(Colecao.id_colecao == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Descoberta com ID {id} não encontrada na coleção."
        )

    # Segurança RNF03: Usuário só pode acessar registros da sua própria coleção
    if item.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você só tem permissão para visualizar itens da sua própria coleção."
        )

    # Receitas associadas à planta da descoberta
    receitas_orm = db.query(Receita).filter(Receita.id_planta == item.id_planta).all()
    receitas_resp = [ReceitaResponse.model_validate(r) for r in receitas_orm]

    resp = ColecaoDetalheResponse(
        id_colecao=item.id_colecao,
        id_usuario=item.id_usuario,
        id_planta=item.id_planta,
        data_descoberta=item.data_descoberta,
        foto_usuario=item.foto_usuario,
        planta=item.planta,
        receitas=receitas_resp
    )
    return resp


@router.delete(
    "/{id}",
    summary="Remover Planta da Coleção (RF11)",
    description="Remove um registro de descoberta da coleção pessoal do usuário autenticado."
)
def remover_da_colecao(
    id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Colecao).filter(Colecao.id_colecao == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Descoberta com ID {id} não encontrada na coleção."
        )

    # Segurança RNF03: Usuário só pode remover itens da sua própria coleção
    if item.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você não tem permissão para remover itens da coleção de outro usuário."
        )

    db.delete(item)
    db.commit()

    return {
        "mensagem": "Planta removida da sua coleção com sucesso.",
        "id_removido": id
    }
