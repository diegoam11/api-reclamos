from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.queja import Queja
from repositories.queja_repository import QuejaRepository
from schemas.base import RqsActions, QuejaBase


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


router = APIRouter()
Queja.metadata.create_all(bind=database_config.engine)


def get_db() -> Session:
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


queja_repository = QuejaRepository()


@router.post("/quejas/")
async def create_quejas(queja: QuejaBase, db: Session = Depends(get_db)):
    try:
        db_queja = queja_repository.create_queja(db, queja.dict())
        return db_queja
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/quejas/")
def get_quejas(db: Session = Depends(get_db)):
    try:
        db_quejas = queja_repository.get_quejas(db)
        return db_quejas
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/quejas/{id_queja}")
def get_queja_por_id(id_queja: int, db: Session = Depends(get_db)):
    try:
        queja = queja_repository.get_queja_by_id(db, id_queja)
        if queja is None:
            raise CustomException(status_code=404, detail="Queja not found")
        return queja
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/quejas/cliente/{id_cliente}")
def get_queja_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        quejas = queja_repository.get_queja_by_id_cliente(db, id_cliente)
        if quejas is None:
            raise CustomException(status_code=404, detail="Queja not found")

        return quejas
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.patch("/quejas/actions/{id_queja}")
def update_reclamo(
    id_queja: int, queja_actions: RqsActions, db: Session = Depends(get_db)
):
    try:
        queja = queja_repository.get_queja_by_id(db, id_queja)

        if queja is None:
            raise CustomException(status_code=404, detail="Queja not found")

        queja.estado = 1

        queja.estado = 1
        queja.acciones_tomadas = queja_actions.acciones_tomadas
        queja.fecha_respuesta = queja_actions.fecha_respuesta

        db.add(queja)
        db.commit()
        db.refresh(queja)
        return queja
    except CustomException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
