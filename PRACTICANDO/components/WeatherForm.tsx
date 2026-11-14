"use client";

import { useState } from "react";

export type QueryParams = {
  lat: string;
  lon: string;
  start: string;
  end: string;
};

type Mode = "dia" | "rango";

export default function WeatherForm({ onFetch }: { onFetch: (data: QueryParams) => void }) {
  const [mode, setMode] = useState<Mode>("rango");
  const [lat, setLat] = useState("-4.90");
  const [lon, setLon] = useState("-80.68");
  const [fecha, setFecha] = useState("20261108");
  const [start, setStart] = useState("20261020");
  const [end, setEnd] = useState("20261108");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // En modo "1 día" el inicio y el fin son la misma fecha
    onFetch(mode === "dia" ? { lat, lon, start: fecha, end: fecha } : { lat, lon, start, end });
  };

  const fieldClass = "border p-2 rounded w-full";

  return (
    <form onSubmit={handleSubmit} className="p-6 bg-white rounded-lg shadow-md space-y-4">
      <h2 className="text-xl font-bold">Consultar Clima</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <label className="flex flex-col gap-1 text-sm text-zinc-600">
          Latitud
          <input
            className={fieldClass}
            inputMode="decimal"
            aria-label="Latitud"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-zinc-600">
          Longitud
          <input
            className={fieldClass}
            inputMode="decimal"
            aria-label="Longitud"
            value={lon}
            onChange={(e) => setLon(e.target.value)}
          />
        </label>
      </div>

      <fieldset className="space-y-3">
        <legend className="text-sm text-zinc-600 mb-1">Fechas</legend>

        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setMode("dia")}
            className={`flex-1 py-2 rounded text-sm font-medium ${
              mode === "dia" ? "bg-blue-600 text-white" : "bg-zinc-100 text-zinc-700"
            }`}
          >
            1 día
          </button>
          <button
            type="button"
            onClick={() => setMode("rango")}
            className={`flex-1 py-2 rounded text-sm font-medium ${
              mode === "rango" ? "bg-blue-600 text-white" : "bg-zinc-100 text-zinc-700"
            }`}
          >
            Rango de fechas
          </button>
        </div>

        {mode === "dia" ? (
          <label className="flex flex-col gap-1 text-sm text-zinc-600">
            Fecha (AAAAMMDD)
            <input
              className={fieldClass}
              aria-label="Fecha, formato AAAAMMDD"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
            />
          </label>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <label className="flex flex-col gap-1 text-sm text-zinc-600">
              Inicio (AAAAMMDD)
              <input
                className={fieldClass}
                aria-label="Fecha de inicio, formato AAAAMMDD"
                value={start}
                onChange={(e) => setStart(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-sm text-zinc-600">
              Fin (AAAAMMDD)
              <input
                className={fieldClass}
                aria-label="Fecha de fin, formato AAAAMMDD"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
              />
            </label>
          </div>
        )}
      </fieldset>

      <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
        Consultar NASA
      </button>
    </form>
  );
}
