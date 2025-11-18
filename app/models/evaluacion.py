from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from beanie import Document, PydanticObjectId


class EstadoEvaluacionEnum(str, Enum):
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"

class Evaluacion(BaseModel):
    id_evaluacion: Optional[PydanticObjectId] = None
    id_secretario : Optional[PydanticObjectId] = None
    fecha_evaluacion: Optional[datetime] = None
    justificacion: Optional[str]
    acta_aprobacion: Optional[str] = None
    estado: EstadoEvaluacionEnum
    