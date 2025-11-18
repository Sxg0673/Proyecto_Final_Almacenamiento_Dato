# Modelo instalacion
from enum import Enum
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date

class tipoEnum(str, Enum):
    SALON = "salon"
    AUDITORIO = "auditorio"
    LABORATORIO = "laboratorio"
    CANCHA = "cancha"


class Instalacion(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    ubicacion: Optional[str] = None
    capacidad: int
    tipo: Optional[tipoEnum] = None

    class Settings:
        name = "instalaciones"