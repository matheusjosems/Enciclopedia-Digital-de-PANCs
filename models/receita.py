from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Receita(Base):
    __tablename__ = "receitas"

    id_receita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_planta = Column(Integer, ForeignKey("plantas.id_planta", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(150), nullable=False)
    ingredientes = Column(Text, nullable=False)
    modo_preparo = Column(Text, nullable=False)
    tempo_preparo = Column(String(50), nullable=True)
    rendimento = Column(String(50), nullable=True)

    planta = relationship("Planta", back_populates="receitas")

    def __repr__(self):
        return f"<Receita(id={self.id_receita}, titulo='{self.titulo}', id_planta={self.id_planta})>"
