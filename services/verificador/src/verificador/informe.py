"""Informe del mes en Markdown, para la revisión humana antes de publicar."""

from __future__ import annotations

from collections.abc import Sequence

from rotacion_contratos import Hechos, Origen
from verificador.verificar import FilaInforme

UMBRAL_PLANTILLAS = 0.5


def renderizar_informe(hechos: Hechos, filas: Sequence[FilaInforme]) -> str:
    """Arma el informe: totales, alertas para el revisor y detalle por zona."""
    total = len(filas)
    con_llm = sum(f.origen_final is Origen.LLM for f in filas)
    con_plantilla = total - con_llm
    con_avisos = sum(f.origen_final is Origen.LLM and bool(f.problemas) for f in filas)

    lineas = [
        f"# Informe de verificación — {hechos.periodo}",
        "",
        f"- **run_id:** `{hechos.run_id}`",
        f"- **Entorno:** `{hechos.entorno.value}`",
        f"- **Zonas:** {total} · con texto del LLM: {con_llm} · con plantilla: {con_plantilla}"
        f" · aprobadas con avisos: {con_avisos}",
        "",
        "## Para el revisor",
        "",
    ]
    alertas = []
    if total and con_plantilla / total > UMBRAL_PLANTILLAS:
        alertas.append(
            "⚠️ Más de la mitad de las zonas quedó con plantilla. Revisar la llave, el crédito o "
            "el prompt del LLM antes de aprobar."
        )
    if con_avisos:
        alertas.append("⚠️ Hay zonas aprobadas con avisos: leerlas en la tabla de abajo.")
    lineas += alertas or ["✅ Sin alertas."]
    lineas += [
        "",
        "Aprobar solo si: los textos se entienden, ninguna cifra se ve rara y cada rotación "
        "tiene un riesgo para revisar con un experto.",
        "",
        "## Detalle por zona",
        "",
        "| Zona | Texto final | Motivo | Problemas |",
        "|---|---|---|---|",
    ]
    for fila in filas:
        problemas = "<br>".join(_escapar(p) for p in fila.problemas) or "—"
        celdas = [fila.zona_id, fila.origen_final.value, _escapar(fila.motivo), problemas]
        lineas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(lineas) + "\n"


def _escapar(texto: str) -> str:
    return texto.replace("|", "\\|").replace("\n", " ")
