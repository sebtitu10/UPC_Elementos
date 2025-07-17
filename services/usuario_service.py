from sqlalchemy.orm import Session
from repository.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, db: Session):
        self.usuario_repository = UsuarioRepository(db)

    def obtener_telefono_por_username(self, username: str) -> str | None:
        """
        Obtiene el número de teléfono de un usuario dado su username.
        """
        telefono = self.usuario_repository.buscar_por_username(username)
        return telefono
    

