from sqlalchemy import Column, Integer, String
from database.database import Base

class Juego_Mesa(Base):
    __tablename__ = "juegos_mesa"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    edad_minima = Column(Integer, nullable=False)
    jugadores_minimos = Column(Integer, nullable=False)
    marca = Column(String, nullable=False)
