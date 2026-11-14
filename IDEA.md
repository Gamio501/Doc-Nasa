# Nuestra idea: "Rotación Inteligente para mi parcela"

## ¿Qué es?
Una página web que abre en el celular. El agricultor marca su campo en un mapa (o usa el GPS) y la app le dice, con datos de la NASA, **cómo está su terreno hoy** y **qué rotación de cultivos le conviene más**.

No reemplaza al agrónomo: es una ayuda para decidir.

## ¿Cómo funciona? (5 pasos)
1. **GPS / mapa** → el agricultor marca su campo.
2. **Diagnóstico Express** → la app muestra vegetación, humedad y temperatura de su zona (semáforo 🟢🟡🔴).
3. **Mis prioridades** → el agricultor mueve 3 deslizadores: ahorrar agua, ganar más, cuidar el suelo.
4. **3 estrategias** → la app compara lado a lado: la rotación actual, una que ahorra agua y una que cuida el suelo, con puntaje 0-100.
5. **Detalle** → por qué se sugiere, qué evidencia tiene, beneficios, qué datos faltan (lagunas) y riesgos a revisar con el experto local.

## ¿Qué datos usa?
- NASA POWER → temperatura y lluvia.
- SMAP → humedad del suelo.
- GPM → lluvia satelital.
- MODIS → vegetación (NDVI).
- SRTM → pendiente y erosión.

## ¿Qué la hace diferente?
- Lenguaje simple (dice "vegetación", no "NDVI").
- Reglas transparentes, no cajas negras.
- Declara siempre la incertidumbre y lo que falta validar.
- Aviso visible: "Esta herramienta apoya tu decisión; no reemplaza a un experto local."

## Funciones extra
- Alertas semáforo para temperatura, sequía y vegetación.
- Escenarios "qué pasa si" (menos lluvia, más calor).
- Mapa con capas y línea de tiempo de suelo desnudo.
- Modo aprendiz para jóvenes que inician en agricultura.

## Núcleo del proyecto: Agente LLM
El agente consulta APIs NASA por la zona marcada, normaliza datos (fechas, unidades, resolución) e interpreta con reglas agronómicas cuál de las 3 rotaciones es la mejor y por qué. Genera JSON estructurado que la web renderiza (tarjetas, semáforo, gráficos, texto simple). El LLM no inventa datos: solo interpreta y presenta cifras ya calculadas; toda cifra sale de un dataset o se marca [SUPUESTO]. Backend FastAPI expone /diagnostico y /rotaciones; frontend Next.js renderiza.

## Para el video
Usuario marca parcela → agente consulta APIs en vivo → LLM interpreta → aparece diagnóstico + 3 estrategias con explicación. Ese es el "momento wow".

## Tecnología
Next.js + TypeScript + Tailwind, MapLibre (mapas), Recharts (gráficos), FastAPI (Python), PWA para uso offline.