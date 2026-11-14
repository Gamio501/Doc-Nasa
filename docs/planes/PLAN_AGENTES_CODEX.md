# PLAN_AGENTES_CODEX.md — Plan de acción del sistema de agentes (para Codex)

> **Para:** Codex (y la persona que lo guía: Persona 2, datos geoespaciales).
> **Qué construye:** la parte "agéntica" del pipeline mensual: grilla y zonas, extracción de datos NASA, control de calidad, calculador, publicador, orquestador y workflows.
> **Qué NO construye:** el intérprete LLM y el verificador (ya hechos en `services/interprete-llm` y `services/verificador`, Persona 5), la app Flutter (Persona 3) ni el contenido agronómico (Persona 4).
> Creado el 2026-11-14. Si algo de este plan choca con `AGENTS.md`, manda `AGENTS.md`.

---

## 0. Cómo usar este plan

1. Codex trabaja **una tarea por sesión y por rama** (sección 7), en el orden de la sección 8.
2. Al empezar cada sesión se le pega el prompt de la sección 11, con el número de tarea.
3. Al terminar cada tarea, Codex abre un Pull Request hacia `develop` y entrega el informe de `REGLAS_GIT.md` (Paso 9). **Una persona revisa y fusiona.**

## 1. Lectura obligatoria antes de cada tarea

| Archivo | Para qué |
|---|---|
| `AGENTS.md` | Reglas del proyecto (no inventar datos, `[SUPUESTO]`, lenguaje simple) |
| `REGLAS_GIT.md` | Flujo obligatorio de ramas, commits, push y Pull Requests |
| `ARQUITECTURA.md` | Servicios, carpetas, dueños y entornos |
| `IDEA.md` | Qué hace la app y por qué los datos son mensuales |
| `contratos/README.md` y `contratos/py/rotacion_contratos/hechos.py` | **El contrato que el calculador debe producir** |
| `services/interprete-llm/README.md`, `services/verificador/README.md` | Cómo llamar a las etapas LLM desde el orquestador |
| `PRACTICANDO/lib/nasaClient.ts` y `PRACTICANDO/AGENTS.md` | Lo que ya aprendimos de NASA POWER (ver §5.3) |

## 2. Reglas para Codex

### 2.1 Alcance

- ✅ Puede crear y editar: `orquestador/`, `services/extractor/`, `services/calculador/`, `services/publicador/`, `infra/`, `.github/workflows/`, y los archivos de **formato** de `agronomia/` (esquema y ejemplos marcados `[SUPUESTO]`).
- ⚠️ Solo por Pull Request aparte, con aprobación de Persona 2, 3 y 5: cualquier cambio en `contratos/`.
- 🚫 No toca: `services/interprete-llm/`, `services/verificador/`, `app/`, `PRACTICANDO/`, `AGENTS.md`, `IDEA.md`, ni el **contenido** agronómico (valores reales de cultivos y umbrales: los define Persona 4).

### 2.2 Código

- Python 3.12. Misma estructura que `services/interprete-llm`: `pyproject.toml`, `requirements.txt` (con `-e ../../contratos/py`), `src/<paquete>/`, `tests/`, `README.md`.
- Tipos en todas las funciones; `mypy --strict` sin errores; `ruff check` y `ruff format` limpios; docstrings estilo Google.
- Nombres de dominio en español, iguales a los contratos (`zona_id`, `celdas`, `indicador`); comentarios en español.
- Modelos inmutables (`frozen=True`); nada de estado global mutable.
- `logging` con el `run_id` en cada mensaje; nunca `print` (salvo la salida de una CLI).
- Configuración por variables de entorno (`infra/config/<entorno>.example.env`); nada fijo en el código.

### 2.3 Datos

