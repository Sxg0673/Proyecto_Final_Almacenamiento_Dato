from app.models.evento import Evento
from app.models.usuario import Usuario
from app.models.organizacion_externa import OrganizacionExterna
from app.models.instalacion import Instalacion
from app.models.facultad import Facultad
from app.models.unidad_academica import UnidadAcademica
from app.models.programa import Programa
# ...cualquier otro modelo con .get() o .save() Beanie

document_models = [Evento, Usuario, OrganizacionExterna, Instalacion, Facultad, UnidadAcademica, Programa]