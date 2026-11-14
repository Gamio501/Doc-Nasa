export type Granularity = "dias" | "semanas" | "meses" | "anios";

export type Query = {
  lat: string;
  lon: string;
  start: string;
  end: string;
};

const DATE_RE = /^\d{8}$/;
const MAX_DAILY_DAYS = 366;

/** Interpreta AAAAMMDD como calendario (Date.UTC es aritmética de fecha, no zona horaria) */
function parseYmd(value: string): { y: number; m: number; d: number } | null {
  if (!DATE_RE.test(value)) return null;

  const y = Number(value.slice(0, 4));
  const m = Number(value.slice(4, 6));
  const d = Number(value.slice(6, 8));

  if (m < 1 || m > 12) return null;
  const daysInMonth = new Date(Date.UTC(y, m, 0)).getUTCDate();
  if (d < 1 || d > daysInMonth) return null;

  return { y, m, d };
}

function daysBetween(a: { y: number; m: number; d: number }, b: { y: number; m: number; d: number }): number {
  const ms = Date.UTC(b.y, b.m - 1, b.d) - Date.UTC(a.y, a.m - 1, a.d);
  return Math.round(ms / 86400000);
}

/**
 * Valida la consulta antes de llamar a la NASA.
 *
 * Devuelve null si todo está bien o un mensaje en español listo para
 * mostrar al usuario. Sin esto, la NASA responde 422 en inglés y la app
 * mostraba siempre el mismo "no se pudo conectar", que es falso: la
 * conexión funcionó, lo que falló fue el pedido.
 */
export function validateQuery(query: Query, granularity: Granularity): string | null {
  const lat = Number(query.lat);
  if (query.lat.trim() === "" || Number.isNaN(lat) || lat < -90 || lat > 90) {
    return "La latitud debe ser un número entre -90 y 90.";
  }

  const lon = Number(query.lon);
  if (query.lon.trim() === "" || Number.isNaN(lon) || lon < -180 || lon > 180) {
    return "La longitud debe ser un número entre -180 y 180.";
  }

  const usesYears = granularity === "meses" || granularity === "anios";

  if (!DATE_RE.test(query.start) || !DATE_RE.test(query.end)) {
    return "Las fechas van en formato AAAAMMDD, por ejemplo 20261108.";
  }

  const start = parseYmd(query.start);
  const end = parseYmd(query.end);
  if (!start || !end) {
    return "Una de las fechas no existe. Revisa el día y el mes.";
  }

  if (usesYears) {
    if (start.y > end.y) {
      return "El año de inicio no puede ser posterior al de fin.";
    }
    return null;
  }

  const diff = daysBetween(start, end);
  if (diff < 0) {
    return "La fecha de fin no puede ser anterior a la de inicio.";
  }
  if (diff >= MAX_DAILY_DAYS) {
    return `Para consultar por días, el rango no puede pasar de ${MAX_DAILY_DAYS} días. Usa la vista de Meses o Años para periodos más largos.`;
  }

  return null;
}
