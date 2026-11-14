"use client";

import { type ParcelSector } from "@/lib/mockData";

interface DemoExpressDiagnosticProps {
  parcel: ParcelSector;
}

export default function DemoExpressDiagnostic({ parcel }: DemoExpressDiagnosticProps) {
  // Evaluador semáforo para humedad radicular GWETROOT
  const getRootStatus = (val: number) => {
    if (val >= 0.35) {
      return {
        badge: "🟢 Nivel Óptimo",
        color: "bg-emerald-100 text-emerald-800 border-emerald-300",
        desc: "Humedad suficiente en zona de raíces (0.1m - 1m). Buena hidratación radicular.",
      };
    } else if (val >= 0.20) {
      return {
        badge: "🟡 Atención / Moderado",
        color: "bg-amber-100 text-amber-800 border-amber-300",
        desc: "Humedad regular. Vigila turnos de riego de la junta de usuarios.",
      };
    } else {
      return {
        badge: "🔴 Riesgo Hídrico",
        color: "bg-red-100 text-red-800 border-red-300",
        desc: "Estrés hídrico en zona de raíces. Requiere riego de auxilio urgente.",
      };
    }
  };

  // Evaluador semáforo para humedad superficial GWETTOP
  const getTopStatus = (val: number) => {
    if (val >= 0.25) {
      return {
        badge: "🟢 Suelo Húmedo",
        color: "bg-emerald-100 text-emerald-800 border-emerald-300",
        desc: "Excelente para germinación de cobertera (0 - 5 cm).",
      };
    } else {
      return {
        badge: "🟡 Capa Superficial Seca",
        color: "bg-amber-100 text-amber-800 border-amber-300",
        desc: "Alta evaporación por radiación. Oportunidad ideal para sembrar abono verde / cobertera.",
      };
    }
  };

  // Evaluador semáforo para temperatura máxima T2M_MAX
  const getTempStatus = (val: number) => {
    if (val >= 35.0) {
      return {
        badge: "🔴 Alerta Térmica Extreme",
        color: "bg-red-100 text-red-800 border-red-300",
        desc: `Calor crítico (${val}°C). Riesgo de aborto floral en mango y caída de fruto en limón.`,
      };
    } else if (val >= 33.0) {
      return {
        badge: "🟡 Calor Elevado",
        color: "bg-amber-100 text-amber-800 border-amber-300",
        desc: `Temperatura alta (${val}°C). Aumenta la evapotranspiración.`,
      };
    } else {
      return {
        badge: "🟢 Temperatura Normal",
        color: "bg-emerald-100 text-emerald-800 border-emerald-300",
        desc: `Temperatura adecuada (${val}°C) para el desarrollo vegetative.`,
      };
    }
  };

  const rootSt = getRootStatus(parcel.gwetroot);
  const topSt = getTopStatus(parcel.gwettop);
  const tempSt = getTempStatus(parcel.t2mMax);

  return (
    <section className="bg-white rounded-xl shadow-md p-5 border border-zinc-200">
      <div className="mb-4 pb-3 border-b border-zinc-100">
        <span className="text-xs font-semibold tracking-wider text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full uppercase">
          Paso 2: Diagnóstico Express NASA
        </span>
        <h2 className="text-xl font-bold text-zinc-800 mt-1">
          Estado Actual del Terreno (Modelos NASA POWER)
        </h2>
        <p className="text-xs text-zinc-500 mt-1">
          Semáforo de salud hídrica y térmica actualizado para {parcel.name}.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Card 1: Humedad Raíz (GWETROOT) */}
        <div className="p-4 rounded-xl border border-zinc-200 bg-zinc-50/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-zinc-500 uppercase">
                Humedad de Raíz (0.1–1m)
              </span>
              <span className="text-xs font-mono font-bold text-zinc-700">
                GWETROOT: {(parcel.gwetroot * 100).toFixed(0)}%
              </span>
            </div>
            <div className="mb-2">
              <span
                className={`inline-block text-xs font-bold px-2.5 py-1 rounded-md border ${rootSt.color}`}
              >
                {rootSt.badge}
              </span>
            </div>
            <p className="text-xs text-zinc-700 leading-relaxed mt-1">
              {rootSt.desc}
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-zinc-200 text-[11px] text-zinc-500">
            Fuente: NASA MERRA-2 Soil Wetness
          </div>
        </div>

        {/* Card 2: Humedad Superficie (GWETTOP) */}
        <div className="p-4 rounded-xl border border-zinc-200 bg-zinc-50/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-zinc-500 uppercase">
                Humedad Superficial (0–5cm)
              </span>
              <span className="text-xs font-mono font-bold text-zinc-700">
                GWETTOP: {(parcel.gwettop * 100).toFixed(0)}%
              </span>
            </div>
            <div className="mb-2">
              <span
                className={`inline-block text-xs font-bold px-2.5 py-1 rounded-md border ${topSt.color}`}
              >
                {topSt.badge}
              </span>
            </div>
            <p className="text-xs text-zinc-700 leading-relaxed mt-1">
              {topSt.desc}
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-zinc-200 text-[11px] text-zinc-500">
            Evalúa la capa de germinación
          </div>
        </div>

        {/* Card 3: Estrés Térmico (T2M_MAX) */}
        <div className="p-4 rounded-xl border border-zinc-200 bg-zinc-50/60 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-zinc-500 uppercase">
                Temperatura Máxima
              </span>
              <span className="text-xs font-mono font-bold text-zinc-700">
                T2M_MAX: {parcel.t2mMax} °C
              </span>
            </div>
            <div className="mb-2">
              <span
                className={`inline-block text-xs font-bold px-2.5 py-1 rounded-md border ${tempSt.color}`}
              >
                {tempSt.badge}
              </span>
            </div>
            <p className="text-xs text-zinc-700 leading-relaxed mt-1">
              {tempSt.desc}
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-zinc-200 text-[11px] text-zinc-500">
            Lluvia diaria: {parcel.prectotcorr} mm/día
          </div>
        </div>
      </div>
    </section>
  );
}
