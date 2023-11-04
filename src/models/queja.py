from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Queja(Base):
    __tablename__ = "queja"

    id_queja = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)
    descripcion = Column(String) 
    peticion_cliente = Column(String) 
    forma_respuesta = Column(Integer)
    fecha_queja = Column(Date)
    estado = Column(Integer)
    acciones_tomadas = Column(String)
    fecha_respuesta = Column(Date)