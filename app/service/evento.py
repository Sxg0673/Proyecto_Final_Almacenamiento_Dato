from fastapi import HTTPException, status
from app.models.evaluacion import Evaluacion
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.models.instalacion import Instalacion
from app.models.organizacion_externa import OrganizacionExterna
from app.schemas import evento
from app.schemas.evento import EstadoEventoEnum, EventoCrear, EventoRespuesta, EventoBD, EventoBD, EventoRespuesta, OrganizacionParticipante, ResponsableRespuesta, EvaluacionRespuesta, InstalacionRespuesta, OrganizacionExternaRespuesta
from beanie import PydanticObjectId
from typing import List, Optional
from app.schemas.evento import EventoRespuesta, ResponsableRespuesta, EvaluacionRespuesta, InstalacionRespuesta, OrganizacionExternaRespuesta, EventoActualizar, EvaluacionCrear
from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, List

# Crear un evento
async def crear_evento(payload: EventoCrear) -> Evento:
    """
    Crea un evento usando Beanie, con las reglas de negocio acordadas.
    """

    # -------------------------------------------------------------
    # 1. Validar fechas
    # -------------------------------------------------------------
    if payload.fecha_fin and payload.fecha_inicio >= payload.fecha_fin:
        raise HTTPException(400, "La fecha de inicio debe ser anterior a la fecha de fin")

    # -------------------------------------------------------------
    # 2. Estado inicial SOLO 'pendiente'
    # -------------------------------------------------------------
    if payload.estado != payload.estado.__class__.PENDIENTE:
        raise HTTPException(400, "El estado inicial de un evento siempre debe ser 'pendiente'.")

    # -------------------------------------------------------------
    # 3. Validar responsables
    # -------------------------------------------------------------
    if not payload.responsables or len(payload.responsables) == 0:
        raise HTTPException(400, "El evento debe tener al menos un responsable.")

    n_principales = sum(1 for r in payload.responsables if r.principal)

    if n_principales != 1:
        raise HTTPException(400, "Debe haber exactamente un responsable principal.")

    # Un evento puede tener responsables de docentes o de estudiantes, pero no ambos
    tipos = set()
    for r in payload.responsables:
        usuario = await Usuario.get(PydanticObjectId(r.id_responsable))
        if not usuario:
            raise HTTPException(404, f"Usuario responsable no encontrado: {r.id_responsable}")

        tipos.add(usuario.rol)

    if "docente" in tipos and "estudiante" in tipos:
        raise HTTPException(
            400,
            "Un evento no puede tener responsables docentes y estudiantes al mismo tiempo."
        )

    # -------------------------------------------------------------
    # 4. Validar instalaciones
    # -------------------------------------------------------------
    if not payload.instalaciones:
        raise HTTPException(400, "Debe asignarse mínimo una instalación.")

    for inst in payload.instalaciones:
        instal = await Instalacion.get(PydanticObjectId(inst.id_instalacion))
        if not instal:
            raise HTTPException(404, f"Instalación no encontrada: {inst.id_instalacion}")

        if payload.asistentes and instal.capacidad < payload.asistentes:
            raise HTTPException(
                400,
                f"La instalación {inst.nombre} no tiene capacidad suficiente."
            )

    # -------------------------------------------------------------
    # 5. Validar organizaciones participantes
    # -------------------------------------------------------------
    if payload.organizaciones_externas:
        for org in payload.organizaciones_externas:
            organizacion = await OrganizacionExterna.get(PydanticObjectId(org.id_organizacion))
            if not organizacion:
                raise HTTPException(404, f"Organización no encontrada: {org.id_organizacion}")

    # -------------------------------------------------------------
    # 6. Crear el documento Beanie y guardarlo
    # -------------------------------------------------------------
    evento_doc = Evento(**payload.model_dump())
    await evento_doc.insert()

    return evento_doc


# Service para listar eventos

