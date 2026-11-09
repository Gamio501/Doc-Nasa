# AGENTS.md — NASA Space Apps 2026: Herramienta de rotación de cultivos

> Documento vivo. Todo agente de IA (y todo miembro del equipo) debe leerlo antes de trabajar y actualizarlo cuando cambie una decisión.
> Las líneas marcadas con `[POR DEFINIR]` son datos que el equipo aún debe completar.

---

## 1. Contexto

- **Evento:** Desafío de aplicaciones espaciales de la NASA 2026 (NASA Space Apps Challenge).
- **Dificultad:** Intermedio / Avanzado.
- **Temas:** Artes y multimedia, Ciencias de la Tierra, Software.
- **Fecha del hackathon:** `[POR DEFINIR]`
- **Duración del hackathon:** `[POR DEFINIR]`
- **Tiempo de preparación:** exactamente 1 semana antes del evento.
- **Líder del documento:** Ian Andrade Gamio (Ingeniería de Sistemas y Computación, UTP; experiencia en desarrollo web y automatización con IA).
- **Idioma de trabajo:** español. Código y nombres técnicos en inglés cuando sea convención.
- **Objetivo de la semana previa:** llegar al hackathon con roles definidos, alcance acotado (región y cultivos), datos NASA ya probados, repositorio listo y pitch esbozado.

---

## 2. Desafío

### Problema
Los agricultores enfrentan temperaturas cambiantes, lluvias impredecibles, escasez de agua, clima extremo y deterioro del suelo. Elegir cultivos para una rotación es difícil: un cultivo que mejora el suelo en un lugar puede gastar demasiada agua, traer enfermedades, no encajar en el mercado local o no calzar con la temporada.

### Qué hay que construir
Una **herramienta de apoyo a la toma de decisiones** (app, modelo, mapa interactivo u otra) que combine observaciones de la Tierra de la NASA con información local de suelo, características de cultivos y prioridades del agricultor, para explorar estrategias de rotación que fortalezcan la salud del suelo y la adaptación al clima.

### Requisitos explícitos
- Comparar **al menos 3 estrategias de rotación, incluida la rotación existente** del agricultor.
- Para cada estrategia explicar: por qué se sugiere, qué evidencia la respalda, qué beneficios ofrece, dónde hay lagunas de información y qué riesgos requieren revisión local.
- La herramienta **apoya, no reemplaza**, el juicio del agricultor ni la experiencia agronómica local. Debe decirlo de forma visible.
- Permitir que el agricultor ingrese sus prioridades o limitaciones (agua, equipos, mercado, ingresos).
- Ser interpretable por personas con poca experiencia técnica o geoespacial.

### Opcional pero valorado
- Resaltar periodos de suelo desnudo, temporadas de mayor vulnerabilidad del cultivo actual y oportunidades de rotación (cortar ciclos de plagas, reducir demanda de agua, mejorar infiltración, ingresos complementarios).
- Explicar términos científicos (evapotranspiración, anomalías de humedad, NDVI, riesgo de heladas, balance hídrico).
- Aclarar diferencia entre observación satelital y medición en tierra, y cómo combinarlas.
- Explicar cómo el modelo trata la incertidumbre y dónde se necesita validación local.
- Mapas interactivos, líneas de tiempo, superposiciones, deslizadores de escenarios (lluvia/temperatura).
- Visualizar vulnerabilidades a nivel de campo (erosión, estrés hídrico, heladas).
- Armonizar datasets de distinta resolución a una cuadrícula común.

### Datasets NASA sugeridos por el desafío
SMAP, ECOSTRESS, GPM, Landsat, MODIS, NASA POWER, GRACE y GRACE-FO, SRTM (u otros de elevación), GEDI (biomasa).

### Criterios de evaluación de los jueces
`[POR DEFINIR]` — revisar la página oficial del desafío y la pestaña **Recursos**.

---

## 3. Equipo

| Nombre | Carrera / perfil | Rol principal | Disponibilidad | Contacto |
|---|---|---|---|---|
| Ian Andrade Gamio | Ing. Sistemas y Computación (UTP), web + automatización con IA | `[POR DEFINIR]` (sugerido: desarrollo de la app e integración de IA) | `[POR DEFINIR]` | github.com/Gamio501 |
| `[POR DEFINIR]` | | | | |
| `[POR DEFINIR]` | | | | |
| `[POR DEFINIR]` | | | | |

- **Tamaño del equipo:** `[POR DEFINIR]`
- **Mentor/a agrónomo/a:** `[POR DEFINIR]`
- **Canal de comunicación (WhatsApp, Discord, etc.):** `[POR DEFINIR]`
- **Brechas de conocimiento conocidas:** teledetección y agronomía suelen ser las más difíciles de cubrir en un equipo de ingeniería de sistemas.

---

## 4. Herramientas

