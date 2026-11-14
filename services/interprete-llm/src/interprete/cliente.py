"""Cliente del LLM. La interfaz `ClienteLLM` permite probar sin llamar a la API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import anthropic
from rotacion_contratos import InterpretacionLLM

from interprete.config import Config


@dataclass(frozen=True)
class RespuestaLLM:
    """Resultado de una llamada.

    Attributes:
        contenido: Interpretación validada, o `None` si el modelo no la entregó.
        stop_reason: Motivo de parada (`end_turn`, `max_tokens`, `refusal`…).
        modelo: Modelo que respondió.
        request_id: Id de la petición, para reportar fallas.
    """

    contenido: InterpretacionLLM | None
    stop_reason: str | None
    modelo: str
    request_id: str | None


class ClienteLLM(Protocol):
    """Cualquier cliente capaz de interpretar una zona."""

    def interpretar(self, sistema: str, mensaje: str) -> RespuestaLLM: ...


class ClienteClaude:
    """Cliente real sobre la Claude API con salida estructurada.

    El prompt de sistema va con `cache_control`, porque se repite igual en todas
    las zonas de la corrida; solo cambian los hechos del mensaje.
    """

    def __init__(self, config: Config, client: anthropic.Anthropic | None = None) -> None:
        self._config = config
        self._client = client or anthropic.Anthropic(
            timeout=config.timeout_s, max_retries=config.max_reintentos
        )

    def interpretar(self, sistema: str, mensaje: str) -> RespuestaLLM:
        """Pide la interpretación de una zona.

        Raises:
            anthropic.APIError: Errores de la API; los clasifica `interpretar.py`.
            pydantic.ValidationError: Si la respuesta no cumple el esquema.
        """
        respuesta = self._client.messages.parse(
            model=self._config.modelo,
            max_tokens=self._config.max_tokens,
            system=[{"type": "text", "text": sistema, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": mensaje}],
            output_format=InterpretacionLLM,
        )
        completa = respuesta.stop_reason not in ("refusal", "max_tokens")
        return RespuestaLLM(
            contenido=respuesta.parsed_output if completa else None,
            stop_reason=respuesta.stop_reason,
            modelo=respuesta.model,
            request_id=respuesta._request_id,
        )
