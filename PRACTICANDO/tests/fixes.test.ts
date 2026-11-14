import { describe, it, expect } from "vitest";
import { toWeekly, resolveYearRange } from "../lib/aggregate";
import { sortPoints, type Point } from "../lib/sort";
import type { DayData } from "../lib/parseNasa";

describe("toWeekly", () => {
  it("redondea el promedio a un decimal para no mostrar 27.03666666666666", () => {
    const dias: DayData[] = [
      { date: "20261102", temp: 26.55, precip: 1 },
      { date: "20261103", temp: 27.47, precip: 3 },
      { date: "20261104", temp: 26.61, precip: 0 },
    ];

    const semanas = toWeekly(dias);

    expect(semanas[0].temp).toBe(26.9); // 26.8766... → 26.9
    expect(String(semanas[0].temp).length).toBeLessThanOrEqual(4);
  });
});

describe("resolveYearRange", () => {
  it("recorta el año actual porque aún no está completo", () => {
    const r = resolveYearRange("2020", "2026", 2026);

    expect(r.start).toBe("2020");
    expect(r.end).toBe("2025");
    expect(r.note).toContain("2025");
  });

  it("devuelve error si no queda ningún año completo", () => {
    const r = resolveYearRange("2026", "2026", 2026);

    expect(r.error).toBeTruthy();
    expect(r.start).toBeUndefined();
  });

  it("no toca nada si el rango ya son años completos", () => {
    const r = resolveYearRange("2020", "2025", 2026);

    expect(r.start).toBe("2020");
    expect(r.end).toBe("2025");
    expect(r.note).toBeUndefined();
    expect(r.error).toBeUndefined();
  });
});

describe("sortPoints", () => {
  it("ordena las fechas en orden real, no alfabético", () => {
    const points: Point[] = [
      { label: "01/11/2026", sortLabel: "20261101", temp: 26.5 },
      { label: "20/10/2026", sortLabel: "20261020", temp: 25.8 },
      { label: "31/10/2026", sortLabel: "20261031", temp: 25.4 },
    ];

    const orden = sortPoints(points, "label", true).map((p) => p.label);

    // 20/10 viene antes que 31/10 que viene antes que 01/11
    expect(orden).toEqual(["20/10/2026", "31/10/2026", "01/11/2026"]);
  });

  it("ordena los meses de enero a diciembre, no alfabéticamente", () => {
    const points: Point[] = [
      { label: "Abr 2026", sortLabel: "202604", temp: 28.11 },
      { label: "Ene 2026", sortLabel: "202601", temp: 26.64 },
      { label: "Feb 2026", sortLabel: "202602", temp: 27.64 },
    ];

    const orden = sortPoints(points, "label", true).map((p) => p.label);

    expect(orden).toEqual(["Ene 2026", "Feb 2026", "Abr 2026"]);
  });

  it("ordena de mayor a menor con los vacíos al final", () => {
    const points: Point[] = [
      { label: "a", sortLabel: "1", temp: 25 },
      { label: "b", sortLabel: "2", temp: null },
      { label: "c", sortLabel: "3", temp: 30 },
    ];

    const orden = sortPoints(points, "temp", false).map((p) => p.temp);

    expect(orden).toEqual([30, 25, null]);
  });
});
