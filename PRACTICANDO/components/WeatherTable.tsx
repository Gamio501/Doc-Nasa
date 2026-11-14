"use client";

import { useState } from "react";
import { sortPoints, type Point, type SortKey } from "@/lib/sort";

export default function WeatherTable({ data, unit }: { data: Point[]; unit: string }) {
  const [sortKey, setSortKey] = useState<SortKey>("label");
  const [asc, setAsc] = useState(true);

  const sorted = sortPoints(data, sortKey, asc);

  const toggle = (key: SortKey) => {
    if (key === sortKey) setAsc(!asc);
    else {
      setSortKey(key);
      setAsc(key === "label");
    }
  };

  const arrow = (key: SortKey) => (sortKey === key ? (asc ? " ↑" : " ↓") : "");

  return (
    <div className="w-full bg-white p-4 rounded-lg shadow-md overflow-x-auto">
      <h2 className="text-lg font-bold mb-3">Detalle ({data.length} puntos)</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-zinc-200 text-left">
            <th className="py-2 pr-4 cursor-pointer select-none" onClick={() => toggle("label")}>
              Fecha{arrow("label")}
            </th>
            <th className="py-2 cursor-pointer select-none" onClick={() => toggle("temp")}>
              Temperatura{arrow("temp")}
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((row) => (
            <tr key={row.sortLabel} className="border-b border-zinc-100">
              <td className="py-2 pr-4 text-zinc-700">{row.label}</td>
              <td className="py-2">
                {row.temp === null ? (
                  <span className="text-amber-700">Sin datos</span>
                ) : (
                  <span>
                    {row.temp} {unit}
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-xs text-zinc-500 mt-3">
        Toca “Fecha” o “Temperatura” para ordenar. Con temperatura puedes ver la más alta primero.
      </p>
    </div>
  );
}
