# reclamo_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.reclamo import Reclamo
from repositories.reclamo_repository import ReclamoRepository
from schemas.base import ReclamoBase
from enum import Enum
from strategies.strategies import (
    EmailResponseStrategy,
    LetterResponseStrategy,
    InPersonResponseStrategy,
)


class FormaRespuesta(Enum):
    EMAIL = "email"
    LETTER = "letter"
    IN_PERSON = "in_person"


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

        forma_respuesta = FormaRespuesta(reclamo.forma_respuesta.lower())

        if forma_respuesta == FormaRespuesta.EMAIL:
            email_strategy = EmailResponseStrategy()
            db_reclamo.set_response_strategy(email_strategy)
        elif forma_respuesta == FormaRespuesta.LETTER:
            letter_strategy = LetterResponseStrategy()
            db_reclamo.set_response_strategy(letter_strategy)
        elif forma_respuesta == FormaRespuesta.IN_PERSON:
            in_person_strategy = InPersonResponseStrategy()
            db_reclamo.set_response_strategy(in_person_strategy)

        db_reclamo.execute_response_strategy()
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


@router.get("/reclamos/{id_cliente}")
def get_reclamo_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        reclamo = reclamo_repository.get_reclamo_by_id_cliente(db, id_cliente)
        return reclamo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
