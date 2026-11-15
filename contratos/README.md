# contratos/ — la ley entre servicios y app

**Responsables:** Persona 2 + Persona 3 + Persona 5 (los tres aprueban cada cambio)

JSON Schema versionados (`schema_version`). Se escriben **antes** del código.

| Archivo | Estado | Quién lo produce → quién lo usa |
|---|---|---|
| `hechos.schema.json` | v1.0 ✅ | `calculador` → `interprete-llm`, `verificador`, `publicador` |
| `interpretacion_llm.schema.json` | v1.0 ✅ | Lo que el LLM rellena por zona (salida estructurada) |
| `interpretacion.schema.json` | v1.0 ✅ | `interprete-llm` y `verificador` → `publicador` |
| `formula_puntaje.md` | v1.0 ✅ | `calculador` (pesos por defecto) y `app` (deslizadores) |
| `manifest.schema.json` | pendiente | `publicador` → `app` |
| `paquete.schema.md` | pendiente | `publicador` → `app` (tablas SQLite) |
| `ejemplos/hechos_ejemplo.json` | v1.0 ✅ | Datos de ejemplo `[SUPUESTO]` para tests |

## Fuente de verdad

Los modelos Python de `py/rotacion_contratos/` (pydantic) generan los `*.schema.json`. **No editar los JSON a mano**:

```bash
cd contratos/py
pip install -e .              # una vez
python -m rotacion_contratos.exportar  # regenera los *.schema.json
pytest                        # falla si un esquema quedó desactualizado
```

Los servicios Python importan los modelos (`from rotacion_contratos import Hechos`); Flutter genera los suyos desde los `*.schema.json`.

## Reglas

- Un cambio que rompe compatibilidad sube la versión mayor (`2.0`) y se avisa a todo el equipo.
- `-999` de la NASA llega como `null`, nunca como `0`.
- Toda cifra que la app muestra está en `hechos`: el LLM no calcula números.
