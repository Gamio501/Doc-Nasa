"""CLI del intérprete.

Uso:
    python -m interprete --hechos runs/dev/<run_id>/02_calculador/hechos.json \\
        --salida runs/dev/<run_id>/03_interprete/interpretacion.json [--sin-llm]

Códigos de salida: 0 = archivo escrito; 1 = entrada inválida; 2 = error de
configuración del LLM (llave, permisos, modelo).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from contratos import Hechos
from pydantic import ValidationError

from interprete.cliente import ClienteClaude, ClienteLLM
from interprete.config import Config
from interprete.interpretar import ErrorConfiguracionLLM, interpretar_hechos
from interprete.prompt import cargar_sistema

log = logging.getLogger("interprete")

FabricaCliente = Callable[[Config], ClienteLLM]


def _parsear(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="interprete", description=__doc__)
    parser.add_argument("--hechos", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument(
        "--sin-llm", action="store_true", help="No llamar al LLM: todas las zonas a plantilla"
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, fabrica: FabricaCliente = ClienteClaude) -> int:
    """Ejecuta la etapa y devuelve el código de salida."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = _parsear(argv)
    try:
        hechos = Hechos.model_validate_json(args.hechos.read_text(encoding="utf-8"))
        config = Config.desde_entorno(os.environ)
        sistema = cargar_sistema(config.prompt_path)
    except (OSError, ValueError, ValidationError) as exc:
        log.error("entrada inválida: %s", exc)
        return 1

    cliente = None if args.sin_llm else fabrica(config)
    try:
        resultado = interpretar_hechos(hechos, cliente, sistema)
    except ErrorConfiguracionLLM as exc:
        log.error("configuración del LLM inválida, se detiene la corrida: %s", exc)
        return 2

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(resultado.model_dump_json(indent=2), encoding="utf-8")
    con_llm = sum(z.contenido is not None for z in resultado.zonas)
    log.info("run_id=%s zonas=%d con_llm=%d", hechos.run_id, len(resultado.zonas), con_llm)
    return 0


if __name__ == "__main__":
    sys.exit(main())
