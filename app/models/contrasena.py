# Modelo Contraseña
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from beanie import PydanticObjectId

class EstadoContrasenaEnum(str, Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"

class Contrasena(BaseModel):
    id_contrasena : Optional[PydanticObjectId] = None
    fecha_cambio : date
    contrasena: str
    estado: EstadoContrasenaEnum
    