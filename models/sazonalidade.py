from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PlantaSazonalidade(Base):
    __tablename__ = "planta_sazonalidade"

    id_planta = Column(Integer, ForeignKey("plantas.id_planta", ondelete="CASCADE"), primary_key=True)
    mes = Column(Integer, primary_key=True)  # 1 a 12 (Janeiro a Dezembro)

    planta = relationship("Planta", back_populates="sazonalidades")

    def __repr__(self):
        return f"<PlantaSazonalidade(id_planta={self.id_planta}, mes={self.mes})>"
