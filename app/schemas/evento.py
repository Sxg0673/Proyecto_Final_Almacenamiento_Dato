from enum import Enum
from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class EstadoEventoEnum(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class EstadoEvaluacionEnum(str, Enum):
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


class TipoEventoEnum(str, Enum):
    LUDICO = "ludico"
    ACADEMICO = "academico"

class TipoAvalEnum(str, Enum):
    DIRECTOR_DOCENCIA = "director_docencia"
    DIRECTOR_PROGRAMA = "director_programa"


class Responsable(BaseModel):
    id_responsable: PydanticObjectId = Field(..., description="ID unico del responsable")
    nombre: str = Field(..., description="Nombre del responsable")
    tipo_aval: TipoAvalEnum = Field(..., description="Tipo aval")
    principal: Optional[bool] = False


class Instalacion(BaseModel):
    id_instalacion: PydanticObjectId = Field(..., description="ID unico de la instalacion")
    nombre: str
    capacidad: int

class Representante(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    legal: Optional[bool] = None

class OrganizacionParticipante(BaseModel):
    id_organizacion: PydanticObjectId = Field(..., description="ID unico de la organizacion participante")
    nombre: Optional[str] = None
    representantes: List[Representante] = Field(default_factory=list)
    certificado: Optional[str] = None


class EvaluacionCrear(BaseModel):
    id_secretario: str
    justificacion: Optional[str] = None
    acta_aprobacion: Optional[str] = None
    estado: EstadoEvaluacionEnum



# Schemas Principales

class EventoCrear(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    tipo_evento: TipoEventoEnum 
    estado: EstadoEventoEnum = EstadoEventoEnum.PENDIENTE
    responsables: List[Responsable] = Field(default_factory=list)
    instalaciones: List[Instalacion] = Field(default_factory=list)
    organizaciones_externas: List[OrganizacionParticipante] = Field(default_factory=list)
    asistentes: Optional[int] = 0

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Feria de Innovación 2025",
                "descripcion": "Evento académico con participación de empresas externas",
                "fecha_inicio": "2025-11-10T09:00:00Z",
                "fecha_fin": "2025-11-11T18:00:00Z",
                "tipo_evento": "academico",
                "responsables": [
                    {
                        "id_responsable": "672d2b7a5e8c112233445566",
                        "nombre": "Laura Gómez",
                        "tipo_aval": "director_docencia",
                        "principal": True
                    }
                ],
                "instalaciones": [
                    {
                        "id_instalacion": "672d2b7a5e8c112233445567",
                        "nombre": "Auditorio Central",
                        "capacidad": 300
                    }
                ],
                "organizaciones_participantes": [
                    {
                        "id_organizacion": "672d2b7a5e8c112233445568",
                        "nombre": "Empresa ABC",
                        "representantes": [
                            {"nombre": "Carlos López", "cargo": "Gerente", "legal": True}
                        ],
                        "certificado": "certificado_abc.pdf"
                    }
                ],
                "asistentes": 150
            }
        }
    }
    


class EventoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    asistentes: Optional[int] = None
    responsables: Optional[List[Responsable]] = None
    instalaciones: Optional[List[Instalacion]] = None
    organizaciones_externas: Optional[List[OrganizacionParticipante]] = None
    


# Schema de salida: Responsable
class ResponsableRespuesta(BaseModel):
    id_responsable: str
    nombre: str
    tipo_aval: TipoAvalEnum 
    principal: bool

    @field_validator('id_responsable', mode='before')
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

# Schema de salida: Evaluación
class EvaluacionRespuesta(BaseModel):
    id_evaluacion: str
    id_secretario: str
    fecha_evaluacion: Optional[datetime] = None
    justificacion: Optional[str] = None
    acta_aprobacion: Optional[str] = None
    estado: EstadoEvaluacionEnum 

    @field_validator('id_evaluacion', 'id_secretario', mode='before')
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class RepresentanteRespuesta(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    legal: Optional[bool] = None

# Schema de salida: Organización externa
class OrganizacionExternaRespuesta(BaseModel):
    id_organizacion: str
    nombre: Optional[str] = None
    representantes: List[RepresentanteRespuesta] = Field(default_factory=list)
    certificado: Optional[str] = None

    @field_validator('id_organizacion', mode='before')
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

# Schema de salida: Instalación
class InstalacionRespuesta(BaseModel):
    id_instalacion: str
    nombre: str
    capacidad: int
    
    @field_validator('id_instalacion', mode='before')
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

# Schema de salida: Evento
class EventoRespuesta(BaseModel):
    _id: str    
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: EstadoEventoEnum
    tipo_evento: TipoEventoEnum 
    responsables: List[ResponsableRespuesta] = Field(default_factory=list)
    evaluaciones: List[EvaluacionRespuesta] = Field(default_factory=list)
    instalaciones: List[InstalacionRespuesta] = Field(default_factory=list)
    organizaciones_externas: List[OrganizacionExternaRespuesta] = Field(default_factory=list)

    model_config = dict(arbitrary_types_allowed=True)

    @field_validator('_id', mode='before', check_fields=False)
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    model_config = {
        "populate_by_name": True
    }


# Schema de llegada desde BD

# Schema de llegada: Responsable
class ResponsableBD(BaseModel):
    id_responsable: ObjectId
    nombre: str
    tipo_aval: TipoAvalEnum 
    principal: Optional[bool] = False

    model_config = dict(arbitrary_types_allowed=True)

# Schema de llegada: Evaluación
class EvaluacionBD(BaseModel):
    id_evaluacion: ObjectId
    id_secretario: ObjectId
    fecha_evaluacion: Optional[datetime] = None
    justificacion: Optional[str] = None
    acta_aprobacion: Optional[str] = None
    estado: EstadoEvaluacionEnum 

    model_config = dict(arbitrary_types_allowed=True)

# Schema de llegada: Organización externa
class OrganizacionExternaBD(BaseModel):
    id_organizacion: ObjectId
    nombre: Optional[str] = None
    representantes: List[Representante] = []
    certificado: Optional[str] = None

    model_config = dict(arbitrary_types_allowed=True)

# Schema de llegada: Instalación
class InstalacionBD(BaseModel):
    id_instalacion: ObjectId
    nombre: str
    capacidad: int

    model_config = dict(arbitrary_types_allowed=True)

# Schema de llegada: Evento
class EventoBD(BaseModel):
    _id: ObjectId
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[str] = None
    responsables: List[ResponsableBD] = []
    evaluaciones: List[EvaluacionBD] = []
    instalaciones: List[InstalacionBD] = []
    organizaciones_externas: List[OrganizacionExternaBD] = []

    model_config = dict(arbitrary_types_allowed=True)