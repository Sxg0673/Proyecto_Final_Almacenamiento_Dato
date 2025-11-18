# Modelo Responsable
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import date
from beanie import Document, PydanticObjectId

class TipoAvalEnum(str, Enum):
    DIRECTORDOCENTE = "director_docencia"
    DIRECTORPROGRAMA = "director_programa"

class Responsable(BaseModel):
    id_responsable: Optional[PydanticObjectId] = None
    nombre: str
    principal: Optional[bool] = False
    tipo_aval: TipoAvalEnum