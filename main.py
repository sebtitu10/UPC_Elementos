from fastapi import FastAPI
from api import police

from database.database import engine
from database.models import Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Polcias API")

# Incluir routers

app.include_router(police.router, prefix="/api")