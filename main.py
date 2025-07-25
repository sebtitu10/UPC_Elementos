
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from typing import Dict
import logging
from api import police
from api import ia
from api import user


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
app.include_router(user.router, prefix="/api")


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
        "alert_information": "Test",
        "cordinates": {
            "latitude": -0.22985,
            "longitude": -78.52495
        },
        "date": "2023-10-01",
        "time": "18:20:30",
        "stream_url": "http://192.168.11.105:4747/video",
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

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await websocket.accept()
        active_connections[client_id] = websocket
        logger.info(f"WebSocket conectado para cliente {client_id}")
        
        # Mantener la conexión activa
        while True:
            try:
                # Esperar por mensajes del cliente (opcional)
                data = await websocket.receive_text()
                logger.info(f"Mensaje recibido de {client_id}: {data}")
            except Exception as e:
                logger.error(f"Error en WebSocket {client_id}: {e}")
                break
                
    except Exception as e:
        logger.error(f"Error en conexión WebSocket {client_id}: {e}")
    finally:
        # Limpiar conexión cuando se desconecte
        if client_id in active_connections:
            del active_connections[client_id]
            logger.info(f"WebSocket desconectado para cliente {client_id}")