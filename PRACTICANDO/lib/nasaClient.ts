import { parseNasaResponse, type DayData } from "./parseNasa";
import { parseMonthlyResponse, type MonthData } from "./parseMonthly";

const PARAMS = "T2M_MAX,PRECTOTCORR";
const BASE = "https://power.larc.nasa.gov/api/temporal";

/**
 * Error que ya viene traducido al español y con el motivo real de la NASA.
 * Se lanza solo cuando la NASA rechaza el pedido (HTTP 4xx/5xx), no cuando
 * falla la conexión.
 */
export class NasaError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NasaError";
  }
}

/** Traduce los mensajes que la NASA devuelve en inglés a algo que el usuario entienda */
function translateNasaMessage(raw: string): string {
  const m = raw.toLowerCase();

  if (m.includes("end date is greater")) return "La fecha de fin no puede ser anterior a la de inicio.";
  if (m.includes("start date format") || m.includes("end date format")) {
    return "Las fechas van en formato AAAAMMDD, por ejemplo 20261108.";
  }
  if (m.includes("less than or equal to 90")) return "La latitud debe estar entre -90 y 90.";
  if (m.includes("less than or equal to 180")) return "La longitud debe estar entre -180 y 180.";
  if (m.includes("available to")) return "La NASA aún no tiene datos para esas fechas.";
  if (m.includes("unable to parse")) return "Una de las fechas no tiene un formato válido.";

  return "La NASA rechazó la consulta. Revisa las fechas y las coordenadas.";
}

/** Extrae los motivos que la NASA adjunta en la respuesta de error */
function readNasaReasons(body: unknown): string[] {
  if (!body || typeof body !== "object") return [];
  const b = body as { messages?: unknown; detail?: unknown };

  const fromMessages = Array.isArray(b.messages) ? b.messages.filter((x): x is string => typeof x === "string") : [];
  const fromDetail = Array.isArray(b.detail)
    ? b.detail.map((d) => (d && typeof d === "object" && "msg" in d ? String((d as { msg: unknown }).msg) : ""))
    : [];

  return [...fromMessages, ...fromDetail].filter(Boolean);
}

async function getJson(url: string): Promise<unknown> {
  const response = await fetch(url);

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const reasons = readNasaReasons(body);
    throw new NasaError(reasons.length > 0 ? translateNasaMessage(reasons[0]) : "La NASA no respondió. Intenta de nuevo.");
  }

  return response.json();
}

/** Datos diarios. El tope de rango lo pone validateQuery antes de llegar aquí. */
export async function fetchWeatherData(
  lat: string,
  lon: string,
  start: string,
  end: string
): Promise<DayData[]> {
  const url = `${BASE}/daily/point?parameters=${PARAMS}&community=AG&longitude=${lon}&latitude=${lat}&start=${start}&end=${end}&format=JSON`;
  const data = (await getJson(url)) as Parameters<typeof parseNasaResponse>[0];
  return parseNasaResponse(data);
}

/**
 * Datos mensuales. La API pide AÑOS (start=2025&end=2026), no fechas.
 * De aquí salen tanto la vista "Meses" como la vista "Años".
 */
export async function fetchMonthlyData(
  lat: string,
  lon: string,
  startYear: string,
  endYear: string
): Promise<MonthData[]> {
  const url = `${BASE}/monthly/point?parameters=${PARAMS}&community=AG&longitude=${lon}&latitude=${lat}&start=${startYear}&end=${endYear}&format=JSON`;
  const data = (await getJson(url)) as Parameters<typeof parseMonthlyResponse>[0];
  return parseMonthlyResponse(data);
}

/**
 * Trae la respuesta cruda del endpoint mensual para extraer las claves
 * anuales "xx13" (la NASA no tiene endpoint /yearly).
 */
export async function fetchMonthlyRaw(
  lat: string,
  lon: string,
  startYear: string,
  endYear: string
): Promise<Record<string, number>> {
  const url = `${BASE}/monthly/point?parameters=${PARAMS}&community=AG&longitude=${lon}&latitude=${lat}&start=${startYear}&end=${endYear}&format=JSON`;
  const data = (await getJson(url)) as { properties: { parameter: Record<string, Record<string, number>> } };
  return data.properties.parameter.T2M_MAX ?? {};
}