- **Nunca inventar cifras.** Todo valor sale de un dataset; si un dato falta, se guarda `None` y se registra en `lagunas`. Los valores de ejemplo se marcan `[SUPUESTO]`.
- `-999` (y cualquier "fill value" de la NASA) → `None`, nunca `0`.
- Nombres de datasets, colecciones y parámetros: **verificarlos** en la documentación oficial antes de usarlos. Los marcados `[VERIFICAR]` en este plan no están confirmados.
- Salidas **deterministas**: JSON con claves ordenadas, listas ordenadas por id. Misma entrada → mismo archivo.
- Cada etapa escribe **solo** en su carpeta de la corrida (§6) y valida su salida contra el contrato **antes** de escribirla.
- Nunca subir datos a git (`runs/` está en `.gitignore`).

### 2.4 Llamadas externas

- Cada llamada con **tiempo de espera** explícito (30 s por defecto) y **reintentos con espera creciente** (3 intentos) solo para 429, 5xx y errores de red.
- Concurrencia baja (máximo 2 peticiones simultáneas a NASA POWER) y caché local por petición, para no saturar los servicios de la NASA.
- **Los tests nunca llaman a la red.** Las fuentes externas van detrás de una interfaz (`Protocol`) y en los tests se usa una implementación falsa o respuestas grabadas en `tests/fixtures/`.

### 2.5 Secretos

- Credenciales solo por variables de entorno: `EARTHDATA_TOKEN`, `GEE_PROJECT`, `GEE_SERVICE_ACCOUNT_FILE`, `ANTHROPIC_API_KEY`. Nunca en el código, en logs ni en git.
- En GitHub Actions, los secretos viven en los entornos `desarrollo` y `produccion`.

### 2.6 Git (resumen de `REGLAS_GIT.md`)

- Rama por tarea desde `develop` actualizado (nombre en §7). Commits `tipo(área): descripción`.
- `git add` solo de los archivos de la tarea; revisar `git diff --staged`.
- Antes del push: tests, `ruff`, `mypy` y `git rebase origin/develop`.
- Pull Request hacia `develop`. **Codex nunca aprueba ni fusiona.**

### 2.7 Cuándo detenerse y preguntar

- Hace falta cambiar un contrato.
- No se puede verificar el nombre de un dataset o parámetro.
- Hacen falta credenciales que no están.
- Una regla agronómica es ambigua o falta un valor (preguntar a Persona 4; mientras tanto, `[SUPUESTO]`).
- Un test solo pasaría llamando a la red.

## 3. Lo que ya existe (no rehacer)

| Pieza | Dónde | Qué ofrece |
|---|---|---|
| Contrato `hechos` v1 | `contratos/py/rotacion_contratos/hechos.py` | `Hechos`, `Zona`, `Indicador`, `AptitudCultivo`, `Rotacion`, `Factor`, `Subpuntajes` con validaciones |
| Ejemplo válido | `contratos/ejemplos/hechos_ejemplo.json` | Una zona completa `[SUPUESTO]` |
| Fórmula de puntaje | `contratos/formula_puntaje.md` | Pesos por defecto que el calculador debe usar |
| Intérprete LLM | `python -m interprete` | Ver códigos de salida en §6.2 |
| Verificador | `python -m verificador` | Ver códigos de salida en §6.2 |

Instalar el entorno (una vez, desde la raíz):

```bash
# Desde la raíz del repo (en Linux/macOS: .venv/bin/python)
python -m venv .venv
.venv/Scripts/python -m pip install -e contratos/py -e services/interprete-llm \
  -e services/verificador pytest pytest-cov ruff mypy
```

Ojo: los `requirements.txt` de cada servicio usan rutas relativas (`-e ../../contratos/py`) que pip resuelve **desde la carpeta actual**: se instalan con `cd services/<servicio> && pip install -r requirements.txt`.

## 4. Arquitectura de la corrida mensual

```
orquestador ── crea run_id ──► 00_grilla ──► 01_extractor ──► 01b_calidad ──► 02_calculador
                                                                                   │
              06_publicador ◄── (aprobación humana en prod) ◄── 04_verificador ◄── 03_interprete
```

## 5. Decisiones técnicas para esta parte

### 5.1 Grilla y zonas

