type NasaResponse = {
  properties: {
    parameter: {
      T2M_MAX: Record<string, number>;
      PRECTOTCORR: Record<string, number>;
    };
  };
};

export type DayData = {
  date: string;
  temp: number | null;
  precip: number | null;
};

const MISSING = -999;

function clean(value: number | undefined): number | null {
  if (value === undefined || value === MISSING) return null;
  return value;
}

/**
 * Convierte la respuesta diaria de la NASA en una lista.
 *
 * Lee T2M_MAX (la temperatura máxima del día) y NO T2M (el promedio del
 * día): la app promete "la temperatura más alta" y el promedio estaría
 * 6 °C por debajo del valor real en un día caluroso.
 *
 * Ordena explícitamente por fecha en vez de confiar en el orden de las
 * claves del objeto.
 */
export function parseNasaResponse(response: NasaResponse): DayData[] {
  const { T2M_MAX, PRECTOTCORR } = response.properties.parameter;

  return Object.keys(T2M_MAX)
    .map((date) => ({
      date,
      temp: clean(T2M_MAX[date]),
      precip: clean(PRECTOTCORR[date]),
    }))
    .sort((a, b) => a.date.localeCompare(b.date));
}
