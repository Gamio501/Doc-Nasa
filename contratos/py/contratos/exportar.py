"""Genera los JSON Schema de `contratos/` desde los modelos Python.

Uso: `python -m contratos.exportar` (desde `contratos/py`). Un test falla si
los archivos quedaron desactualizados.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from contratos.hechos import Hechos
from contratos.interpretacion import Interpretaciones, InterpretacionLLM

DESTINO = Path(__file__).resolve().parents[2]

ESQUEMAS: dict[str, type[BaseModel]] = {
    "hechos.schema.json": Hechos,
    "interpretacion.schema.json": Interpretaciones,
    "interpretacion_llm.schema.json": InterpretacionLLM,
}


def renderizar(modelo: type[BaseModel]) -> str:
    """Devuelve el JSON Schema del modelo con formato estable."""
    esquema = modelo.model_json_schema()
    return json.dumps(esquema, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def exportar(destino: Path = DESTINO) -> list[Path]:
    """Escribe cada esquema en `destino` y devuelve las rutas escritas."""
    rutas = []
    for nombre, modelo in ESQUEMAS.items():
        ruta = destino / nombre
        ruta.write_text(renderizar(modelo), encoding="utf-8", newline="\n")
        rutas.append(ruta)
    return rutas


if __name__ == "__main__":
    for ruta in exportar():
        print(f"escrito {ruta}")
