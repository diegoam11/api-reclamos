from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class TipoSolicitud(Base):
    __tablename__ = "tipo_solicitud"

    id_tipo_solicitud = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    solicitudes = relationship("Solicitud", back_populates="tipo_solicitud")
