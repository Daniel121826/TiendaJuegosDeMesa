from pydantic import BaseModel, EmailStr

class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    edad: int
    dni: str
    telefono: int

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    id: int

class Config:
    orm_mode = True