# Modelo OrganizacionParticipante
from typing import List, List, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel

class Representante(BaseModel):
    nombre: str
    cargo: Optional[str] = None
    legal: bool


class OrganizacionParticipante(BaseModel):
    id_organizacion: Optional[PydanticObjectId] = None
    nombre: Optional[str]
    certificado: str
    representante: List[Representante] = []