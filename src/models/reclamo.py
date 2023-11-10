from models.tipo_reclamo import TipoReclamo
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Reclamo(Base):
    __tablename__ = "reclamo"

    id_reclamo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)
    id_tipo_reclamo = Column(Integer, ForeignKey('tipo_reclamo.id_tipo_reclamo'))

    tipo_bien_contratado = Column(Integer) # producto, servicio (setear)
    orden_compra = Column(Integer)
    codigo_producto = Column(Integer)
    fecha_compra = Column(Date) #AGREGADO
    
    forma_respuesta = Column(String) # Correo Electrónico, Carta, Presencial (setear)
    fecha_reclamo = Column(Date)

    detalle_reclamo = Column(String)
    monto_reclamado = Column(Numeric)
    peticion_del_cliente = Column(String)

    acciones_tomadas = Column(String)    
    estado = Column(Integer) # pendiente, resuelto
    fecha_respuesta = Column(Date) #fecha resolución
    fecha_limite = Column(Date)  #AGREGADO

    tipo_reclamo = relationship("TipoReclamo", back_populates="reclamos")