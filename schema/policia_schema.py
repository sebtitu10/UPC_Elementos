from pydantic import BaseModel
from datetime import date
from typing import Literal

class PoliciaOut(BaseModel):
    id: int
    nombre_completo: str
    numero_placa: str
    rango: str | None
    fecha_ingreso: date
    estado: str
    jefatura_name: str

    class Config:
        orm_mode = True



class Identificacion(BaseModel):
    nombre: str
    placa: str
    rango: str


class PoliciaMockupSchema(BaseModel):
    id: int
    identificacion: Identificacion
    estado_actual: Literal["ACTIVO", "INACTIVO"]
    fecha_ingreso: str  # Formato dd/mm/aaaa
    jefatura: str

    class Config:
        from_attributes = True  #