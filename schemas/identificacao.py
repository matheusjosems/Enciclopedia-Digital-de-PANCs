from typing import Optional, List
from pydantic import BaseModel
from schemas.receita import ReceitaResponse


class IdentificacaoAlternativa(BaseModel):
    id_planta: int
    nome_popular: str
    nome_cientifico: str
    confianca: float


class IdentificacaoResponse(BaseModel):
    id_planta: int
    nome_popular: str
    nome_cientifico: str
    familia: Optional[str] = None
    confianca: float  # Taxa percentual (ex: 88.5)
    baixa_confianca: bool = False  # Indica alerta de baixa confiança (RNF07)
    aviso_confianca: Optional[str] = None  # Orientação para reenvio se confiança for baixa (RNF07)
    foto_enviada_url: str
    aviso_seguranca: str  # Aviso ético/botânico obrigatório (RF14)
    descricao: Optional[str] = None
    partes_comestiveis: Optional[str] = None
    cuidados: Optional[str] = None
    receitas_sugeridas: List[ReceitaResponse] = []
    outras_possibilidades: List[IdentificacaoAlternativa] = []