async def listar_eventos() -> List[EventoRespuesta]:
    """
    Obtiene todos los eventos desde la BD (Evento) y los convierte
    a EventoRespuesta para devolverlos por la API.
    """
    # 1. Traer todos los eventos desde la base de datos
    eventos_bd: List[Evento] = await Evento.find_all().to_list()

    eventos_respuesta: List[EventoRespuesta] = []

    for evento in eventos_bd:
        # Convertir responsables
        responsables_resp = [
            ResponsableRespuesta(
                id_responsable=r.id_responsable,
                nombre=r.nombre,
                tipo_aval=r.tipo_aval,
                principal=r.principal
            )
            for r in getattr(evento, "responsables", [])
        ]

        # Convertir evaluaciones
        evaluaciones_resp = [
            EvaluacionRespuesta(
                id_evaluacion=e.id_evaluacion,
                id_secretario=e.id_secretario,
                fecha_evaluacion=e.fecha_evaluacion,
                justificacion=e.justificacion,
                acta_aprobacion=e.acta_aprobacion,
                estado=e.estado
            )
            for e in getattr(evento, "evaluaciones", [])
        ]

        # Convertir instalaciones
        instalaciones_resp = [
            InstalacionRespuesta(
                id_instalacion=i.id_instalacion,
                nombre=i.nombre,
                capacidad=i.capacidad
            )
            for i in getattr(evento, "instalaciones", [])
        ]

        # Convertir organizaciones externas
        organizaciones_resp = [
            OrganizacionExternaRespuesta(
                id_organizacion=o.id_organizacion,
                nombre=o.nombre,
                representantes=getattr(o, "representantes", []),
                certificado=getattr(o, "certificado", None)
            )
            for o in getattr(evento, "organizaciones_externas", [])
        ]
        # Crear objeto EventoRespuesta
        evento_resp = EventoRespuesta(
            _id=evento._id,
            nombre=evento.nombre,
            tipo_evento=getattr(evento, "tipo_evento", None),
            descripcion=getattr(evento, "descripcion", None),
            fecha_inicio=getattr(evento, "fecha_inicio", None),
            fecha_fin=getattr(evento, "fecha_fin", None),
            estado=getattr(evento, "estado", None),
            responsables=responsables_resp,
            evaluaciones=evaluaciones_resp,
            instalaciones=instalaciones_resp,
            organizaciones_externas=organizaciones_resp
        )

        eventos_respuesta.append(evento_resp)

    return eventos_respuesta


# Actualizar un evento existente
async def actualizar_evento(id_evento: str, datos_actualizados: EventoActualizar) -> EventoRespuesta:
    """
    Actualiza un evento existente parcialmente en MongoDB.
    Solo se aplican los campos enviados en `datos_actualizados`.
    """

    # 1) Validar que el ID sea un ObjectId válido
    if not PydanticObjectId.is_valid(id_evento):
        raise HTTPException(400, "El ID del evento no es válido.")

    # 2) Buscar el evento en la base de datos
    evento = await Evento.get(PydanticObjectId(id_evento))
    if not evento:
        raise HTTPException(404, "Evento no encontrado.")

    # 3) Validar reglas de negocio
    #    Ejemplo: estado no permite ciertos cambios (aquí adaptamos según tu enum)
    if evento.estado != "pendiente":  # Solo se permite actualizar si el estado es 'pendiente'
        raise HTTPException(400, "No se puede actualizar un evento que no esté pendiente.")

    # 4) Validar fechas si se envían
    fi: Optional[datetime] = datos_actualizados.fecha_inicio
    ff: Optional[datetime] = datos_actualizados.fecha_fin
    if fi and ff and fi > ff:
        raise HTTPException(400, "La fecha de inicio debe ser anterior o igual a la fecha de fin.")

    # 5) Validar responsables si se envían
    if datos_actualizados.responsables:
        n_principales = sum(1 for r in datos_actualizados.responsables if r.principal)
        if n_principales != 1:
            raise HTTPException(400, "Debe haber exactamente un responsable principal.")
        tipos = set()
        for r in datos_actualizados.responsables:
            from app.models.usuario import Usuario
            usuario = await Usuario.get(PydanticObjectId(r.id_responsable))
            if not usuario:
                raise HTTPException(404, f"Responsable no encontrado: {r.id_responsable}")
            tipos.add(usuario.rol)
        if "docente" in tipos and "estudiante" in tipos:
            raise HTTPException(
                400,
                "Un evento no puede tener responsables docentes y estudiantes al mismo tiempo."
            )

    # 6) Validar instalaciones si se envían
    if datos_actualizados.instalaciones:
        from app.models.instalacion import Instalacion
        for inst in datos_actualizados.instalaciones:
            instalacion = await Instalacion.get(PydanticObjectId(inst.id_instalacion))
            if not instalacion:
                raise HTTPException(404, f"Instalación no encontrada: {inst.id_instalacion}")
            if datos_actualizados.asistentes and instalacion.capacidad < datos_actualizados.asistentes:
                raise HTTPException(
                    400,
                    f"La instalación {instalacion.nombre} no tiene capacidad suficiente."
                )

    # 7) Validar organizaciones externas si se envían
    if datos_actualizados.organizaciones_externas:
        from app.models.organizacion_externa import OrganizacionExterna
        for org in datos_actualizados.organizaciones_externas:
            organizacion = await OrganizacionExterna.get(PydanticObjectId(org.id_organizacion))
            if not organizacion:
                raise HTTPException(404, f"Organización no encontrada: {org.id_organizacion}")

    # 8) Aplicar cambios (solo los campos enviados)
    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(evento, campo, valor)

    # 9) Guardar cambios
    await evento.save()  # Beanie actualiza solo los campos modificados

    # 10) Retornar el evento actualizado usando el schema de salida
    return EventoRespuesta(**evento.model_dump())


