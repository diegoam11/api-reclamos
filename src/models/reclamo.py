from models.tipo_reclamo import TipoReclamo
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Reclamo(Base):
    __tablename__ = "reclamo"

    id_reclamo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)
    id_tipo_reclamo = Column(Integer, ForeignKey('tipo_reclamo.id_tipo_reclamo'))
    tipo_bien_contratado = Column(Integer)
    codigo_producto = Column(Integer)
    orden_compra = Column(Integer)
    descripcion = Column(String)
    monto_reclamado = Column(Numeric)
    peticion_del_cliente = Column(String)
    forma_respuesta = Column(Integer)
    fecha_reclamo = Column(Date)
    estado = Column(Integer)
    acciones_tomadas = Column(String)
    fecha_respuesta = Column(Date)

    tipo_reclamo = relationship("TipoReclamo", back_populates="reclamos")
