from sqlalchemy.orm import Session
from sqlalchemy import case
from models.solicitud import Solicitud
from models.tipo_solicitud import TipoSolicitud
from utils.date_utils import calculate_fecha_limite, date_now


class SolicitudRepository:
    def create_solicitud(self, db: Session, solicitud_data):
        fecha_solicitud = date_now()
        fecha_limite = calculate_fecha_limite(fecha_solicitud)

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
        return db.query(
            Solicitud.id_solicitud,
            Solicitud.id_tipo_solicitud,
            TipoSolicitud.nombre.label("tipo_solicitud"),
            Solicitud.id_cliente,
            TipoSolicitud.id_area.label("id_area_asociada"),
            case(
                (TipoSolicitud.id_area == 1, "Clientes"),
                (TipoSolicitud.id_area == 2, "Ventas"),
                (TipoSolicitud.id_area == 3, "Reclamos, Solicitudes y Quejas"),
                (TipoSolicitud.id_area == 4, "Reparaciones"),
                (TipoSolicitud.id_area == 5, "Marketing"),
                (TipoSolicitud.id_area == 6, "Autoconsulta"),
            ).label("area_asociada"),
            Solicitud.tipo_bien_contratado.label("id_tipo_bien_contratado"),
            case(
                (Solicitud.tipo_bien_contratado == 0, "producto"),
                (Solicitud.tipo_bien_contratado != 0, "servicio"),
            ).label("tipo_bien_contratado"),
            Solicitud.orden_compra,
            Solicitud.codigo_producto,
            Solicitud.forma_respuesta,
            Solicitud.detalle_solicitud,
            Solicitud.peticion_cliente,
            Solicitud.estado.label("id_estado"),
            case(
                (Solicitud.estado is None, "derivado"),
                (Solicitud.estado == 0, "derivado"),
                (Solicitud.estado == 1, "resuelto"),
            ).label("estado"),
            Solicitud.fecha_solicitud,
            Solicitud.fecha_limite,
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

    def get_solicitud_by_id(self, db: Session, id_solicitud: int):
        return (
            db.query(Solicitud)
            .filter(Solicitud.id_solicitud == id_solicitud)
            .one_or_none()
        )

    def get_solicitud_by_id_cliente(self, db: Session, id_cliente: int):
        solicitudes = (
            self._get_solicitudes_query(db)
            .filter(Solicitud.id_cliente == id_cliente)
            .all()
        )

        result = [dict(solicitud._asdict()) for solicitud in solicitudes]

        return result or None

    def get_solicitudes_by_area(self, db: Session, id_area: int):
        solicitudes = (
            self._get_solicitudes_query(db)
            .filter(TipoSolicitud.id_area == id_area)
            .all()
        )
        result = [dict(solicitud._asdict()) for solicitud in solicitudes]
        return result or None
