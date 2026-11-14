import type { DayData } from "./parseNasa";

export type { DayData };

export type WeekData = {
  date: string; // clave de la semana para el eje del gráfico
  temp: number | null;
  precip: number | null;
  days: number; // días totales que caen en la semana
  missing: number; // cuántos no tenían dato (para el aviso)
};

/** Semana ISO del año: devuelve clave tipo "2026-W45" */
function isoWeekKey(isoDate: string): string {
  const y = Number(isoDate.slice(0, 4));
  const m = Number(isoDate.slice(4, 6)) - 1;
  const d = Number(isoDate.slice(6, 8));

  const date = new Date(Date.UTC(y, m, d));
  // El jueves de la misma semana decide el año ISO
  const day = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - day);
  const isoYear = date.getUTCFullYear();
  const yearStart = new Date(Date.UTC(isoYear, 0, 1));
  const week = Math.ceil(((date.getTime() - yearStart.getTime()) / 86400000 + 1) / 7);

  return `${isoYear}-W${String(week).padStart(2, "0")}`;
}

function average(values: number[]): number | null {
  if (values.length === 0) return null;
  return values.reduce((sum, v) => sum + v, 0) / values.length;
}

/**
 * Agrupa días en semanas ISO.
 * - temp: promedio SOLO de los días con dato (nunca promedia null)
 * - precip: suma de los días con dato
 * - missing: días sin dato, para que la interfaz avise
 */
export function toWeekly(days: DayData[]): WeekData[] {
  const groups = new Map<string, DayData[]>();

  for (const day of days) {
    const key = isoWeekKey(day.date);
    const list = groups.get(key);
    if (list) list.push(day);
    else groups.set(key, [day]);
  }

  return Array.from(groups.entries()).map(([date, list]) => {
    const temps = list.map((d) => d.temp).filter((v): v is number => v !== null);
    const precips = list.map((d) => d.precip).filter((v): v is number => v !== null);

    return {
      date,
      temp: round1(average(temps)),
      precip: precips.reduce((sum, v) => sum + v, 0),
      days: list.length,
      missing: list.length - temps.length,
    };
  });
}

/** Redondea a 1 decimal: nadie quiere leer 27.03666666666666 en pantalla */
function round1(value: number | null): number | null {
  if (value === null) return null;
  return Math.round(value * 10) / 10;
}

/**
 * Quita la clave anual "xx13" que la NASA mete dentro de los datos mensuales.
 * Sin esto aparecería un "mes 13" en el gráfico.
 */
export function filterAnnualKey(monthly: Record<string, number>): string[] {
  return Object.keys(monthly).filter((key) => !key.endsWith("13"));
}

export type YearData = {
  year: string;
  temp: number | null;
};

/**
 * Extrae los promedios anuales (las claves "xx13" del endpoint mensual).
 * Es la única forma de obtener años: no existe endpoint /yearly.
 * Los años sin datos (-999) se descartan en vez de inventar un valor.
 */
export function pickAnnualKey(monthly: Record<string, number>): YearData[] {
  return Object.keys(monthly)
    .filter((key) => key.endsWith("13"))
    .map((key) => ({
      year: key.slice(0, 4),
      temp: monthly[key] === -999 ? null : monthly[key],
    }))
    .filter((item): item is YearData => item.temp !== null)
    .sort((a, b) => a.year.localeCompare(b.year));
}

export type YearRange = {
  start?: string;
  end?: string;
  note?: string;
  error?: string;
};

/**
 * Prepara el rango de años para la vista "Años".
 *
 * La NASA solo guarda el promedio anual (clave xx13) cuando el año ya
 * terminó, así que recortamos el año en curso. Si no queda ningún año
 * completo, devolvemos error en vez de inventar un número.
 */
export function resolveYearRange(startYear: string, endYear: string, currentYear: number): YearRange {
  const lastComplete = String(currentYear - 1);
  const end = endYear > lastComplete ? lastComplete : endYear;

  if (startYear > end) {
    return {
      error: `Para ver años necesitas un rango con al menos un año completo. El año ${currentYear} todavía no termina; prueba con ${Number(lastComplete) - 4} a ${lastComplete}.`,
    };
  }

  const note = endYear > lastComplete
    ? `El año ${endYear} aún no está completo: mostramos hasta ${end}.`
    : undefined;

  return { start: startYear, end, note };
}
