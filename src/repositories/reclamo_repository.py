from sqlalchemy.orm import Session
from models.reclamo import Reclamo


class ReclamoRepository:
    def create_reclamo(self, db: Session, reclamo_data):
        db_reclamo = Reclamo(**reclamo_data)
        db.add(db_reclamo)
        db.commit()
        db.refresh(db_reclamo)
        return db_reclamo

    def get_reclamos(self, db: Session):
        return db.query(Reclamo).all()

    def get_reclamo_by_id_cliente(self, db: Session, id_cliente: int):
        return db.query(Reclamo).filter(Reclamo.id_cliente == id_cliente).all()
