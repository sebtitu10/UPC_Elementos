from pydantic import BaseModel
from typing import Optional

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