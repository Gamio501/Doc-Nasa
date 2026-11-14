# contratos/ — la ley entre servicios y app

**Responsables:** Persona 2 + Persona 3 + Persona 5 (los tres aprueban cada cambio)

JSON Schema versionados (`schema_version`). Se escriben **antes** del código.

- `hechos.schema.json`, `interpretacion.schema.json`, `manifest.schema.json`
- `paquete.schema.md`: tablas SQLite del paquete.
- `formula_puntaje.md`: suma ponderada que hace el teléfono con los deslizadores.

Un cambio que rompe compatibilidad sube la versión mayor y se avisa a todo el equipo.
