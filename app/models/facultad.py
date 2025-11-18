# Modelo de Facultad
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date


class Facultad(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    descripcion: Optional[str] = None

    class Settings:
        name = "facultades"