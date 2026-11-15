# Fórmula del puntaje personalizado (v1)

El `calculador` entrega, por cada cultivo y cada rotación, **seis subpuntajes de 0 a 100**: `agua`, `ingresos`, `suelo`, `erosion`, `clima` y `mercado` (ver `hechos.schema.json` → `Subpuntajes`).
El teléfono **no** aplica reglas agronómicas: solo combina esos subpuntajes con los tres deslizadores del agricultor.

## Deslizadores → pesos

Cada deslizador va de 0 a 100 (valor inicial: 50).

| Criterio | Peso |
|---|---|
| `agua` | `ahorrar_agua` |
| `ingresos` | `ganar_mas` × 0,5 |
| `mercado` | `ganar_mas` × 0,5 |
| `suelo` | `cuidar_suelo` × 0,5 |
| `erosion` | `cuidar_suelo` × 0,5 |
| `clima` | 50 (fijo: el riesgo climático siempre cuenta) |

## Puntaje

```
puntaje_personal = Σ (peso_c × subpuntaje_c) / Σ peso_c
```

- Se redondea a entero para mostrarlo ("72 % factible").
- Si todos los deslizadores están en 0, solo pesa `clima`.
- Con los tres deslizadores en 50, el resultado debe coincidir con el `puntaje` del `calculador`: el `calculador` usa estos mismos pesos por defecto. Hay un test en cada lado que lo comprueba.

## Ejemplo

Subpuntajes del limón (ejemplo `[SUPUESTO]`): agua 60, ingresos 85, suelo 70, erosion 80, clima 75, mercado 90. Deslizadores: ahorrar_agua 80, ganar_mas 50, cuidar_suelo 20.

```
pesos  = agua 80, ingresos 25, mercado 25, suelo 10, erosion 10, clima 50   (suma 200)
puntos = 80·60 + 25·85 + 25·90 + 10·70 + 10·80 + 50·75 = 14 425
puntaje_personal = 14 425 / 200 = 72,1 → 72
```
