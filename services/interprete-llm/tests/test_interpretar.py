"""Tests de la interpretación por zona y de la clasificación de fallas."""

from __future__ import annotations

import anthropic
import pytest
from pydantic import ValidationError
from rotacion_contratos import Hechos, InterpretacionLLM, Origen, Zona

from interprete.cliente import RespuestaLLM
from interprete.interpretar import (
    MOTIVO_SIN_LLM,
    ErrorConfiguracionLLM,
    interpretar_hechos,
    interpretar_zona,
)
from tests.conftest import PETICION, ClienteFalso, contenido_para, respuesta_http, respuesta_ok


def _que_lanza(exc: Exception) -> ClienteFalso:
    def responder(_sistema: str, _mensaje: str) -> RespuestaLLM:
        raise exc

    return ClienteFalso(responder)


def test_zona_interpretada_por_el_llm(zona: Zona) -> None:
    contenido = contenido_para(zona)
    cliente = ClienteFalso(lambda _s, _m: respuesta_ok(contenido))
    resultado = interpretar_zona(zona, cliente, "sistema", "2026-10")
    assert resultado.origen is Origen.LLM
    assert resultado.contenido == contenido
    assert (resultado.modelo, resultado.request_id) == ("claude-opus-5-5", "req_1")
    sistema, mensaje = cliente.llamadas[0]
    assert sistema == "sistema" and zona.zona_id in mensaje


@pytest.mark.parametrize("stop_reason", ["refusal", "max_tokens"])
def test_respuesta_sin_contenido_queda_como_error(zona: Zona, stop_reason: str) -> None:
    cliente = ClienteFalso(
        lambda _s, _m: RespuestaLLM(None, stop_reason, "claude-opus-5-5", "req_2")
    )
    resultado = interpretar_zona(zona, cliente, "sistema", "2026-10")
    assert resultado.origen is Origen.ERROR
    assert resultado.contenido is None
    assert stop_reason in (resultado.error or "")
    assert resultado.request_id == "req_2"


@pytest.mark.parametrize(
    ("exc", "texto"),
    [
        (anthropic.RateLimitError("x", response=respuesta_http(429), body=None), "429"),
        (anthropic.InternalServerError("x", response=respuesta_http(500), body=None), "500"),
        (anthropic.BadRequestError("muy largo", response=respuesta_http(400), body=None), "400"),
        (anthropic.APIConnectionError(request=PETICION), "sin conexión"),
        (anthropic.APITimeoutError(request=PETICION), "sin conexión"),
    ],
)
def test_fallas_de_una_zona_no_detienen_la_corrida(zona: Zona, exc: Exception, texto: str) -> None:
    resultado = interpretar_zona(zona, _que_lanza(exc), "sistema", "2026-10")
    assert resultado.origen is Origen.ERROR
    assert texto in (resultado.error or "")


def test_respuesta_fuera_de_esquema_queda_como_error(zona: Zona) -> None:
    try:
        InterpretacionLLM.model_validate({"resumen_zona": 1})
    except ValidationError as exc:
        error = exc
    resultado = interpretar_zona(zona, _que_lanza(error), "sistema", "2026-10")
    assert resultado.origen is Origen.ERROR
    assert "fuera del esquema" in (resultado.error or "")


@pytest.mark.parametrize(
    "exc",
    [
        anthropic.AuthenticationError("llave", response=respuesta_http(401), body=None),
        anthropic.PermissionDeniedError("permiso", response=respuesta_http(403), body=None),
        anthropic.NotFoundError("modelo", response=respuesta_http(404), body=None),
    ],
)
def test_errores_de_configuracion_detienen_la_corrida(zona: Zona, exc: Exception) -> None:
    with pytest.raises(ErrorConfiguracionLLM):
        interpretar_zona(zona, _que_lanza(exc), "sistema", "2026-10")


def test_interpretar_hechos_recorre_todas_las_zonas(hechos: Hechos) -> None:
    contenido = contenido_para(hechos.zonas[0])
    cliente = ClienteFalso(lambda _s, _m: respuesta_ok(contenido))
    resultado = interpretar_hechos(hechos, cliente, "sistema")
    assert resultado.run_id == hechos.run_id
    assert resultado.verificada is False
    assert [z.zona_id for z in resultado.zonas] == [z.zona_id for z in hechos.zonas]
    assert len(cliente.llamadas) == len(hechos.zonas)


def test_sin_llm_no_llama_a_la_api(hechos: Hechos) -> None:
    resultado = interpretar_hechos(hechos, None, "sistema")
    assert all(z.origen is Origen.ERROR for z in resultado.zonas)
    assert all(z.error == MOTIVO_SIN_LLM for z in resultado.zonas)
