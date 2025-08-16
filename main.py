
from fastapi import FastAPI, Request, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from typing import Dict
import logging
import pika, ssl  # <-- Agregar pika y ssl para RabbitMQ
import time
import threading

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

# Eliminar lógica de WebSocket
# active_connections: Dict[str, WebSocket] = {}


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

# Configuración RabbitMQ
rabbitmq_host = 'fuji.lmq.cloudamqp.com'
rabbitmq_user = 'tbvqnboe'
rabbitmq_pass = '2We4NDH_v8JhKtmj8edqWm7KDfqTFbcu'
rabbitmq_vhost = 'tbvqnboe'
queue_name = 'notificaciones'

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
context = ssl.create_default_context()
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=5671,
    virtual_host=rabbitmq_vhost,
    credentials=credentials,
    ssl_options=pika.SSLOptions(context)
)

# Singleton de conexión y canal
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel_lock = threading.Lock()  # Protege el canal para concurrencia

pending_messages = {}

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
    # for cam_id, ws in list(active_connections.items()):
    #     try:
    #         await ws.send_json(datos_quemados)
    #         logger.info(f"Notificación enviada a WebSocket de cámara {cam_id}")
    #     except Exception as e:
    #         logger.error(f"Error enviando a WebSocket de cámara {cam_id}: {e}")
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

# Eliminar endpoint WebSocket y lógica relacionada
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     ...

# Endpoint para obtener una alerta desde RabbitMQ
@app.post("/get_alerta")
def get_alerta():
    timeout = 10  # segundos
    start_time = time.time()
    with channel_lock:
        while time.time() - start_time < timeout:
            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=False)
            if method_frame:
                try:
                    data = json.loads(body)
                except Exception:
                    data = body.decode()
                delivery_tag = method_frame.delivery_tag
                pending_messages[delivery_tag] = {
                    "body": body,
                }
                return {
                    "mensaje": "Alerta recibida de RabbitMQ",
                    "data": data,
                    "delivery_tag": delivery_tag
                }
            time.sleep(1)
    return {"mensaje": "No hay alertas en la cola"}

@app.post("/ack_alerta")
def ack_alerta(delivery_tag: int = Body(...)):
    msg_info = pending_messages.pop(delivery_tag, None)
    if not msg_info:
        return {"mensaje": "No se encontró el mensaje pendiente para ACK"}
    with channel_lock:
        channel.basic_ack(delivery_tag=delivery_tag)
    return {"mensaje": "Mensaje confirmado y eliminado de la cola"}