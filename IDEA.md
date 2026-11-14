# Nuestra idea: "Rotación Inteligente Piura"

> Versión 2.1 (2026-11-14). Cambia la idea original de web a **app móvil Flutter que funciona sin internet**,
> con datos de la NASA que un sistema de agentes actualiza **una vez al mes**.
> Incorpora la retroalimentación del mentor del 2026-11-14 (sección 12).
> Las decisiones que cambian respecto de `AGENTS.md` están en la sección 10.

## 1. ¿Qué es?

Una app para celular (Android primero) que ayuda al agricultor de Piura a decidir **qué sembrar y cómo rotar sus cultivos**, con datos satelitales de la NASA ya interpretados en lenguaje simple.

- **Funciona sin internet.** Todo lo que el agricultor consulta ya está guardado en el teléfono.
- **Se actualiza cada mes.** Cuando el teléfono encuentra señal (wifi o datos), descarga el paquete del mes, que es pequeño (unos pocos MB).
- **No reemplaza al agrónomo.** Es una ayuda para decidir, y lo dice en cada pantalla: *"Esta herramienta apoya tu decisión; no reemplaza a un experto local."*

**Por qué mensual y offline:** muchos agricultores no tienen señal estable en el campo (por ejemplo, en las parcelas de Chulucanas no hay señal, cables ni postes). Además, los datos que importan para sembrar (vegetación, humedad del suelo, lluvia acumulada) cambian en semanas, no en minutos, y la NASA publica algunos con días o semanas de retraso.

Por eso la app **no se actualiza cada vez que la NASA publica algo**. Se juntan los datos y se publica **una actualización grande al cierre de cada mes** (o cada bimestre si el mes viene con pocos datos nuevos). Es más completa y evita depender de la red.

## 2. Los tres apartados de la app

### 2.1 Mi zona: clima y tierra

Lo que el cultivo necesita saber, con semáforo 🟢🟡🔴 y palabras simples:

| Indicador | Qué le dice al agricultor | Fuente |
|---|---|---|
| Temperatura (máxima, mínima, días de calor extremo) | "Este mes hizo más calor de lo normal" | NASA POWER |
| Lluvia del mes y comparación con lo normal | "Mes más seco que el promedio" | NASA POWER / GPM IMERG |
| Humedad del suelo | "La tierra está seca en tu zona" | SMAP |
| Vegetación (salud de las plantas) | "Las plantas de tu zona están verdes / estresadas" | MODIS NDVI (o HLS a 30 m) |
| Pendiente y riesgo de erosión | "Terreno inclinado: cuidado con lavado del suelo" | SRTM |
| Evapotranspiración (agua que pierde la planta) | "Tu cultivo va a necesitar más riego" | NASA POWER / ECOSTRESS |

Cada dato muestra **de qué fecha es**, si es **dato de tu zona o de tu parcela**, y su **nivel de confianza**.

### 2.2 Recomendaciones (apartado general)

1. **Mapa de Piura con la problemática.** La región dividida en celdas (cuadrícula de ~5 km) coloreadas según el problema principal: sequía, calor, suelo con poca vegetación, erosión. El mapa funciona offline: son polígonos guardados en el teléfono, no imágenes descargadas.
2. **Tocar una zona** abre su ficha:
   - **Camino 1 — "¿Qué me conviene sembrar?":** el agricultor elige **la temporada de siembra** (por ejemplo, noviembre–diciembre) y la app muestra un **ranking de cultivos** para esa temporada y esas condiciones: *1.º limón, 2.º mango, 3.º …*, cada uno con su puntaje de aptitud 0–100, su *por qué* y con qué **confianza** se dice (ver nota abajo).
   - **Comparación de 3 rotaciones:** la actual del agricultor, una que ahorra agua y una que cuida el suelo, con puntaje 0–100, evidencia, beneficios, lagunas de información y riesgos para revisar con un experto local.
   - **Mis prioridades:** deslizadores de *ahorrar agua*, *ganar más* y *cuidar el suelo* (y limitaciones de equipo o mercado) que reordenan las recomendaciones.
3. **Camino 2 — "Quiero sembrar…"**: el agricultor elige un cultivo (por ejemplo, mango) y la app le responde **"te lo recomiendo" o "no te lo recomiendo"**, con su **factibilidad en %** (por ejemplo, *72 % factible*), las razones a favor, las razones en contra y qué tendría que cuidar. Se calcula dentro del teléfono, sin internet.
4. **Mi ubicación:** el GPS funciona sin datos móviles; la app abre directo en la zona del agricultor.

