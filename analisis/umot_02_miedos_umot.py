"""UMOT 02 - Miedos y frustraciones en el pool UMOT (se va / no recomienda).

Subagente D (UMOT + demografía), Portillo (Grupo Americar, Chile). Extracción 2026-11-23.
Pool UMOT por encuesta = Detractor (NPS 0-6) OR volver = "No" OR volver = "No sé".
Un ítem de escala 1-5 con valor <=2 se toma como indicador de frustración/miedo.
[HIPÓTESIS] La etiqueta de miedo es interpretación de la calificación baja, no dato declarado.
Fuentes: inputs_clean/*.parquet (Mecánica, Venta-Nuevo, Venta-Usados, Clicar).
Universos: GRUPO_COMPLETO y PORTILLO_HIPOTESIS (\\bPORT; BLOQUEADO: Beto / Iván Balaguera).
Imprime conteos; sin texto libre salvo la opción --citas (ver abajo).

Cómo reproducirlo: python3 analisis/umot_02_miedos_umot.py
"""
import glob
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "2026-11-23"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from umot_01_recomendacion_retorno import (  # noqa: E402
    ITEMS, NPS_COL, SUC_COL, VOLVER_COL, categoria_nps, cargar, pct,
)

FEAR_LABEL = {  # (encuesta, item) -> miedo candidato
    ("Mecanica", "Claridad precios"): "Miedo a costos poco claros",
    ("Mecanica", "Claridad reparación"): "Miedo a reparación no explicada",
    ("Mecanica", "Calidad servicio"): "Miedo a trabajo mal hecho",
    ("Mecanica", "Comunicación"): "Miedo a quedar sin respuesta",
    ("Mecanica", "Fluidez"): "Miedo a proceso largo o desordenado",
    ("Mecanica", "Acogida sala espera"): "Miedo a mal trato en recepción",
    ("VentaNuevo", "Claridad precios/financ."): "Miedo a precio o financiamiento poco claro",
    ("VentaNuevo", "Comunicación vendedor"): "Miedo a vendedor inaccesible",
    ("VentaNuevo", "Fluidez"): "Miedo a proceso de entrega largo",
    ("VentaNuevo", "Acogida sala"): "Miedo a mal trato en sala",
    ("VentaUsados", "Claridad precios/financ."): "Miedo a precio o financiamiento poco claro",
    ("VentaUsados", "Comunicación vendedor"): "Miedo a vendedor inaccesible",
    ("VentaUsados", "Fluidez"): "Miedo a proceso de entrega largo",
    ("VentaUsados", "Acogida sala"): "Miedo a mal trato en sala",
    ("Clicar", "Claridad oferta final"): "Miedo a oferta baja o poco clara",
    ("Clicar", "Facilidad vender"): "Miedo a trámite complicado para vender",
    ("Clicar", "Comunicación"): "Miedo a quedar sin respuesta",
    ("Clicar", "Rapidez"): "Miedo a demora en la venta",
}
FUENTE = {"Mecanica": "CR_2025-Mecánica", "VentaNuevo": "CR_2025-Venta-Nuevo",
          "VentaUsados": "CR_2025-Venta-Usados", "Clicar": "CR_Clicar"}
SUC_FILTRO = {"Mecanica": "nombre_sucursal", "VentaNuevo": "nombre_concesionario",
              "VentaUsados": "nombre_concesionario", "Clicar": "nombre_sucursal"}


def pool_umot(df, enc):
    cat = categoria_nps(df[NPS_COL[enc]])
    volver = df[VOLVER_COL[enc]].astype(str)
    return (cat == "Detractor") | volver.isin(["No", "No sé"])


def main():
    conteo = {}  # miedo -> {enc: n}
    print(f"UMOT 02 - Miedos en pool UMOT | extracción {FECHA}")
    for enc in FUENTE:
        df = cargar(FUENTE[enc] + "_*")
        pool = pool_umot(df, enc)
        suc = df[SUC_FILTRO[enc]].fillna("").astype(str)
        porte = suc.str.contains(r"\bPORT", case=False, regex=True)
        print(f"\n### {enc} | pool UMOT GRUPO={int(pool.sum())} ({pct(pool.sum(), len(df)):.1f}% de filas) "
              f"| pool UMOT PORTILLO_HIPOTESIS={int((pool & porte).sum())}")
        for item, col in ITEMS[enc].items():
            v = pd.to_numeric(df[col], errors="coerce")
            bajo = pool & (v <= 2)
            n_pool = int(pool.sum())
            n_bajo = int(bajo.sum())
            miedo = FEAR_LABEL[(enc, item)]
            conteo.setdefault(miedo, {})[enc] = n_bajo
            print(f"  {miedo} [{item}]: <=2 en pool n={n_bajo} ({pct(n_bajo, n_pool):.1f}%) "
                  f"| PORTILLO_HIPOTESIS n={int((bajo & porte).sum())}")
        # Sentimiento negativo del motivo, dentro del pool
        if "sentimiento" in df.columns:
            neg = pool & (df["sentimiento"] == "Negative")
            print(f"  Motivo NPS con sentimiento Negative dentro del pool: n={int(neg.sum())} "
                  f"({pct(neg.sum(), pool.sum()):.1f}% del pool)")
    print("\n### Ranking por n total (todas las encuestas, GRUPO_COMPLETO) [sesgo: Mecánica domina por volumen]")
    total = sorted(((sum(d.values()), m, d) for m, d in conteo.items()), reverse=True)
    for n_tot, miedo, d in total:
        detalle = ", ".join(f"{k}={v}" for k, v in d.items() if v)
        print(f"  n={n_tot:6d} | {miedo} | {detalle}")


if __name__ == "__main__":
    main()
