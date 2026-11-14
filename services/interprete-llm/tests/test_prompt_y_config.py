"""Tests del prompt y de la configuración."""

from __future__ import annotations

from pathlib import Path

import pytest
from contratos import Zona

from interprete.config import MODELO_POR_DEFECTO, RAIZ_SERVICIO, Config
from interprete.prompt import cargar_sistema, construir_mensaje


def test_el_mensaje_incluye_hechos_y_cobertura_obligatoria(zona: Zona) -> None:
    mensaje = construir_mensaje(zona, "2026-10")
    assert "<hechos>" in mensaje and "</hechos>" in mensaje
    assert "Periodo de los datos: 2026-10." in mensaje
    assert "limon/nov-dic" in mensaje and "mango/nov-dic" in mensaje
    assert "actual, agua, suelo" in mensaje
    assert "ind-humedad_suelo" in mensaje


def test_el_mensaje_es_estable_para_los_mismos_hechos(zona: Zona) -> None:
    assert construir_mensaje(zona, "2026-10") == construir_mensaje(zona, "2026-10")


def test_el_prompt_v1_existe_y_prohibe_inventar_cifras() -> None:
    sistema = cargar_sistema(RAIZ_SERVICIO / "prompts" / "sistema_v1.md")
    assert "No hagas cálculos nuevos" in sistema
    assert "no reemplaza a un experto" in sistema


def test_prompt_vacio_es_error(tmp_path: Path) -> None:
    vacio = tmp_path / "sistema_vacio.md"
    vacio.write_text("   \n", encoding="utf-8")
    with pytest.raises(ValueError, match="vacío"):
        cargar_sistema(vacio)


def test_config_por_defecto_usa_opus_y_prompt_v1() -> None:
    config = Config.desde_entorno({})
    assert config.modelo == MODELO_POR_DEFECTO == "claude-opus-5-5"
    assert config.max_tokens == 16000
    assert config.prompt_path.name == "sistema_v1.md"


def test_config_lee_variables_de_entorno() -> None:
    config = Config.desde_entorno(
        {
            "LLM_MODEL": "claude-haiku-5-5",
            "LLM_MAX_TOKENS": "8000",
            "LLM_TIMEOUT_S": "30",
            "LLM_MAX_RETRIES": "4",
            "PROMPT_VERSION": "v2",
        }
    )
    assert config.modelo == "claude-haiku-5-5"
    assert (config.max_tokens, config.timeout_s, config.max_reintentos) == (8000, 30.0, 4)
    assert config.prompt_path.name == "sistema_v2.md"


@pytest.mark.parametrize(
    "env",
    [{"LLM_MAX_TOKENS": "0"}, {"LLM_TIMEOUT_S": "-1"}, {"LLM_MAX_RETRIES": "-1"}],
)
def test_config_rechaza_valores_invalidos(env: dict[str, str]) -> None:
    with pytest.raises(ValueError):
        Config.desde_entorno(env)
