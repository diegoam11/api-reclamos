from sqlalchemy.orm import Session
from models.reclamo import Reclamo

class ReclamoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_reclamo(self, reclamo_data):
        db_reclamo = Reclamo(**reclamo_data)
        self.db.add(db_reclamo)
        self.db.commit()
        self.db.refresh(db_reclamo)
        return db_reclamo

    def get_reclamos(self):
        return self.db.query(Reclamo).all()
    
    def get_reclamo_by_id_cliente(self, id_cliente: int):
        return self.db.query(Reclamo).filter(Reclamo.id_cliente == id_cliente).all()

        