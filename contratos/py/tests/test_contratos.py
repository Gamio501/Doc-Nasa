"""Tests del contrato v1: el ejemplo es válido y las reglas de coherencia se cumplen."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from rotacion_contratos.exportar import DESTINO, ESQUEMAS, renderizar
from rotacion_contratos.hechos import Hechos
from rotacion_contratos.interpretacion import AVISO_EXPERTO, InterpretacionZona, Origen

EJEMPLO = DESTINO / "ejemplos" / "hechos_ejemplo.json"


@pytest.fixture
def datos() -> dict[str, Any]:
    cargado: dict[str, Any] = json.loads(EJEMPLO.read_text(encoding="utf-8"))
    return cargado


def _zona(datos: dict[str, Any]) -> dict[str, Any]:
    zona: dict[str, Any] = datos["zonas"][0]
    return zona


def test_el_ejemplo_cumple_el_contrato(datos: dict[str, Any]) -> None:
    hechos = Hechos.model_validate(datos)
    assert hechos.zonas[0].zona_id == "PIU-SUL-01"
    assert hechos.zonas[0].indicadores[3].valor is None  # -999 de la NASA llega como None


def test_rechaza_menos_de_tres_rotaciones(datos: dict[str, Any]) -> None:
    _zona(datos)["rotaciones"] = _zona(datos)["rotaciones"][:2]
    with pytest.raises(ValidationError, match="at least 3"):
        Hechos.model_validate(datos)


def test_exige_exactamente_una_rotacion_actual(datos: dict[str, Any]) -> None:
    _zona(datos)["rotaciones"][1]["es_actual"] = True
    with pytest.raises(ValidationError, match="exactamente una rotación actual"):
        Hechos.model_validate(datos)


def test_rechaza_factor_que_cita_indicador_inexistente(datos: dict[str, Any]) -> None:
    _zona(datos)["aptitud_cultivos"][0]["factores"][0]["indicador_ids"] = ["ind-no_existe"]
    with pytest.raises(ValidationError, match="indicadores inexistentes"):
        Hechos.model_validate(datos)


def test_rechaza_indicadores_repetidos(datos: dict[str, Any]) -> None:
    zona = _zona(datos)
    zona["indicadores"].append(copy.deepcopy(zona["indicadores"][0]))
    with pytest.raises(ValidationError, match="indicadores repetidos"):
        Hechos.model_validate(datos)


def test_rechaza_cultivo_y_temporada_repetidos(datos: dict[str, Any]) -> None:
    zona = _zona(datos)
    zona["aptitud_cultivos"].append(copy.deepcopy(zona["aptitud_cultivos"][0]))
    with pytest.raises(ValidationError, match="cultivo y temporada repetidos"):
        Hechos.model_validate(datos)


def test_rechaza_zonas_repetidas(datos: dict[str, Any]) -> None:
    datos["zonas"].append(copy.deepcopy(_zona(datos)))
    with pytest.raises(ValidationError, match="zonas repetidas"):
        Hechos.model_validate(datos)


@pytest.mark.parametrize(
    ("ruta", "valor"),
    [
        (("run_id",), "octubre"),
        (("periodo",), "2026-10-01"),
        (("zonas", 0, "aptitud_cultivos", 0, "puntaje"), 120),
        (("zonas", 0, "indicadores", 0, "id"), "temp_max"),
    ],
)
def test_rechaza_formatos_invalidos(
    datos: dict[str, Any], ruta: tuple[Any, ...], valor: Any
) -> None:
    destino: Any = datos
    for paso in ruta[:-1]:
        destino = destino[paso]
    destino[ruta[-1]] = valor
    with pytest.raises(ValidationError):
        Hechos.model_validate(datos)


def test_rechaza_campos_extra(datos: dict[str, Any]) -> None:
    datos["inventado"] = 1
    with pytest.raises(ValidationError, match="Extra inputs"):
        Hechos.model_validate(datos)


def test_interpretacion_zona_lleva_siempre_el_aviso() -> None:
    zona = InterpretacionZona(zona_id="PIU-SUL-01", origen=Origen.ERROR, error="sin red")
    assert zona.aviso == AVISO_EXPERTO
    assert zona.problemas == []


@pytest.mark.parametrize("nombre", sorted(ESQUEMAS))
def test_los_json_schema_estan_actualizados(nombre: str) -> None:
    ruta: Path = DESTINO / nombre
    assert ruta.exists(), f"Falta {nombre}: correr `python -m rotacion_contratos.exportar`"
    assert ruta.read_text(encoding="utf-8") == renderizar(ESQUEMAS[nombre]), (
        f"{nombre} desactualizado: correr `python -m rotacion_contratos.exportar`"
    )
