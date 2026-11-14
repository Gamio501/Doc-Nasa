"""Contrato `interpretacion` v1: textos simples por zona.

- `InterpretacionLLM` es lo que el LLM rellena (salida estructurada). No lleva
  restricciones de longitud ni patrones: eso lo revisa el verificador.
- `Interpretaciones` es el archivo que escriben `interprete-llm` y `verificador`.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field

from contratos.hechos import PATRON_RUN_ID, Entorno

AVISO_EXPERTO: Final = "Esta herramienta apoya tu decisión; no reemplaza a un experto local."


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class TextoIndicador(Base):
    indicador_id: str
    texto: str


class Evidencia(Base):
    indicador_id: str
    frase: str


class TextoCultivo(Base):
    cultivo_id: str
    temporada: str
    por_que: str
    a_favor: list[str]
    en_contra: list[str]
    cuidados: list[str]
    evidencia: list[Evidencia]


class TextoRotacion(Base):
    rotacion_id: str
    por_que: str
    evidencia: list[Evidencia]
    beneficios: list[str]
    lagunas: list[str]
    riesgos_validar_experto: list[str]


class InterpretacionLLM(Base):
    """Esquema que el LLM debe llenar para una zona."""

    resumen_zona: str
    indicadores: list[TextoIndicador]
    cultivos: list[TextoCultivo]
    rotaciones: list[TextoRotacion]


class Origen(StrEnum):
    LLM = "llm"
    PLANTILLA = "plantilla"
    ERROR = "error"


class InterpretacionZona(Base):
    zona_id: str
    origen: Origen
    modelo: str | None = None
    request_id: str | None = None
    contenido: InterpretacionLLM | None = None
    error: str | None = None
    problemas: list[str] = Field(default_factory=list)
    aviso: Literal["Esta herramienta apoya tu decisión; no reemplaza a un experto local."] = (
        AVISO_EXPERTO
    )


class Interpretaciones(Base):
    """Archivo `interpretacion.json` (de `interprete-llm`) o `interpretacion_verificada.json`."""

    schema_version: Literal["1.0"]
    run_id: str = Field(pattern=PATRON_RUN_ID)
    entorno: Entorno
    verificada: bool
    zonas: list[InterpretacionZona]
