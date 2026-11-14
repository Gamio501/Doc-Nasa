"""Une hechos e interpretación: aprueba lo que pasa, pone plantilla a lo demás."""

from __future__ import annotations

from dataclasses import dataclass

from contratos import Hechos, Interpretaciones, InterpretacionZona, Origen, Zona
from verificador.plantillas import plantilla
from verificador.revisar import Severidad, revisar


class ErrorEntrada(ValueError):
    """Los archivos de entrada no corresponden a la misma corrida."""


@dataclass(frozen=True)
class FilaInforme:
    zona_id: str
    origen_final: Origen
    motivo: str
    problemas: tuple[str, ...]


def verificar(
    hechos: Hechos, interpretaciones: Interpretaciones
) -> tuple[Interpretaciones, list[FilaInforme]]:
    """Verifica cada zona y devuelve la interpretación final y las filas del informe.

    Raises:
        ErrorEntrada: Si `run_id` no coincide o hay zonas que no están en los hechos.
    """
    if interpretaciones.run_id != hechos.run_id:
        raise ErrorEntrada(
            f"run_id distinto: hechos={hechos.run_id} interpretacion={interpretaciones.run_id}"
        )
    por_zona = {z.zona_id: z for z in interpretaciones.zonas}
    sobrantes = set(por_zona) - {z.zona_id for z in hechos.zonas}
    if sobrantes:
        raise ErrorEntrada(f"zonas que no están en los hechos: {sorted(sobrantes)}")

    zonas: list[InterpretacionZona] = []
    filas: list[FilaInforme] = []
    for zona in hechos.zonas:
        final, fila = _verificar_zona(zona, por_zona.get(zona.zona_id), hechos.periodo)
        zonas.append(final)
        filas.append(fila)
    resultado = Interpretaciones(
        schema_version="1.0",
        run_id=hechos.run_id,
        entorno=hechos.entorno,
        verificada=True,
        zonas=zonas,
    )
    return resultado, filas


def _verificar_zona(
    zona: Zona, entrada: InterpretacionZona | None, periodo: str
) -> tuple[InterpretacionZona, FilaInforme]:
    if entrada is None or entrada.contenido is None:
        motivo = "sin interpretación" if entrada is None else f"sin LLM: {entrada.error}"
        return _con_plantilla(zona, entrada, periodo, motivo, [])

    problemas = revisar(zona, entrada.contenido, periodo)
    textos = [str(p) for p in problemas]
    if any(p.severidad is Severidad.BLOQUEANTE for p in problemas):
        return _con_plantilla(zona, entrada, periodo, "no pasó la verificación", textos)

    aprobada = entrada.model_copy(update={"problemas": textos, "error": None})
    motivo = "aprobada" if not textos else "aprobada con avisos"
    return aprobada, FilaInforme(zona.zona_id, Origen.LLM, motivo, tuple(textos))


def _con_plantilla(
    zona: Zona,
    entrada: InterpretacionZona | None,
    periodo: str,
    motivo: str,
    problemas: list[str],
) -> tuple[InterpretacionZona, FilaInforme]:
    final = InterpretacionZona(
        zona_id=zona.zona_id,
        origen=Origen.PLANTILLA,
        modelo=entrada.modelo if entrada else None,
        request_id=entrada.request_id if entrada else None,
        contenido=plantilla(zona, periodo),
        error=motivo,
        problemas=problemas,
    )
    return final, FilaInforme(zona.zona_id, Origen.PLANTILLA, motivo, tuple(problemas))
