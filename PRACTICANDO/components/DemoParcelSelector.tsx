"use client";

import { type ParcelSector, MOCK_PARCELS } from "@/lib/mockData";

interface DemoParcelSelectorProps {
  selectedParcel: ParcelSector;
  onSelectParcel: (parcel: ParcelSector) => void;
  selectedCrop: "mango" | "limon";
  onChangeCrop: (crop: "mango" | "limon") => void;
  onUseGps: () => void;
  gpsActive: boolean;
}

export default function DemoParcelSelector({
  selectedParcel,
  onSelectParcel,
  selectedCrop,
  onChangeCrop,
  onUseGps,
  gpsActive,
}: DemoParcelSelectorProps) {
  return (
    <section className="bg-white rounded-xl shadow-md p-5 border border-zinc-200">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4 pb-3 border-b border-zinc-100">
        <div>
          <span className="text-xs font-semibold tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full uppercase">
            Paso 1: Ubicación & Parcela
          </span>
          <h2 className="text-xl font-bold text-zinc-800 mt-1">
            Selección del Campo en Piura
          </h2>
        </div>

        <button
          onClick={onUseGps}
          className={`flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            gpsActive
              ? "bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-300"
              : "bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200"
          }`}
        >
          <span>📍</span>
          <span>{gpsActive ? "GPS Activo (Tambogrande)" : "Detectar mi posición por GPS"}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-5">
        {MOCK_PARCELS.map((parcel) => {
          const isSelected = selectedParcel.id === parcel.id && !gpsActive;
          return (
            <button
              key={parcel.id}
              onClick={() => onSelectParcel(parcel)}
              className={`text-left p-3.5 rounded-lg border transition-all ${
                isSelected
                  ? "border-emerald-600 bg-emerald-50/60 ring-2 ring-emerald-500/20 shadow-sm"
                  : "border-zinc-200 hover:border-zinc-300 bg-zinc-50/50 hover:bg-white"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-zinc-900 text-sm">{parcel.name}</span>
                {isSelected && <span className="text-emerald-600 text-xs font-bold">✓ Seleccionado</span>}
              </div>
              <p className="text-xs text-zinc-600 mb-1.5">{parcel.valley}</p>
              <div className="flex items-center gap-2 text-[11px] text-zinc-500 font-mono">
                <span>Lat: {parcel.lat}</span>
                <span>•</span>
                <span>Lon: {parcel.lon}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Visual Simulated Map & Coordinates Header */}
      <div className="relative overflow-hidden rounded-lg border border-emerald-900/10 bg-slate-900 text-white p-4 mb-4">
        <div className="absolute -right-10 -bottom-10 opacity-10 text-8xl select-none pointer-events-none">
          🗺️
        </div>
        <div className="relative z-10 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <div>
            <p className="text-xs text-emerald-400 font-mono">
              [Mapa Simulado Leaflet] Parcela activa:
            </p>
            <p className="text-base font-bold text-white">
              {selectedParcel.name}
            </p>
            <p className="text-xs text-zinc-300 mt-0.5">
              Tipo de suelo: <span className="text-emerald-200 font-medium">{selectedParcel.soilType}</span>
            </p>
          </div>
          <div className="bg-slate-800/90 border border-slate-700 px-3 py-1.5 rounded text-xs font-mono text-emerald-300">
            {selectedParcel.lat.toFixed(4)}°, {selectedParcel.lon.toFixed(4)}°
          </div>
        </div>
      </div>

      {/* Selector de Cultivo Actual */}
      <div className="pt-2">
        <label className="block text-xs font-semibold text-zinc-600 mb-2 uppercase tracking-wider">
          Cultivo Principal Actual en la Parcela:
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => onChangeCrop("mango")}
            className={`p-3 rounded-lg border flex items-center justify-center gap-2.5 font-medium text-sm transition-all ${
              selectedCrop === "mango"
                ? "border-amber-500 bg-amber-50 text-amber-900 font-bold ring-2 ring-amber-400/30"
                : "border-zinc-200 bg-white text-zinc-700 hover:bg-zinc-50"
            }`}
          >
            <span className="text-xl">🥭</span>
            <span>Mango (Kent / Haden)</span>
          </button>
          <button
            onClick={() => onChangeCrop("limon")}
            className={`p-3 rounded-lg border flex items-center justify-center gap-2.5 font-medium text-sm transition-all ${
              selectedCrop === "limon"
                ? "border-lime-600 bg-lime-50 text-lime-900 font-bold ring-2 ring-lime-400/30"
                : "border-zinc-200 bg-white text-zinc-700 hover:bg-zinc-50"
            }`}
          >
            <span className="text-xl">🍋</span>
            <span>Limón Sutil</span>
          </button>
        </div>
      </div>
    </section>
  );
}
