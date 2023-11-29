from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class TipoSolicitud(Base):
    __tablename__ = "tipo_solicitud"

    id_tipo_solicitud = Column(Integer, primary_key=True, index=True)
    id_area = Column(Integer, ForeignKey('area.id_area'))  # Relación con "Area"
    nombre = Column(String)

    solicitudes = relationship("Solicitud", back_populates="tipo_solicitud")
    area = relationship("Area", back_populates="tipos_solicitud")