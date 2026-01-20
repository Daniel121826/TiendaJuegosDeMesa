from fastapi import FastAPI

from database.database import Base, engine
from routes import empleados, juegos_mesa

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(empleados.router)
app.include_router(juegos_mesa.router)

@app.get("/")
def root():
    return {"message": "API de usuarios con FastAPI y SQLite"}