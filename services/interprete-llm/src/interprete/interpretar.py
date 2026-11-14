"""Interpreta todas las zonas de un `hechos.json`.

Regla de fallas:
- Errores de configuración (llave inválida, sin permiso, modelo inexistente)
  detienen la corrida: fallarían en todas las zonas y hay que arreglarlos.
- Errores de una zona (red, límite de uso, 5xx, respuesta inválida, refusal)
  se registran como `origen: error`; el verificador pondrá la plantilla.
"""

from __future__ import annotations

import logging

import anthropic
from contratos import Hechos, Interpretaciones, InterpretacionZona, Origen, Zona
from pydantic import ValidationError

from interprete.cliente import ClienteLLM
from interprete.prompt import construir_mensaje

log = logging.getLogger(__name__)

MOTIVO_SIN_LLM = "LLM desactivado (--sin-llm)"


class ErrorConfiguracionLLM(RuntimeError):
    """La API rechazó la configuración: no tiene sentido seguir con otras zonas."""


def interpretar_zona(
    zona: Zona, cliente: ClienteLLM, sistema: str, periodo: str
) -> InterpretacionZona:
    """Interpreta una zona sin dejar que una falla puntual detenga la corrida.

    Raises:
        ErrorConfiguracionLLM: Llave inválida, sin permisos o modelo inexistente.
    """
    mensaje = construir_mensaje(zona, periodo)
    try:
        respuesta = cliente.interpretar(sistema, mensaje)
    except (
        anthropic.AuthenticationError,
        anthropic.PermissionDeniedError,
        anthropic.NotFoundError,
    ) as exc:
        raise ErrorConfiguracionLLM(f"{type(exc).__name__}: {exc.message}") from exc
    except anthropic.BadRequestError as exc:
        return _error(zona, f"petición rechazada (400): {exc.message}")
    except anthropic.RateLimitError:
        return _error(zona, "límite de uso de la API (429) tras los reintentos")
    except anthropic.APIStatusError as exc:
        return _error(zona, f"error de la API ({exc.status_code})")
    except anthropic.APIConnectionError:
        return _error(zona, "sin conexión con la API o tiempo agotado")
    except ValidationError as exc:
        return _error(zona, f"respuesta fuera del esquema: {exc.error_count()} errores")

    if respuesta.contenido is None:
        return _error(
            zona,
            f"el modelo no entregó la interpretación (stop_reason={respuesta.stop_reason})",
            modelo=respuesta.modelo,
            request_id=respuesta.request_id,
        )
    return InterpretacionZona(
        zona_id=zona.zona_id,
        origen=Origen.LLM,
        modelo=respuesta.modelo,
        request_id=respuesta.request_id,
        contenido=respuesta.contenido,
    )


def interpretar_hechos(
    hechos: Hechos, cliente: ClienteLLM | None, sistema: str
) -> Interpretaciones:
    """Interpreta todas las zonas. Con `cliente=None` no llama al LLM (modo plantillas).

    Raises:
        ErrorConfiguracionLLM: Ver `interpretar_zona`.
    """
    zonas = []
    for zona in hechos.zonas:
        if cliente is None:
            resultado = _error(zona, MOTIVO_SIN_LLM)
        else:
            resultado = interpretar_zona(zona, cliente, sistema, hechos.periodo)
        log.info("run_id=%s zona=%s origen=%s", hechos.run_id, zona.zona_id, resultado.origen.value)
        zonas.append(resultado)
    return Interpretaciones(
        schema_version="1.0",
        run_id=hechos.run_id,
        entorno=hechos.entorno,
        verificada=False,
        zonas=zonas,
    )


def _error(
    zona: Zona, motivo: str, *, modelo: str | None = None, request_id: str | None = None
) -> InterpretacionZona:
    log.warning("zona=%s sin interpretación LLM: %s", zona.zona_id, motivo)
    return InterpretacionZona(
        zona_id=zona.zona_id,
        origen=Origen.ERROR,
        modelo=modelo,
        request_id=request_id,
        error=motivo,
    )
