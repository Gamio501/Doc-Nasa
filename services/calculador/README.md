# services/calculador

**Responsables:** Persona 2 (código) + Persona 4 (reglas)

Calcula indicadores, semáforo, subpuntajes por criterio, aptitud por cultivo y temporada, y puntaje de rotaciones con las reglas de `agronomia/`.

- Salida: `runs/<entorno>/<run_id>/02_calculador/hechos.json` según `contratos/hechos.schema.json`.
- Los puntajes los decide este servicio, **no el LLM**.
