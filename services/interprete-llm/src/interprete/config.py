"""Configuración del intérprete, leída de variables de entorno."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

RAIZ_SERVICIO = Path(__file__).resolve().parents[2]
MODELO_POR_DEFECTO = "claude-opus-5-5"


@dataclass(frozen=True)
class Config:
    """Parámetros del intérprete LLM.

    Attributes:
        modelo: Id del modelo de Claude.
        max_tokens: Tope de tokens de salida por zona.
        timeout_s: Tiempo máximo por llamada, en segundos.
        max_reintentos: Reintentos automáticos del SDK (429, 5xx, red).
        prompt_path: Archivo del prompt de sistema versionado.
    """

    modelo: str = MODELO_POR_DEFECTO
    max_tokens: int = 16000
    timeout_s: float = 120.0
    max_reintentos: int = 2
    prompt_path: Path = RAIZ_SERVICIO / "prompts" / "sistema_v1.md"

    def __post_init__(self) -> None:
        if self.max_tokens <= 0:
            raise ValueError(f"LLM_MAX_TOKENS debe ser positivo: {self.max_tokens}")
        if self.timeout_s <= 0:
            raise ValueError(f"LLM_TIMEOUT_S debe ser positivo: {self.timeout_s}")
        if self.max_reintentos < 0:
            raise ValueError(f"LLM_MAX_RETRIES no puede ser negativo: {self.max_reintentos}")

    @classmethod
    def desde_entorno(cls, env: Mapping[str, str]) -> Config:
        """Construye la configuración desde un diccionario de variables de entorno.

        Args:
            env: Normalmente `os.environ`.

        Returns:
            Configuración validada.

        Raises:
            ValueError: Si un valor numérico no es válido.
        """
        version = env.get("PROMPT_VERSION", "v1")
        return cls(
            modelo=env.get("LLM_MODEL") or MODELO_POR_DEFECTO,
            max_tokens=int(env.get("LLM_MAX_TOKENS", "16000")),
            timeout_s=float(env.get("LLM_TIMEOUT_S", "120")),
            max_reintentos=int(env.get("LLM_MAX_RETRIES", "2")),
            prompt_path=RAIZ_SERVICIO / "prompts" / f"sistema_{version}.md",
        )
