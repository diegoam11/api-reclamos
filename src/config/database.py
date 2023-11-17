from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DatabaseConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConfigSingleton, cls).__new__(cls)
            cls._instance.engine = create_engine(URL_DATABASE)
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

URL_DATABASE = 'postgresql://user1:R4Jq7r9YyhtZCBGS9zSzZA0ZPLHBnA8w@dpg-clbfgoent67s73advds0-a.oregon-postgres.render.com/database_rqs'
database_config = DatabaseConfigSingleton()

Base = declarative_base()