- **Celda:** cuadrado de ~5 km (0,045° de lado `[SUPUESTO]`), id `PIU-<fila><columna>` con 2 dígitos cada uno (ej. `PIU-0412`).
- **Zona:** bloque de 4 × 4 celdas (~20 km), id `PIU-<PROV>-<nn>` (ej. `PIU-SUL-01`). Es la unidad que interpreta el LLM.
- **Área:** `dev` = provincia de prueba (Sullana); `prod` = región Piura. Los límites salen de un archivo de configuración con su caja (bbox) `[VERIFICAR coordenadas]`. Si después se consiguen polígonos oficiales de provincias, se recorta la grilla con ellos.

### 5.2 Fuentes

| Indicador (`id`) | Fuente | Acceso | Resolución | Prioridad |
|---|---|---|---|---|
| `ind-temp_max` | NASA POWER `T2M_MAX` | REST, sin llave | ~55 km | P0 |
| `ind-temp_min` | NASA POWER `T2M_MIN` | REST, sin llave | ~55 km | P0 |
| `ind-lluvia_mes` | NASA POWER `PRECTOTCORR` | REST, sin llave | ~55 km | P0 |
| `ind-vegetacion` | MODIS `MOD13Q1` NDVI (`MODIS/061/MOD13Q1` `[VERIFICAR]`) | Earth Engine | 250 m | P1 |
| `ind-humedad_suelo` | SMAP (colección `[VERIFICAR]`) | Earth Engine | 9 km | P1 |
| `ind-lluvia_satelital` | GPM IMERG mensual (colección `[VERIFICAR]`) | Earth Engine | ~10 km | P2 |
| `ind-pendiente` | SRTM (`USGS/SRTMGL1_003` `[VERIFICAR]`) + `ee.Terrain.slope` | Earth Engine | 30 m | P2 |

`valor_normal` = promedio del mismo mes en un periodo histórico fijo (`[SUPUESTO]` 2001–2020 para POWER; 2016–2025 para MODIS) y se documenta en el README del extractor.

### 5.3 Lo que ya sabemos de NASA POWER (de `PRACTICANDO/`)

- El endpoint **diario** recibe fechas `YYYYMMDD`; el **mensual pide años** (`start=2025&end=2026`).
- No existe endpoint anual: el año sale de la clave `AAAA13` del mensual.
- Retrasos: los datos diarios tardan ~3 días; el mes anterior puede llegar como `-999` aunque ya terminó. Eso es un dato faltante, no un error del código.
- `T2M_MAX` (máxima) no es `T2M` (promedio): la app habla de "la temperatura más alta".
- Responde **422 en inglés** ante entradas inválidas: validar antes de llamar.
- Varias celdas de 5 km caen en el mismo píxel de POWER: agrupar peticiones por píxel para no repetirlas.

### 5.4 Confianza

| Situación | `confianza` |
|---|---|
| Dato del mes, sin huecos | `alta` |
| Dato con huecos parciales, rellenado con el mes anterior o con resolución mayor a 25 km | `media` |
| Más de la mitad de las celdas de la zona sin dato, o dato atrasado | `baja` |

## 6. Estructura de una corrida

### 6.1 Carpetas

```
runs/<entorno>/<run_id>/
├── 00_grilla/        grilla.geojson, zonas.json
├── 01_extractor/     crudos.parquet, faltantes.json, fuentes.json
├── 01b_calidad/      calidad.json
├── 02_calculador/    hechos.json                      ← contrato Hechos
├── 03_interprete/    interpretacion.json              ← lo escribe interprete-llm
├── 04_verificador/   interpretacion_verificada.json, informe.md
├── 06_publicador/    paquete-AAAA-MM.sqlite.gz, manifest.json
└── resumen.json      estado y duración de cada etapa
```

`run_id` = `AAAA-MM-` + 6 caracteres `[a-z0-9]` aleatorios (cumple `PATRON_RUN_ID` del contrato).

### 6.2 Códigos de salida que el orquestador debe respetar

