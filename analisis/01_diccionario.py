"""
Fase 0 — Diccionario de datos desde inputs_clean/*.parquet
Escribe research/00_diccionario_datos.md (solo conteos; sin filas crudas).

Cómo reproducirlo (desde la raíz del proyecto):
    python3 analisis/00_anonimizar.py   # primero
    python3 analisis/01_diccionario.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "inputs_clean"
OUT = ROOT / "research" / "00_diccionario_datos.md"

KEY_COLS = ["des_marca", "marca", "marca_sucursal", "nombre_sucursal", "nombre_concesionario",
            "concesionario", "tipo_oportunidad", "tipo_de_cuenta", "area_de_negocio", "grupo", "empresa"]
NULL_COLS = ["fecha respuesta", "fecha", "fec_factura", "fecha_pa", "fecha_cierre_ot",
             "nps", "sentimiento", "Macrocategoría 1", "Microcategoría 1"]


def fecha_rango(df: pd.DataFrame) -> str:
    for col in ["fecha respuesta", "fecha", "fec_factura", "fecha_pa"]:
        if col in df.columns:
            s = pd.to_datetime(df[col], errors="coerce", format="mixed")
            if s.notna().any():
                return f"{col}: {s.min():%Y-%m-%d} a {s.max():%Y-%m-%d} (válidas {s.notna().sum()})"
    return "sin columna de fecha reconocible"


def section(path: Path) -> list[str]:
    df = pd.read_parquet(path)
    lines = [f"## {path.name}", "", f"- Filas: **{len(df)}** | Columnas: {len(df.columns)}",
             f"- Rango de fechas: {fecha_rango(df)}"]
    nulls = [c for c in NULL_COLS if c in df.columns]
    if nulls:
        lines.append("- Nulos en columnas relevantes:")
        for c in nulls:
            lines.append(f"  - `{c}`: {df[c].isna().sum()} ({df[c].isna().mean():.1%})")
    for c in KEY_COLS:
        if c in df.columns:
            vc = df[c].fillna("<vacío>").value_counts().head(15)
            lines.append(f"- Valores de `{c}` (top 15, {df[c].nunique(dropna=False)} únicos):")
            for val, n in vc.items():
                lines.append(f"  - {val}: {n}")
    lines.append("")
    return lines


def main() -> None:
    header = ["# Diccionario de datos — Fase 0", "",
              "Fuente: inputs_clean/*.parquet (generados por analisis/00_anonimizar.py desde inputs_raw/).",
              "Fecha de extracción de los archivos: 2026-11-23.", "",
              "## Estado de CASOS_PBI__2_.xlsx (hojas Case / Hoja1)", "",
              "**NO VERIFICADO / BLOQUEADO.** El archivo no está en inputs_raw/ (no se encontró en el home ",
              "del usuario al buscar CASOS_PBI*.xlsx). Dependencia: Beto (entregar el archivo). ",
              "La validación de Hoja1 (empresa, area_negocio, motivo_reclamo en 0.0; ciudad vacía) queda ",
              "pendiente hasta tener el archivo.", ""]
    body: list[str] = []
    for p in sorted(CLEAN.glob("*.parquet")):
        body += section(p)
    OUT.write_text("\n".join(header + body), encoding="utf-8")
    print(f"Escrito: {OUT} ({len(body)} líneas)")


if __name__ == "__main__":
    main()
