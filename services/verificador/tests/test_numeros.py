"""Tests de extracción y comparación de cifras."""

from __future__ import annotations

import pytest

from contratos import Zona
from verificador.numeros import cifras_permitidas, coincide, numeros_en


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("Llovió 2 mm", [2.0]),
        ("humedad 0,12 m3/m3", [0.12]),
        ("33.4 °C", [33.4]),
        ("bajó -60 %", [60.0]),
        ("1.200 hectáreas", [1200.0]),
        ("periodo 2026-10", [2026.0, 10.0]),
        ("producto T2M_MAX y MOD13Q1", []),
        ("sin números", []),
    ],
)
def test_numeros_en(texto: str, esperado: list[float]) -> None:
    assert numeros_en(texto) == esperado


def test_cifras_permitidas_incluye_datos_puntajes_y_periodo(zona: Zona) -> None:
    permitidas = cifras_permitidas(zona, "2026-10")
    for cifra in (33.4, 31.2, 7.1, 2.0, 60.0, 0.12, 55.0, 74.0, 61.0, 2026.0, 10.0, 100.0):
        assert cifra in permitidas


def test_los_subpuntajes_no_son_cifras_permitidas(zona: Zona) -> None:
    permitidas = cifras_permitidas(zona, "2026-10")
    assert 45.0 not in permitidas  # subpuntaje de mercado de la rotación "suelo"
    assert 85.0 not in permitidas


@pytest.mark.parametrize(
    ("numero", "valido"),
    [(33.0, True), (34.0, False), (0.1, True), (0.4, False), (72.0, False), (100.0, True)],
)
def test_coincide_tolera_redondeo(zona: Zona, numero: float, valido: bool) -> None:
    assert coincide(numero, cifras_permitidas(zona, "2026-10")) is valido
