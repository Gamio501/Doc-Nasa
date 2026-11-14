# AGENTS.md — App del Clima NASA

Web PWA en español para consultar el clima de una fecha y lugar vía la API NASA
POWER. Primera versión: base limpia y confiable para aprender a usar APIs y
modelar datos (no es el MVP del reto NASA Space Apps).

## Stack y estructura

- **Next.js 16.4.6** (App Router, Turbopack) + **React 19.3** + **TypeScript 5** + **Tailwind CSS 4.3** + **Recharts 3.10**.
- `app/page.tsx` — orquestación: validación, llamada a la NASA, estado (granularidad, puntos, errores).
- `app/layout.tsx` — `lang="es"`, metadata, enlace al manifest (PWA).
- `components/WeatherForm.tsx` — formulario: modo "1 día" / "Rango", coordenadas, `aria-label` en cada input.
- `components/WeatherChart.tsx` — gráfico lineal Recharts; `connectNulls={false}` (corta la línea en huecos).
- `components/WeatherTable.tsx` — tabla ordenable (delega el orden en `lib/sort`).
- `lib/nasaClient.ts` — cliente NASA POWER (diario + mensual), clase `NasaError` y traducción de errores 422.
- `lib/parseNasa.ts` / `lib/parseMonthly.ts` — parseo de respuestas; `-999` → `null`.
- `lib/aggregate.ts` — semanas ISO, clave anual `xx13`, `resolveYearRange`.
- `lib/sort.ts` — orden cronológico real por `sortLabel` (nunca por el texto visible).
- `lib/validate.ts` — validación previa en español; tipo `Granularity`; tope de 366 días.
- `tests/*.test.ts` — 7 archivos, 34 tests (vitest).
- `public/manifest.json`, `public/icon.svg` — PWA.

## Comandos

```bash
npm run dev      # desarrollo → http://localhost:3000
npm test         # vitest run (34 tests)
npx next build   # build + type check
npm run lint     # eslint
```

No hace falta `npm install`: las dependencias ya están instaladas.

## Conveniones

- **Textos de interfaz en español**; identificadores de código en inglés; comentarios en español.
- Fechas AAAAMMDD; se formatean **recortando strings** (`iso.slice(6,8)/...`), nunca `new Date()` → cero riesgo UTC.
- Diseño móvil-first con Tailwind: tarjetas `bg-white rounded-lg shadow-md`, acento `bg-blue-600`, avisos ámbar (`bg-amber-50`), errores `text-red-600 bg-red-50`.
- Tests en español describiendo el comportamiento ("la temperatura máxima, no el promedio").

## Patrones a seguir

- **TDD**: primero test rojo, luego implementar (`tests/fixes.test.ts` es el mejor ejemplo).
- Referencia de estilo: `lib/validate.ts` (JSDoc explicando el *por qué*, mensajes listos para el usuario).
- Errores de dominio como clase propia (`NasaError`) traducida al español en `translateNasaMessage`.

## Reglas de dominio / trampas conocidas

- **`T2M_MAX`, no `T2M`**: la app promete "la temperatura más alta"; `T2M` es el promedio (~6 °C por debajo).
- **`-999` = sin dato** → `null`, nunca `0`; el gráfico se corta y la tabla dice "Sin datos".
- **Endpoint diario** acepta fechas `YYYYMMDD`; **endpoint mensual pide AÑOS** (`start=2025&end=2026`).
- **No existe `/yearly`**: los años salen de la clave `xx13` del endpoint mensual (`pickAnnualKey`); `resolveYearRange` recorta al último año completo.
- **Retrasos de datos**: diarios ~3 días; el mensual puede faltar el mes anterior aunque ya haya terminado (nov 2026 → oct 2026 = `-999`). Es dato de la NASA, no bug: avisar, no inventar.
- La NASA responde **422 en inglés** para entradas inválidas; validar antes (`validateQuery`) y si llega, traducir (`NasaError`).
- Ordenar fechas **siempre por `sortLabel`**: `"01/11/2026"` ordenado alfabéticamente va antes que `"20/10/2026"`.
- La clave `xx13` debe filtrarse en la vista "Meses" o aparece un "mes 13".

## Memoria
- Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y las decisiones
tomadas.
- Al terminar una tarea, actualízalo: estado actual, decisiones importantes (con su
porqué) y errores a evitar.
- Mantenlo breve (máximo ~50 líneas): resume o elimina lo que ya no aporte.
- Si algo se convierte en una regla permanente, propón moverlo a `AGENTS.md` en lugar de
dejarlo en la memoria.
- No guardes nunca datos sensibles (claves, tokens, datos personales). 

## Forma de trabajar

- Planificar antes de tocar código cuando el cambio toque `page.tsx` o agregaciones; cambios pequeños y por partes.
- Al terminar: correr la verificación completa y explicar en 3-4 líneas qué cambió + decisiones tomadas por cuenta propia.
- Si la spec tiene una incoherencia, decirla antes de resolverla por cuenta propia.
- Todo lo que hagamos debes explicarmelo ya que estoy aprendiendo esta tecnologia. 

## Límites

- ✅ **Siempre:** arreglar bugs, añadir tests, traducir errores al español, avisar cuando falten datos.
- ⚠️ **Preguntar antes:** dependencias nuevas, archivos nuevos, cambiar el formato de los datos mostrados, añadir funcionalidad no pedida (la spec dice "no añadas nada que no aparezca en este mensaje").
- 🚫 **Nunca:** inventar cifras ni citas; mostrar `-999` como valor; usar UTC para fechas; tocar `NASA/AGENTS.md` (documento madre del hackathon) ni borrar tests para "hacer pasar" la suite.

## Verificación

Antes de dar cualquier cambio por terminado, en este orden:

```bash
npm test         # debe dar 34/34 (o más)
npx next build   # debe compilar sin errores de tipos
npm run lint     # debe salir limpio
```

Y una comprobación real en el navegador (`npm run dev` → localhost:3000): consultar Piura por defecto, verificar 🔥, las 4 granularidades y que un error inválido muestre mensaje en español sin datos obsoletos en pantalla.
