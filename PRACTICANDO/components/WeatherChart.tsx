"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import type { Point } from "@/lib/sort";

export type { Point };

export default function WeatherChart({ data }: { data: Point[] }) {
  const missingCount = data.filter((d) => d.temp === null).length;

  return (
    <div className="w-full bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-lg font-bold mb-1">Temperatura a lo largo del tiempo</h2>
      <p className="text-xs text-zinc-500 mb-3">
        Orden cronológico. La línea se corta donde la NASA no tiene datos.
      </p>

      {missingCount > 0 && (
        <p className="text-xs bg-amber-50 text-amber-800 border border-amber-200 rounded p-2 mb-3">
          ⚠️ Faltan datos de la NASA en {missingCount} de {data.length} puntos. La línea aparece
          cortada en esos lugares: no inventamos valores.
        </p>
      )}

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" fontSize={11} />
            <YAxis fontSize={11} unit="°C" />
            <Tooltip />
            {/* connectNulls={false} = cortar la línea en los huecos */}
            <Line
              type="monotone"
              dataKey="temp"
              stroke="#2563eb"
              strokeWidth={2}
              dot={data.length <= 40}
              connectNulls={false}
              name="Temperatura"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
