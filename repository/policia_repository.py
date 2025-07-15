from sqlalchemy.orm import Session
from database.models import Policia

class PoliciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_todos(self):
        """Lista todos los policías en la base de datos."""
        return self.db.query(Policia).all()

    def obtener_por_id(self, policia_id: int):
        """Obtiene un policía por su ID."""
        return self.db.query(Policia).filter(Policia.id == policia_id).first()