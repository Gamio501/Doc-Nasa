"use client";

import { useState } from "react";
import WeatherForm, { type QueryParams } from "@/components/WeatherForm";
import WeatherChart from "@/components/WeatherChart";
import WeatherTable from "@/components/WeatherTable";
import { fetchWeatherData, fetchMonthlyData, fetchMonthlyRaw, NasaError } from "@/lib/nasaClient";
import { toWeekly, pickAnnualKey, resolveYearRange } from "@/lib/aggregate";
import { validateQuery, type Granularity } from "@/lib/validate";
import type { Point } from "@/lib/sort";

const OPTIONS: { value: Granularity; label: string }[] = [
  { value: "dias", label: "Días" },
  { value: "semanas", label: "Semanas" },
  { value: "meses", label: "Meses" },
  { value: "anios", label: "Años" },
];

/** Qué significa la cifra del 🔥 en cada vista, para no etiquetar un promedio como "más alta" */
const HOTTEST_LABEL: Record<Granularity, string> = {
  dias: "La temperatura más alta del periodo",
  semanas: "La semana con la temperatura más alta promedio",
  meses: "El mes con la temperatura más alta promedio",
  anios: "El año con la temperatura más alta promedio",
};

const METRIC_EXPLANATION: Record<Granularity, string> = {
  dias: "Es la temperatura máxima del aire a 2 metros que registró la NASA ese día.",
  semanas: "Es el promedio de las temperaturas máximas diarias de esa semana.",
  meses: "Es el promedio de las temperaturas máximas diarias de ese mes.",
  anios: "Es el promedio de las temperaturas máximas diarias de ese año.",
};

const SPATIAL_NOTE =
  "La NASA calcula este valor para una zona de varios decenas de kilómetros a la redonda, no para una chacra en particular.";

/** "20261108" → "08/11/2026" (recorte de string: no pasa por UTC) */
function formatDay(iso: string): string {
  return `${iso.slice(6, 8)}/${iso.slice(4, 6)}/${iso.slice(0, 4)}`;
}

const MONTH_NAMES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];

function formatMonth(key: string): string {
  const month = Number(key.slice(4, 6)) - 1;
  return `${MONTH_NAMES[month] ?? key.slice(4, 6)} ${key.slice(0, 4)}`;
}

