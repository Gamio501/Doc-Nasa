# SPEC_MVP.md — Maqueta del MVP (versión para validar con el agrónomo mentor)

> Complementa a `AGENTS.md`. Documento vivo: cualquier cambio de decisión se anota en la sección 11.
> Marcadores: `[POR DEFINIR]` = falta decidir · `[EJEMPLO]` = dato inventado a reemplazar por dato real.

---

## 1. Propósito

Mostrar al agrónomo mentor **la lógica y el flujo** de la herramienta para que corrija cultivos, rotaciones y prioridades **antes** de construir con datos reales.

- Es una **maqueta con datos de ejemplo**, no la entrega final al desafío.
- Toda cifra inventada debe verse rotulada en pantalla como **"Datos de ejemplo"**.
- Meta de la reunión: salir con correcciones concretas y una lista de lo que el mentor validaría.

## 2. Principios de diseño

1. **Apoya, no reemplaza**: el aviso aparece en la primera pantalla y en cada recomendación.
2. **Explicable antes que sofisticado**: reglas y puntajes simples, sin modelos entrenados.
3. **Honestidad sobre lo que no se sabe**: cada estrategia muestra lagunas de información y riesgos.
4. **Móvil primero**: web que se abre con un enlace, pensada para pantalla de celular y que también se ve bien en laptop.
5. **Lenguaje de agricultor**: "vegetación" en lugar de "NDVI", "semana seca" en lugar de "anomalía de humedad".

## 3. Usuario y escenario

- **Usuario:** agricultor o técnico de una zona agrícola `[POR DEFINIR]` (candidata a confirmar: Sullana / Piura).
- **Situación:** tiene un cultivo actual y quiere explorar cómo cambiar su rotación para cuidar el suelo y el agua sin perder ingresos.
- **Cultivos del ejemplo:** 3 o 4 `[POR DEFINIR con el mentor]`.

## 4. Flujo de pantallas (5)

| # | Pantalla | Contenido | Datos |
|---|---|---|---|
| 1 | **Inicio** | Elegir zona y cultivo actual. Aviso: "Esta herramienta apoya tu decisión; no reemplaza a un experto local" | Zona y cultivos `[EJEMPLO]` |
| 2 | **Mis prioridades** | Tres deslizadores: ahorrar agua · ingresos · cuidar el suelo. Opcional: limitaciones (equipos, mercado) | Entrada del usuario |
| 3 | **Clima de la zona** | Temperatura y lluvia recientes, pronóstico corto, un aviso en una frase ("semana seca, poca humedad") | `[EJEMPLO]`, luego fuentes reales |
| 4 | **Tres estrategias** | Tarjetas lado a lado: rotación actual + 2 alternativas. Puntaje 0–100 y una frase de por qué | Reglas y pesos `[EJEMPLO]` |
| 5 | **Detalle de estrategia** | Por qué se sugiere · evidencia · beneficios · lagunas de información · riesgos para revisión local · aviso de apoyo | Texto `[EJEMPLO]` |

Opcionales si sobra tiempo: mapa con una capa de vegetación o suelo desnudo, línea de tiempo de periodos de campo desnudo, glosario de una línea por término.

## 5. Estrategias a comparar (mínimo 3)

| Estrategia | Idea | Estado |
|---|---|---|
| **A. Rotación actual** | La que usa hoy el agricultor (la define el mentor) | `[POR DEFINIR]` |
| **B. Enfoque en agua** | Incluye cultivos de menor demanda de agua o tolerantes a sequía | `[POR DEFINIR]` |
| **C. Enfoque en suelo** | Incluye cultivo de cobertura o fijador de nitrógeno | `[POR DEFINIR]` |

Los nombres y cultivos concretos los propone o corrige el mentor.

## 6. Lógica de puntuación (conceptual)

- **Criterios:** uso de agua · ingresos · salud del suelo (materia orgánica, nitrógeno) · riesgo de erosión · exposición al clima (calor, lluvia irregular) · ajuste al mercado local.
- Cada cultivo y rotación recibe una valoración simple por criterio (por ejemplo, baja / media / alta) a partir de una tabla de reglas.
- El puntaje final combina los criterios con **pesos que salen de los deslizadores** del agricultor.
- La explicación se arma con las mismas reglas: se muestran los 2 o 3 criterios que más pesaron.
- Cada recomendación debe declarar su **incertidumbre** (qué dato falta o es aproximado).

## 7. Datos: ahora vs. después

| Elemento | En la maqueta | Fuente real prevista (a confirmar en la investigación) |
|---|---|---|
| Temperatura y lluvia históricas y recientes | `[EJEMPLO]` | NASA POWER |
| Pronóstico corto | `[EJEMPLO]` | Fuente de pronóstico distinta a la NASA (por investigar) |
| Vegetación (estado del cultivo) | Imagen o valor `[EJEMPLO]` | NDVI de MODIS u otro producto (por investigar) |
| Humedad del suelo / lluvia satelital | Valor `[EJEMPLO]` | SMAP, GPM (por investigar) |
| Pendiente y erosión | Texto `[EJEMPLO]` | SRTM u otro modelo de elevación (por investigar) |
| Tabla de cultivos y rotaciones | Valores `[EJEMPLO]` | Validados por el agrónomo mentor |

**Regla clave:** los datos de ejemplo se inventan con la **misma estructura** que tendrán los reales (mismos campos, unidades y periodos), para cambiar la fuente sin rehacer pantallas.

Estructura conceptual de los datos:
- **Clima diario:** fecha · temperatura mínima y máxima · lluvia · fuente · fecha de consulta.
- **Cultivo:** nombre · ciclo y épocas de siembra y cosecha · demanda de agua · si fija nitrógeno · si protege el suelo · profundidad de raíz · tolerancia a sequía · potencial de mercado.
- **Rotación:** secuencia de cultivos por temporada · efectos esperados por criterio.
- **Indicador de zona:** nombre · valor · periodo · resolución · fuente · limitaciones.

## 8. Qué debe validar el agrónomo

- ¿Los cultivos y las tres rotaciones tienen sentido en la zona?
- ¿Las tres prioridades son las que mueven la decisión de un agricultor? ¿Cuáles faltan?
- ¿Qué alerta climática le importa más y con qué umbral?
- ¿Qué debería revisar siempre un experto local antes de recomendar un cultivo?
- ¿Qué faltaría para que él recomendara usar la herramienta?

## 9. Fuera de alcance de esta maqueta

- Modelos entrenados o predicciones por IA.
- Cobertura de varias regiones.
- App instalable, cuentas de usuario o base de datos.
- Detalle a nivel de parcela individual (la resolución de los datos satelitales no lo permite).

## 10. Criterios de "listo" para la reunión

- [ ] Las 5 pantallas navegables (aunque sea en maqueta).
- [ ] Rótulo "Datos de ejemplo" visible en cada pantalla con datos inventados.
- [ ] Tres estrategias con explicación completa (por qué, evidencia, beneficios, lagunas, riesgos).
- [ ] Aviso de "apoya, no reemplaza" visible.
- [ ] Preguntas del mentor (sección 8) impresas o a la mano.

## 11. Decisiones abiertas y registro

| Tema | Estado |
|---|---|
| Zona y cultivos del ejemplo | `[POR DEFINIR]` |
| Fuente de pronóstico | Pendiente de investigación |
| Uso de mapa en la versión del hackathon | Pendiente |
| Qué parte de la maqueta se reutiliza en el evento | Revisar reglas oficiales de "construir durante el evento" |

| Fecha | Cambio |
|---|---|
| 2026-11-13 | Creación del documento |
