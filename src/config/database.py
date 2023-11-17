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

URL_DATABASE = 'postgresql://user1:YDfR9jtgGp6be1z6tUE3kIu7rhlUWvqA@dpg-clbhu94tv1ns73ej7nig-a.oregon-postgres.render.com/database_rqs_e716'
database_config = DatabaseConfigSingleton()

Base = declarative_base()

