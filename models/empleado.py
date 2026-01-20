from sqlalchemy import Column, Integer, String
from database.database import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    edad = Column(Integer, nullable=False)
    dni = Column(String, unique=True, nullable=False)
    telefono = Column(Integer, unique=True, nullable=False)