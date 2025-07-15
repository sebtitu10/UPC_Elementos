

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
import logging
import pymongo
from schema.alerta_schema import AlertaRequest
from repository.alerta_repository import AlertaRepository
from services.police import generar_parte_policial

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuración de MongoDB
MONGO_URI = "mongodb+srv://USR-Multimedia:Multi12345@cluster0.utjyivv.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "USR-Multimedia"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
alertas_collection = db["alertas"]


# Eliminar las definiciones duplicadas de Dispositivo, Coordenadas y AlertaRequest aquí

@router.post("/ia/recibir_alerta")
async def recibir_alerta(data: AlertaRequest):
    logger.info(f"Alerta recibida: {data.dict()}")
    print("Alerta recibida:", data.dict())
    # Guardar en MongoDB usando el repositorio
    repo = AlertaRepository()
    mongo_id = repo.insertar_alerta(data.dict())
    # Generar parte policial con IA
    parte_policial = generar_parte_policial(data)
    return {"mensaje": "Alerta recibida y guardada", "data": data.dict(), "mongo_id": mongo_id, "parte_policial": parte_policial}
