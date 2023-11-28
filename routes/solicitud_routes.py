from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.solicitud import Solicitud
from repositories.solicitud_repository import SolicitudRepository
from schemas.base import SolicitudBase

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
    # try:
        db_solicitudes = solicitud_repository.get_solicitudes(db)
        return db_solicitudes
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/solicitudes/{id_cliente}")
def get_solicitud_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        solicitud = solicitud_repository.get_solicitud_by_id_cliente(db, id_cliente)  
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")