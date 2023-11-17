from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Queja(Base):
    __tablename__ = "queja"

    id_queja = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)

    tipo_bien_contratado = Column(Integer) 
    orden_compra = Column(Integer) 
    codigo_producto = Column(Integer) 
    fecha_compra = Column(Date) 
    
    forma_respuesta = Column(String)
    fecha_queja = Column(Date) 
    
    detalle_queja = Column(String) 
    peticion_cliente = Column(String) 
    
    acciones_tomadas = Column(String)
    estado = Column(Integer)
    fecha_respuesta = Column(Date)
    fecha_limite = Column(Date)