# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la base de datos en memoria
DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Caso(Base):
    __tablename__ = "casos"
    
    id = Column(Integer, primary_key=True, index=True)
    contexto = Column(String, index=True)
    descripcion = Column(String)
    escala=Column(Integer)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)