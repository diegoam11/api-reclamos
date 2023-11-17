# reclamo.py
from models.tipo_reclamo import TipoReclamo
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from strategies.strategies import ResponseStrategy

class Reclamo(Base):
    __tablename__ = "reclamo"

    id_reclamo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer)
    id_tipo_reclamo = Column(Integer, ForeignKey('tipo_reclamo.id_tipo_reclamo'))

    tipo_bien_contratado = Column(Integer) 
    orden_compra = Column(Integer)
    codigo_producto = Column(Integer)
    fecha_compra = Column(Date) 
    
    forma_respuesta = Column(String) 
    fecha_reclamo = Column(Date)

    detalle_reclamo = Column(String)
    monto_reclamado = Column(Numeric)
    peticion_cliente = Column(String)

    acciones_tomadas = Column(String)    
    estado = Column(Integer) 
    fecha_respuesta = Column(Date) 
    fecha_limite = Column(Date)  

    tipo_reclamo = relationship("TipoReclamo", back_populates="reclamos")

    __allow_unmapped__ = True

    response_strategy: ResponseStrategy = None

    def execute_response_strategy(self):
        if self.response_strategy:
            self.response_strategy.execute(self)
    
    def set_response_strategy(self, strategy: ResponseStrategy):
        self.response_strategy = strategy