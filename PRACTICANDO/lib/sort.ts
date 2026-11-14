export type Point = {
  /** Texto que se muestra en pantalla */
  label: string;
  /** Clave cruda para ordenar de verdad (fecha ISO o AAAAMM) */
  sortLabel: string;
  temp: number | null;
  missing?: number;
};

export type SortKey = "label" | "temp";

/**
 * Ordena los puntos de la tabla.
 *
 * El orden por "label" usa sortLabel, nunca el texto visible:
 * "01/11/2026" ordenado alfabéticamente va antes que "20/10/2026",
 * pero en el calendario viene después.
 *
 * Los null van al final siempre: no compiten con valores reales.
 */
export function sortPoints(points: Point[], key: SortKey, asc: boolean): Point[] {
  return [...points].sort((a, b) => {
    if (key === "label") {
      return asc ? a.sortLabel.localeCompare(b.sortLabel) : b.sortLabel.localeCompare(a.sortLabel);
    }

    if (a.temp === null && b.temp === null) return 0;
    if (a.temp === null) return 1;
    if (b.temp === null) return -1;
    return asc ? a.temp - b.temp : b.temp - a.temp;
  });
}
