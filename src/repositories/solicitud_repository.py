from sqlalchemy.orm import Session
from models.solicitud import Solicitud

class SolicitudRepository:

    def create_solicitud(self, db: Session, solicitud_data):
        db_solicitud = Solicitud(**solicitud_data)
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud

    def get_solicitudes(self, db: Session):
        return db.query(Solicitud).all()
    
    def get_solicitud_by_id_cliente(self, db: Session, id_cliente: int):
        return db.query(Solicitud).filter(Solicitud.id_cliente == id_cliente).all()