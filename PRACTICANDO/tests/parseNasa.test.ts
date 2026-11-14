import { describe, it, expect } from "vitest";
import { parseNasaResponse } from "../lib/parseNasa";

describe("parseNasaResponse", () => {
  it("convierte la respuesta de la NASA en una lista diaria", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "20261101": 32.61, "20261102": 33.1 },
          PRECTOTCORR: { "20261101": 0, "20261102": 1.92 },
        },
      },
    };

    expect(parseNasaResponse(respuesta)).toEqual([
      { date: "20261101", temp: 32.61, precip: 0 },
      { date: "20261102", temp: 33.1, precip: 1.92 },
    ]);
  });

  it("lee T2M_MAX (la máxima del día), no el promedio T2M", () => {
    // El 2026-11-01 la NASA reporta T2M=26.55 y T2M_MAX=32.61.
    // La app promete "la temperatura más alta", así que debe leer T2M_MAX.
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "20261101": 32.61 },
          PRECTOTCORR: { "20261101": 0 },
        },
      },
    };

    expect(parseNasaResponse(respuesta)[0].temp).toBe(32.61);
  });

  it("convierte el relleno -999 en null (dato no disponible)", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "20261101": -999 },
          PRECTOTCORR: { "20261101": -999 },
        },
      },
    };

    expect(parseNasaResponse(respuesta)).toEqual([
      { date: "20261101", temp: null, precip: null },
    ]);
  });

  it("ordena los días cronológicamente aunque lleguen desordenados", () => {
    const respuesta = {
      properties: {
        parameter: {
          T2M_MAX: { "20261103": 30, "20261101": 28, "20261102": 29 },
          PRECTOTCORR: { "20261103": 0, "20261101": 0, "20261102": 0 },
        },
      },
    };

    expect(parseNasaResponse(respuesta).map((d) => d.date)).toEqual([
      "20261101",
      "20261102",
      "20261103",
    ]);
  });
});