### Datos y teledetección
- **NASA POWER** (API sencilla): temperatura, lluvia, radiación. Primer dataset para probar.
- **SMAP:** humedad del suelo.
- **GPM:** precipitación.
- **MODIS / Landsat:** NDVI, vegetación, cobertura.
- **ECOSTRESS:** estrés térmico y evapotranspiración.
- **GRACE / GRACE-FO:** agua subterránea a largo plazo (baja prioridad).
- **SRTM:** elevación y pendiente, útil para riesgo de erosión.
- **GEDI:** biomasa (opcional).
- **Acceso a datos:** Google Earth Engine, NASA Earthdata Search, AppEEARS. Requieren registro previo: hacerlo el día 1.

### Procesamiento y modelado
- Python: `pandas`, `xarray`, `rasterio`, `geopandas`, `numpy`, `scikit-learn` (solo si hace falta).
- Puntuación multicriterio con pesos ajustables por el agricultor (modelo simple y explicable).

### Aplicación
- **Frontend:** web responsive; Leaflet o MapLibre para mapas; gráficos con Chart.js, Recharts o similar.
- **Prototipado rápido alternativo:** Streamlit.
- **IA generativa:** para explicar en lenguaje sencillo el resultado y las lagunas de información, siempre con las cifras calculadas por el modelo (la IA no inventa datos).

### Colaboración
- Repositorio Git (GitHub), `README.md`, este `AGENTS.md`.
- Tablero de tareas simple (GitHub Projects, Trello o Notion). `[POR DEFINIR]`
- Herramienta de diseño (Figma o Canva). `[POR DEFINIR]`

---

## 5. Roles

| Rol | Responsabilidades | Prioridad | Responsable |
|---|---|---|---|
| Líder / storyteller | Alcance, coordinación, pitch, video, documentación | Imprescindible | `[POR DEFINIR]` |
| Científico/a de datos geoespaciales | Descargar y procesar datos NASA, armonizar resoluciones, calcular índices y anomalías | Imprescindible | `[POR DEFINIR]` |
| Desarrollador/a full-stack / frontend | App web, mapas, gráficos, lógica de comparación de estrategias | Imprescindible | `[POR DEFINIR]` |
| Conocimiento agronómico | Validar cultivos y rotaciones de la zona; fuente de reglas agronómicas | Muy importante | `[POR DEFINIR]` |
| Diseñador/a UX/UI | Interfaz clara para agricultores con poca experiencia técnica | Importante | `[POR DEFINIR]` |
| IA / modelado (opcional) | Modelo explicable, incertidumbre, explicaciones en lenguaje natural | Opcional | `[POR DEFINIR]` |

Una persona puede asumir dos roles. Cada rol debe tener al menos un responsable y un suplente.

---

## 6. Planificación

### Semana de preparación

| Día | Objetivo | Entregable | Estado |
|---|---|---|---|
| 1 | Leer desafío y pestaña Recursos. Definir roles. Elegir **una región y 3 o 4 cultivos**. Registrarse en Earthdata y Earth Engine | Roles asignados, alcance escrito | ☐ |
| 2 | Entender los datasets: probar NASA POWER y Earth Engine en una región de prueba | Notebook o script que descarga datos | ☐ |
| 3 | Estudiar agronomía básica de los cultivos elegidos. Contactar mentor agrónomo | Tabla de cultivos con características | ☐ |
| 4 | Pipeline de prueba: descargar, remuestrear y calcular 2 o 3 indicadores (NDVI, lluvia, humedad) | Pipeline funcionando en la región de prueba | ☐ |
| 5 | Diseñar lógica de puntuación de rotaciones y boceto de interfaz | Esquema de puntuación + wireframes | ☐ |
| 6 | Estructura del proyecto: repositorio, plantilla de app, esquema del pitch | Repo base desplegable | ☐ |
| 7 | Simulacro: pitch de 3 minutos y reparto de tareas finales | Pitch ensayado, backlog del hackathon | ☐ |

### Durante el hackathon (borrador)
`[POR DEFINIR]` — dividir las horas disponibles en: datos y modelo, app, pulido de interfaz, video/pitch, margen final. Dejar al menos el último bloque libre para pruebas y entrega.

### Definición de "hecho" (mínimo viable)
- Una región, 3 o 4 cultivos, 3 estrategias de rotación comparadas (incluida la actual).
- Al menos 3 indicadores NASA integrados y explicados.
- Prioridades del agricultor ajustables.
- Explicación por estrategia: razón, evidencia, beneficios, lagunas, riesgos.
- Aviso visible de que la herramienta no reemplaza al experto local.
- Demo funcional + video/pitch.

---

## 7. Reglas

### Reglas del desafío
- Cumplir todos los requisitos de la sección 2.
- Revisar las reglas oficiales de NASA Space Apps sobre entrega, licencias, uso de IA y datos. `[POR DEFINIR]`
- Citar todos los datasets NASA y herramientas usadas.

