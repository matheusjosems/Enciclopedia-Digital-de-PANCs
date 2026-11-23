from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Colecao(Base):
    __tablename__ = "colecao"

    id_colecao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False, index=True)
    id_planta = Column(Integer, ForeignKey("plantas.id_planta", ondelete="CASCADE"), nullable=False, index=True)
    data_descoberta = Column(Date, default=date.today, nullable=False)
    foto_usuario = Column(String(500), nullable=True)

    # Restrição de unicidade para evitar duplicatas da mesma planta na coleção do mesmo usuário
    __table_args__ = (
        UniqueConstraint("id_usuario", "id_planta", name="uq_usuario_planta_colecao"),
    )

    usuario = relationship("Usuario", back_populates="colecoes")
    planta = relationship("Planta", back_populates="colecoes")

    def __repr__(self):
        return f"<Colecao(id={self.id_colecao}, id_usuario={self.id_usuario}, id_planta={self.id_planta})>"
