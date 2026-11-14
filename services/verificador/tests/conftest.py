"""Fixtures: hechos de ejemplo y una interpretación del LLM que sí pasa."""

from __future__ import annotations

from pathlib import Path

import pytest

from rotacion_contratos import (
    Hechos,
    Interpretaciones,
    InterpretacionLLM,
    InterpretacionZona,
    Origen,
    Zona,
)
from rotacion_contratos.interpretacion import Evidencia, TextoCultivo, TextoIndicador, TextoRotacion

RAIZ_REPO = Path(__file__).resolve().parents[3]
EJEMPLO = RAIZ_REPO / "contratos" / "ejemplos" / "hechos_ejemplo.json"


@pytest.fixture
def hechos() -> Hechos:
    return Hechos.model_validate_json(EJEMPLO.read_text(encoding="utf-8"))


@pytest.fixture
def zona(hechos: Hechos) -> Zona:
    return hechos.zonas[0]


def contenido_bueno(zona: Zona) -> InterpretacionLLM:
    """Texto como el que debería escribir el LLM: cifras solo de los hechos."""
    return InterpretacionLLM(
        resumen_zona="Octubre fue más seco y caluroso de lo normal en tu zona.",
        indicadores=[
            TextoIndicador(indicador_id=i.id, texto=f"La {i.nombre} se ve así en tu zona.")
            for i in zona.indicadores
        ],
        cultivos=[
            TextoCultivo(
                cultivo_id=a.cultivo_id,
                temporada=a.temporada,
                por_que=f"El {a.cultivo_nombre} saca {a.puntaje:.0f} de 100 para {a.temporada}.",
                a_favor=["Aguanta el calor de la zona."],
                en_contra=["La tierra está seca."],
                cuidados=["Conviene regar temprano."],
                evidencia=[Evidencia(indicador_id="ind-temp_max", frase="Hizo 33 °C.")],
            )
            for a in zona.aptitud_cultivos
        ],
        rotaciones=[
            TextoRotacion(
                rotacion_id=r.rotacion_id,
                por_que="La lluvia fue 60 % menor que lo normal.",
                evidencia=[Evidencia(indicador_id="ind-lluvia_mes", frase="Llovió 2 mm.")],
                beneficios=["Puede ahorrar agua."],
                lagunas=["Falta el dato de vegetación de octubre."],
                riesgos_validar_experto=["Revisa con un técnico si tu pozo alcanza."],
            )
            for r in zona.rotaciones
        ],
    )


def interpretaciones_con(hechos: Hechos, *zonas: InterpretacionZona) -> Interpretaciones:
    return Interpretaciones(
        schema_version="1.0",
        run_id=hechos.run_id,
        entorno=hechos.entorno,
        verificada=False,
        zonas=list(zonas),
    )


def zona_llm(zona: Zona, contenido: InterpretacionLLM) -> InterpretacionZona:
    return InterpretacionZona(
        zona_id=zona.zona_id,
        origen=Origen.LLM,
        modelo="claude-opus-5-5",
        request_id="req_1",
        contenido=contenido,
    )
