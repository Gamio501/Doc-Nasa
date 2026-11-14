import { describe, it, expect } from "vitest";
import { toWeekly, filterAnnualKey, type DayData } from "../lib/aggregate";

describe("toWeekly", () => {
  it("agrupa los días en semanas ISO", () => {
    // 2026-11-02 (lunes) y 2026-11-03 (martes) caen en la misma semana
    const dias: DayData[] = [
      { date: "20261102", temp: 26, precip: 1 },
      { date: "20261103", temp: 28, precip: 3 },
      { date: "20261109", temp: 30, precip: 0 },
    ];

    const semanas = toWeekly(dias);

    expect(semanas).toHaveLength(2);
    expect(semanas[0].temp).toBe(27); // promedio
    expect(semanas[0].precip).toBe(4); // suma
    expect(semanas[1].temp).toBe(30);
  });

  it("promedia solo los días válidos y cuenta los faltantes para avisar", () => {
    const dias: DayData[] = [
      { date: "20261102", temp: 26, precip: 1 },
      { date: "20261103", temp: null, precip: null },
      { date: "20261104", temp: 30, precip: 2 },
    ];

    const semanas = toWeekly(dias);

    expect(semanas[0].temp).toBe(28); // (26+30)/2, nunca toca el null
    expect(semanas[0].days).toBe(3); // total de la semana
    expect(semanas[0].missing).toBe(1); // esto dispara el aviso
  });
});

describe("filterAnnualKey", () => {
  it("elimina la clave anual xx13 de los datos mensuales", () => {
    const mensual: Record<string, number> = {
      "202501": 26.81,
      "202513": 25.63, // promedio anual, no es un mes
    };

    expect(filterAnnualKey(mensual)).toEqual(["202501"]);
  });
});
