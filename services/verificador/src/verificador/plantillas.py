"""Textos de respaldo, generados solo con código a partir de los hechos.

Se usan cuando el LLM no respondió o su texto no pasó la verificación. Deben
pasar las mismas reglas que el LLM (hay un test que lo comprueba).
"""

from __future__ import annotations

from contratos import InterpretacionLLM, Zona
from contratos.hechos import Confianza, Efecto, Escala, Factor, Indicador, Semaforo
from contratos.interpretacion import Evidencia, TextoCultivo, TextoIndicador, TextoRotacion

RIESGO_SIEMPRE = "Revisa esta opción con un técnico o agrónomo de tu zona antes de decidir."
CUIDADO_GENERAL = "Revisa el riego y el estado de tus plantas cada semana."


def formatear(valor: float) -> str:
    """Número en formato peruano: enteros desde 10, dos decimales por debajo."""
    if abs(valor) >= 10:
        return str(round(valor))
    return f"{valor:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def plantilla(zona: Zona, periodo: str) -> InterpretacionLLM:
    """Interpretación completa de una zona sin LLM."""
    return InterpretacionLLM(
        resumen_zona=_resumen(zona),
        indicadores=[_texto_indicador(i, periodo) for i in zona.indicadores],
        cultivos=[
            TextoCultivo(
                cultivo_id=a.cultivo_id,
                temporada=a.temporada,
                por_que=(
                    f"Para {a.temporada}, el {a.cultivo_nombre} tiene aptitud {a.nivel.value} "
                    f"en tu zona ({formatear(a.puntaje)} de 100)."
                ),
                a_favor=_descripciones(a.factores, Efecto.A_FAVOR),
                en_contra=_descripciones(a.factores, Efecto.EN_CONTRA),
                cuidados=[f"Cuida esto: {d}" for d in _descripciones(a.factores, Efecto.EN_CONTRA)]
                or [CUIDADO_GENERAL],
                evidencia=_evidencia(a.factores),
            )
            for a in zona.aptitud_cultivos
        ],
        rotaciones=[
            TextoRotacion(
                rotacion_id=r.rotacion_id,
                por_que=(
                    f"{r.nombre}: {formatear(r.puntaje)} de 100."
                    + (" Es la que usas hoy." if r.es_actual else "")
                ),
                evidencia=_evidencia(r.factores),
                beneficios=_descripciones(r.factores, Efecto.A_FAVOR),
                lagunas=_lagunas(zona, r.confianza),
                riesgos_validar_experto=[
                    *_descripciones(r.factores, Efecto.EN_CONTRA),
                    RIESGO_SIEMPRE,
                ],
            )
            for r in zona.rotaciones
        ],
    )


def _resumen(zona: Zona) -> str:
    rojos = [i.nombre for i in zona.indicadores if i.semaforo is Semaforo.ROJO]
    texto = (
        f"Atención en tu zona: {', '.join(rojos)} en rojo este mes."
        if rojos
        else "Este mes no hay alertas rojas en tu zona."
    )
    if any(i.valor is None for i in zona.indicadores):
        texto += " Algunos datos faltan."
    return texto


def _texto_indicador(ind: Indicador, periodo: str) -> TextoIndicador:
    donde = " (dato de tu zona)" if ind.escala is Escala.ZONA else ""
    if ind.valor is None:
        texto = f"{ind.nombre.capitalize()}: sin dato este mes{donde}."
    else:
        texto = f"{ind.nombre.capitalize()}: {formatear(ind.valor)} {ind.unidad} en {periodo}"
        if ind.diferencia_pct is not None and ind.diferencia_pct != 0:
            sentido = "más" if ind.diferencia_pct > 0 else "menos"
            texto += f", {formatear(abs(ind.diferencia_pct))} % {sentido} que lo normal"
        texto += f"{donde}."
    return TextoIndicador(indicador_id=ind.id, texto=texto)


def _descripciones(factores: list[Factor], efecto: Efecto) -> list[str]:
    return [f.descripcion for f in factores if f.efecto is efecto]


def _evidencia(factores: list[Factor]) -> list[Evidencia]:
    vistas: dict[str, str] = {}
    for factor in factores:
        for ind_id in factor.indicador_ids:
            vistas.setdefault(ind_id, factor.descripcion)
    return [Evidencia(indicador_id=i, frase=f) for i, f in vistas.items()]


def _lagunas(zona: Zona, confianza: Confianza) -> list[str]:
    lagunas = list(zona.lagunas)
    lagunas += [
        f"Falta el dato de {i.nombre} este mes." for i in zona.indicadores if i.valor is None
    ]
    if confianza is Confianza.BAJA:
        lagunas.append("Esta recomendación es poco segura: hay pocos datos.")
    return lagunas
