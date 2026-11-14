# services/verificador

**Responsable:** Persona 5

Revisa la interpretación del LLM de cada zona contra los `hechos`. Lo que pasa se publica; lo que no pasa se reemplaza por una **plantilla generada por código**. Escribe `informe.md` para la **revisión humana** antes de producción.

## Uso

```bash
python -m verificador \
  --hechos runs/dev/<run_id>/02_calculador/hechos.json \
  --interpretacion runs/dev/<run_id>/03_interprete/interpretacion.json \
  --salida runs/dev/<run_id>/04_verificador/interpretacion_verificada.json \
  --informe runs/dev/<run_id>/04_verificador/informe.md
```

Códigos de salida: `0` = archivos escritos; `1` = entrada inválida (incluye `run_id` distinto entre archivos) → el orquestador detiene la corrida.

## Reglas

| Regla | Si falla |
|---|---|
| Un texto por cada indicador, cada (cultivo, temporada) y cada rotación; sin repetidos ni inventados | Plantilla |
| La evidencia solo cita indicadores de la zona | Plantilla |
| Toda cifra del texto existe en los hechos (redondeo tolerado; subpuntajes no cuentan) | Plantilla |
| Sin lenguaje de certeza ("garantiza", "sin duda", "siempre", "100 %") | Plantilla |
| Cada rotación tiene al menos un riesgo para revisar con un experto | Plantilla |
| Sin textos vacíos | Plantilla |
| Jerga técnica (NDVI, evapotranspiración, anomalía) | Aviso en el informe |
| Textos largos; datos faltantes que ninguna rotación menciona | Aviso en el informe |

La plantilla pasa las mismas reglas (hay un test que lo comprueba). El informe avisa si más de la mitad de las zonas quedó con plantilla.

## Tests

```bash
cd services/verificador
pytest --cov
ruff check . && mypy src tests
```
