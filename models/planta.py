from pydantic import BaseModel 

class Planta (BaseModel):
    id: int
    nome_popular: str
    nome_cientifico: str
    descricao: str 
