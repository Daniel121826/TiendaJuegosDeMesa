from pydantic import BaseModel

class Juegos_MesaBase(BaseModel):
    nombre: str
    categoria: str
    edad_minima: int
    jugadores_minimos: int
    marca: str

class Juegos_MesaCreate(Juegos_MesaBase):
    pass

class Juegos_MesaResponse(Juegos_MesaBase):
    id: int

class Config:
    orm_mode = True