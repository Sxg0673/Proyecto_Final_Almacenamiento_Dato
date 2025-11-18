from ast import List
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.agregaciones import organizador
from app.schemas.evento import EvaluacionCrear, EvaluacionCrear, EventoActualizar, EventoCrear, EventoRespuesta
from app.crud import evento as crud
from app.models.evento import Evento
from app.schemas.evento import EventoRespuesta
from app.service.evento import agregar_evaluacion_a_evento, agregar_evaluacion_a_evento, eliminar_evento, listar_eventos as listar_eventos_service
from app.service.evento import crear_evento as crear_evento_service
from app.crud.evento import get_evento_por_id, listar_responsables_evento_crud
from app.service.evento import actualizar_evento as actualizar_evento_service


router = APIRouter(
    prefix="/eventos",
    tags=["eventos"]
    )

# Crear Evento
@router.post("/", response_model=EventoRespuesta, status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoCrear):
    return await crear_evento_service(evento)

# Listar Eventos
@router.get("/", response_model=list[EventoRespuesta], summary="Listar eventos",)
async def get_eventos():
    """Listar todos los eventos."""
    eventos = await listar_eventos_service()  # service maneja la conversión ObjectId -> str
    return eventos

# Obtener Evento por ID
@router.get("/{id_evento}", response_model=EventoRespuesta, status_code=status.HTTP_200_OK)
async def obtener_evento(id_evento: str):
    """
    Obtener un evento por su ObjectId.
    """
    try:
        evento = await get_evento_por_id(id_evento)
        return evento
    except ValueError as e:
        # Errores controlados desde el service
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Si ya es un HTTPException desde el service, la dejamos pasar
        raise

# Actualizar Evento

# Actualizar Evento parcialmente
@router.patch("/{id_evento}", response_model=EventoRespuesta, status_code=status.HTTP_200_OK)
async def patch_evento(id_evento: str, evento: EventoActualizar):
    """
    Actualiza un evento parcialmente.
    Solo se aplican los campos enviados en `evento`.
    """
    try:
        evento_actualizado = await actualizar_evento_service(id_evento, evento)
        return evento_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise


    # Endpoint DELETE para eliminar un evento
@router.delete("/{id_evento}", status_code=status.HTTP_200_OK)
async def delete_evento(id_evento: str):
    """
    Elimina un evento por su ObjectId.
    Retorna un mensaje de éxito si se elimina correctamente.
    """
    try:
        resultado = await eliminar_evento(id_evento)
        return resultado
    except HTTPException:
        raise

@router.post("/{id_evento}/evaluaciones", response_model=EventoRespuesta, status_code=status.HTTP_201_CREATED)
async def agregar_evaluacion(id_evento: str, payload: EvaluacionCrear):
    """
    Agregar una evaluación a un evento existente.
    Actualiza automáticamente el estado del evento según la evaluación.
    """
    try:
        evento_actualizado = await agregar_evaluacion_a_evento(id_evento, payload)
        return evento_actualizado
    except HTTPException:
        raise


# Listar responsables de un evento
@router.get(
    "/{id_evento}/responsables",
    response_model=List[organizador],
    summary="Listar responsables del evento",
)
async def get_responsables_evento(id_evento: str):
    """
    Retorna los responsables del evento indicado por su ID.
    """
    responsables = await listar_responsables_evento_crud(id_evento)
    return responsables