async def obtener_evento_por_id(id_evento: str) -> EventoRespuesta:
    """
    Obtiene un evento por su ID.
    """

    # 1. Validar que el ID sea un ObjectId válido
    if not PydanticObjectId.is_valid(id_evento):
        raise HTTPException(
            status_code=400,
            detail="El ID del evento no es válido."
        )

    # 2. Buscar el evento
    evento = await Evento.get(PydanticObjectId(id_evento))

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado."
        )

    # 3. Retornar usando el schema de salida
    return EventoRespuesta(**evento.model_dump())


# Eliminar un evento
async def eliminar_evento(id_evento: str) -> dict:
    """
    Elimina un evento por su ID.
    Retorna un mensaje de éxito si se elimina correctamente.
    """

    # 1. Validar que el ID sea un ObjectId válido
    if not PydanticObjectId.is_valid(id_evento):
        raise HTTPException(
            status_code=400,
            detail="El ID del evento no es válido."
        )

    # 2. Buscar el evento
    evento = await Evento.get(PydanticObjectId(id_evento))
    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado."
        )

    # 3. Eliminar el evento
    await evento.delete()

    # 4. Retornar mensaje de éxito
    return {"message": f"Evento con ID {id_evento} eliminado correctamente."}


async def agregar_evaluacion_a_evento(id_evento: str, payload: EvaluacionCrear) -> Evento:
    """
    Añade una evaluación a un evento y actualiza su estado según la evaluación.
    """

    # 1. Validar ObjectId
    if not PydanticObjectId.is_valid(id_evento):
        raise HTTPException(status_code=400, detail="El ID del evento no es válido.")
    if not PydanticObjectId.is_valid(payload.id_secretario):
        raise HTTPException(status_code=400, detail="El ID del secretario no es válido.")

    # 2. Buscar evento y secretario
    evento = await Evento.get(PydanticObjectId(id_evento))
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    secretario = await Usuario.get(PydanticObjectId(payload.id_secretario))
    if not secretario:
        raise HTTPException(status_code=404, detail="Secretario no encontrado.")

    # 3. Construir la evaluación embebida
    nueva_eval = Evaluacion(
        id_evaluacion=str(PydanticObjectId()),
        id_secretario=payload.id_secretario,
        fecha_evaluacion=datetime.utcnow(),
        justificacion=payload.justificacion,
        acta_aprobacion=payload.acta_aprobacion,
        estado=payload.estado
    )

    # 4. Agregar evaluación a la lista
    evento.evaluaciones.append(nueva_eval)

    # 5. Actualizar el estado del evento (regla de negocio)
    if payload.estado == "aprobado":
        evento.estado = "aprobado"
    elif payload.estado == "rechazado":
        evento.estado = "rechazado"

    # 6. Guardar cambios
    await evento.save()

    return EventoRespuesta(**evento.model_dump())
    