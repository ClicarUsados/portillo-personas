"""
Fase 0 — Mapeo tentativo de Portillo dentro de los inputs (hipótesis, no confirmada).
Escribe research/00_mapeo_portillo.md con conteos por prefijo de sucursal/concesionario.

Universos:
  PORTILLO_HIPOTESIS  = registros cuyo nombre de sucursal/concesionario contiene "PORT" como token
                        (PORT TOYOTA ..., ..., PORTILLO) — evidencia explícita, pero no confirmada.
  GRUPO_COMPLETO      = todo el archivo (Grupo Americar, todas las marcas/sucursales).
Lo que no aparece como PORT* queda fuera de PORTILLO_HIPOTESIS. Confirmar con Beto / Iván Balaguera.

Cómo reproducirlo (desde la raíz del proyecto):
    python3 analisis/02_mapeo_portillo.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "inputs_clean"
OUT = ROOT / "research" / "00_mapeo_portillo.md"

BRANCH_COLS = ["nombre_concesionario", "nombre_sucursal"]
PORT_RE = re.compile(r"(^|\s)PORT(\s|$)|PORTILLO", re.IGNORECASE)
GROUP_PREFIXES = ["SAIS", "DENALI", "COSE", "GAP", "ACSA", "PORT", "PRE", "FLOTA", "USADOS", "SALAZAR", "ALESSANDRI"]


def branch_series(df: pd.DataFrame) -> pd.Series:
    for col in BRANCH_COLS:
        if col in df.columns and df[col].notna().any():
            return df[col].fillna("").astype(str).str.strip().str.upper()
    return pd.Series([""] * len(df))


def main() -> None:
    lines = ["# Mapeo Portillo — Fase 0 (HIPÓTESIS)", "",
             "Fuente: inputs_clean/*.parquet. Fecha de extracción de los archivos: 2026-11-23.", "",
             "**Estado: [HIPÓTESIS] — BLOQUEADO.** Ninguna fuente marca explícitamente a Portillo como grupo. ",
             "Confirmación requerida: Beto / Iván Balaguera (qué sucursales y marcas pertenecen a Portillo).", "",
             "## Conteo por archivo", "",
             "| Archivo | Filas | Filas PORTILLO_HIPOTESIS | % | Columna usada |",
             "|---|---:|---:|---:|---|"]
    prefix_lines: list[str] = []
    for f in sorted(CLEAN.glob("*.parquet")):
        df = pd.read_parquet(f)
        br = branch_series(df)
        mask = br.map(lambda s: bool(PORT_RE.search(s)))
        col = next((c for c in BRANCH_COLS if c in df.columns and df[c].notna().any()), "NINGUNA")
        name = f.name.split("__")[0][:45]
        pct = (mask.mean() * 100) if len(df) else 0.0
        lines.append(f"| {name} | {len(df)} | {int(mask.sum())} | {pct:.1f}% | {col} |")
        if mask.any():
            top = br[mask].value_counts().head(10)
            prefix_lines.append(f"### {name}")
            prefix_lines += [f"- `{k}`: {v}" for k, v in top.items()]
            prefix_lines.append("")
        counts = br.str.split().str[0].value_counts()
        known = {p: int(counts.get(p, 0)) for p in GROUP_PREFIXES}
        prefix_lines.append(f"Primer token por prefijo en {name}: {known}")
        prefix_lines.append("")

    lines += ["", "## Sucursales/concesionarios que contienen PORT / PORTILLO (top 10 por archivo)", ""]
    lines += prefix_lines
    lines += ["", "## Dudas abiertas (BLOQUEOS)", "",
              "- **Bloqueado:** confirmar si PORT TOYOTA*, MG PLAZA EGAÑA PORTILLO, etc. son Portillo. Depende de: Beto / Iván Balaguera.",
              "- **Bloqueado:** prefijos SAIS, DENALI, COSE, GAP, ACSA (¿otras empresas del holding? ¿marcas?). Depende de: Beto / Iván Balaguera.",
              "- **Regla:** SAIS y Clicar son hermanas de grupo, no competencia. Competencia externa = resto del mercado.",
              "- **Venta-Usados:** `nombre_sucursal` y `marca_sucursal` vienen vacíos; el mapeo usa `nombre_concesionario` (sí poblado).",
              "- **Lead-Portillo:** `nombre_sucursal` contiene PORTILLO explícito en varias filas; el archivo se llama Lead-Portillo pero no todas sus filas son necesariamente Portillo (p. ej. 'GAP COSTANERA CENTER PEUGEOT'). [HIPÓTESIS]",
              "", "## Universos de trabajo", "",
              "- **PORTILLO_HIPOTESIS**: filas con PORT/PORTILLO en nombre de sucursal/concesionario (tabla arriba).",
              "- **GRUPO_COMPLETO**: todo el archivo, marcado como Grupo Americar.",
              "- Cada reporte debe declarar cuál universo usa."]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Escrito: {OUT}")


if __name__ == "__main__":
    main()
