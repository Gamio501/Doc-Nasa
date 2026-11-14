"""Contrato `hechos` v1: salida del calculador y entrada del intérprete LLM.

Cada número que la app muestra nace aquí. El LLM solo puede repetir estas
cifras; nunca calcular otras.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "1.0"

PATRON_RUN_ID = r"^\d{4}-\d{2}-[a-z0-9]{6}$"
PATRON_PERIODO = r"^\d{4}-\d{2}$"
PATRON_INDICADOR_ID = r"^ind-[a-z0-9_]+$"


class Base(BaseModel):
    """Base común: no acepta campos extra y es inmutable."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class Entorno(StrEnum):
    DEV = "dev"
    PROD = "prod"


class Confianza(StrEnum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Semaforo(StrEnum):
    VERDE = "verde"
    AMARILLO = "amarillo"
    ROJO = "rojo"
    SIN_DATO = "sin_dato"


class Escala(StrEnum):
    """Si el dato describe la zona (~5–55 km) o casi la parcela (≤ 250 m)."""

    ZONA = "zona"
    PARCELA = "parcela"


class Efecto(StrEnum):
    A_FAVOR = "a_favor"
    EN_CONTRA = "en_contra"


class Nivel(StrEnum):
    ALTO = "alto"
    MEDIO = "medio"
    BAJO = "bajo"


class Indicador(Base):
    """Un dato de la zona, ya limpio (-999 de la NASA llega como `None`)."""

    id: str = Field(pattern=PATRON_INDICADOR_ID, description="Ej. ind-humedad_suelo")
    nombre: str = Field(min_length=1, description="Nombre simple: 'humedad del suelo'")
    valor: float | None
    unidad: str
    periodo: str = Field(pattern=PATRON_PERIODO)
    valor_normal: float | None = Field(description="Promedio histórico del mismo mes")
    diferencia_pct: float | None = Field(
        description="(valor - valor_normal) / valor_normal * 100, calculado por el código"
    )
    resolucion_km: float = Field(gt=0)
    fuente: str = Field(min_length=1, description="Producto exacto, ej. 'SMAP SPL3SMP_E'")
    confianza: Confianza
    escala: Escala
    semaforo: Semaforo


class Factor(Base):
    """Una regla agronómica que pesó en un puntaje (sale de agronomia/reglas.yaml)."""

    regla_id: str = Field(min_length=1)
    efecto: Efecto
    descripcion: str = Field(min_length=1, description="En español simple")
    indicador_ids: list[str]


class Subpuntajes(Base):
    """Puntaje 0–100 por criterio. El teléfono los combina con los deslizadores."""

    agua: float = Field(ge=0, le=100)
    ingresos: float = Field(ge=0, le=100)
    suelo: float = Field(ge=0, le=100)
    erosion: float = Field(ge=0, le=100)
    clima: float = Field(ge=0, le=100)
    mercado: float = Field(ge=0, le=100)


class AptitudCultivo(Base):
    cultivo_id: str = Field(min_length=1)
    cultivo_nombre: str = Field(min_length=1)
    temporada: str = Field(min_length=1, description="Ej. 'nov-dic'")
    puntaje: float = Field(ge=0, le=100)
    nivel: Nivel
    subpuntajes: Subpuntajes
    factores: list[Factor]
    confianza: Confianza


class Rotacion(Base):
    rotacion_id: str = Field(min_length=1, description="Ej. 'actual', 'agua', 'suelo'")
    nombre: str = Field(min_length=1)
    es_actual: bool
    secuencia: list[str] = Field(min_length=1, description="cultivo_id por temporada")
    puntaje: float = Field(ge=0, le=100)
    subpuntajes: Subpuntajes
    factores: list[Factor]
    confianza: Confianza


class Zona(Base):
    zona_id: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    provincia: str = Field(min_length=1)
    celdas: list[str] = Field(min_length=1)
    indicadores: list[Indicador] = Field(min_length=1)
    aptitud_cultivos: list[AptitudCultivo] = Field(min_length=1)
    rotaciones: list[Rotacion] = Field(min_length=3, description="El reto exige 3 o más")
    lagunas: list[str] = Field(description="Datos que faltan o son dudosos")

    @model_validator(mode="after")
    def _validar_coherencia(self) -> Zona:
        ids = [i.id for i in self.indicadores]
        if len(ids) != len(set(ids)):
            raise ValueError(f"{self.zona_id}: hay indicadores repetidos")
        rot_ids = [r.rotacion_id for r in self.rotaciones]
        if len(rot_ids) != len(set(rot_ids)):
            raise ValueError(f"{self.zona_id}: hay rotaciones repetidas")
        if sum(r.es_actual for r in self.rotaciones) != 1:
            raise ValueError(f"{self.zona_id}: debe haber exactamente una rotación actual")
        claves = [(a.cultivo_id, a.temporada) for a in self.aptitud_cultivos]
        if len(claves) != len(set(claves)):
            raise ValueError(f"{self.zona_id}: cultivo y temporada repetidos")
        conocidos = set(ids)
        factores = [f for a in self.aptitud_cultivos for f in a.factores] + [
            f for r in self.rotaciones for f in r.factores
        ]
        desconocidos = {i for f in factores for i in f.indicador_ids} - conocidos
        if desconocidos:
            raise ValueError(
                f"{self.zona_id}: factores citan indicadores inexistentes {desconocidos}"
            )
        return self

    def indicador_ids(self) -> set[str]:
        """Ids de indicadores de la zona."""
        return {i.id for i in self.indicadores}


class Hechos(Base):
    """Archivo `hechos.json` de una corrida."""

    schema_version: Literal["1.0"]
    run_id: str = Field(pattern=PATRON_RUN_ID, description="AAAA-MM-xxxxxx")
    entorno: Entorno
    periodo: str = Field(pattern=PATRON_PERIODO)
    zonas: list[Zona] = Field(min_length=1)

    @model_validator(mode="after")
    def _zonas_unicas(self) -> Hechos:
        ids = [z.zona_id for z in self.zonas]
        if len(ids) != len(set(ids)):
            raise ValueError("hay zonas repetidas")
        return self
