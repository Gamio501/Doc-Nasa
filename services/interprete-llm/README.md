# services/interprete-llm

**Responsable:** Persona 5

Convierte `hechos.json` en textos simples por zona con la Claude API y salida JSON estructurada.

- `prompts/`: prompt de sistema versionado (`sistema_v1.md`, `sistema_v2.md`…).
- `plantillas/`: textos de respaldo si el LLM falla.
- `evals/`: casos de prueba revisados por el agrónomo.
- Regla: el LLM solo usa cifras de la entrada y cita el indicador. Nunca inventa datos.
