from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.planta import Planta
from models.receita import Receita
from schemas.receita import ReceitaResponse, ReceitaDetalheResponse

router = APIRouter(tags=["Receitas"])


@router.get(
    "/plantas/{id}/receitas",
    response_model=List[ReceitaResponse],
    summary="Receitas Culinárias da Planta (RF07)",
    description="Lista todas as receitas gastronômicas e sugestões de preparo associadas à PANC informada."
)
def listar_receitas_por_planta(
    id: int,
    db: Session = Depends(get_db)
):
    planta = db.query(Planta).filter(Planta.id_planta == id).first()
    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planta com ID {id} não encontrada no catálogo."
        )

    receitas = db.query(Receita).filter(Receita.id_planta == id).all()
    return receitas


@router.get(
    "/receitas/{id}",
    response_model=ReceitaDetalheResponse,
    summary="Ficha Completa da Receita (RF13)",
    description="Retorna o passo a passo de uma receita culinária PANC, com título, ingredientes, modo de preparo, tempo e rendimento."
)
def detalhar_receita(
    id: int,
    db: Session = Depends(get_db)
):
    receita = db.query(Receita).filter(Receita.id_receita == id).first()
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receita com ID {id} não encontrada."
        )

    # Adiciona dados da planta associada para conveniência do front-end
    resp = ReceitaDetalheResponse(
        id_receita=receita.id_receita,
        id_planta=receita.id_planta,
        titulo=receita.titulo,
        ingredientes=receita.ingredientes,
        modo_preparo=receita.modo_preparo,
        tempo_preparo=receita.tempo_preparo,
        rendimento=receita.rendimento,
        nome_popular_planta=receita.planta.nome_popular if receita.planta else None,
        nome_cientifico_planta=receita.planta.nome_cientifico if receita.planta else None
    )
    return resp


@router.get(
    "/receitas",
    response_model=List[ReceitaResponse],
    summary="Listar Todas as Receitas Culinárias",
    description="Retorna o catálogo geral de receitas disponíveis para PANCs do Cerrado."
)
def listar_todas_receitas(
    db: Session = Depends(get_db)
):
    return db.query(Receita).order_by(Receita.titulo.asc()).all()
