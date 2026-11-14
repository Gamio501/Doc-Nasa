type NasaResponse = {
  properties: {
    parameter: {
      T2M_MAX: Record<string, number>;
      PRECTOTCORR: Record<string, number>;
    };
  };
};

export type MonthData = {
  date: string; // "202501"
  temp: number | null;
  precip: number | null;
};

const MISSING = -999;

function clean(value: number | undefined): number | null {
  if (value === undefined || value === MISSING) return null;
  return value;
}

/**
 * Convierte la respuesta del endpoint mensual en una lista.
 *
 * Usa T2M_MAX (promedio de las máximas del mes) para que coincida con lo
 * que muestra la app en el resto de las vistas. Descarta la clave anual
 * "xx13" que la NASA incluye junto a los meses.
 */
export function parseMonthlyResponse(response: NasaResponse): MonthData[] {
  const { T2M_MAX, PRECTOTCORR } = response.properties.parameter;

  return Object.keys(T2M_MAX)
    .filter((key) => !key.endsWith("13"))
    .map((date) => ({
      date,
      temp: clean(T2M_MAX[date]),
      precip: clean(PRECTOTCORR[date]),
    }))
    .sort((a, b) => a.date.localeCompare(b.date));
}
