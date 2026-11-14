"""Tests de las reglas de revisión y de las plantillas."""

from __future__ import annotations

from contratos import InterpretacionLLM, Zona
from contratos.interpretacion import Evidencia
from tests.conftest import contenido_bueno
from verificador.plantillas import RIESGO_SIEMPRE, formatear, plantilla
from verificador.revisar import Problema, Severidad, revisar


def _bloqueantes(problemas: list[Problema]) -> list[str]:
    return [p.mensaje for p in problemas if p.severidad is Severidad.BLOQUEANTE]


def _con(contenido: InterpretacionLLM, **cambios: object) -> InterpretacionLLM:
    return contenido.model_copy(update=cambios)


def test_texto_correcto_no_tiene_problemas(zona: Zona) -> None:
    assert revisar(zona, contenido_bueno(zona), "2026-10") == []


def test_bloquea_cifra_inventada(zona: Zona) -> None:
    contenido = _con(contenido_bueno(zona), resumen_zona="Riega 45 litros por planta.")
    bloqueantes = _bloqueantes(revisar(zona, contenido, "2026-10"))
    assert any("resumen_zona" in m and "45.0" in m for m in bloqueantes)


def test_bloquea_cultivo_faltante_y_rotacion_inventada(zona: Zona) -> None:
    bueno = contenido_bueno(zona)
    rotacion_extra = bueno.rotaciones[0].model_copy(update={"rotacion_id": "inventada"})
    contenido = _con(
        bueno, cultivos=bueno.cultivos[:1], rotaciones=[*bueno.rotaciones, rotacion_extra]
    )
    bloqueantes = _bloqueantes(revisar(zona, contenido, "2026-10"))
    assert any("cultivos sin texto" in m and "mango" in m for m in bloqueantes)
    assert any("rotaciones que no existen" in m and "inventada" in m for m in bloqueantes)


def test_bloquea_indicadores_repetidos(zona: Zona) -> None:
    bueno = contenido_bueno(zona)
    contenido = _con(bueno, indicadores=[*bueno.indicadores, bueno.indicadores[0]])
    assert any("repetidos" in m for m in _bloqueantes(revisar(zona, contenido, "2026-10")))


def test_bloquea_evidencia_inexistente(zona: Zona) -> None:
    bueno = contenido_bueno(zona)
    cultivo = bueno.cultivos[0].model_copy(
        update={"evidencia": [Evidencia(indicador_id="ind-no_existe", frase="x")]}
    )
    contenido = _con(bueno, cultivos=[cultivo, *bueno.cultivos[1:]])
    assert any("ind-no_existe" in m for m in _bloqueantes(revisar(zona, contenido, "2026-10")))


def test_bloquea_lenguaje_de_certeza(zona: Zona) -> None:
    contenido = _con(contenido_bueno(zona), resumen_zona="El limón te garantiza buena cosecha.")
    assert any("certeza" in m for m in _bloqueantes(revisar(zona, contenido, "2026-10")))


def test_bloquea_rotacion_sin_riesgo_para_el_experto(zona: Zona) -> None:
    bueno = contenido_bueno(zona)
    sin_riesgo = bueno.rotaciones[0].model_copy(update={"riesgos_validar_experto": []})
    contenido = _con(bueno, rotaciones=[sin_riesgo, *bueno.rotaciones[1:]])
    assert any("sin riesgos" in m for m in _bloqueantes(revisar(zona, contenido, "2026-10")))


def test_bloquea_texto_vacio(zona: Zona) -> None:
    contenido = _con(contenido_bueno(zona), resumen_zona="  ")
    assert any("texto vacío" in m for m in _bloqueantes(revisar(zona, contenido, "2026-10")))


def test_avisa_jerga_y_textos_largos_sin_bloquear(zona: Zona) -> None:
    contenido = _con(contenido_bueno(zona), resumen_zona="El NDVI bajó. " + "Mucho calor. " * 30)
    problemas = revisar(zona, contenido, "2026-10")
    assert _bloqueantes(problemas) == []
    avisos = [p.mensaje for p in problemas]
    assert any("NDVI" in m for m in avisos)
    assert any("largo" in m for m in avisos)


def test_avisa_si_hay_huecos_y_ninguna_rotacion_los_menciona(zona: Zona) -> None:
    bueno = contenido_bueno(zona)
    rotaciones = [r.model_copy(update={"lagunas": []}) for r in bueno.rotaciones]
    problemas = revisar(zona, _con(bueno, rotaciones=rotaciones), "2026-10")
    assert _bloqueantes(problemas) == []
    assert any("lagunas" in p.mensaje for p in problemas)


def test_la_plantilla_pasa_las_mismas_reglas_que_el_llm(zona: Zona) -> None:
    contenido = plantilla(zona, "2026-10")
    assert _bloqueantes(revisar(zona, contenido, "2026-10")) == []
    assert len(contenido.cultivos) == len(zona.aptitud_cultivos)
    assert len(contenido.rotaciones) == len(zona.rotaciones)


def test_la_plantilla_usa_cifras_reales_y_avisa_datos_faltantes(zona: Zona) -> None:
    contenido = plantilla(zona, "2026-10")
    textos = {t.indicador_id: t.texto for t in contenido.indicadores}
    assert textos["ind-lluvia_mes"] == (
        "Lluvia del mes: 2 mm en 2026-10, 60 % menos que lo normal (dato de tu zona)."
    )
    assert "sin dato este mes" in textos["ind-vegetacion"]
    assert "en rojo" in contenido.resumen_zona and "Algunos datos faltan" in contenido.resumen_zona
    actual = next(r for r in contenido.rotaciones if r.rotacion_id == "actual")
    assert "Es la que usas hoy." in actual.por_que
    assert actual.riesgos_validar_experto[-1] == RIESGO_SIEMPRE
    poco_segura = next(r for r in contenido.rotaciones if r.rotacion_id == "agua")
    assert any("poco segura" in t for t in poco_segura.lagunas)


def test_formatear_numeros() -> None:
    assert (formatear(33.4), formatear(0.12), formatear(2.0), formatear(7.1)) == (
        "33",
        "0,12",
        "2",
        "7,1",
    )
