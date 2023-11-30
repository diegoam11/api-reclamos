from sqlalchemy.orm import Session
from sqlalchemy import case
from models.queja import Queja
from utils.date_utils import calculate_fecha_limite, date_now


class QuejaRepository:
    def create_queja(self, db: Session, queja_data):
        fecha_queja = date_now()
        fecha_limite = calculate_fecha_limite(fecha_queja)

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
            Queja.id_cliente,
            Queja.tipo_bien_contratado.label("id_tipo_bien_contratado"),
            case(
                (Queja.tipo_bien_contratado == 0, "producto"),
                (Queja.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Queja.orden_compra,
            Queja.codigo_producto,
            Queja.forma_respuesta,
            Queja.detalle_queja,
            Queja.peticion_cliente,
            Queja.estado.label("id_estado"),
            case(
                (Queja.estado is None, "derivado"),
                (Queja.estado == 0, "derivado"),
                (Queja.estado == 1, "resuelto"),
            ).label("estado"),
            Queja.fecha_compra,
            Queja.fecha_queja,
            Queja.fecha_limite,
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

    def get_queja_by_id(self, db: Session, id_queja: int):
        return db.query(Queja).filter(Queja.id_queja == id_queja).one_or_none()

    def get_queja_by_id_cliente(self, db: Session, id_cliente: int):
        quejas = self._get_quejas_query(db).filter(Queja.id_cliente == id_cliente).all()
        result = [dict(queja._asdict()) for queja in quejas]
        return result or None
