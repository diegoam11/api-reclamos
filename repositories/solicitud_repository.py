from sqlalchemy.orm import Session
from sqlalchemy import case
from models.solicitud import Solicitud
from models.tipo_solicitud import TipoSolicitud
from datetime import datetime, timedelta


class SolicitudRepository:
    def create_solicitud(self, db: Session, solicitud_data):
        fecha_solicitud = datetime.now()
        fecha_limite = self._calculate_fecha_limite(fecha_solicitud)

        solicitud_data.update(
            {
                "fecha_solicitud": fecha_solicitud,
                "fecha_limite": fecha_limite,
                "estado": 0,
            }
        )

        db_solicitud = Solicitud(**solicitud_data)
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud

    def _get_solicitudes_query(self, db: Session):
        print("hola")
        return db.query(
            Solicitud.id_solicitud,
            Solicitud.tipo_bien_contratado.label("id_tipo_bien_contratado"),
            case(
                (Solicitud.tipo_bien_contratado == 0, "producto"),
                (Solicitud.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Solicitud.codigo_producto,
            Solicitud.forma_respuesta,
            Solicitud.detalle_solicitud,
            Solicitud.peticion_cliente,
            Solicitud.estado.label("id_estado"),
            case(
                (Solicitud.estado is None, "pendiente"),
                (Solicitud.estado == 0, "pendiente"),
                (Solicitud.estado == 1, "derivado"),
                (Solicitud.estado == 2, "resuelto"),
            ).label("estado"),
            Solicitud.fecha_limite,
            Solicitud.id_tipo_solicitud,
            TipoSolicitud.nombre.label("tipo_solicitud"),
            Solicitud.id_cliente,
            Solicitud.orden_compra,
            Solicitud.fecha_solicitud,
            Solicitud.acciones_tomadas,
            Solicitud.fecha_respuesta,
        ).join(TipoSolicitud)

    def get_solicitudes(self, db: Session):

        solicitudes = self._get_solicitudes_query(db).all()

        result = []
        for solicitud in solicitudes:
            solicitud_dict = dict(solicitud._asdict())
            result.append(solicitud_dict)

        return result

    def get_solicitud_by_id_cliente(self, db: Session, id_cliente: int):
        solicitudes = (
            self._get_solicitudes_query(db).filter(Solicitud.id_cliente == id_cliente).all()
        )

        result = []
        for solicitud in solicitudes:
            solicitud_dict = dict(solicitud._asdict())
            result.append(solicitud_dict)

        return result

    def _calculate_fecha_limite(self, fecha_solicitud):
        delta_dias = 15

        fecha_limite = fecha_solicitud
        dias_habiles = 0

        while dias_habiles < delta_dias:
            fecha_limite += timedelta(days=1)
            if fecha_limite.weekday() not in [5, 6]:
                dias_habiles += 1

        return fecha_limite