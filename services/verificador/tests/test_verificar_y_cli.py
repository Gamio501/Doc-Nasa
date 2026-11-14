"""Tests del flujo completo del verificador, del informe y de la CLI."""

from __future__ import annotations

from pathlib import Path

import pytest

from contratos import Hechos, Interpretaciones, InterpretacionZona, Origen
from tests.conftest import EJEMPLO, contenido_bueno, interpretaciones_con, zona_llm
from verificador.__main__ import main
from verificador.informe import renderizar_informe
from verificador.verificar import ErrorEntrada, verificar


def test_aprueba_texto_del_llm_que_pasa(hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    resultado, filas = verificar(
        hechos, interpretaciones_con(hechos, zona_llm(zona, contenido_bueno(zona)))
    )
    assert resultado.verificada is True
    final = resultado.zonas[0]
    assert final.origen is Origen.LLM
    assert final.contenido == contenido_bueno(zona)
    assert filas[0].motivo == "aprobada"


def test_cifra_inventada_pasa_a_plantilla(hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    malo = contenido_bueno(zona).model_copy(update={"resumen_zona": "Riega 45 litros."})
    resultado, filas = verificar(hechos, interpretaciones_con(hechos, zona_llm(zona, malo)))
    final = resultado.zonas[0]
    assert final.origen is Origen.PLANTILLA
    assert final.contenido is not None and final.contenido != malo
    assert final.request_id == "req_1"
    assert any("45.0" in p for p in final.problemas)
    assert filas[0].motivo == "no pasó la verificación"


def test_zona_con_error_del_llm_pasa_a_plantilla(hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    error = InterpretacionZona(zona_id=zona.zona_id, origen=Origen.ERROR, error="sin red")
    resultado, filas = verificar(hechos, interpretaciones_con(hechos, error))
    assert resultado.zonas[0].origen is Origen.PLANTILLA
    assert filas[0].motivo == "sin LLM: sin red"


def test_zona_ausente_recibe_plantilla(hechos: Hechos) -> None:
    resultado, filas = verificar(hechos, interpretaciones_con(hechos))
    assert resultado.zonas[0].origen is Origen.PLANTILLA
    assert filas[0].motivo == "sin interpretación"


def test_aprobada_con_avisos_conserva_el_texto(hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    con_jerga = contenido_bueno(zona).model_copy(update={"resumen_zona": "El NDVI bajó."})
    resultado, filas = verificar(hechos, interpretaciones_con(hechos, zona_llm(zona, con_jerga)))
    assert resultado.zonas[0].origen is Origen.LLM
    assert filas[0].motivo == "aprobada con avisos"
    assert any("NDVI" in p for p in resultado.zonas[0].problemas)


def test_rechaza_run_id_distinto(hechos: Hechos) -> None:
    otra = interpretaciones_con(hechos).model_copy(update={"run_id": "2026-10-otro01"})
    with pytest.raises(ErrorEntrada, match="run_id distinto"):
        verificar(hechos, otra)


def test_rechaza_zonas_que_no_estan_en_los_hechos(hechos: Hechos) -> None:
    ajena = InterpretacionZona(zona_id="PIU-XXX-99", origen=Origen.ERROR, error="x")
    with pytest.raises(ErrorEntrada, match="PIU-XXX-99"):
        verificar(hechos, interpretaciones_con(hechos, ajena))


def test_informe_alerta_si_mas_de_la_mitad_queda_con_plantilla(hechos: Hechos) -> None:
    _, filas = verificar(hechos, interpretaciones_con(hechos))
    informe = renderizar_informe(hechos, filas)
    assert f"`{hechos.run_id}`" in informe
    assert "con plantilla: 1" in informe
    assert "Más de la mitad" in informe
    assert "| PIU-SUL-01 | plantilla | sin interpretación |" in informe


def test_informe_sin_alertas(hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    _, filas = verificar(
        hechos, interpretaciones_con(hechos, zona_llm(zona, contenido_bueno(zona)))
    )
    assert "✅ Sin alertas." in renderizar_informe(hechos, filas)


def test_cli_escribe_interpretacion_verificada_e_informe(tmp_path: Path, hechos: Hechos) -> None:
    zona = hechos.zonas[0]
    entrada = tmp_path / "interpretacion.json"
    entrada.write_text(
        interpretaciones_con(hechos, zona_llm(zona, contenido_bueno(zona))).model_dump_json(),
        encoding="utf-8",
    )
    salida = tmp_path / "04" / "interpretacion_verificada.json"
    informe = tmp_path / "04" / "informe.md"
    codigo = main(
        [
            "--hechos", str(EJEMPLO),
            "--interpretacion", str(entrada),
            "--salida", str(salida),
            "--informe", str(informe),
        ]
    )  # fmt: skip
    assert codigo == 0
    verificada = Interpretaciones.model_validate_json(salida.read_text(encoding="utf-8"))
    assert verificada.verificada is True
    assert "Informe de verificación" in informe.read_text(encoding="utf-8")


def test_cli_con_entrada_invalida_devuelve_1(tmp_path: Path) -> None:
    codigo = main(
        [
            "--hechos", str(EJEMPLO),
            "--interpretacion", str(tmp_path / "no_existe.json"),
            "--salida", str(tmp_path / "s.json"),
            "--informe", str(tmp_path / "i.md"),
        ]
    )  # fmt: skip
    assert codigo == 1
