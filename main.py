from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Caso

app = FastAPI()

# Configuración del middleware CORS
origins = [
    "http://localhost:3000",  # Cambia esto según tus necesidades
    "https://example.com",
    "*",  # No recomendado en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear un modelo Pydantic para la entrada de los casos
class CasoCreate(BaseModel):
    contexto: str
    descripcion: str
    escala:int

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/casos/")
async def create_caso(caso: CasoCreate, db: Session = Depends(get_db)):
    new_caso = Caso(contexto=caso.contexto, descripcion=caso.descripcion,escala=caso.escala)
    db.add(new_caso)
    db.commit()
    db.refresh(new_caso)
    return new_caso

@app.get("/casos/")
async def read_casos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    casos = db.query(Caso).offset(skip).limit(limit).all()
    return casos

# Ruta para eliminar todos los datos de la tabla Caso
@app.delete("/casos/")
async def delete_all_casos(db: Session = Depends(get_db)):
    try:
        num_deleted = db.query(Caso).delete()
        db.commit()
        return {"message": f"Se eliminaron {num_deleted} casos."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


