"""Reglas que revisa el verificador sobre la interpretación de una zona."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Hashable, Iterable, Iterator, Sequence, Set
from dataclasses import dataclass
from enum import StrEnum

from rotacion_contratos import InterpretacionLLM, Zona
from rotacion_contratos.interpretacion import TextoCultivo, TextoRotacion
from verificador.numeros import cifras_permitidas, coincide, numeros_en

MAX_RESUMEN = 300
MAX_POR_QUE = 400

_CERTEZA = re.compile(
    r"\bgarantiz\w*|\bsin duda\b|\bseguro que\b|\bes seguro\b|\bsiempre\b|\bnunca falla\b"
    r"|\b100\s?%",
    re.IGNORECASE,
)
_JERGA = re.compile(r"\bNDVI\b|evapotranspiraci|anomal[ií]a", re.IGNORECASE)


class Severidad(StrEnum):
    BLOQUEANTE = "bloqueante"  # la zona pasa a plantilla
    AVISO = "aviso"  # se publica, pero el revisor humano debe mirarlo


@dataclass(frozen=True)
class Problema:
    severidad: Severidad
    mensaje: str

    def __str__(self) -> str:
        return f"[{self.severidad.value}] {self.mensaje}"


def textos(contenido: InterpretacionLLM) -> Iterator[tuple[str, str]]:
    """Recorre todos los textos visibles para el agricultor como (campo, texto)."""
    yield "resumen_zona", contenido.resumen_zona
    for ind in contenido.indicadores:
        yield f"indicadores[{ind.indicador_id}]", ind.texto
    for cul in contenido.cultivos:
        campo = f"cultivos[{cul.cultivo_id}/{cul.temporada}]"
        yield f"{campo}.por_que", cul.por_que
        for nombre, lista in (
            ("a_favor", cul.a_favor),
            ("en_contra", cul.en_contra),
            ("cuidados", cul.cuidados),
        ):
            for texto in lista:
                yield f"{campo}.{nombre}", texto
        for ev in cul.evidencia:
            yield f"{campo}.evidencia", ev.frase
    for rot in contenido.rotaciones:
        campo = f"rotaciones[{rot.rotacion_id}]"
        yield f"{campo}.por_que", rot.por_que
        for nombre, lista in (
            ("beneficios", rot.beneficios),
            ("lagunas", rot.lagunas),
            ("riesgos_validar_experto", rot.riesgos_validar_experto),
        ):
            for texto in lista:
                yield f"{campo}.{nombre}", texto
        for ev in rot.evidencia:
            yield f"{campo}.evidencia", ev.frase


def revisar(zona: Zona, contenido: InterpretacionLLM, periodo: str) -> list[Problema]:
    """Devuelve los problemas de la interpretación de una zona (vacía si está bien)."""
    return [
        *_cobertura(zona, contenido),
        *_evidencia(zona, contenido),
        *_cifras(zona, contenido, periodo),
        *_lenguaje(contenido),
        *_riesgos_y_lagunas(zona, contenido),
    ]


def _bloq(mensaje: str) -> Problema:
    return Problema(Severidad.BLOQUEANTE, mensaje)


def _aviso(mensaje: str) -> Problema:
    return Problema(Severidad.AVISO, mensaje)


def _comparar(
    nombre: str, esperadas: Set[Hashable], recibidas: Sequence[Hashable]
) -> list[Problema]:
    problemas = []
    repetidas = [k for k, n in Counter(recibidas).items() if n > 1]
    if repetidas:
        problemas.append(_bloq(f"{nombre} repetidos: {sorted(map(str, repetidas))}"))
    faltan = esperadas - set(recibidas)
    if faltan:
        problemas.append(_bloq(f"{nombre} sin texto: {sorted(map(str, faltan))}"))
    sobran = set(recibidas) - esperadas
    if sobran:
        inexistentes = sorted(map(str, sobran))
        problemas.append(_bloq(f"{nombre} que no existen en los hechos: {inexistentes}"))
    return problemas


def _cobertura(zona: Zona, contenido: InterpretacionLLM) -> list[Problema]:
    return [
        *_comparar(
            "indicadores",
            set(zona.indicador_ids()),
            [i.indicador_id for i in contenido.indicadores],
        ),
        *_comparar(
            "cultivos",
            {(a.cultivo_id, a.temporada) for a in zona.aptitud_cultivos},
            [(c.cultivo_id, c.temporada) for c in contenido.cultivos],
        ),
        *_comparar(
            "rotaciones",
            {r.rotacion_id for r in zona.rotaciones},
            [r.rotacion_id for r in contenido.rotaciones],
        ),
    ]


def _evidencia(zona: Zona, contenido: InterpretacionLLM) -> list[Problema]:
    citadas = [e.indicador_id for c in contenido.cultivos for e in c.evidencia] + [
        e.indicador_id for r in contenido.rotaciones for e in r.evidencia
    ]
    inventadas = sorted(set(citadas) - zona.indicador_ids())
    return [_bloq(f"evidencia cita indicadores inexistentes: {inventadas}")] if inventadas else []


def _cifras(zona: Zona, contenido: InterpretacionLLM, periodo: str) -> list[Problema]:
    permitidas = cifras_permitidas(zona, periodo)
    problemas = []
    for campo, texto in textos(contenido):
        extranas = [n for n in numeros_en(texto) if not coincide(n, permitidas)]
        if extranas:
            problemas.append(_bloq(f"cifra que no está en los hechos en {campo}: {extranas}"))
    return problemas


def _lenguaje(contenido: InterpretacionLLM) -> list[Problema]:
    problemas = []
    for campo, texto in textos(contenido):
        if not texto.strip():
            problemas.append(_bloq(f"texto vacío en {campo}"))
        if certeza := _CERTEZA.search(texto):
            problemas.append(_bloq(f"lenguaje de certeza «{certeza.group()}» en {campo}"))
        if jerga := _JERGA.search(texto):
            problemas.append(_aviso(f"jerga técnica «{jerga.group()}» en {campo}"))
    if len(contenido.resumen_zona) > MAX_RESUMEN:
        problemas.append(_aviso(f"resumen_zona largo ({len(contenido.resumen_zona)} caracteres)"))
    items: list[TextoCultivo | TextoRotacion] = [*contenido.cultivos, *contenido.rotaciones]
    for item in items:
        if len(item.por_que) > MAX_POR_QUE:
            problemas.append(_aviso(f"por_que largo ({len(item.por_que)} caracteres)"))
    return problemas


def _riesgos_y_lagunas(zona: Zona, contenido: InterpretacionLLM) -> list[Problema]:
    problemas = [
        _bloq(f"rotación {r.rotacion_id} sin riesgos para validar con un experto")
        for r in contenido.rotaciones
        if not any(t.strip() for t in r.riesgos_validar_experto)
    ]
    hay_huecos = bool(zona.lagunas) or any(i.valor is None for i in zona.indicadores)
    if hay_huecos and not _alguna(r.lagunas for r in contenido.rotaciones):
        problemas.append(_aviso("faltan datos en la zona pero ninguna rotación menciona lagunas"))
    return problemas


def _alguna(listas: Iterable[list[str]]) -> bool:
    return any(t.strip() for lista in listas for t in lista)
