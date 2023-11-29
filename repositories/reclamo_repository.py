from sqlalchemy.orm import Session
from sqlalchemy import case
from models.reclamo import Reclamo
from models.tipo_reclamo import TipoReclamo
from utils.date_utils import calculate_fecha_limite, date_now

class ReclamoRepository:
    def create_reclamo(self, db: Session, reclamo_data):
        fecha_reclamo = date_now()
        fecha_limite = calculate_fecha_limite(fecha_reclamo)

        reclamo_data.update(
            {
                "fecha_reclamo": fecha_reclamo,
                "fecha_limite": fecha_limite,
                "estado": 0,
            }
        )

        db_reclamo = Reclamo(**reclamo_data)
        db.add(db_reclamo)
        db.commit()
        db.refresh(db_reclamo)
        return db_reclamo

    def _get_reclamos_query(self, db: Session):
        return db.query(
            Reclamo.id_reclamo,
            Reclamo.tipo_bien_contratado.label("id_tipo_bien_contratado"),
            case(
                (Reclamo.tipo_bien_contratado == 0, "producto"),
                (Reclamo.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Reclamo.codigo_producto,
            Reclamo.forma_respuesta,
            Reclamo.detalle_reclamo,
            Reclamo.peticion_cliente,
            Reclamo.estado.label("id_estado"),
            case(
                (Reclamo.estado is None, "derivado"),
                (Reclamo.estado == 0, "derivado"),
                (Reclamo.estado == 1, "resuelto"),
            ).label("estado"),
            Reclamo.fecha_limite,
            Reclamo.id_tipo_reclamo,
            TipoReclamo.nombre.label("tipo_reclamo"),
            Reclamo.id_cliente,
            Reclamo.orden_compra,
            Reclamo.fecha_compra,
            Reclamo.fecha_reclamo,
            Reclamo.monto_reclamado,
            Reclamo.acciones_tomadas,
            Reclamo.fecha_respuesta,
        ).join(TipoReclamo)

    def get_reclamos(self, db: Session):
        reclamos = self._get_reclamos_query(db).all()

        result = []
        for reclamo in reclamos:
            reclamo_dict = dict(reclamo._asdict())
            result.append(reclamo_dict)

        return result

    def get_reclamo_by_id(self, db: Session, id_reclamo: int):
        return db.query(Reclamo).filter(Reclamo.id_reclamo == id_reclamo).one_or_none()

    def get_reclamo_by_id_cliente(self, db: Session, id_cliente: int):
        reclamo = db.query(Reclamo).filter(Reclamo.id_cliente == id_cliente).all()
        return reclamo or None
