"""CLI del verificador.

Uso:
    python -m verificador --hechos .../02_calculador/hechos.json \\
        --interpretacion .../03_interprete/interpretacion.json \\
        --salida .../04_verificador/interpretacion_verificada.json \\
        --informe .../04_verificador/informe.md

Códigos de salida: 0 = archivos escritos; 1 = entrada inválida.
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from contratos import Hechos, Interpretaciones
from verificador.informe import renderizar_informe
from verificador.verificar import ErrorEntrada, verificar

log = logging.getLogger("verificador")


def _parsear(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="verificador", description=__doc__)
    parser.add_argument("--hechos", type=Path, required=True)
    parser.add_argument("--interpretacion", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--informe", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Ejecuta la etapa y devuelve el código de salida."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = _parsear(argv)
    try:
        hechos = Hechos.model_validate_json(args.hechos.read_text(encoding="utf-8"))
        entrada = Interpretaciones.model_validate_json(
            args.interpretacion.read_text(encoding="utf-8")
        )
        resultado, filas = verificar(hechos, entrada)
    except (OSError, ValidationError, ErrorEntrada) as exc:
        log.error("entrada inválida: %s", exc)
        return 1

    for ruta in (args.salida, args.informe):
        ruta.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(resultado.model_dump_json(indent=2), encoding="utf-8")
    args.informe.write_text(renderizar_informe(hechos, filas), encoding="utf-8")
    plantillas = sum(f.origen_final.value == "plantilla" for f in filas)
    log.info("run_id=%s zonas=%d plantillas=%d", hechos.run_id, len(filas), plantillas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
