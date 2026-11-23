from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from schemas.planta import PlantaResponse
from schemas.receita import ReceitaResponse


class ColecaoBase(BaseModel):
    id_planta: int
    foto_usuario: Optional[str] = None
    data_descoberta: Optional[date] = None


class ColecaoCreate(ColecaoBase):
    pass


class ColecaoResponse(BaseModel):
    id_colecao: int
    id_usuario: int
    id_planta: int
    data_descoberta: date
    foto_usuario: Optional[str] = None
    planta: Optional[PlantaResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ColecaoDetalheResponse(ColecaoResponse):
    receitas: List[ReceitaResponse] = []
