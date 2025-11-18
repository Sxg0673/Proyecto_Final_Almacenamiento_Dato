# Modelo OrganizacionExterna
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List


# ----- Subdocumentos -----

class RepresentanteLegal(BaseModel):
    nombre: str
    cargo: str
    correo: str


class Direccion(BaseModel):
    departamento: str
    ciudad: str


class Contacto(BaseModel):
    telefonos: List[int] = Field(default_factory=list)
    direccion: Direccion


# ----- Documento principal -----

class OrganizacionExterna(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    sector_economico: Optional[str]
    actividad_principal: Optional[str]
    representante_legal: RepresentanteLegal
    contacto: Optional[Contacto]

    class Settings:
        name = "organizaciones_externas"
