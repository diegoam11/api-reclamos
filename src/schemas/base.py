from pydantic import BaseModel
from datetime import date

class ReclamoBase(BaseModel):
    id_cliente: int
    id_tipo_reclamo: int

    fecha_reclamo: date
    forma_respuesta: str
    tipo_bien_contratado: int
    fecha_compra: date
    orden_compra: int
    codigo_producto: int
    detalle_reclamo: str
    monto_reclamado: float
    peticion_cliente: str
    

class QuejaBase(BaseModel):
    id_cliente: int
    fecha_queja: date
    forma_respuesta: int
    tipo_bien_contratado: int
    fecha_compra: date
    orden_compra: int
    codigo_producto: int
    detalle_queja: str
    peticion_cliente: str
    
    
class SolicitudBase(BaseModel):
    id_cliente: int
    id_tipo_solicitud: int
    tipo_bien_contratado: int
    codigo_producto: int
    orden_compra: int
    descripcion: str
    peticion_del_cliente: str
    forma_respuesta: int
    fecha_solicitud: date
