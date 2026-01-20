from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.empleado import Empleado
from schemas.empleado import EmpleadoCreate, EmpleadoResponse

router = APIRouter(
    prefix="/empleados",
    tags=["empleados"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[EmpleadoResponse])
def get_empleados(db: Session = Depends(get_db)):
    return db.query(Empleado).all()

@router.get("/{empleado_id}", response_model=EmpleadoResponse)
def get_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return empleado

@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    existing_empleado = db.query(Empleado).filter(Empleado.email == empleado.email).first()
    if existing_empleado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El empleado ya existe"
        )

    new_empleado = Empleado(**empleado.dict())
    db.add(new_empleado)
    db.commit()
    db.refresh(new_empleado)
    return new_empleado

@router.put("/{empleado_id}", response_model=EmpleadoResponse)
def update_empleado(empleado_id: int, empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    stored_empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not stored_empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    for key, value in empleado.dict().items():
        setattr(stored_empleado, key, value)

    db.commit()
    db.refresh(stored_empleado)
    return stored_empleado

@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    db.delete(empleado)
    db.commit()