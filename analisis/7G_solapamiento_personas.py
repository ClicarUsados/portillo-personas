"""7G - Solapamiento de respondentes entre familias de miedo (P1-P5) y entre MdV.

Auditoría MdV, 2026-11-23. Mide cuántos respondentes comparten las familias que
sostienen P1 a P5 dentro de cada encuesta. NO hay clave de respondente entre
encuestas, así que el solapamiento solo se mide dentro de cada archivo.

Definiciones (idénticas a research/06_arquetipos_cliente.md):
  Detractor = NPS 0-6 (umot_01.categoria_nps).
  FMOT (venta) y SMOT (taller): detractor y nota <=2 (venta) o <=3 (taller).
  UMOT: pool = detractor OR volver en {"No", "No sé"}; ítem <=2 dentro del pool.

Solo lee inputs_clean/ (vía umot_01.cargar_todo). Imprime conteos, no filas ni texto.
Cómo reproducirlo: python3 analisis/7G_solapamiento_personas.py
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from umot_01_recomendacion_retorno import (  # noqa: E402
    NPS_COL, VOLVER_COL, cargar_todo, categoria_nps,
)

PERSONAS = ["P1", "P2", "P3", "P4", "P5"]
MAPA_VENTA = {
    "P1": "Fluidez general del proceso",
    "P2": "Facilidad de comunicación con vendedor",
    "P3": "Claridad de precios y opciones de financiamiento",
    "P4": "Información proporcionada por vendedor",
    "P5": "Atención del vendedor",
}
MAPA_UMOT_VENTA = {
    "P1": "Fluidez general del proceso",
    "P2": "Facilidad de comunicación con vendedor",
    "P3": "Claridad de precios y opciones de financiamiento",
    "P5": "Acogida en sala de ventas",
}
# Mecánica: posiciones de columna (ver analisis/smot_mecanica.py DRIVERS y umot_01 ITEMS)
MAPA_SMOT_MEC = {"P1": 28, "P2": 26, "P3": 24, "P4": 25, "P5": 23}
MAPA_UMOT_MEC = {"P1": 27, "P2": 26, "P3": 24, "P4": 25, "P5": 22}


def num(s):
    return pd.to_numeric(s, errors="coerce")


def detractor(df, enc):
    return categoria_nps(df[NPS_COL[enc]]) == "Detractor"


def pool_umot(df, enc):
    return detractor(df, enc) | df[VOLVER_COL[enc]].astype(str).isin(["No", "No sé"])


def familias(df, enc):
    """Devuelve {(persona, mdv): Series booleana}."""
    fam = {}
    det = detractor(df, enc)
    pool = pool_umot(df, enc)
    if enc == "Mecanica":
        for p, i in MAPA_SMOT_MEC.items():
            fam[(p, "SMOT")] = det & (num(df.iloc[:, i]) <= 3)
        for p, i in MAPA_UMOT_MEC.items():
            fam[(p, "UMOT")] = pool & (num(df.iloc[:, i]) <= 2)
        return fam
    cols_fmot = dict(MAPA_VENTA)
    if enc == "VentaUsados":
        cols_fmot.pop("P4")  # no hay columna equivalente en Usados
    for p, col in cols_fmot.items():
        fam[(p, "FMOT")] = det & (num(df[col]) <= 2)
    for p, col in MAPA_UMOT_VENTA.items():
        fam[(p, "UMOT")] = pool & (num(df[col]) <= 2)
    return fam


def main():
    fuentes = cargar_todo()
    nombres = {"Mecanica": "Mecánica (SMOT/UMOT)", "VentaNuevo": "Venta-Nuevo (FMOT/UMOT)",
               "VentaUsados": "Venta-Usados (FMOT/UMOT)"}
    print("7G - Solapamiento de respondentes | extracción 2026-11-23")
    print("Solo dentro de cada archivo: no hay clave de respondente entre archivos.\n")
    resumen = {}
    for enc in ["VentaNuevo", "VentaUsados", "Mecanica"]:
        df = fuentes[enc]
        fam = familias(df, enc)
        det = detractor(df, enc)
        pool = pool_umot(df, enc)
        print(f"### {nombres[enc]} | filas={len(df)} | detractores={int(det.sum())} | pool UMOT={int(pool.sum())}")
        for (p, mdv), m in sorted(fam.items()):
            print(f"  {p} {mdv}: n={int(m.sum())}")
        # Conjuntos por persona (unión de sus MdV dentro del archivo)
        sets = {}
        for p in PERSONAS:
            idx = set()
            for (pp, _), m in fam.items():
                if pp == p:
                    idx |= set(df.index[m.values])
            sets[p] = idx
            print(f"  respondentes únicos {p} (unión de sus MdV en este archivo): {len(idx)}")
        # Solapamiento entre personas
        print("  Solapamiento entre personas (|Pi ∩ Pj|):")
        for i, a in enumerate(PERSONAS):
            for b in PERSONAS[i + 1:]:
                inter = len(sets[a] & sets[b])
                if inter:
                    print(f"    {a} ∩ {b} = {inter}")
        conteo = {}
        for p in PERSONAS:
            for q in sets[p]:
                conteo[q] = conteo.get(q, 0) + 1
        n_multi = sum(1 for v in conteo.values() if v >= 2)
        n_tri = sum(1 for v in conteo.values() if v >= 3)
        print(f"  respondentes en >=2 personas: {n_multi} | en >=3 personas: {n_tri} | total en alguna persona: {len(conteo)}")
        # Solapamiento dentro de cada persona entre MdV de detractor y UMOT
        print("  Dentro de cada persona: MdV detractor vs UMOT (pool)")
        mdv_det = "FMOT" if enc != "Mecanica" else "SMOT"
        for p in PERSONAS:
            if (p, mdv_det) not in fam or (p, "UMOT") not in fam:
                continue
            a = set(df.index[fam[(p, mdv_det)].values])
            b = set(df.index[fam[(p, "UMOT")].values])
            print(f"    {p}: {mdv_det}={len(a)} | UMOT={len(b)} | en ambos={len(a & b)} "
                  f"| {mdv_det} sin UMOT={len(a - b)} | UMOT sin {mdv_det}={len(b - a)}")
        resumen[enc] = {"det": int(det.sum()), "pool": int(pool.sum()), "multi": n_multi}
        print()
    print("### Totales (suma de archivos; NO son personas únicas, no hay clave entre archivos)")
    for enc, v in resumen.items():
        print(f"  {enc}: detractores={v['det']} | pool UMOT={v['pool']} | respondentes en >=2 personas={v['multi']}")


if __name__ == "__main__":
    main()