### Reglas de trabajo del equipo
- El alcance pequeño y bien terminado gana a un alcance ambicioso a medias.
- Toda decisión de alcance se registra en este documento.
- Ningún cambio grande de dirección sin avisar al líder.
- Commits pequeños y frecuentes; rama `main` siempre funcional.

### Reglas para agentes de IA
- Leer este archivo antes de proponer o escribir código.
- No inventar datos, cifras ni citas científicas: todo valor mostrado debe venir de un dataset o estar marcado como supuesto.
- Mantener el modelo **simple y explicable**; evitar cajas negras.
- Toda recomendación de rotación debe incluir: razón, evidencia, beneficios, lagunas de información y riesgos para revisión local.
- Mostrar incertidumbre y no presentar resultados como certezas.
- Recordar siempre que la herramienta apoya, no reemplaza, al agricultor y al experto local.
- Usar lenguaje sencillo para el usuario final (agricultor).
- Registrar en la sección 8 o 9 toda idea nueva o descartada.
- Marcar con `[SUPUESTO]` cualquier dato que no esté verificado.

---

## 8. Ideas generadas

Estado: ✅ adoptada · 🟡 por evaluar · ⬜ sin decidir

| # | Idea | Estado |
|---|---|---|
| 1 | Elegir **una sola región** y 3 o 4 cultivos para mantener el alcance pequeño | 🟡 |
| 2 | Si se elige la zona norte de Perú (por ejemplo, valle de Piura/Chira, cerca de Sullana), usar cultivos locales y contexto de pequeños agricultores y mypes | 🟡 |
| 3 | Empezar con **NASA POWER** por ser la API más sencilla | ✅ |
| 4 | Usar **Google Earth Engine** para MODIS/Landsat/SMAP/GPM | 🟡 |
| 5 | Modelo de **puntuación multicriterio** con pesos ajustables (agua, ingresos, suelo, erosión, mercado) | 🟡 |
| 6 | Deslizadores de prioridades del agricultor que recalculan el ranking de rotaciones | 🟡 |
| 7 | Mapa interactivo con capas: humedad del suelo, NDVI, lluvia, riesgo de erosión (con SRTM) | 🟡 |
| 8 | Línea de tiempo que muestre periodos de suelo desnudo y temporadas vulnerables | 🟡 |
| 9 | Deslizadores de escenario (menos lluvia, más temperatura) para simular el efecto en cada rotación | ⬜ |
| 10 | Tarjeta por estrategia: por qué, evidencia, beneficios, lagunas, riesgos | ✅ |
| 11 | Panel "Qué debe validar un experto local" en cada recomendación | ✅ |
| 12 | Glosario sencillo integrado (NDVI, evapotranspiración, anomalía de humedad) | 🟡 |
| 13 | IA generativa solo para redactar explicaciones a partir de los resultados calculados | 🟡 |
| 14 | Interfaz móvil primero, con iconos y poco texto técnico | 🟡 |
| 15 | Comparador visual lado a lado de las 3 estrategias | 🟡 |
| 16 | Videopitch con historia de un agricultor (conecta con el tema Artes y multimedia) | ⬜ |
| 17 | Streamlit como plan B de prototipo rápido | ⬜ |

---

## 9. Ideas descartadas

> Descartadas por defecto para proteger el alcance. El equipo puede reabrirlas si sobra tiempo.

| Idea | Motivo |
|---|---|
| Cubrir varias regiones o todo un país desde el inicio | Alcance demasiado grande para el tiempo disponible |
| Modelo de aprendizaje profundo complejo | Difícil de explicar, exige muchos datos y el reto pide transparencia |
| Dar prioridad a GRACE / GRACE-FO | Resolución gruesa y poco útil a escala de finca; baja prioridad |
| Recomendar una única rotación "correcta" | El reto pide comparar estrategias y respetar el juicio del agricultor |
| Que la IA genere cifras o predicciones por sí sola | Riesgo de datos inventados; solo debe explicar resultados calculados |
| Integrar todos los datasets sugeridos | Mejor pocos indicadores bien integrados que muchos a medias |
| Reemplazar la validación del experto local | Contradice el espíritu del desafío |

---

## 10. Pendientes y decisiones abiertas

- [ ] Fecha y duración exactas del hackathon
- [ ] Tamaño y perfiles del equipo
- [ ] Región y cultivos elegidos
- [ ] Mentor agrónomo
- [ ] Criterios de evaluación y reglas oficiales
- [ ] Revisar pestaña Recursos del desafío
- [ ] Registro en Earthdata y Earth Engine
- [ ] Herramientas de comunicación y gestión de tareas
- [ ] Plan B si falla un dataset o la conexión

---

## 11. Registro de cambios

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-11-07 | Creación del documento | Ian / Claude |