| Etapa | `0` | `1` | `2` |
|---|---|---|---|
| Etapas de Codex | Salida escrita y válida | Entrada inválida o falla → detener | — |
| `python -m interprete` | Escrito (puede haber zonas con `origen: error`) | Entrada inválida → detener | Configuración del LLM inválida → detener y avisar a Persona 5 |
| `python -m verificador` | Escrito | Entrada inválida → detener | — |

Si una etapa termina con un código distinto de `0`, **la corrida se detiene y no se publica nada**. El último paquete bueno sigue vigente.

## 7. Tareas

Cada tarea indica: rama, carpeta, entrada, salida, pasos y criterios de aceptación. **Cobertura mínima de tests: 80 %** en cada servicio.

### T1 — Grilla y zonas · `feat/orquestador-grilla`

- **Carpeta:** `orquestador/` (módulo `grilla`).
- **Entrada:** `orquestador/config/area_dev.yaml` y `area_prod.yaml` (bbox, tamaño de celda, tamaño de zona, código de provincia).
- **Salida:** `00_grilla/grilla.geojson` (un polígono por celda con `celda_id`) y `00_grilla/zonas.json` (`zona_id`, `nombre`, `provincia`, `celdas`, `centro`).
- **Pasos:** 1) leer y validar la configuración; 2) generar celdas; 3) agrupar en zonas de 4 × 4; 4) escribir ordenado.
- **Aceptación:** ids estables entre corridas; ninguna celda en dos zonas; toda celda en una zona; tests de bordes (bbox que no es múltiplo exacto del tamaño de celda).
- **Contrato:** proponer `rotacion_contratos/grilla.py` en un **PR aparte** (`feat/contratos-grilla`), porque la app y el publicador también lo usan.

### T2 — Extractor NASA POWER · `feat/extractor-power`

- **Carpeta:** `services/extractor/` (paquete `extractor`, módulo `power`).
- **Entrada:** `zonas.json` + `grilla.geojson` + `--periodo AAAA-MM`.
- **Salida:** `01_extractor/crudos.parquet` (columnas: `celda_id`, `indicador`, `periodo`, `valor`, `valor_normal`, `fuente`, `resolucion_km`), `faltantes.json`, `fuentes.json` (URL y fecha de consulta de cada petición).
- **Pasos:** 1) cliente POWER detrás de un `Protocol`; 2) agrupar celdas por píxel POWER; 3) mensual del periodo + climatología para `valor_normal`; 4) `-999` → `None`; 5) caché local; 6) CLI `python -m extractor power ...`.
- **Aceptación:** respuestas grabadas en `tests/fixtures/` (incluida una con `-999` y una 422); ninguna petición repetida por píxel; reintentos probados con un cliente falso que falla dos veces y luego responde.

### T3 — Extractor Earth Engine · `feat/extractor-earthengine`

- **Carpeta:** `services/extractor/` (módulo `earthengine`).
- **Salida:** agrega filas a `crudos.parquet` para `ind-vegetacion`, `ind-humedad_suelo` (y `ind-lluvia_satelital`, `ind-pendiente` si da el tiempo).
- **Pasos:** 1) autenticación con cuenta de servicio (`GEE_SERVICE_ACCOUNT_FILE`, `GEE_PROJECT`); 2) verificar cada colección en el catálogo oficial y anotar el id exacto en el README; 3) máscara de calidad (nubes); 4) `reduceRegions` con la media por celda; 5) escala del producto (ej. NDVI × 0,0001 `[VERIFICAR]`).
- **Aceptación:** sin credenciales, la CLI falla con un mensaje claro (código 1); los tests usan una fuente falsa, nunca `ee` real; un mes nublado produce `None` y una entrada en `faltantes.json`.
- **Prioridad:** P1. Si no hay credenciales de Earth Engine a tiempo, la demo sigue solo con POWER.

### T4 — Control de calidad · `feat/extractor-calidad`

- **Carpeta:** `services/extractor/` (módulo `calidad`), etapa `01b_calidad`.
- **Salida:** `calidad.json` por zona e indicador: `% celdas sin dato`, `fuera_de_rango`, `atrasado`, `confianza` (§5.4) y `lagunas` en español simple ("No hay dato de vegetación de octubre por nubes").
- **Aceptación:** rangos físicos por indicador en configuración (ej. temperatura −10 a 50 °C); los valores fuera de rango pasan a `None` y quedan en el informe; tests de cada regla de confianza.

