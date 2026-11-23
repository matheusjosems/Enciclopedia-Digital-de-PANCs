from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReceitaBase(BaseModel):
    titulo: str
    ingredientes: str
    modo_preparo: str
    tempo_preparo: Optional[str] = "15 minutos"
    rendimento: Optional[str] = "2 a 4 porções"


class ReceitaCreate(ReceitaBase):
    id_planta: int


class ReceitaResponse(ReceitaBase):
    id_receita: int
    id_planta: int

    model_config = ConfigDict(from_attributes=True)


class ReceitaDetalheResponse(ReceitaResponse):
    nome_popular_planta: Optional[str] = None
    nome_cientifico_planta: Optional[str] = None
