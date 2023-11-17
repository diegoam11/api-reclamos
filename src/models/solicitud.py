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
    codigo_producto = Column(Integer)
    orden_compra = Column(Integer)
    descripcion = Column(String)
    peticion_del_cliente = Column(String)
    forma_respuesta = Column(Integer)
    fecha_solicitud = Column(Date)
    estado = Column(Integer)
    acciones_tomadas = Column(String)
    fecha_respuesta = Column(Date)

    tipo_solicitud = relationship("TipoSolicitud", back_populates="solicitudes")