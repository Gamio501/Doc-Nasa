import { describe, it, expect } from "vitest";
import { validateQuery } from "../lib/validate";

const base = { lat: "-4.90", lon: "-80.68", start: "20261020", end: "20261108" };

describe("validateQuery", () => {
  it("acepta una consulta diaria válida", () => {
    expect(validateQuery(base, "dias")).toBeNull();
  });

  it("rechaza latitud fuera de rango", () => {
    expect(validateQuery({ ...base, lat: "999" }, "dias")).toContain("latitud");
  });

  it("rechaza latitud que no es número", () => {
    expect(validateQuery({ ...base, lat: "abc" }, "dias")).toContain("latitud");
  });

  it("rechaza longitud fuera de rango", () => {
    expect(validateQuery({ ...base, lon: "-999" }, "dias")).toContain("longitud");
  });

  it("rechaza fecha con guiones (pide AAAAMMDD)", () => {
    expect(validateQuery({ ...base, start: "2026-11-01" }, "dias")).toContain("AAAA");
  });

  it("rechaza fecha imposible como 20261345", () => {
    expect(validateQuery({ ...base, start: "20261345" }, "dias")).toBeTruthy();
  });

  it("rechaza cuando la fecha de fin es anterior a la de inicio", () => {
    expect(
      validateQuery({ ...base, start: "20261108", end: "20261020" }, "dias")
    ).toContain("fin");
  });

  it("rechaza rangos diarios de más de 366 días", () => {
    expect(validateQuery({ ...base, start: "20200101", end: "20261108" }, "dias")).toContain("366");
  });

  it("permite un solo día (inicio igual a fin)", () => {
    expect(validateQuery({ ...base, start: "20261108", end: "20261108" }, "dias")).toBeNull();
  });

  it("rechaza años invertidos en la vista de meses", () => {
    expect(validateQuery({ ...base, start: "20260101", end: "20250101" }, "meses")).toContain("año");
  });

  it("permite rangos largos en la vista de meses (no aplica el tope de 366)", () => {
    expect(validateQuery({ ...base, start: "20200101", end: "20261108" }, "meses")).toBeNull();
  });
});
