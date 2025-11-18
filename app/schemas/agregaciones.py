from pydantic import BaseModel


class organizador(BaseModel):
    _id_org: str
    nombre: str
    rol: str
    vinculacion: str