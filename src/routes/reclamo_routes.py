from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.reclamo import Reclamo
from repositories.reclamo_repository import ReclamoRepository
from schemas.base import ReclamoBase

router = APIRouter()
Reclamo.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
reclamo_repository = ReclamoRepository

@router.post("/reclamos/")
async def create_reclamos(reclamo: ReclamoBase, db: db_dependency):
    db_reclamo = reclamo_repository(db).create_reclamo(reclamo.dict())
    return db_reclamo
