from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class EstadoEnum(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class Director(BaseModel):
    nombre: str
    correo: str
    estado: EstadoEnum
    fechaInicio: date
    fechaFin: Optional[date] = None
    
