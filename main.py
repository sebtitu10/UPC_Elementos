
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from typing import Dict
import logging
from api import police
from api import ia


from database.database import engine
from database.models import Base


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Kuntur API")

# Almacén para conexiones WebSocket activas
active_connections: Dict[str, WebSocket] = {}


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
app.include_router(ia.router, prefix="/api")

# Cargar cámaras desde archivo
def cargar_camaras():
    with open("cameras.json") as f:
        return json.load(f)

# Endpoint para recibir eventos y notificar por WebSocket
@app.post("/webhook")
async def recibir_evento(request: Request):
    # Datos quemados
    datos_quemados = {
        "_id": {"$oid": "686da5d4bc8ef480d0eb9899"},
        "device_id": "CAM-UPC-01",
        "device_type": "camera",
        "location": "Quito - La Mariscal",
        "alert_information": "Estoy viendo a tres personas armadas",
        "cordinates": {
            "latitude": -0.22985,
            "longitude": -78.52495
        },
        "date": "2023-10-01",
        "time": "18:20:30",
        "stream_url": "rtsp://192.168.1.10/live",
        "transcription_video": "Se observan dos individuos corriendo por la calle armados con pistolas.",
        "transcription_audio": None,
        "media_duration": 120,
        "key_words": ["robo", "arma", "moto"],
        "confidence_level": 0.92
    }
    # ENVÍA el mensaje a todos los clientes conectados
    for cam_id, ws in list(active_connections.items()):
        try:
            await ws.send_json(datos_quemados)
            logger.info(f"Notificación enviada a WebSocket de cámara {cam_id}")
        except Exception as e:
            logger.error(f"Error enviando a WebSocket de cámara {cam_id}: {e}")
    return {
        "mensaje": "Notificación enviada",
        "data_recibida": datos_quemados,
        "respuesta_ficticia": {
            "alert_information": datos_quemados["alert_information"],
            "location": datos_quemados["location"],
            "cordinates": datos_quemados["cordinates"],
            "stream_url": datos_quemados["stream_url"],
            "transcription_video": datos_quemados["transcription_video"],
            "media_duration": datos_quemados["media_duration"],
            "key_words": datos_quemados["key_words"],
            "confidence_level": datos_quemados["confidence_level"]
        }
    }

# Página principal

# Vista de cámara
@app.get("/ver_camara", response_class=HTMLResponse)
async def ver_camara(request: Request, ip: str):
    return templates.TemplateResponse("camera_view.html", {"request": request, "ip": ip})

# WebSocket para cámaras
@app.websocket("/ws/{camara_id}")
async def websocket_endpoint(websocket: WebSocket, camara_id: str):
    await websocket.accept()
    logger.info(f"Cliente conectado por WebSocket para cámara {camara_id}")
    active_connections[camara_id] = websocket
    try:
        while True:
            # Mantener la conexión abierta
            data = await websocket.receive_text()
    except Exception as e:
        logger.error(f"Error en WebSocket para cámara {camara_id}: {e}")
    finally:
        active_connections.pop(camara_id, None)
        logger.info(f"Cliente desconectado del WebSocket para cámara {camara_id}")