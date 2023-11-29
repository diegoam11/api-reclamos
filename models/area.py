from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Area(Base):
    __tablename__ = "area"

    id_area = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    tipos_reclamo = relationship("TipoReclamo", back_populates="area")
    tipos_solicitud = relationship("TipoSolicitud", back_populates="area")
