from models.tipo_solicitud import TipoSolicitud
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Solicitud(Base):
    __tablename__ = "solicitud"

    id_solicitud = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)
    id_tipo_solicitud = Column(Integer, ForeignKey('tipo_solicitud.id_tipo_solicitud'))

    tipo_bien_contratado = Column(Integer) 
    orden_compra = Column(Integer)
    codigo_producto = Column(Integer)

    forma_respuesta = Column(String)
    fecha_solicitud = Column(Date)

    detalle_solicitud = Column(String)
    peticion_cliente = Column(String)
    
    acciones_tomadas = Column(String)
    estado = Column(Integer)
    fecha_respuesta = Column(Date)
    fecha_limite = Column(Date)

    tipo_solicitud = relationship("TipoSolicitud", back_populates="solicitudes")

    __allow_unmapped__ = True