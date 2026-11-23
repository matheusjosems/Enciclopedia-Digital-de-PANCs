from typing import Optional
from pydantic import BaseModel, ConfigDict


class RegiaoBase(BaseModel):
    nome: str
    tipo: Optional[str] = None


class RegiaoCreate(RegiaoBase):
    pass


class RegiaoResponse(RegiaoBase):
    id_regiao: int

    model_config = ConfigDict(from_attributes=True)
