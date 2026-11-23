from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabela associativa n:m PLANTA_REGIAO conforme diagrama ER
planta_regiao = Table(
    "planta_regiao",
    Base.metadata,
    Column("id_planta", Integer, ForeignKey("plantas.id_planta", ondelete="CASCADE"), primary_key=True),
    Column("id_regiao", Integer, ForeignKey("regioes.id_regiao", ondelete="CASCADE"), primary_key=True)
)


class Regiao(Base):
    __tablename__ = "regioes"

    id_regiao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    tipo = Column(String(50), nullable=True)  # ex: Bioma, Região Geográfica, Estado

    plantas = relationship(
        "Planta",
        secondary=planta_regiao,
        back_populates="regioes"
    )

    def __repr__(self):
        return f"<Regiao(id={self.id_regiao}, nome='{self.nome}', tipo='{self.tipo}')>"
