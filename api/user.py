from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from services.usuario_service import UsuarioService

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/{username}/telefono")
def obtener_telefono(username: str, db: Session = Depends(get_db)):
    """
    Endpoint que retorna el número de teléfono de un usuario dado su username.
    """
    service = UsuarioService(db)
    telefono = service.obtener_telefono_por_username(username)

    if telefono is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"telefono": telefono}