> **Nota sobre el "%":** el porcentaje que mostramos es un **puntaje de factibilidad** (0–100 %) calculado con reglas agronómicas, **no una probabilidad de éxito de la cosecha**: para eso haría falta un modelo calibrado con cosechas reales. La app lo explica en una línea ("72 % = qué tan bien encaja tu tierra y tu clima con lo que necesita el cultivo") y siempre lo acompaña de la **confianza** del dato (según cuántos datos hay y qué tan recientes son). Es más honesto y el jurado lo valora.

### 2.3 Tips para cultivar

- **Guía por cultivo:** cuándo sembrar, cuánta agua necesita, plagas comunes en la zona, cosecha.
- **Para empezar (modo aprendiz):** cultivos que **no son pesados** de llevar con el tipo de suelo y clima de tu zona, pensado para jóvenes que inician.
- **Tips según tu zona:** si tu celda tiene suelo seco o erosión, la app prioriza tips de cobertura, riego y conservación del suelo.
- **Glosario simple:** vegetación (NDVI), evapotranspiración, humedad del suelo, anomalía de lluvia.

## 3. ¿Cómo funciona por dentro?

```
CADA MES (servidor, automático)                         EN EL TELÉFONO (sin internet)
──────────────────────────────                          ─────────────────────────────
1. Agente extractor  → consulta APIs NASA              ┌─ Mapa de Piura offline
2. Normalización     → fechas, unidades, -999 → vacío  │  Ficha de zona
                       todo a la misma cuadrícula      │  "Quiero sembrar…"
3. Cálculo (código)  → indicadores, semáforo,          │  Tips y glosario
                       aptitud por cultivo, rotaciones │
4. LLM intérprete    → textos simples por zona (JSON)  │
5. Validación        → ¿cada cifra existe en datos?    │
6. Publicación       → paquete del mes (SQLite + JSON) ─┘ se descarga cuando hay señal
```

### 3.1 Sistema de agentes mensual

| Agente | Qué hace | Quién decide los números |
|---|---|---|
| **Extractor** | Consulta NASA POWER, Earth Engine (MODIS, SMAP, GPM, SRTM) y SoilGrids (suelo). Reintenta si falla y registra qué dato faltó | — |
| **Control de calidad** | Revisa huecos, valores `-999`, fechas atrasadas y valores fuera de rango. Marca la confianza de cada celda | Código |
| **Calculador** | Aplica la tabla de reglas agronómicas validada por el agrónomo: aptitud por cultivo, puntaje de rotaciones | **Código** (transparente, reproducible) |
| **Intérprete (LLM)** | Convierte los resultados en explicaciones simples: por qué, evidencia, beneficios, lagunas, riesgos, tips de la zona | El LLM **solo explica** cifras ya calculadas |
| **Verificador** | Comprueba que cada cifra del texto exista en los datos de entrada. Si falla, usa un texto de plantilla | Código |
| **Revisión humana** | El equipo (y el agrónomo cuando pueda) lee el informe del mes y aprueba antes de publicar: que los datos no tengan conflictos ni valores raros | **Personas** |
| **Publicador** | Solo después de la aprobación, arma el paquete versionado (`2026-12`), lo comprime y lo sube | — |

**Regla de oro:** el LLM no inventa datos ni decide puntajes. Toda cifra sale de un dataset o se marca `[SUPUESTO]`. Ningún paquete llega a los agricultores sin revisión humana.

**Historial que se acumula:** cada mes el paquete nuevo se suma a la serie histórica de la zona (no la reemplaza). Mientras más meses se acumulan, mejor se comparan "este mes" con "lo normal" y más confiables salen las recomendaciones. A futuro, con suficiente historial y datos de cosechas reales, se podría entrenar un modelo de pronóstico.

### 3.2 Cómo usamos el LLM

- **Entrada:** JSON de hechos por zona (indicador, valor, unidad, periodo, resolución, fuente, confianza) + tabla de reglas agronómicas.
- **Salida:** JSON con estructura fija (*structured outputs*), que la app pinta directamente en tarjetas.
- **Instrucciones fijas:** usar solo cifras de la entrada, citar el indicador, declarar lagunas, español sencillo, incluir siempre el aviso del experto local.
- **Por zona, no por celda:** el LLM escribe una explicación por grupo de celdas parecidas (o por distrito); las celdas heredan el texto. Así el costo mensual queda en pocos dólares `[ESTIMADO]`.
- **Plan B sin LLM:** si la API del LLM falla, el verificador usa textos de plantilla. La app nunca queda vacía.
- **Evaluación:** 5–10 zonas de prueba revisadas por el agrónomo antes de publicar el primer paquete.

