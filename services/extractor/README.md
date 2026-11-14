# services/extractor

**Responsable:** Persona 2

Consulta NASA POWER y Earth Engine (MODIS, SMAP, GPM, SRTM) por celda de la grilla de Piura.

- Entrada: grilla + periodo (`AAAA-MM`) + `run_id`.
- Salida: `runs/<entorno>/<run_id>/01_extractor/crudos.parquet` + `faltantes.json`.
- Cada llamada externa con tiempo de espera y reintentos. `-999` se guarda como vacío, nunca como 0.