### T5 — Calculador · `feat/calculador-reglas`

- **Carpeta:** `services/calculador/` + formato en `agronomia/`.
- **Entrada:** `crudos.parquet`, `calidad.json`, `zonas.json`, `agronomia/*.yaml`.
- **Salida:** `02_calculador/hechos.json`, **validado con `rotacion_contratos.Hechos` antes de escribir**.
- **Pasos:**
  1. Definir el **formato** de `agronomia/cultivos.yaml`, `reglas.yaml` y `rotaciones.yaml` (esquema pydantic en el calculador) y crear ejemplos marcados `[SUPUESTO]` para limón, mango y un tercer cultivo. Persona 4 reemplaza los valores.
  2. Agregar celdas → zona (mediana por indicador) y calcular `diferencia_pct`.
  3. Semáforo con umbrales de `reglas.yaml`.
  4. Por cada (cultivo, temporada): subpuntajes, `factores` (regla aplicada + `descripcion` + `indicador_ids`), `puntaje` con la fórmula de `contratos/formula_puntaje.md` y pesos por defecto, `nivel` y `confianza`.
  5. Rotaciones: al menos 3, exactamente una `es_actual`.
  6. `lagunas` de la zona desde `calidad.json`.
- **Aceptación:** test que reproduce el ejemplo numérico de `formula_puntaje.md` (72,1); test de que la salida valida con `Hechos`; test de que `-999` nunca llega como `0`; la misma entrada produce el mismo archivo byte a byte.

### T6 — Publicador · `feat/publicador-paquete`

- **Antes:** PR de contrato `feat/contratos-paquete` con `contratos/paquete.schema.md` (tablas SQLite) y `manifest.schema.json`, acordado con Persona 3 (la app lo lee).
- **Carpeta:** `services/publicador/`.
- **Entrada:** `hechos.json`, `interpretacion_verificada.json`, `grilla.geojson`, `agronomia/tips/`, `agronomia/glosario.yaml`.
- **Salida:** `paquete-AAAA-MM.sqlite.gz` + `manifest.json` (`version`, `run_id`, `entorno`, `fecha`, `url`, `sha256`, `tamano_bytes`, `schema_version`).
- **Pasos:** 1) crear el SQLite según el contrato; 2) comprimir; 3) calcular `sha256`; 4) subir: `dev` → *prerelease* `datos-dev-AAAA-MM` en GitHub Releases; `prod` → release `datos-AAAA-MM` `[SUPUESTO: a confirmar con el líder]`; 5) opción `--demo` que copia el paquete a `app/assets/paquete_demo/`.
- **Aceptación:** se niega a publicar si `interpretacion_verificada.json` tiene `verificada: false`; en `prod` se niega sin el flag `--publicar`; tamaño del paquete < 5 MB para la provincia de prueba.

### T7 — Orquestador · `feat/orquestador-pipeline`

- **Carpeta:** `orquestador/`.
- **CLI:** `python -m orquestador --entorno dev --periodo 2026-10 [--sin-llm] [--hasta <etapa>] [--publicar]`.
- **Pasos:** 1) crear `run_id` y la carpeta de la corrida; 2) ejecutar cada etapa como subproceso **desde la raíz del repo**; 3) respetar la tabla de códigos de §6.2; 4) escribir `resumen.json` con estado, duración y código de cada etapa; 5) publicar solo si todas las etapas terminaron en `0` y, en `prod`, solo con `--publicar`.
- **Aceptación:** test con etapas falsas que prueba: corrida completa; detención en la primera falla; código `2` del intérprete detiene y deja el motivo en `resumen.json`; `--hasta verificador` no publica.

### T8 — CI y pipeline mensual · `ci/pipeline-mensual`

