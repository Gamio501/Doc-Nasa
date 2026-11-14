"""Fixtures compartidas: hechos de ejemplo del contrato y un cliente LLM falso."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import httpx2
import pytest
from rotacion_contratos import Hechos, InterpretacionLLM, Zona
from rotacion_contratos.interpretacion import Evidencia, TextoCultivo, TextoIndicador, TextoRotacion

from interprete.cliente import RespuestaLLM

RAIZ_REPO = Path(__file__).resolve().parents[3]
EJEMPLO = RAIZ_REPO / "contratos" / "ejemplos" / "hechos_ejemplo.json"
PETICION = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


@pytest.fixture
def hechos() -> Hechos:
    return Hechos.model_validate_json(EJEMPLO.read_text(encoding="utf-8"))


@pytest.fixture
def zona(hechos: Hechos) -> Zona:
    return hechos.zonas[0]


def contenido_para(zona: Zona) -> InterpretacionLLM:
    """Interpretación válida y completa para la zona dada."""
    return InterpretacionLLM(
        resumen_zona="Mes más seco y caluroso de lo normal en tu zona.",
        indicadores=[
            TextoIndicador(indicador_id=i.id, texto=f"{i.nombre} en tu zona.")
            for i in zona.indicadores
        ],
        cultivos=[
            TextoCultivo(
                cultivo_id=a.cultivo_id,
                temporada=a.temporada,
                por_que="Encaja con tu zona.",
                a_favor=["Aguanta el calor."],
                en_contra=[],
                cuidados=["Riega con cuidado."],
                evidencia=[Evidencia(indicador_id="ind-temp_max", frase="Hace calor.")],
            )
            for a in zona.aptitud_cultivos
        ],
        rotaciones=[
            TextoRotacion(
                rotacion_id=r.rotacion_id,
                por_que="Cuida el suelo.",
                evidencia=[],
                beneficios=["Menos agua."],
                lagunas=["Falta el dato de vegetación."],
                riesgos_validar_experto=["Revisa el riego con un técnico."],
            )
            for r in zona.rotaciones
        ],
    )


@dataclass
class ClienteFalso:
    """Cliente que devuelve respuestas o lanza errores programados."""

    responder: Callable[[str, str], RespuestaLLM]
    llamadas: list[tuple[str, str]] = field(default_factory=list)

    def interpretar(self, sistema: str, mensaje: str) -> RespuestaLLM:
        self.llamadas.append((sistema, mensaje))
        return self.responder(sistema, mensaje)


def respuesta_ok(contenido: InterpretacionLLM) -> RespuestaLLM:
    return RespuestaLLM(
        contenido=contenido, stop_reason="end_turn", modelo="claude-opus-5-5", request_id="req_1"
    )


def respuesta_http(status: int) -> httpx2.Response:
    return httpx2.Response(status, request=PETICION)
