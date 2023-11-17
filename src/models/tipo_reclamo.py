# models/tipo_reclamo.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from models.area import Area  # Importa la clase "Area" desde el archivo "area.py"

class TipoReclamo(Base):
    __tablename__ = "tipo_reclamo"

    id_tipo_reclamo = Column(Integer, primary_key=True, index=True)
    id_area = Column(Integer, ForeignKey('area.id_area'))  # Relación con "Area"
    nombre = Column(String)
    
    # Define una relación inversa con la tabla 'reclamo'
    reclamos = relationship("Reclamo", back_populates="tipo_reclamo")
    area = relationship("Area", back_populates="tipos_reclamo")
