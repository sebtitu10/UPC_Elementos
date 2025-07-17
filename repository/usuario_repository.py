from sqlalchemy.orm import Session
from database.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_username(self, username: str):
        """Busca un usuario por su nombre de usuario y retorna solo el teléfono."""
        resultado = self.db.query(Usuario.telefono).filter(Usuario.username == username).first()
        return resultado[0] if resultado else None