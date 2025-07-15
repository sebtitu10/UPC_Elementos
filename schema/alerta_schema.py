from pydantic import BaseModel
from typing import Optional

class Dispositivo(BaseModel):
    id: Optional[str] = None
    tipo: Optional[str] = None
    ip: Optional[str] = None

class Coordenadas(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None

class AlertaRequest(BaseModel):
    alerta: Optional[str] = None
    coordenadas: Optional[Coordenadas] = None
    descripcion: Optional[str] = None
    dispositivo: Optional[Dispositivo] = None
    duracionVideo: Optional[int] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    nivelConfianza: Optional[str] = None
    nombrePolicia: Optional[str] = None
    palabrasClave: Optional[str] = None
    pnc: Optional[str] = None
    rango: Optional[str] = None
    ubicacion: Optional[str] = None 