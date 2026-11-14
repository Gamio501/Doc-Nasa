"""Tests del cliente Claude (con un SDK simulado) y de la CLI."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import anthropic
import pytest
from rotacion_contratos import Hechos, Interpretaciones, InterpretacionLLM, Origen, Zona

from interprete.__main__ import main
from interprete.cliente import ClienteClaude, ClienteLLM, RespuestaLLM
from interprete.config import Config
from tests.conftest import EJEMPLO, ClienteFalso, contenido_para, respuesta_http, respuesta_ok


class _MessagesSimulados:
    def __init__(self, respuesta: Any) -> None:
        self.respuesta = respuesta
        self.kwargs: dict[str, Any] = {}

    def parse(self, **kwargs: Any) -> Any:
        self.kwargs = kwargs
        return self.respuesta


def _sdk_simulado(stop_reason: str, parsed: InterpretacionLLM | None) -> Any:
    respuesta = SimpleNamespace(
        stop_reason=stop_reason, parsed_output=parsed, model="claude-opus-5-5", _request_id="req_9"
    )
    return SimpleNamespace(messages=_MessagesSimulados(respuesta))


def test_cliente_claude_envia_sistema_cacheable_y_esquema(zona: Zona) -> None:
    sdk = _sdk_simulado("end_turn", contenido_para(zona))
    cliente = ClienteClaude(Config(modelo="claude-opus-5-5", max_tokens=1234), client=sdk)
    respuesta = cliente.interpretar("SISTEMA", "MENSAJE")
    kwargs = sdk.messages.kwargs
    assert kwargs["model"] == "claude-opus-5-5"
    assert kwargs["max_tokens"] == 1234
    assert kwargs["output_format"] is InterpretacionLLM
    assert kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert kwargs["system"][0]["text"] == "SISTEMA"
    assert kwargs["messages"] == [{"role": "user", "content": "MENSAJE"}]
    assert respuesta.contenido == contenido_para(zona)
    assert respuesta.request_id == "req_9"


@pytest.mark.parametrize("stop_reason", ["refusal", "max_tokens"])
def test_cliente_claude_descarta_respuestas_incompletas(zona: Zona, stop_reason: str) -> None:
    sdk = _sdk_simulado(stop_reason, contenido_para(zona))
    respuesta = ClienteClaude(Config(), client=sdk).interpretar("S", "M")
    assert respuesta.contenido is None
    assert respuesta.stop_reason == stop_reason


def test_cliente_claude_crea_su_sdk_con_timeout_y_reintentos(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-prueba-no-real")
    cliente = ClienteClaude(Config(timeout_s=12.0, max_reintentos=3))
    sdk = cliente._client
    assert isinstance(sdk, anthropic.Anthropic)
    assert sdk.max_retries == 3


def _fabrica(cliente: ClienteLLM) -> Any:
    return lambda _config: cliente


def test_cli_escribe_la_interpretacion(tmp_path: Path, hechos: Hechos) -> None:
    contenido = contenido_para(hechos.zonas[0])
    salida = tmp_path / "03_interprete" / "interpretacion.json"
    codigo = main(
        ["--hechos", str(EJEMPLO), "--salida", str(salida)],
        fabrica=_fabrica(ClienteFalso(lambda _s, _m: respuesta_ok(contenido))),
    )
    assert codigo == 0
    resultado = Interpretaciones.model_validate_json(salida.read_text(encoding="utf-8"))
    assert resultado.zonas[0].origen is Origen.LLM


def test_cli_sin_llm_no_crea_cliente(tmp_path: Path) -> None:
    def fabrica_prohibida(_config: Config) -> ClienteLLM:
        raise AssertionError("no debía crear el cliente")

    salida = tmp_path / "interpretacion.json"
    codigo = main(
        ["--hechos", str(EJEMPLO), "--salida", str(salida), "--sin-llm"], fabrica=fabrica_prohibida
    )
    assert codigo == 0
    datos = json.loads(salida.read_text(encoding="utf-8"))
    assert datos["zonas"][0]["origen"] == "error"


def test_cli_con_hechos_invalidos_devuelve_1(tmp_path: Path) -> None:
    malo = tmp_path / "hechos.json"
    malo.write_text('{"schema_version": "9"}', encoding="utf-8")
    codigo = main(["--hechos", str(malo), "--salida", str(tmp_path / "s.json"), "--sin-llm"])
    assert codigo == 1
    assert not (tmp_path / "s.json").exists()


def test_cli_con_llave_invalida_devuelve_2(tmp_path: Path) -> None:
    def responder(_s: str, _m: str) -> RespuestaLLM:
        raise anthropic.AuthenticationError("llave", response=respuesta_http(401), body=None)

    salida = tmp_path / "s.json"
    codigo = main(
        ["--hechos", str(EJEMPLO), "--salida", str(salida)],
        fabrica=_fabrica(ClienteFalso(responder)),
    )
    assert codigo == 2
    assert not salida.exists()
