from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.reclamo import Reclamo
from repositories.reclamo_repository import ReclamoRepository
from schemas.base import ReclamoBase

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
        db_reclamo = reclamo_repository(db).create_reclamo(reclamo.dict())
        return db_reclamo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/reclamos/")
def get_reclamos(db: Session = Depends(get_db)):
    try:
        db_reclamos = reclamo_repository(db).get_reclamos()
        return db_reclamos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/reclamos/{id_cliente}")
def get_reclamo_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        reclamo = reclamo_repository(db).get_reclamo_by_id_cliente(id_cliente)
        if not reclamo:
            raise HTTPException(status_code=404, detail="Reclamo no encontrado")
        return reclamo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
