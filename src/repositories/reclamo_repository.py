from sqlalchemy import Session
from models.reclamo import Reclamo

class ReclamoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_reclamo(self, descripcion: str):
        db_reclamo = Reclamo(descripcion=descripcion)
        self.db.add(db_reclamo)
        self.db.commit()
        self.db.refresh(db_reclamo)
        return db_reclamo
