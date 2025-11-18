# Modelo programa
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date
from pydantic import BaseModel
from app.models.facultad import Facultad
from app.models.director import Director

class FacultadRef(BaseModel):
    id_facultad: PydanticObjectId
    nombre: str


class Programa(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    codigo: str
    # Se agrega la relación con Facultad y Directores
    facultad: FacultadRef
    director: List[Director] = []

    class Settings:
        name = "programas"