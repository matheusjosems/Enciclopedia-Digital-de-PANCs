from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.planta import Planta
from models.regiao import Regiao
from schemas.planta import PlantaResponse

router = APIRouter(prefix="/plantas", tags=["Plantas"])


@router.get(
    "",
    response_model=List[PlantaResponse],
    summary="Catálogo de PANCs com Busca Avançada (RF12)",
    description="Lista as PANCs catalogadas com suporte a busca textual por nome (popular ou científico), filtro por região/bioma e paginação."
)
def listar_plantas(
    nome: Optional[str] = Query(None, description="Busca textual por nome popular ou científico (ex: 'ora', 'peixinho', 'curcuma')"),
    regiao: Optional[str] = Query(None, description="Filtra por região ou bioma (ex: 'Cerrado', 'Mata Atlântica', 'Sudeste')"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(50, ge=1, le=100, description="Quantidade máxima de registros retornados"),
    db: Session = Depends(get_db)
):
    query = db.query(Planta)

    # Busca inteligente por nome popular OU nome científico
    if nome and nome.strip():
        termo = f"%{nome.strip()}%"
        query = query.filter(
            or_(
                Planta.nome_popular.ilike(termo),
                Planta.nome_cientifico.ilike(termo)
            )
        )

    # Filtro por região / bioma
    if regiao and regiao.strip():
        query = query.join(Planta.regioes).filter(
            Regiao.nome.ilike(f"%{regiao.strip()}%")
        )

    plantas = (
        query.order_by(Planta.nome_popular.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return plantas


@router.get(
    "/{id}",
    response_model=PlantaResponse,
    summary="Ficha Completa da Planta (RF06)",
    description="Retorna todos os detalhes técnicos e botânicos de uma PANC: nome popular, científico, família, descrição, partes comestíveis, cuidados e fotos."
)
def detalhar_planta(
    id: int,
    db: Session = Depends(get_db)
):
    planta = db.query(Planta).filter(Planta.id_planta == id).first()
    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Planta com ID {id} não encontrada no catálogo."
        )
    return planta
