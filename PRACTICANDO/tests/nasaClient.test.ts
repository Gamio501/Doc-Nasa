import { describe, it, expect, vi, afterEach } from "vitest";
import { fetchWeatherData, fetchMonthlyData, NasaError } from "../lib/nasaClient";

afterEach(() => {
  vi.unstubAllGlobals();
});

const dailyBody = {
  properties: { parameter: { T2M_MAX: { "20261020": 32.6 }, PRECTOTCORR: { "20261020": 1.5 } } },
};

describe("fetchWeatherData", () => {
  it("arma la URL diaria con la ubicación, fechas y parámetros", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => dailyBody });
    vi.stubGlobal("fetch", fetchMock);

    await fetchWeatherData("-4.90", "-80.68", "20261020", "20261108");

    const url = fetchMock.mock.calls[0][0] as string;
    expect(url).toContain("/api/temporal/daily/point");
    expect(url).toContain("latitude=-4.90");
    expect(url).toContain("longitude=-80.68");
    expect(url).toContain("start=20261020");
    expect(url).toContain("end=20261108");
    expect(url).toContain("parameters=T2M_MAX");
    expect(url).toContain("community=AG");
  });

  it("lanza NasaError con el motivo real cuando la NASA responde 422", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({ messages: ["The end date is greater then start date"] }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(fetchWeatherData("-4.90", "-80.68", "20261108", "20261020")).rejects.toThrow(
      NasaError
    );
    await expect(fetchWeatherData("-4.90", "-80.68", "20261108", "20261020")).rejects.toThrow(
      /fin.*anterior|anterior.*fin/i
    );
  });

  it("devuelve la temperatura máxima, no el promedio", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => dailyBody }));

    const datos = await fetchWeatherData("-4.90", "-80.68", "20261020", "20261108");

    expect(datos[0].temp).toBe(32.6);
  });
});

describe("fetchMonthlyData", () => {
  it("arma la URL mensual pidiendo AÑOS, no fechas", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ properties: { parameter: { T2M_MAX: {}, PRECTOTCORR: {} } } }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await fetchMonthlyData("-4.90", "-80.68", "2020", "2026");

    const url = fetchMock.mock.calls[0][0] as string;
    expect(url).toContain("/api/temporal/monthly/point");
    expect(url).toContain("start=2020");
    expect(url).toContain("end=2026");
  });
});
