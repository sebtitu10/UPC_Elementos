

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import logging
import pymongo
from schema.alerta_schema import AlertaRequest
from repository.alerta_repository import AlertaRepository
from repository.parte_repository import ParteRepository
from services.police import generar_parte_policial, generar_pdf_parte_policial
from fastapi.responses import StreamingResponse
from fastapi import Request
from services.police import subir_pdf_a_github

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

class Coordenadas(BaseModel):
    latitude: float
    longitude: float

class WebhookRequest(BaseModel):
    id: Optional[Dict[str, Any]] = Field(None, alias="_id", example={"$oid": "686da5d4bc8ef480d0eb9899"})
    device_id: str = Field(..., example="CAM-UPC-01")
    device_type: str = Field(..., example="camera")
    location: str = Field(..., example="Quito - La Mariscal")
    alert_information: str = Field(..., example="Test")
    cordinates: Coordenadas = Field(..., example={"latitude": -0.22985, "longitude": -78.52495})
    date: str = Field(..., example="2023-10-01")
    time: str = Field(..., example="18:20:30")
    stream_url: str = Field(..., example="http://192.168.11.105:4747/video")
    transcription_video: Optional[str] = Field(None, example="Se observan dos individuos corriendo por la calle armados con pistolas.")
    transcription_audio: Optional[str] = None
    media_duration: int = Field(..., example=120)
    key_words: List[str] = Field(..., example=["robo", "arma", "moto"])
    confidence_level: float = Field(..., example=0.92)

    class Config:
        from_attributes = True

class WebhookResponse(BaseModel):
    mensaje: str = Field(..., example="Notificación enviada")
    data_recibida: WebhookRequest
    respuesta_ficticia: Dict[str, Any]


@router.post("/ia/recibir_alerta")
async def recibir_alerta(data: AlertaRequest):
    logger.info(f"Alerta recibida: {data.dict()}")
    print("Alerta recibida:", data.dict())
    # Guardar en MongoDB usando el repositorio
    repo = AlertaRepository()
    mongo_id = repo.insertar_alerta(data.dict())
    # Generar parte policial con IA
    parte_policial = generar_parte_policial(data)
    # Guardar el parte policial en la colección 'parte'
    parte_repo = ParteRepository()
    parte_id = parte_repo.insertar_parte(parte_policial)
    try:
        pdf_bytes = generar_pdf_parte_policial(parte_policial)
        # Subir el PDF a GitHub Pages
        url_publica = subir_pdf_a_github(
            pdf_bytes,
            "parte_policial.pdf",      # Puedes personalizar el nombre
            "UPC_Elementos",           # Tu repo
            "ejcondorf88",             # Tu usuario
            "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"  # Tu token
        )
        return {
            "mensaje": "Alerta recibida, guardada y PDF generado",
            "mongo_id": mongo_id,
            "parte_policial": parte_policial,
            "parte_id": parte_id,
            "url_pdf": url_publica
        }
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        return {"mensaje": "Alerta recibida y guardada", "data": data.dict(), "mongo_id": mongo_id, "parte_policial": parte_policial}


@router.post(
    "/notificacion_webhook",
    summary="Recibe notificaciones tipo webhook",
    tags=["Webhook"],
    response_model=WebhookResponse,
    response_description="Respuesta de confirmación con los datos recibidos y una respuesta ficticia."
)
async def recibir_webhook(data: WebhookRequest):
    """
    Recibe notificaciones tipo webhook con información de alertas y devuelve una confirmación junto con los datos principales recibidos.

    Ejemplo de request:
    {
        "_id": {"$oid": "686da5d4bc8ef480d0eb9899"},
        "device_id": "CAM-UPC-01",
        "device_type": "camera",
        "location": "Quito - La Mariscal",
        "alert_information": "Test",
        "cordinates": {"latitude": -0.22985, "longitude": -78.52495},
        "date": "2023-10-01",
        "time": "18:20:30",
        "stream_url": "http://192.168.11.105:4747/video",
        "transcription_video": "Se observan dos individuos corriendo por la calle armados con pistolas.",
        "transcription_audio": null,
        "media_duration": 120,
        "key_words": ["robo", "arma", "moto"],
        "confidence_level": 0.92
    }
    """
    return {
        "mensaje": "Notificación enviada",
        "data_recibida": data,
        "respuesta_ficticia": {
            "alert_information": data.alert_information,
            "location": data.location,
            "cordinates": data.cordinates,
            "stream_url": data.stream_url,
            "transcription_video": data.transcription_video,
            "media_duration": data.media_duration,
            "key_words": data.key_words,
            "confidence_level": data.confidence_level
        }
    }
