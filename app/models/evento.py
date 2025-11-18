# Modelo Evento
from enum import Enum
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date, datetime
from app.models.responsable import Responsable
from app.models.usuario import Usuario
from app.models.instalacion import Instalacion
from app.models.instalacion_evento import Instalacion_evento
from app.models.organizacion_participante import OrganizacionParticipante
from app.models.evaluacion import Evaluacion

class EstadoEventoEnum(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class TipoEventoEnum(str, Enum):
    LUDICO = "ludico"
    ACADEMICO = "academico"

class Evento(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: EstadoEventoEnum
    tipo_evento: TipoEventoEnum
    asistentes: int

    responsables: List[Responsable] = []
    instalaciones: List[Instalacion_evento] = []
    organizaciones_externas: List[OrganizacionParticipante] = []
    evaluaciones: List[Evaluacion] = []


    class Settings:
        name = "eventos"