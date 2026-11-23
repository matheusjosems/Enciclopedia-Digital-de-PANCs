from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from schemas.regiao import RegiaoResponse


class PlantaBase(BaseModel):
    nome_popular: str
    nome_cientifico: str
    familia: Optional[str] = None
    descricao: Optional[str] = None
    partes_comestiveis: Optional[str] = None
    cuidados: Optional[str] = None
    sabor: Optional[str] = None
    foto_url: Optional[str] = None


class PlantaCreate(PlantaBase):
    pass


class PlantaUpdate(BaseModel):
    nome_popular: Optional[str] = None
    nome_cientifico: Optional[str] = None
    familia: Optional[str] = None
    descricao: Optional[str] = None
    partes_comestiveis: Optional[str] = None
    cuidados: Optional[str] = None
    sabor: Optional[str] = None
    foto_url: Optional[str] = None


class PlantaResponse(PlantaBase):
    id_planta: int
    regioes: List[RegiaoResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Alias para retrocompatibilidade
PlantaSchema = PlantaResponse
