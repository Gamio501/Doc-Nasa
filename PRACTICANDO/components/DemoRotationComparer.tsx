"use client";

import { type RotationStrategy, MOCK_STRATEGIES } from "@/lib/mockData";

interface DemoRotationComparerProps {
  crop: "mango" | "limon";
  parcelName: string;
}

export default function DemoRotationComparer({
  crop,
  parcelName,
}: DemoRotationComparerProps) {
  const strategies: RotationStrategy[] = MOCK_STRATEGIES[crop] ?? [];
  const cropTitle = crop === "mango" ? "Mango (Kent / Haden)" : "Limón Sutil";

  return (
    <section className="bg-white rounded-xl shadow-md p-5 border border-zinc-200">
      <div className="mb-4 pb-3 border-b border-zinc-100 flex flex-col md:flex-row md:items-center justify-between gap-2">
        <div>
          <span className="text-xs font-semibold tracking-wider text-purple-700 bg-purple-50 px-2.5 py-1 rounded-full uppercase">
            Paso 3: Comparador de 3 Estrategias NASA
          </span>
          <h2 className="text-xl font-bold text-zinc-800 mt-1">
            Estrategias de Rotación y Cobertera para {cropTitle}
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Comparativa basada en evidencias satelitales NASA y validación agronómica INIA en {parcelName}.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {strategies.map((strat) => {
          const isRec = strat.recommended;
          return (
            <div
              key={strat.id}
              className={`rounded-xl border transition-all flex flex-col justify-between p-4 ${
                isRec
                  ? "border-emerald-500 bg-emerald-50/30 ring-2 ring-emerald-500/20 shadow-md"
                  : "border-zinc-200 bg-white"
              }`}
            >
              <div>
                {/* Header Badge */}
                <div className="flex items-center justify-between mb-3">
                  <span
                    className={`text-[11px] font-bold px-2.5 py-1 rounded-full border ${
                      strat.badgeColor === "green"
                        ? "bg-emerald-100 text-emerald-800 border-emerald-300"
                        : strat.badgeColor === "amber"
                        ? "bg-amber-100 text-amber-800 border-amber-300"
                        : "bg-zinc-100 text-zinc-700 border-zinc-300"
                    }`}
                  >
                    {strat.badge}
                  </span>
                  {isRec && (
                    <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                      Recomendado
                    </span>
                  )}
                </div>

                {/* Title */}
                <h3 className="font-bold text-base text-zinc-900 mb-3 leading-snug">
                  {strat.title}
                </h3>

                {/* 1. Por qué se sugiere */}
                <div className="mb-3.5">
                  <span className="block text-[11px] font-bold text-zinc-500 uppercase tracking-wide mb-1">
                    1. ¿Por qué se propone?
                  </span>
                  <p className="text-xs text-zinc-700 leading-relaxed bg-zinc-50 p-2.5 rounded border border-zinc-100">
                    {strat.why}
                  </p>
                </div>

                {/* 2. Evidencia NASA */}
                <div className="mb-3.5">
                  <span className="block text-[11px] font-bold text-blue-700 uppercase tracking-wide mb-1">
                    📡 2. Evidencia NASA
                  </span>
                  <p className="text-xs text-zinc-700 leading-relaxed bg-blue-50/50 p-2.5 rounded border border-blue-100/70">
                    {strat.nasaEvidence}
                  </p>
                </div>

                {/* 3. Beneficios en Suelo & Agua */}
                <div className="mb-3.5">
                  <span className="block text-[11px] font-bold text-emerald-700 uppercase tracking-wide mb-1">
                    🌱 3. Beneficios Suelo y Agua
                  </span>
                  <ul className="space-y-1.5 pl-1">
                    {strat.soilWaterBenefits.map((ben, idx) => (
                      <li key={idx} className="text-xs text-zinc-700 flex items-start gap-1.5">
                        <span className="text-emerald-600 font-bold">•</span>
                        <span>{ben}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* 4. Lagunas de Información */}
                <div className="mb-3.5">
                  <span className="block text-[11px] font-bold text-amber-700 uppercase tracking-wide mb-1">
                    🔍 4. Laguna de Información
                  </span>
                  <p className="text-xs text-zinc-600 italic leading-relaxed">
                    "{strat.dataGaps}"
                  </p>
                </div>

                {/* 5. Riesgos a Revisar Localmente */}
                <div className="mb-2">
                  <span className="block text-[11px] font-bold text-red-700 uppercase tracking-wide mb-1">
                    ⚠️ 5. Revisión Local Necesaria
                  </span>
                  <p className="text-xs text-zinc-800 bg-red-50/60 p-2 rounded border border-red-100">
                    {strat.localRisks}
                  </p>
                </div>
              </div>

              {/* Action / Call to action */}
              <div className="mt-4 pt-3 border-t border-zinc-100">
                <button
                  onClick={() =>
                    alert(
                      `Seleccionaste explorar la ${strat.title} para tu parcela ${parcelName}. En la app final esto generará el reporte exportable en PDF.`
                    )
                  }
                  className={`w-full py-2 rounded-lg text-xs font-bold transition-all ${
                    isRec
                      ? "bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm"
                      : "bg-zinc-100 hover:bg-zinc-200 text-zinc-800"
                  }`}
                >
                  {isRec ? "Seleccionar Estrategia Recomendada" : "Explorar esta estrategia"}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Mandatory NASA Disclaimer */}
      <div className="mt-6 p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3 text-amber-900">
        <span className="text-2xl">⚠️</span>
        <div className="text-xs leading-relaxed">
          <p className="font-bold mb-0.5">Aviso Importante sobre la Toma de Decisiones:</p>
          <p>
            Esta herramienta combina observaciones satelitales de la NASA (NASA POWER / MERRA-2) con
            modelos de rotación agrícola. <strong>Apoya, pero no reemplaza</strong> el criterio del
            agricultor ni la asistencia técnica de un agrónomo en el campo.
          </p>
        </div>
      </div>
    </section>
  );
}
