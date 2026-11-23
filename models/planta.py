from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base


class Planta(Base):
    __tablename__ = "plantas"

    id_planta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_popular = Column(String(150), nullable=False, index=True)
    nome_cientifico = Column(String(150), nullable=False, unique=True, index=True)
    familia = Column(String(100), nullable=True)
    descricao = Column(Text, nullable=True)
    partes_comestiveis = Column(Text, nullable=True)
    cuidados = Column(Text, nullable=True)
    sabor = Column(String(255), nullable=True)
    foto_url = Column(String(500), nullable=True)

    # Relacionamentos
    receitas = relationship(
        "Receita",
        back_populates="planta",
        cascade="all, delete-orphan"
    )
    colecoes = relationship(
        "Colecao",
        back_populates="planta",
        cascade="all, delete-orphan"
    )
    regioes = relationship(
        "Regiao",
        secondary="planta_regiao",
        back_populates="plantas"
    )
    sazonalidades = relationship(
        "PlantaSazonalidade",
        back_populates="planta",
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        # Compatibilidade com código legado que usa 'id' em vez de 'id_planta' ou 'foto'
        if "id" in kwargs and "id_planta" not in kwargs:
            kwargs["id_planta"] = kwargs.pop("id")
        if "foto" in kwargs and "foto_url" not in kwargs:
            kwargs["foto_url"] = kwargs.pop("foto")
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.id_planta

    @id.setter
    def id(self, value):
        self.id_planta = value

    @property
    def foto(self):
        return self.foto_url

    @foto.setter
    def foto(self, value):
        self.foto_url = value

    def __repr__(self):
        return f"<Planta(id={self.id_planta}, nome_popular='{self.nome_popular}', nome_cientifico='{self.nome_cientifico}')>"
