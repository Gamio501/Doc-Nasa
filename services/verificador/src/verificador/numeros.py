"""Extracción de números de un texto en español y cifras permitidas por zona."""

from __future__ import annotations

import re
from collections.abc import Iterable

from contratos import Zona
from contratos.hechos import AptitudCultivo, Rotacion

# Un número que no está pegado a letras (evita el "3" de "m3" o el "2" de "T2M").
_NUMERO = re.compile(r"(?<![A-Za-zÁÉÍÓÚáéíóúñÑ_\d])-?\d+(?:[.,]\d+)*(?![A-Za-zÁÉÍÓÚáéíóúñÑ_\d])")
_MILES = re.compile(r"-?\d{1,3}(?:\.\d{3})+")

# Escala de los puntajes ("74 de 100"): se puede escribir sin venir de un dato.
CONSTANTES_PERMITIDAS = frozenset({100.0})


def _a_float(texto: str) -> float | None:
    if _MILES.fullmatch(texto):
        return float(texto.replace(".", ""))
    normal = texto.replace(",", ".")
    if normal.count(".") > 1:
        return None
    return float(normal)


def numeros_en(texto: str) -> list[float]:
    """Devuelve los números escritos en `texto`, en valor absoluto.

    Acepta coma o punto decimal ("0,12", "33.4") y miles con punto ("1.200").

    Examples:
        >>> numeros_en("Llovió 2 mm, 60 % menos; humedad 0,12 m3/m3")
        [2.0, 60.0, 0.12]
    """
    valores = []
    for coincidencia in _NUMERO.finditer(texto):
        valor = _a_float(coincidencia.group())
        if valor is not None:
            valores.append(abs(valor))
    return valores


def cifras_permitidas(zona: Zona, periodo: str) -> frozenset[float]:
    """Cifras que un texto de la zona puede repetir (en valor absoluto).

    Incluye valores de indicadores, puntajes, el periodo y los números que ya
    traen las descripciones de reglas y las lagunas. Los subpuntajes quedan
    fuera a propósito: son muchos enteros redondos (45, 50, 55…) y abrirían la
    puerta a cifras inventadas como "riega 45 litros".
    """
    cifras: set[float] = set(CONSTANTES_PERMITIDAS)
    cifras.update(abs(float(parte)) for parte in periodo.split("-"))
    for ind in zona.indicadores:
        for valor in (ind.valor, ind.valor_normal, ind.diferencia_pct, ind.resolucion_km):
            if valor is not None:
                cifras.add(abs(valor))
    evaluados: list[AptitudCultivo | Rotacion] = [*zona.aptitud_cultivos, *zona.rotaciones]
    textos_confiables: list[str] = list(zona.lagunas)
    for evaluado in evaluados:
        cifras.add(evaluado.puntaje)
        textos_confiables.extend(f.descripcion for f in evaluado.factores)
    for texto in textos_confiables:
        cifras.update(numeros_en(texto))
    return frozenset(cifras)


def coincide(numero: float, permitidas: Iterable[float]) -> bool:
    """True si `numero` es una cifra permitida, tolerando redondeo.

    Cifras ≥ 1 aceptan redondeo a entero (33,4 → 33); cifras < 1 aceptan
    redondeo a un decimal (0,12 → 0,1).
    """
    for cifra in permitidas:
        tolerancia = 0.5 if cifra >= 1 else 0.05
        if abs(numero - cifra) <= tolerancia + 1e-9:
            return True
    return False
