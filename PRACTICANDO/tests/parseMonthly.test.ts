import { describe, it, expect } from "vitest";
import { parseMonthlyResponse } from "../lib/parseMonthly";

describe("parseMonthlyResponse", () => {
  it("convierte los meses a una lista ordenada cronológicamente", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "202501": 31.81, "202502": 32.92 },
          PRECTOTCORR: { "202501": 0.39, "202502": 1.24 },
        },
      },
    };

    expect(parseMonthlyResponse(respuesta)).toEqual([
      { date: "202501", temp: 31.81, precip: 0.39 },
      { date: "202502", temp: 32.92, precip: 1.24 },
    ]);
  });

  it("descarta el promedio anual xx13 para que no aparezca como mes 13", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "202501": 31.81, "202513": 30.63 },
          PRECTOTCORR: { "202501": 0.39, "202513": 0.66 },
        },
      },
    };

    expect(parseMonthlyResponse(respuesta)).toEqual([
      { date: "202501", temp: 31.81, precip: 0.39 },
    ]);
  });

  it("convierte el relleno -999 en null", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "202610": -999 },
          PRECTOTCORR: { "202610": -999 },
        },
      },
    };

    expect(parseMonthlyResponse(respuesta)).toEqual([
      { date: "202610", temp: null, precip: null },
    ]);
  });
});
