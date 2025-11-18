from fastapi import APIRouter

# Importa el enrutador específico del módulo de eventos
from app.api.v1.routes import evento

# Crea un enrutador principal para la v1
api_router_v1 = APIRouter()

# Incluye el enrutador de eventos bajo el prefijo /eventos
# Todas las rutas en evento.router ahora comenzarán con /eventos
# y estarán agrupadas bajo la etiqueta "Eventos" en la documentación.
api_router_v1.include_router(evento.router, prefix="/eventos", tags=["eventos"])

# Si en el futuro tienes un enrutador para "Doctores", lo agregarías aquí:
# from app.api.v1.routes import doctor
# api_router_v1.include_router(doctor.router, prefix="/doctores", tags=["Doctores"])