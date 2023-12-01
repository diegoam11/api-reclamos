from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.reclamo import Reclamo
from repositories.reclamo_repository import ReclamoRepository
from schemas.base import ReclamoBase, RqsActions


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


router = APIRouter()
Reclamo.metadata.create_all(bind=database_config.engine)


def get_db() -> Session:
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


reclamo_repository = ReclamoRepository()


@router.post("/reclamos/")
async def create_reclamos(reclamo: ReclamoBase, db: Session = Depends(get_db)):
    try:
        db_reclamo = reclamo_repository.create_reclamo(db, reclamo.dict())
        return db_reclamo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/reclamos/")
def get_reclamos(db: Session = Depends(get_db)):
    try:
        db_reclamos = reclamo_repository.get_reclamos(db)
        return db_reclamos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/reclamos/area/{id_area}")
def get_reclamos_by_area(id_area: int, db: Session = Depends(get_db)):
    try:
        reclamos = reclamo_repository.get_reclamos_by_area(db, id_area)
        return reclamos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/reclamos/{id_reclamo}")
def get_reclamo_by_id(id_reclamo: int, db: Session = Depends(get_db)):
    try:
        reclamo = reclamo_repository.get_reclamo_by_id(db, id_reclamo)
        if reclamo is None:
            raise CustomException(status_code=404, detail="Reclamo not found")
        return reclamo
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/reclamos/cliente/{id_cliente}")
def get_reclamo_by_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        reclamo = reclamo_repository.get_reclamo_by_id_cliente(db, id_cliente)
        if reclamo is None:
            raise CustomException(status_code=404, detail="Reclamo not found")
        return reclamo
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/reclamos/actions/{id_reclamo}")
def update_reclamo(
    id_reclamo: int, reclamo_actions: RqsActions, db: Session = Depends(get_db)
):
    try:
        reclamo = reclamo_repository.get_reclamo_by_id(db, id_reclamo)

        if reclamo is None:
            raise CustomException(status_code=404, detail="Reclamo not found")

        reclamo.estado = 1
        reclamo.acciones_tomadas = reclamo_actions.acciones_tomadas
        reclamo.fecha_respuesta = reclamo_actions.fecha_respuesta

        db.add(reclamo)
        db.commit()
        db.refresh(reclamo)
        return reclamo
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
