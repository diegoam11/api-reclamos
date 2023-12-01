from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.solicitud import Solicitud
from repositories.solicitud_repository import SolicitudRepository
from schemas.base import RqsActions, SolicitudBase


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


router = APIRouter()
Solicitud.metadata.create_all(bind=database_config.engine)


def get_db() -> Session:
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


solicitud_repository = SolicitudRepository()


@router.post("/solicitudes/")
async def create_solicitudes(solicitud: SolicitudBase, db: Session = Depends(get_db)):
    try:
        db_solicitud = solicitud_repository.create_solicitud(db, solicitud.dict())
        return db_solicitud
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/solicitudes/")
def get_solicitudes(db: Session = Depends(get_db)):
    try:
        db_solicitudes = solicitud_repository.get_solicitudes(db)
        return db_solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/solicitudes/area/{id_area}")
def get_solicitudes_by_area(id_area: int, db: Session = Depends(get_db)):
    try:
        solicitudes = solicitud_repository.get_solicitudes_by_area(db, id_area)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/solicitudes/{id_solicitud}")
def get_solicitud_por_id(id_solicitud: int, db: Session = Depends(get_db)):
    try:
        solicitud = solicitud_repository.get_solicitud_by_id(db, id_solicitud)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/solicitudes/cliente/{id_cliente}")
def get_solicitud_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        solicitudes = solicitud_repository.get_solicitud_by_id_cliente(db, id_cliente)
        if solicitudes is None:
            raise CustomException(status_code=404, detail="Solicitud not found")
        return solicitudes
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/solicitudes/actions/{id_solicitud}")
def update_reclamo(
    id_solicitud: int, solicitud_actions: RqsActions, db: Session = Depends(get_db)
):
    try:
        solicitud = solicitud_repository.get_solicitud_by_id(db, id_solicitud)

        if solicitud is None:
            raise CustomException(status_code=404, detail="Solicitud not found")

        solicitud.estado = 1
        solicitud.acciones_tomadas = solicitud_actions.acciones_tomadas
        solicitud.fecha_respuesta = solicitud_actions.fecha_respuesta

        db.add(solicitud)
        db.commit()
        db.refresh(solicitud)
        return solicitud

    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