- **Archivos:** `.github/workflows/ci-servicios.yml` y `.github/workflows/pipeline-mensual.yml`.
- **`ci-servicios.yml`:** en cada Pull Request, para cada carpeta de `services/`, `orquestador/` y `contratos/py`: instalar `requirements.txt`, `ruff check`, `ruff format --check`, `mypy`, `pytest --cov`.
- **`pipeline-mensual.yml`:** `schedule: cron "0 11 5 * *"` (día 5, ~6 a. m. en Lima) + `workflow_dispatch`. Job `dev` (entorno `desarrollo`) → job `prod` (entorno `produccion`, `needs: dev`), que **espera la aprobación humana** configurada en GitHub. Subir `runs/` como *artifact* de cada job.
- **Aceptación:** el workflow pasa `actionlint` (o se valida a mano); ningún secreto aparece en los logs; si el entorno `produccion` no existe todavía, documentarlo en el PR (lo crea el administrador, `ARQUITECTURA.md` §7.6).

## 8. Orden y ruta crítica del hackathon

```
T1 ──► T2 ──► T4 ──► T5 ──► T7 (con --sin-llm, luego con LLM) ──► T6 (--demo) ──► T8
        └──► T3 (P1, en paralelo si hay credenciales)
```

**Ruta mínima para la demo:** T1 → T2 → T5 (solo POWER) → T7 → T6 con `--demo`. T3, T4 completo y T8 se suman si sobra tiempo.

## 9. Definición de "hecho" de cada tarea

- [ ] Criterios de aceptación de la tarea cumplidos
- [ ] `pytest --cov` ≥ 80 %, `ruff check`, `ruff format --check` y `mypy --strict` limpios
- [ ] README del servicio actualizado (uso, variables de entorno, códigos de salida)
- [ ] Ningún secreto, dato pesado ni archivo generado (`.coverage`, `*.egg-info`) en el commit
- [ ] Pull Request hacia `develop` con la plantilla completa e informe del Paso 9 de `REGLAS_GIT.md`

## 10. Riesgos de esta parte

| Riesgo | Plan B |
|---|---|
| Earth Engine sin credenciales a tiempo | Demo solo con NASA POWER; `ind-vegetacion` queda `None` con su laguna |
| NASA POWER lento o con límite | Caché por píxel y corrida `dev` solo con Sullana |
| Reglas agronómicas sin validar | Ejemplos `[SUPUESTO]` visibles en el informe; Persona 4 los reemplaza |
| El contrato no alcanza | Detenerse y proponer el cambio en un PR de `contratos/` |

## 11. Prompt para pegar en Codex

```text
Eres Codex trabajando en el repositorio Doc-Nasa (NASA Space Apps 2026, Piura).
Tarea: T<N> de docs/planes/PLAN_AGENTES_CODEX.md.

Antes de escribir código:
1. Lee AGENTS.md, REGLAS_GIT.md, ARQUITECTURA.md y docs/planes/PLAN_AGENTES_CODEX.md completos.
2. Lee la sección de la tarea T<N> y los contratos en contratos/py/rotacion_contratos/.
3. Resume en 5 líneas qué vas a hacer, qué archivos vas a crear y qué no vas a tocar.

Reglas obligatorias:
- Sigue el flujo de REGLAS_GIT.md: rama desde develop actualizado, commits tipo(área): descripción,
  PR hacia develop. Nunca hagas push a main ni a develop; nunca apruebes ni fusiones el PR.
- No toques services/interprete-llm, services/verificador, app/, contratos/ (salvo PR aparte
  aprobado), AGENTS.md ni IDEA.md.
- No inventes cifras ni nombres de datasets: verifica en la documentación oficial o marca [VERIFICAR].
  -999 de la NASA es None, nunca 0. Valores de ejemplo marcados [SUPUESTO].
- Los tests no llaman a la red. Cobertura ≥ 80 %. ruff y mypy --strict limpios.
- Ante cualquier duda de la sección 2.7 del plan, detente y pregunta.

Al terminar, entrega el informe del Paso 9 de REGLAS_GIT.md (rama, commits, PR, pruebas, pendientes).
```
