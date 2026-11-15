"""Modelos Python de los contratos v1 (fuente de verdad de los JSON Schema)."""

from rotacion_contratos.hechos import SCHEMA_VERSION, Hechos, Zona
from rotacion_contratos.interpretacion import (
    AVISO_EXPERTO,
    Interpretaciones,
    InterpretacionLLM,
    InterpretacionZona,
    Origen,
)

__all__ = [
    "AVISO_EXPERTO",
    "SCHEMA_VERSION",
    "Hechos",
    "InterpretacionLLM",
    "InterpretacionZona",
    "Interpretaciones",
    "Origen",
    "Zona",
]
