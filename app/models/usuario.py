# Modelo Usuario
from enum import Enum
from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import date
from app.models.vinculacion import Vinculacion
from app.models.contrasena import Contrasena

# Los tipos de usuario posibles
class rolEnum(str, Enum):
    DOCENTE = "docente"
    ESTUDIANTE = "estudiante"
    SECRETARIA = "secretaria"


class Usuario(Document):
    _id: Optional[PydanticObjectId] = None
    nombre: str
    correo: str
    rol: rolEnum
    # Atributos embebidos y relaciones
    vinculacion: Optional[List[Vinculacion]] = []
    contrasena: Optional[List[Contrasena]] = []
   
    class Settings:
        name = "usuarios"