### 3.3 Actualización y uso offline

- El paquete mensual se guarda en una base local del teléfono (SQLite).
- La app revisa si hay paquete nuevo **solo cuando hay señal**; si no, sigue con el último y muestra "datos de octubre 2026".
- Tamaño previsto: ~1–3 MB comprimido para toda la región `[ESTIMADO]`.
- **Formas de recibir la actualización**, de la más simple a la más elaborada:
  1. **Wifi o datos móviles** cuando el agricultor va al pueblo o a la ciudad.
  2. **Punto de actualización con internet satelital** (por ejemplo, un router Starlink) que lleva un técnico, la cooperativa, la junta de usuarios de riego o la municipalidad a la comunidad una vez al mes: todos los teléfonos cercanos se actualizan en minutos. El internet se usa **solo para actualizar**, no para usar la app.
  3. **De teléfono a teléfono** (Bluetooth / Nearby Share) para quienes casi nunca tienen señal `[IDEA FUTURA]`.

## 4. ¿Qué datos usa?

| Dato | Fuente | Resolución | Frecuencia | Acceso |
|---|---|---|---|---|
| Temperatura, lluvia, radiación, evapotranspiración | NASA POWER | ~55 km | diaria → resumen mensual | Gratis, sin llave |
| Vegetación (NDVI) | MODIS MOD13Q1 / HLS | 250 m / 30 m | 16 días / 2–3 días | Gratis (Earth Engine) |
| Humedad del suelo | SMAP | 9–36 km | 2–3 días | Gratis (Earth Engine / Earthdata) |
| Lluvia satelital | GPM IMERG | ~10 km | 30 min → mensual | Gratis (Earth Engine) |
| Pendiente y erosión | SRTM | 30 m | estático | Gratis (Earth Engine) |
| Tipo de suelo | ISRIC SoilGrids (no NASA) | 250 m | estático | Gratis |
| Reglas de cultivos y rotaciones | Agrónomo mentor | — | por temporada | Validación local |

**Honestidad de escala:** vegetación y pendiente llegan cerca de la parcela; clima y humedad son datos **de zona**. La app lo dice en cada indicador.

## 5. ¿Qué la hace diferente?

- **Funciona sin internet**, pensada para el campo real de Piura.
- **Lenguaje simple** ("vegetación", no "NDVI") y semáforo en vez de gráficos técnicos.
- **Reglas transparentes**: el puntaje se puede explicar; el LLM solo traduce a palabras simples.
- **Declara la incertidumbre** y qué falta validar con un experto local.
- **Hiper-local** frente a herramientas estatales (MIDAGRI, INIA, SENASA), que son de escala macro.

## 6. Cumplimiento del reto

| Requisito del desafío | Dónde se cumple |
|---|---|
| Comparar al menos 3 rotaciones, incluida la actual | Ficha de zona → comparación de 3 rotaciones |
| Por qué, evidencia, beneficios, lagunas, riesgos | Tarjeta de cada rotación y de cada cultivo recomendado |
| Prioridades y limitaciones del agricultor | Deslizadores + "Quiero sembrar…" |
| Interpretable sin experiencia técnica | Semáforo, lenguaje simple, glosario |
| Apoya, no reemplaza | Aviso visible en cada pantalla |
| Datos de observación de la Tierra de la NASA | POWER, MODIS/HLS, SMAP, GPM, SRTM |
| Incertidumbre y validación local | Nivel de confianza por dato y por recomendación |

## 7. Tecnología

- **App:** Flutter (Dart), Android primero. Mapa offline con `flutter_map` y polígonos GeoJSON (sin descargar teselas). Base local SQLite. GPS con `geolocator`. Elegimos Flutter sobre Kotlin/Java nativo porque el equipo ya domina Dart, es más liviano de desarrollar y el mentor lo recomendó (sección 12).
- **Pipeline mensual:** Python (pandas, xarray, Earth Engine API), ejecutado por un programador de tareas mensual (por ejemplo GitHub Actions con `schedule`).
- **LLM:** Claude API con salida JSON estructurada, solo dentro del pipeline (nunca en el teléfono).
- **Distribución del paquete:** archivo estático versionado (por ejemplo GitHub Releases o almacenamiento en la nube). No hace falta un servidor encendido todo el tiempo.

## 8. Alcance para el hackathon (48 horas)

