# Modelo Vinculacion
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from beanie import PydanticObjectId

class EstadoVinculacionEnum(str, Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"
    TERMINADA = "terminada"

class Vinculacion(BaseModel):
    unidadAcademicaId: Optional[PydanticObjectId] = None # Docente
    programaId: Optional[PydanticObjectId] = None # Estudiante
    facultadId: Optional[PydanticObjectId] = None # Secretaria
    # El usuario solo puede pertenecer a una vinculacion
    # Los atributos pertenecen a la vinculacion del usuario
    fechaInicio: date
    fechaFin: Optional[date] = None
    estado: EstadoVinculacionEnum
    nombre: Optional[str]