from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class TipoReclamo(Base):
    __tablename__ = "tipo_reclamo"

    id_tipo_reclamo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    # Define una relación inversa con la tabla 'reclamo'
    reclamos = relationship("Reclamo", back_populates="tipo_reclamo")
