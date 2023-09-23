from sqlalchemy import Column, Integer, String
from config.database import Base

class Reclamo(Base):
    __tablename__ = "reclamo"

    id_reclamo = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
