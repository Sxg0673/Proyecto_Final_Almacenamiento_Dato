from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from typing import List, Optional, Dict, Any
from app.schemas.agregaciones import organizador
from app.schemas.evento import EvaluacionCrear, EventoActualizar, EventoActualizar, EventoCrear, EventoRespuesta
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.models.instalacion import Instalacion
from app.models.organizacion_externa import OrganizacionExterna 
from bson import ObjectId
from datetime import datetime
from app.db.mongodb import db
from app.core.config import settings
from app.service.evento import actualizar_evento, eliminar_evento, listar_eventos
from app.service.evento import crear_evento as crear_evento_service
from app.service.evento import obtener_evento_por_id, agregar_evaluacion_a_evento

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.post("/", response_model=EventoRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_evento(payload: EventoCrear):
    """
    Endpoint para crear un evento.
    Delegación total al service.
    """
    return await crear_evento_service(payload)



# Listar eventos 
@router.get("/", response_model=List[EventoRespuesta])
async def get_eventos():
    """Listar todos los eventos."""
    return await listar_eventos()


async def get_evento_por_id(id_evento: str):
    """
    CRUD para obtener un evento por su ID.
    Solo delega al service.
    """
    return await obtener_evento_por_id(id_evento)


@router.patch("/{id_evento}", response_model=EventoRespuesta)
async def patch_evento(id_evento: str, payload: EventoActualizar):
    """
    Endpoint para actualizar un evento parcialmente.
    """
    return await actualizar_evento(id_evento, payload)


@router.delete("/{id_evento}", status_code=status.HTTP_200_OK)
async def delete_evento(id_evento: str):
    """
    Endpoint para eliminar un evento por su ID.
    """
    try:
        resultado = await eliminar_evento(id_evento)
        return resultado
    except HTTPException:
        raise

@router.post("/{id_evento}/evaluaciones", response_model=EventoRespuesta)
async def agregar_evaluacion(id_evento: str, payload: EvaluacionCrear):
    """
    Agregar una evaluación a un evento y actualizar su estado.
    """
    try:
        evento_actualizado = await agregar_evaluacion_a_evento(id_evento, payload)
        return evento_actualizado
    except HTTPException:
        raise


async def listar_responsables_evento_crud(id_evento: str):
    """
    Retorna los responsables del evento usando un aggregate con $lookup y $unwind.
    """

    # 1. Validar que el ID sea un ObjectId válido
    try:
        object_id = PydanticObjectId(id_evento)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de evento no válido."
        )

    # 2. Verificar que el evento exista
    evento = await Evento.get(object_id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un evento con el ID {id_evento}."
        )

    # 3. Ejecutar el pipeline
    pipeline = [
        {"$match": {"_id": object_id}},
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "responsables.id_responsable",
                "foreignField": "_id",
                "as": "organizador"
            }
        },
        {"$unwind": {"path": "$organizador"}},
        {"$unwind": {"path": "$organizador.vinculacion"}},
        {
            "$project": {
                "_id": 0,
                "_id_org": "$organizador._id",
                "nombre": "$organizador.nombre",
                "rol": "$organizador.rol",
                "vinculacion": "$organizador.vinculacion.nombre"
            }
        }
    ]

    resultado = await Evento.aggregate(pipeline).to_list()

    # 4. Si no hay responsables (teóricamente nunca pasaría)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El evento no tiene responsables registrados."
        )

    # 5. Convertir cada resultado al schema organizdor
    return [organizador(**r) for r in resultado]
