from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from routes import empleados, juegos_mesa

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=[
"http://localhost:5173", # React (Vite)
"http://localhost:3000" # React (Create React App)
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.include_router(empleados.router)
app.include_router(juegos_mesa.router)

@app.get("/")
def root():
    return {"message": "API de usuarios con FastAPI y SQLite"}