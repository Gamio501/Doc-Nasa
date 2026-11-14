# services/interprete-llm

**Responsable:** Persona 5

Convierte `hechos.json` en textos simples por zona con la Claude API y **salida estructurada** (`InterpretacionLLM` de `contratos/`). El LLM **solo explica** cifras ya calculadas: no decide puntajes ni inventa datos.

## Uso

```bash
# Desde la raíz del repo, con el entorno virtual activo
pip install -r services/interprete-llm/requirements.txt   # una vez (desde la carpeta del servicio)
export ANTHROPIC_API_KEY=...                               # nunca en el código ni en git

python -m interprete \
  --hechos runs/dev/<run_id>/02_calculador/hechos.json \
  --salida runs/dev/<run_id>/03_interprete/interpretacion.json

# Sin LLM (todas las zonas quedan para plantilla del verificador):
python -m interprete --hechos ... --salida ... --sin-llm
```

| Código de salida | Significado | Qué hace el orquestador |
|---|---|---|
| `0` | Archivo escrito (algunas zonas pueden tener `origen: error`) | Sigue con el verificador |
| `1` | `hechos.json` inválido o prompt inexistente | Detiene la corrida |
| `2` | Llave inválida, sin permisos o modelo inexistente | Detiene la corrida; avisar a Persona 5 |

## Variables de entorno

| Variable | Por defecto | Para qué |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Llave de la Claude API (secreto del entorno de GitHub) |
| `LLM_MODEL` | `claude-opus-5-5` | Modelo |
| `LLM_MAX_TOKENS` | `16000` | Tope de salida por zona |
| `LLM_TIMEOUT_S` | `120` | Tiempo máximo por llamada |
| `LLM_MAX_RETRIES` | `2` | Reintentos del SDK (429, 5xx, red) |
| `PROMPT_VERSION` | `v1` | Usa `prompts/sistema_<versión>.md` |

## Cómo está hecho

- `prompts/sistema_v1.md`: reglas para el LLM (solo cifras de los hechos, cobertura exacta, español sencillo, sin certezas). Un cambio de reglas = archivo nuevo `sistema_v2.md`, no se edita el anterior.
- `cliente.py`: `messages.parse(output_format=InterpretacionLLM)` con el prompt de sistema cacheable (`cache_control`).
- `interpretar.py`: una llamada por zona. Fallas de una zona (red, 429, 5xx, 400, refusal, respuesta cortada o fuera del esquema) → `origen: error`. Fallas de configuración (401, 403, 404) → detienen la corrida.
- `evals/`: casos de prueba revisados por el agrónomo (pendiente).

## Tests

```bash
cd services/interprete-llm
pytest --cov      # no llaman a la API: usan un cliente falso
ruff check . && mypy src tests
```
