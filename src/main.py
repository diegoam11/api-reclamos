from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated

from models.reclamo import Reclamo
from repositories.reclamo_repository import ReclamoRepository
from schemas.base import ReclamoBase

from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
Reclamo.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
reclamo_repository = ReclamoRepository

@app.post("/reclamos/")
async def create_reclamos(reclamo: ReclamoBase, db: db_dependency):
    db_reclamo = reclamo_repository(db).create_reclamo(reclamo.descripcion)
    return db_reclamo
