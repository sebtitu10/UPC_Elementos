from fastapi import APIRouter, Depends
from schema.policia_schema import PoliciaOut, PoliciaMockupSchema, Identificacion
from repository.policia_repository import PoliciaRepository
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db

#Inicializar router

router = APIRouter(prefix="/policias", tags=["Policias"])

@router.get("/",response_model=List[PoliciaMockupSchema])
def listar_policias(db: Session = Depends(get_db)):
    repo = PoliciaRepository(db)
    policias = repo.listar_todos()

    return [
        PoliciaMockupSchema(
            id=p.id,
            identificacion=Identificacion(
                nombre=p.nombre_completo,
                placa=p.numero_placa,
                rango=p.rango or "Sin rango"
            ),
            estado_actual=p.estado.upper(),
            fecha_ingreso=p.fecha_ingreso.strftime("%d/%m/%Y"),
            jefatura=p.jefatura_name
        )
        for p in policias
    ]