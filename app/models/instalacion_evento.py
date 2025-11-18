# Modelo instalacion
from enum import Enum
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date

from pydantic import BaseModel
from app.models.instalacion import tipoEnum


class Instalacion_evento(BaseModel):
    id_instalacion: Optional[PydanticObjectId] = None
    nombre: str
    ubicacion: Optional[str] = None
    capacidad: int
    tipo: Optional[tipoEnum] = None