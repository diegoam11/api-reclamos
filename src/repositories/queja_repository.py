from sqlalchemy.orm import Session
from models.queja import Queja

class QuejaRepository:
    def create_queja(self, db: Session, queja_data):
        db_queja = Queja(**queja_data)
        db.add(db_queja)
        db.commit()
        db.refresh(db_queja)
        return db_queja

    def get_quejas(self, db: Session):
        return db.query(Queja).all()
    
    def get_queja_by_id_cliente(self, db: Session, id_cliente: int):
        return db.query(Queja).filter(Queja.id_cliente == id_cliente).all()