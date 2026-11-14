"""Construcción del prompt: sistema fijo (cacheable) + hechos de una zona."""

from __future__ import annotations

import json
from pathlib import Path

from rotacion_contratos import Zona


def cargar_sistema(ruta: Path) -> str:
    """Lee el prompt de sistema versionado.

    Raises:
        FileNotFoundError: Si la versión pedida no existe.
    """
    texto = ruta.read_text(encoding="utf-8").strip()
    if not texto:
        raise ValueError(f"El prompt de sistema está vacío: {ruta}")
    return texto


def construir_mensaje(zona: Zona, periodo: str) -> str:
    """Arma el mensaje de usuario con los hechos de una zona.

    El JSON va con claves ordenadas para que el mismo hecho produzca siempre el
    mismo texto (útil para comparar corridas y para la caché).

    Args:
        zona: Hechos de la zona, ya validados por el contrato.
        periodo: Mes de los datos (`AAAA-MM`).

    Returns:
        Mensaje listo para enviar al modelo.
    """
    hechos = json.dumps(zona.model_dump(mode="json"), ensure_ascii=False, sort_keys=True)
    cultivos = ", ".join(f"{a.cultivo_id}/{a.temporada}" for a in zona.aptitud_cultivos)
    rotaciones = ", ".join(r.rotacion_id for r in zona.rotaciones)
    indicadores = ", ".join(i.id for i in zona.indicadores)
    return (
        f"Periodo de los datos: {periodo}.\n"
        f"<hechos>\n{hechos}\n</hechos>\n\n"
        "Interpreta esta zona siguiendo tus instrucciones. Cobertura obligatoria:\n"
        f"- indicadores: {indicadores}\n"
        f"- cultivos (cultivo_id/temporada): {cultivos}\n"
        f"- rotaciones: {rotaciones}"
    )
