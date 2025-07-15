from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import police

from database.database import engine
from database.models import Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Polcias API")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes, puedes restringir según necesidad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(police.router, prefix="/api")