from sqlalchemy.orm import Session
from sqlalchemy import case
from models.queja import Queja
from datetime import datetime, timedelta


class QuejaRepository:
    def create_queja(self, db: Session, queja_data):
        fecha_queja = datetime.now()
        fecha_limite = self._calculate_fecha_limite(fecha_queja)

        queja_data.update(
            {
                "fecha_queja": fecha_queja,
                "fecha_limite": fecha_limite,
                "estado": 0,
            }
        )

        db_queja = Queja(**queja_data)
        db.add(db_queja)
        db.commit()
        db.refresh(db_queja)
        return db_queja

    def _get_quejas_query(self, db: Session):
        return db.query(
            Queja.id_queja,
            Queja.tipo_bien_contratado.label("id_tipo_bien_contratado"),
            case(
                (Queja.tipo_bien_contratado == 0, "producto"),
                (Queja.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Queja.codigo_producto,
            Queja.forma_respuesta,
            Queja.detalle_queja,
            Queja.peticion_cliente,
            Queja.estado.label("id_estado"),
            case(
                (Queja.estado is None, "pendiente"),
                (Queja.estado == 0, "pendiente"),
                (Queja.estado == 1, "derivado"),
                (Queja.estado == 2, "resuelto"),
            ).label("estado"),
            Queja.fecha_limite,
            Queja.id_cliente,
            Queja.orden_compra,
            Queja.fecha_compra,
            Queja.fecha_queja,
            Queja.acciones_tomadas,
            Queja.fecha_respuesta,
        )

    def get_quejas(self, db: Session):
        quejas = self._get_quejas_query(db).all()

        result = []
        for queja in quejas:
            queja_dict = dict(queja._asdict())
            result.append(queja_dict)

        return result

    def get_queja_by_id_cliente(self, db: Session, id_cliente: int):
        quejas = (
            self._get_quejas_query(db).filter(Queja.id_cliente == id_cliente).all()
        )

        result = []
        for queja in quejas:
            queja_dict = dict(queja._asdict())
            result.append(queja_dict)

        return result

    def _calculate_fecha_limite(self, fecha_queja):
        delta_dias = 15

        fecha_limite = fecha_queja
        dias_habiles = 0

        while dias_habiles < delta_dias:
            fecha_limite += timedelta(days=1)
            if fecha_limite.weekday() not in [5, 6]:
                dias_habiles += 1

        return fecha_limite