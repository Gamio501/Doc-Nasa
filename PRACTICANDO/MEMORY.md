# MEMORY.md — App del Clima
Memoria del proyecto entre sesiones. Máximo ~50 líneas: resume o elimina lo que ya no
aporte.

## Estado actual
- v1 funcionando y verificada (2026-11-12): **34/34 tests, `next build` ✅, `eslint` ✅**.
- Funciones: consulta NASA POWER por coordenadas; modo "1 día" y rango (máx. 366 días);
  selector Días/Semanas/Meses/Años; 🔥 con la máxima real; gráfico lineal que se corta en
  huecos; tabla ordenable (mayor→menor); explicación en español; PWA manifest.
- Validación previa en español (`lib/validate.ts`) + traducción de errores 422 de la NASA
  (`NasaError`); los datos obsoletos se limpian al fallar una consulta.
- Verificado en navegador (escritorio y móvil, sin overflow). Dev server en localhost:3000.
- Sin localStorage: todo es estado de React en memoria; al recargar se pierden los resultados
  (por diseño).

## Decisiones (y por qué)
- Gráfico cronológico + tabla ordenable: ordenar una serie temporal por valor destruye la
  tendencia; el "mayor a menor" vive en la tabla (incoherencia de la spec, informada).
- `T2M_MAX` y no `T2M`: la app promete la temperatura más alta (T2M estaba ~6 °C abajo).
- Semanas calculadas en cliente y años desde la clave `xx13` mensual: la NASA no tiene
  endpoint semanal ni /yearly (verificado 404).
- `-999` → `null`: nunca inventar cifras; aviso visible y línea cortada.
- Fechas formateadas por recorte de string: cero riesgo UTC (spec lo exige).

## Aprendizajes y errores a evitar
- El endpoint mensual pide **años** (`start=2025`), no `YYYYMM`.
- Retrasos NASA: diarios ~3 días; mensual puede faltar el mes anterior aunque haya terminado
  (oct 2026 = `-999` hoy) → avisar, no es bug.
- Ordenar por el texto visible rompe las fechas (`01/11` < `20/10`): usar `sortLabel`.
- Los índices de `input` en el DOM cambian al alternar modo "1 día"/"Rango": localizar por
  `aria-label` en pruebas con navegador.
- `@next/swc-win32-x64-msvc` no debe ir en `dependencies` (rompe instalación fuera de Windows).

## Próximos pasos
- Menores de la revisión pendientes: `PRECTOTCORR` pedido sin renderizar, plurales "día(s)",
  `filterAnnualKey` sin usar, accesibilidad de `th`, README de create-next-app, iconos
  192/512, sin `AbortController`.
- UX meses: mostrar nombre de los meses sin dato en el aviso (opción 1 propuesta, sin decidir).
- PWA real: `next-pwa`/service worker aún no instalados (solo manifest + icon).
