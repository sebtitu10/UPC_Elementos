from sqlalchemy import Column, Integer, String,Date,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Policia(Base):
    __tablename__ = 'policias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    numero_placa = Column(String(20), unique=True, nullable=False)
    rango = Column(String(50))
    fecha_ingreso = Column(Date, nullable=False)
    estado = Column(String(10), nullable=False, default='activo')
    jefatura_name = Column(String(100), nullable=False)

    # Restricción para estado
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'inactivo')", name="check_estado_valido"),
    )

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(100))
    email = Column(String(100))

