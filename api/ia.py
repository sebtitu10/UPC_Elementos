

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Modelo Pydantic para el body
class Dispositivo(BaseModel):
    id: Optional[str]
    tipo: Optional[str]
    ip: Optional[str]

class Coordenadas(BaseModel):
    lat: float
    lng: float

class AlertaRequest(BaseModel):
    alerta: Optional[str]
    coordenadas: Coordenadas
    descripcion: str
    dispositivo: Dispositivo
    duracionVideo: Optional[int]
    fecha: str
    hora: str
    nivelConfianza: str
    nombrePolicia: str
    palabrasClave: str
    pnc: str
    rango: str
    ubicacion: str

@router.post("/ia/recibir_alerta")
async def recibir_alerta(data: AlertaRequest):
    logger.info(f"Alerta recibida: {data.dict()}")
    print("Alerta recibida:", data.dict())
    return {"mensaje": "Alerta recibida", "data": data.dict()}
