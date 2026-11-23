from pydantic import BaseModel, ConfigDict, Field


class PlantaSazonalidadeBase(BaseModel):
    mes: int = Field(..., ge=1, le=12, description="Mês do ano (1 a 12)")


class PlantaSazonalidadeCreate(PlantaSazonalidadeBase):
    id_planta: int


class PlantaSazonalidadeResponse(PlantaSazonalidadeBase):
    id_planta: int

    model_config = ConfigDict(from_attributes=True)
