from pydantic import BaseModel
from datetime import date

class ReclamoBase(BaseModel):
    id_cliente: int
    id_tipo_reclamo: int
    tipo_bien_contratado: int
    codigo_producto: int
    orden_compra: int
    descripcion: str
    monto_reclamado: float
    peticion_del_cliente: str
    forma_respuesta: int
    fecha_reclamo: date

class QuejaBase(BaseModel):
    id_cliente: int
    descripcion: str
    peticion_cliente: str
    forma_respuesta: int
    fecha_queja: date

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