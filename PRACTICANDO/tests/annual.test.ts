import { describe, it, expect } from "vitest";
import { pickAnnualKey } from "../lib/aggregate";

describe("pickAnnualKey", () => {
  it("devuelve solo los promedios anuales xx13", () => {
    const mensual: Record<string, number> = {
      "202501": 26.81,
      "202502": 27.92,
      "202513": 25.63,
      "202613": 26.94,
    };

    expect(pickAnnualKey(mensual)).toEqual([
      { year: "2025", temp: 25.63 },
      { year: "2026", temp: 26.94 },
    ]);
  });

  it("ignora los -999 de años sin datos", () => {
    const mensual: Record<string, number> = { "202613": -999 };

    expect(pickAnnualKey(mensual)).toEqual([]);
  });
});
