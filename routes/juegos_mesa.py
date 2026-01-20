from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.juego_mesa import Juego_Mesa
from schemas.juego_mesa import Juegos_MesaCreate, Juegos_MesaResponse

router = APIRouter(
    prefix="/juegos_mesa",
    tags=["juegos_mesa"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Juegos_MesaResponse])
def get_juegos_mesa(db: Session = Depends(get_db)):
    return db.query(Juego_Mesa).all()

@router.get("/{juego_mesa_id}", response_model=Juegos_MesaResponse)
def get_juego_mesa(juego_mesa_id: int, db: Session = Depends(get_db)):
    juego_mesa = db.query(Juego_Mesa).filter(Juego_Mesa.id == juego_mesa_id).first()
    if not juego_mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego de mesa no encontrado"
        )
    return juego_mesa

@router.post("/", response_model=Juegos_MesaResponse, status_code=status.HTTP_201_CREATED)
def create_juego_mesa(juego_mesa: Juegos_MesaCreate, db: Session = Depends(get_db)):
    existing_juego_mesa = db.query(Juego_Mesa).filter(Juego_Mesa.nombre == juego_mesa.nombre).first()
    if existing_juego_mesa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El juego de mesa ya existe"
        )

    new_juego_mesa = Juego_Mesa(**juego_mesa.model_dump())
    db.add(new_juego_mesa)
    db.commit()
    db.refresh(new_juego_mesa)
    return new_juego_mesa
@router.put("/{juego_mesa_id}", response_model=Juegos_MesaResponse)
def update_juego_mesa(juego_mesa_id: int, juego_mesa: Juegos_MesaCreate, db: Session = Depends(get_db)):
    stored_juego_mesa = db.query(Juego_Mesa).filter(Juego_Mesa.id == juego_mesa_id).first()
    if not stored_juego_mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego de mesa no encontrado"
        )

    for key, value in juego_mesa.model_dump().items():
        setattr(stored_juego_mesa, key, value)
    db.commit()
    db.refresh(stored_juego_mesa)
    return stored_juego_mesa

@router.delete("/{juego_mesa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_juego_mesa(juego_mesa_id: int, db: Session = Depends(get_db)):
    juego_mesa = db.query(Juego_Mesa).filter(Juego_Mesa.id == juego_mesa_id).first()
    if not juego_mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Juego de mesa no encontrado"
        )

    db.delete(juego_mesa)
    db.commit()