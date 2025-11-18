from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.v1.routes import evento
# Importa el enrutador principal que agrupa todos los endpoints de la v1
from app.api.v1.api import api_router_v1
# Importa la configuración centralizada
from app.core.config import settings

#ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
     # Conexión a MongoDB (Beanie + Motor)
    await connect_to_mongo()
    yield
     # Cierre limpio de la conexión al apagar el servidor
    await close_mongo_connection()

# Crea la instancia principal de la aplicación FastAPI
# Se añade metadata que se usará en la documentación automática de la API
app = FastAPI(
    title=settings.APP_NAME,
    description="La API del proyecto, del tercer y el corte que definira mi beca",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
# --- Configuración de Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Inclusión de Enrutadores de la API ---

# Incluye todas las rutas de la v1 bajo el prefijo global /api/v1
# La URL final para crear un paciente será: http://.../api/v1/pacientes/
app.include_router(api_router_v1, prefix="/api/v1")
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")