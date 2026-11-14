"use client";

import { useState } from "react";
import Link from "next/link";
import { MOCK_PARCELS, type ParcelSector } from "@/lib/mockData";
import DemoParcelSelector from "@/components/DemoParcelSelector";
import DemoExpressDiagnostic from "@/components/DemoExpressDiagnostic";
import DemoRotationComparer from "@/components/DemoRotationComparer";

export default function DemoPage() {
  const [selectedParcel, setSelectedParcel] = useState<ParcelSector>(MOCK_PARCELS[0]);
  const [selectedCrop, setSelectedCrop] = useState<"mango" | "limon">("mango");
  const [gpsActive, setGpsActive] = useState(false);

  const handleSelectParcel = (parcel: ParcelSector) => {
    setSelectedParcel(parcel);
    setSelectedCrop(parcel.crop);
    setGpsActive(false);
  };

  const handleUseGps = () => {
    setGpsActive(true);
    // Simula ubicación del navegador detectada en Tambogrande
    const tambo = MOCK_PARCELS[0];
    setSelectedParcel(tambo);
    setSelectedCrop(tambo.crop);
  };

  return (
    <main className="min-h-screen p-4 md:p-8 bg-zinc-100 flex flex-col items-center">
      {/* Top Banner & Header */}
      <div className="w-full max-w-6xl flex flex-col md:flex-row items-center justify-between gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-zinc-200">
        <div className="flex items-center gap-3">
          <div className="bg-emerald-600 text-white p-2.5 rounded-lg font-bold text-xl select-none">
            🌱
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl md:text-2xl font-bold text-zinc-900">
                Rotación de Cultivos NASA — Piura
              </h1>
              <span className="bg-amber-100 text-amber-800 text-xs font-bold px-2 py-0.5 rounded border border-amber-300">
                DEMO MVP (Datos Mokeados)
              </span>
            </div>
            <p className="text-xs text-zinc-600 mt-0.5">
              Prototipo de flujos e interfaz para el desafío NASA Space Apps 2026.
            </p>
          </div>
        </div>

        {/* Link back to real API weather app */}
        <Link
          href="/"
          className="text-xs font-medium bg-zinc-100 hover:bg-zinc-200 text-zinc-700 px-3.5 py-2 rounded-lg transition-colors border border-zinc-300 flex items-center gap-1.5"
        >
          <span>🌤️</span>
          <span>Ver App Clima Directo (NASA POWER Real)</span>
        </Link>
      </div>

      {/* Main Container */}
      <div className="w-full max-w-6xl flex flex-col gap-6">
        {/* Step 1: Parcel & Location Selector */}
        <DemoParcelSelector
          selectedParcel={selectedParcel}
          onSelectParcel={handleSelectParcel}
          selectedCrop={selectedCrop}
          onChangeCrop={setSelectedCrop}
          onUseGps={handleUseGps}
          gpsActive={gpsActive}
        />

        {/* Step 2: Express Diagnostic Semaphores */}
        <DemoExpressDiagnostic parcel={selectedParcel} />

        {/* Step 3: 3-Strategy Rotation Comparer */}
        <DemoRotationComparer
          crop={selectedCrop}
          parcelName={selectedParcel.name}
        />
      </div>

      {/* Footer */}
      <footer className="w-full max-w-6xl mt-10 pt-6 border-t border-zinc-300 text-center text-xs text-zinc-500">
        <p className="font-semibold text-zinc-700">
          Proyecto NASA Space Apps Challenge 2026 — Región Piura, Perú
        </p>
        <p className="mt-1">
          Stack: Next.js 16 (App Router) + React 19 + TypeScript + Tailwind CSS 4
        </p>
      </footer>
    </main>
  );
}
