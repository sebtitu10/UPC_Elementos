
from fastapi import APIRouter, Request
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/ia/recibir_alerta")
async def recibir_alerta(request: Request):
    body = await request.json()
    logger.info(f"Alerta recibida: {body}")
    print("Alerta recibida:", body)
    return {"mensaje": "Alerta recibida", "data": body}
