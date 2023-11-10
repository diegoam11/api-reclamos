from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import database_config
from models.queja import Queja
from repositories.queja_repository import QuejaRepository
from schemas.base import QuejaBase

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

@router.get("/quejas/{id_cliente}")
def get_queja_de_cliente(id_cliente: int, db: Session = Depends(get_db)):
    try:
        quejas = queja_repository.get_queja_by_id_cliente(db, id_cliente)  
        return quejas        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")