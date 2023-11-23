from sqlalchemy.orm import Session
from sqlalchemy import case
from models.reclamo import Reclamo
from models.tipo_reclamo import TipoReclamo
from datetime import datetime, timedelta


class ReclamoRepository:
    def create_reclamo(self, db: Session, reclamo_data):
        fecha_reclamo = datetime.now()
        fecha_limite = self._calculate_fecha_limite(fecha_reclamo)

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
            Reclamo.tipo_bien_contratado,
            case(
                (Reclamo.tipo_bien_contratado == 0, "producto"),
                (Reclamo.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Reclamo.codigo_producto,
            Reclamo.forma_respuesta,
            Reclamo.detalle_reclamo,
            Reclamo.peticion_cliente,
            case(
                (Reclamo.estado is None, "pendiente"),
                (Reclamo.estado == 0, "pendiente"),
                (Reclamo.estado == 1, "derivado"),
                (Reclamo.estado == 2, "resuelto"),
            ).label("estado"),
            Reclamo.fecha_limite,
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

    def get_reclamo_by_id_cliente(self, db: Session, id_cliente: int):
        reclamos = (
            self._get_reclamos_query(db).filter(Reclamo.id_cliente == id_cliente).all()
        )

        result = []
        for reclamo in reclamos:
            reclamo_dict = dict(reclamo._asdict())
            result.append(reclamo_dict)

        return result

    def _calculate_fecha_limite(self, fecha_reclamo):
        delta_dias = 15

        fecha_limite = fecha_reclamo
        dias_habiles = 0

        while dias_habiles < delta_dias:
            fecha_limite += timedelta(days=1)
            if fecha_limite.weekday() not in [5, 6]:
                dias_habiles += 1

        return fecha_limite