export default function Home() {
  const [granularity, setGranularity] = useState<Granularity>("dias");
  const [points, setPoints] = useState<Point[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [lastDate, setLastDate] = useState("");
  const [lastParams, setLastParams] = useState<QueryParams | null>(null);

  const clearResults = () => {
    setPoints([]);
    setLastDate("");
    setNotice("");
  };

  const run = async (params: QueryParams, gran: Granularity) => {
    setLoading(true);
    setError("");
    setLastParams(params);

    const invalid = validateQuery(params, gran);
    if (invalid) {
      // Un error de validación no debe dejar en pantalla los datos de otra consulta
      clearResults();
      setError(invalid);
      setLoading(false);
      return;
    }

    try {
      if (gran === "meses" || gran === "anios") {
        const startYear = params.start.slice(0, 4);
        const endYear = params.end.slice(0, 4);

        if (gran === "anios") {
          const range = resolveYearRange(startYear, endYear, new Date().getFullYear());
          if (!range.start || !range.end) {
            clearResults();
            setError(range.error ?? "No hay años completos disponibles para ese rango.");
            return;
          }
          if (range.note) setNotice(range.note);

          const annual = pickAnnualKey(await fetchMonthlyRaw(params.lat, params.lon, range.start, range.end));
          if (annual.length === 0) {
            clearResults();
            setError("La NASA aún no tiene promedios anuales para ese rango.");
            return;
          }
          setPoints(annual.map((y) => ({ label: y.year, sortLabel: y.year, temp: y.temp })));
          setLastDate(annual[annual.length - 1].year);
          return;
        }

        const months = await fetchMonthlyData(params.lat, params.lon, startYear, endYear);
        const clean = months.filter((m) => m.temp !== null);
        if (clean.length === 0) {
          clearResults();
          setError("La NASA no tiene datos mensuales para ese rango.");
          return;
        }
        setPoints(months.map((m) => ({ label: formatMonth(m.date), sortLabel: m.date, temp: m.temp })));
        setLastDate(formatMonth(clean[clean.length - 1].date));
        return;
      }

      const days = await fetchWeatherData(params.lat, params.lon, params.start, params.end);
      const clean = days.filter((d) => d.temp !== null);

      if (clean.length === 0) {
        clearResults();
        setError(
          "La NASA no tiene datos para esas fechas. Los datos diarios llegan con unos días de retraso."
        );
        return;
      }

      if (gran === "semanas") {
        const weeks = toWeekly(days);
        setPoints(weeks.map((w) => ({ label: w.date, sortLabel: w.date, temp: w.temp, missing: w.missing })));
        const withMissing = weeks.filter((w) => w.missing > 0).length;
        if (withMissing > 0) setNotice(`${withMissing} semana(s) tienen días sin datos de la NASA.`);
      } else {
        setPoints(days.map((d) => ({ label: formatDay(d.date), sortLabel: d.date, temp: d.temp })));
        if (clean.length < days.length) {
          setNotice(`${days.length - clean.length} día(s) sin datos: la línea aparece cortada.`);
        }
      }

      setLastDate(formatDay(clean[clean.length - 1].date));
    } catch (e) {
      // Nunca dejamos los datos de una consulta anterior junto a un error:
      // el usuario los leería como resultado de la consulta que falló.
      clearResults();
      setError(
        e instanceof NasaError
          ? e.message
          : "No se pudo conectar con la NASA. Revisa tu conexión e inténtalo de nuevo."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFetch = (params: QueryParams) => run(params, granularity);

  const handleGranularity = (gran: Granularity) => {
    setGranularity(gran);
    if (lastParams) void run(lastParams, gran);
  };

  const hottest = points.reduce<Point | null>(
    (max, p) => (p.temp !== null && (max === null || p.temp > (max.temp as number)) ? p : max),
    null
  );

  return (
    <main className="min-h-screen p-4 md:p-8 bg-zinc-100 flex flex-col items-center gap-6">
      {/* Navigation Banner between Real API App and Demo Product MVP */}
      <div className="w-full max-w-2xl bg-white p-3.5 rounded-xl shadow-md border border-zinc-200 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-xs">
          <span className="font-bold text-zinc-800">Modo de Vista:</span>
          <span className="bg-blue-100 text-blue-800 font-semibold px-2 py-0.5 rounded">
            🌤️ Clima NASA POWER Real
          </span>
        </div>
        <a
          href="/demo"
          className="w-full sm:w-auto text-center text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white px-3.5 py-2 rounded-lg transition-all shadow-sm flex items-center justify-center gap-1.5"
        >
          <span>🌱 Probar Demo Producto NASA (Rotación Piura)</span>
          <span>→</span>
        </a>
      </div>

      <h1 className="text-2xl md:text-3xl font-bold text-zinc-800">App del Clima NASA</h1>

      <div className="w-full max-w-2xl flex flex-col gap-6">
        <WeatherForm onFetch={handleFetch} />

        <div className="flex gap-2 bg-white p-2 rounded-lg shadow-md">
          {OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => handleGranularity(opt.value)}
              className={`flex-1 py-2 rounded text-sm font-medium transition-colors ${
                granularity === opt.value
                  ? "bg-blue-600 text-white"
                  : "bg-zinc-100 text-zinc-700 hover:bg-zinc-200"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>

        {loading && <p className="text-center text-zinc-600">Consultando datos a la NASA...</p>}
        {error && <p className="text-center text-red-600 bg-red-50 p-3 rounded">{error}</p>}
        {notice && <p className="text-center text-amber-800 bg-amber-50 p-3 rounded">⚠️ {notice}</p>}

        {points.length > 0 && lastParams && (
          <>
            <p className="text-center text-xs text-zinc-500">
              Consulta: latitud {lastParams.lat}, longitud {lastParams.lon} ·{" "}
              {lastParams.start === lastParams.end
                ? formatDay(lastParams.start)
                : `${formatDay(lastParams.start)} a ${formatDay(lastParams.end)}`}
            </p>

            {lastDate && (
              <p className="text-center text-sm text-zinc-500">
                Datos de la NASA hasta <strong>{lastDate}</strong> (llegan con unos días de retraso)
              </p>
            )}

            <div className="bg-white p-4 rounded-lg shadow-md text-center">
              <p className="text-sm text-zinc-500">{HOTTEST_LABEL[granularity]}</p>
              <p className="text-3xl font-bold text-orange-600">
                🔥 {hottest ? `${hottest.temp} °C` : "—"}
              </p>
              {hottest && <p className="text-sm text-zinc-600 mt-1">{hottest.label}</p>}
            </div>

            <WeatherChart data={points} />
            <WeatherTable data={points} unit="°C" />

            <div className="bg-white p-4 rounded-lg shadow-md">
              <h2 className="font-bold mb-2">¿Qué nos dicen estos datos?</h2>
              <p className="text-sm text-zinc-700 leading-relaxed">
                {hottest && (
                  <>
                    En este periodo, la cifra más alta fue de <strong>{hottest.temp} °C</strong> en{" "}
                    <strong>{hottest.label}</strong>. {METRIC_EXPLANATION[granularity]} {SPATIAL_NOTE}{" "}
                    Los días con más calor suelen aumentar la necesidad de agua de las plantas y el
                    estrés del cultivo.
                  </>
                )}
              </p>
              <p className="text-sm text-zinc-500 mt-3 italic">
                Esta herramienta solo muestra datos observados por la NASA. No reemplaza el juicio de
                un agrónomo ni de quien conoce el terreno.
              </p>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