**Demo mínima (lo que sí o sí debe funcionar):**
1. Pipeline ejecutado **una vez** para Piura con 2–3 cultivos (mango, limón + el que confirme el agrónomo) y 3–4 indicadores.
2. App Flutter con el paquete **incluido dentro de la app**: mapa de Piura → tocar zona → ficha con cultivos por aptitud + 3 rotaciones → "Quiero sembrar…" → tips.
3. Demostración en **modo avión** para probar que funciona sin internet.

**Se muestra pero no tiene que estar completo:** el programador mensual configurado, la descarga automática del paquete y el modo aprendiz completo.

**Se recorta si falta tiempo:** HLS a 30 m (quedarse con MODIS), ECOSTRESS, compartir teléfono a teléfono.

## 9. Para el video

Agricultor sin señal en su chacra → pone el celular en modo avión → abre el mapa de Piura → toca su zona → ve "tierra seca, mes más caluroso de lo normal" → la app le muestra qué cultivos le convienen y compara 3 rotaciones → pregunta "¿y si siembro limón?" → recibe factibilidad y tips. Cierre: "Cada mes, un sistema de agentes trae los datos de la NASA y los traduce para él."

## 10. Decisiones que cambian respecto de `AGENTS.md`

| Tema | `AGENTS.md` decía | Esta versión propone |
|---|---|---|
| Plataforma | Web responsive (Next.js) | App móvil Flutter, offline |
| Mapa | Leaflet + Leaflet Draw | `flutter_map` con polígonos offline |
| IA generativa | Fuera del alcance | LLM **solo en el pipeline mensual**, para explicar; puntajes por código |
| Frecuencia de datos | Consulta en vivo | Paquete mensual |
| Recomendación | Solo rotaciones | Rotaciones + aptitud por cultivo + factibilidad de un cultivo elegido + tips |

Estas decisiones deben aprobarse en equipo y registrarse en `AGENTS.md` (secciones 4, 8 y 11).

## 11. Riesgos y plan B

| Riesgo | Plan B |
|---|---|
| Earth Engine no aprueba el proyecto a tiempo | NASA POWER + AppEEARS precalculado antes de la demo |
| La API del LLM falla o se queda sin crédito | Textos de plantilla generados por código |
| Reglas agronómicas sin validar | Marcar `[SUPUESTO]` en pantalla y listar qué validará el agrónomo |
| Flutter toma más tiempo del previsto | Reutilizar la maqueta web de `PRACTICANDO` como plan B de demo |
| Datos de la NASA con retraso (mes anterior vacío) | Mostrar el último mes disponible con su fecha; nunca inventar. Si faltan muchos datos, publicar bimestral |
| La zona no tiene ninguna señal para actualizar | Punto de actualización con internet satelital o compartir de teléfono a teléfono |

## 12. Retroalimentación del mentor (2026-11-14)

| Lo que dijo el mentor | Cómo queda en la idea |
|---|---|
| Dos caminos: (1) que la app diga qué productos son los mejores para una temporada, en ranking; (2) que el agricultor diga qué quiere sembrar y la app le recomiende o no, con un porcentaje | Sección 2.2: Camino 1 (ranking por temporada) y Camino 2 ("Quiero sembrar…" con factibilidad en %) |
| Un tercer apartado de tips, educativo, para nuevos agricultores | Sección 2.3: tips y modo aprendiz |
| Móvil mejor que web, por la falta de señal; que se guarde toda la información | App Flutter offline con base local (secciones 1 y 3.3) |
| Llevar un router con internet satelital (Starlink) solo para actualizar | Sección 3.3: punto de actualización con internet satelital |
| Que el equipo revise cada actualización para que los datos no tengan conflictos | Sección 3.1: paso de revisión humana antes de publicar |
| No actualizar cada vez que la NASA publica; juntar en actualizaciones grandes al cierre del mes o cada bimestre | Sección 1: actualización al cierre del mes, o bimestral |
| Mientras más información se alimente, mejor el pronóstico | Sección 3.1: historial que se acumula mes a mes |
| Flutter mejor que Kotlin/Java para móvil, si el equipo domina Dart | Sección 7: Flutter. Mentor de referencia en Flutter: Jean Sandoval |

**Diferencia que mantenemos a propósito:** el mentor mencionó "IA o *machine learning*" para el ranking. Para el hackathon usamos **reglas agronómicas transparentes** (el puntaje se puede explicar y no necesita datos de cosechas para entrenar) y el LLM solo traduce los resultados a palabras simples. El *machine learning* queda como mejora futura cuando haya historial suficiente.
