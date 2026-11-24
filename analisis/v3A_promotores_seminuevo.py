"""Subagente A (v3 cliente ideal): promotores de Venta-Usados en el universo Portillo.

Cómo reproducirlo: python3 analisis/v3A_promotores_seminuevo.py

Entrada: inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet
Regla A (principal): campaña == "2025 - Venta Usados Portillo" (114 filas).
Regla B (comparación): nombre_concesionario contiene "PORT" (145 filas).
Promotor: NPS (recomendación) en 9 o 10.
Solo conteos y medias por etapa. No imprime texto libre salvo la bandera --verbatims.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "inputs_clean" / "CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet"
NPS = "En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?"
REASON = "¿Qué te motiva a dar esa puntuación?"
STAGES = [
    "Acogida en sala de ventas",
    "Atención del vendedor",
    "Claridad de precios y opciones de financiamiento",
    "Facilidad de comunicación con vendedor",
    "Fluidez general del proceso",
    "Vehículo en parte de pago",
]
MACRO_COLS = ["Macrocategoría 1", "Macrocategoría 2", "Macrocategoría 3", "Macrocategoría 4", "Macrocategoría 5"]
MIN_N = 30
FECHA_CORTE = "2026-11-23"


def load() -> pd.DataFrame:
    return pd.read_parquet(PARQUET)


def universes(df: pd.DataFrame) -> dict[str, pd.Series]:
    camp = df["campaña o sensor"].fillna("").str.strip()
    suc = df["nombre_concesionario"].fillna("").str.upper()
    rule_a = camp.eq("2025 - Venta Usados Portillo")
    rule_b = suc.str.contains("PORT", regex=False)
    return {"A_campana": rule_a, "B_sucursal_PORT": rule_b}


def scores(df: pd.DataFrame) -> pd.Series:
    """Devuelve la nota NPS como serie numérica."""
    return pd.to_numeric(df[NPS], errors="coerce")


def main(show_verbatims: bool = False) -> None:
    df = load()
    print(f"Filas totales Venta-Usados: {len(df)} · fecha de corte {FECHA_CORTE}")
    unis = universes(df)
    for name, mask in unis.items():
        sub = df[mask]
        nps = scores(sub)
        prom = sub[nps >= 9]
        det = sub[nps <= 6]
        print(f"\n== Regla {name}: n={len(sub)} · promotores 9-10={len(prom)} · detractores 0-6={len(det)} · "
              f"fecha respuesta {sub['fecha respuesta'].min()} a {sub['fecha respuesta'].max()}")
        print("  Promotores por nombre_concesionario:")
        for suc, n in prom["nombre_concesionario"].value_counts().items():
            flag = "  [n<30: no concluir por sucursal]" if n < MIN_N else ""
            print(f"    {suc}: {n}{flag}")
        print("  NPS distribución:", nps.value_counts(dropna=False).sort_index().to_dict())

    # Universo principal: regla A
    sub = df[unis["A_campana"]]
    prom = sub[scores(sub) >= 9]
    print(f"\n== Universo principal (regla A) · promotores n={len(prom)} · no-promotores n={len(sub) - len(prom)}")

    print("\n-- Macrocategorías que mencionan los promotores (presencia en al menos una columna, % de promotores)")
    cats = pd.unique(prom[MACRO_COLS].stack().dropna())
    for cat in cats:
        rows = prom.index[prom[MACRO_COLS].eq(cat).any(axis=1)]
        print(f"   {cat}: {len(rows)} ({len(rows) / len(prom):.1%})")
    print(f"   Filas con al menos una macrocategoría: {prom[MACRO_COLS].notna().any(axis=1).sum()}")

    print("\n-- Notas por etapa (media 1-5 y % de 5) · promotores vs no-promotores")
    other = sub[scores(sub) < 9]
    for st in STAGES:
        p = pd.to_numeric(prom[st], errors="coerce")
        o = pd.to_numeric(other[st], errors="coerce")
        if st == "Vehículo en parte de pago":
            na = (prom[st].astype(str).str.strip().str.lower() == "no aplica").sum()
            pn = p.dropna()
            print(f"   {st}: 'No aplica' en {na} promotores ({na / len(prom):.1%}); "
                  f"entre quienes aplica n={len(pn)}, media {pn.mean():.2f}, %5 {(pn == 5).mean():.1%}")
            continue
        print(f"   {st}: promotores n={p.notna().sum()} media {p.mean():.2f} %5 {(p == 5).mean():.1%} · "
              f"no-promotores n={o.notna().sum()} media {o.mean():.2f} %5 {(o == 5).mean():.1%}")

    print("\n-- Cómo llegó (promotores)")
    print("  ", prom["¿Cómo llegaste a #empresa# para comprar tu auto?"].value_counts(dropna=False).to_dict())
    print("-- Volvería a comprar (promotores)")
    print("  ", prom["Dada tu reciente experiencia de compra, ¿Volverías a comprar en #empresa#?"].value_counts(dropna=False).to_dict())
    print("-- Sentimiento de la razón (promotores)")
    print("  ", prom["sentimiento"].value_counts(dropna=False).to_dict())

    print("\n-- Regla B fuera de la regla A (filas PORT en sucursal que no están en la campaña)")
    extra = df[unis["B_sucursal_PORT"] & ~unis["A_campana"]]
    print(f"   n={len(extra)} · promotores={int((scores(extra) >= 9).sum())} · "
          f"fechas {extra['fecha respuesta'].min()} a {extra['fecha respuesta'].max()}")
    print("   campañas:", extra["campaña o sensor"].value_counts().to_dict())

    if show_verbatims:
        print("\n-- Razones de promotores (row_id | nota | texto) — revisar antes de citar")
        for _, r in prom.iterrows():
            txt = r[REASON]
            if isinstance(txt, str) and txt.strip():
                print(f"{r['row_id']} | {int(scores(r.to_frame().T).iloc[0])} | {txt.strip()}")


if __name__ == "__main__":
    main(show_verbatims="--verbatims" in sys.argv)
