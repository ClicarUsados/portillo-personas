#!/usr/bin/env python3
"""SMOT (subagente C): NPS de taller, drivers por etapa, reparación fallida y motivos.

Fuente: inputs_clean/CR_2025-Mecánica_*.parquet (solo inputs_clean, nunca inputs_raw).
Cómo reproducirlo: python3 analisis/smot_mecanica.py
Opcional: python3 analisis/smot_mecanica.py --citas-out RUTA_FUERA_DEL_PROYECTO

Imprime solo conteos y porcentajes. Las citas (si se piden) se escriben a un archivo
externo al proyecto, anonimizadas y de <=15 palabras, para revisión manual.
"""
import argparse
import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
ARCHIVO = RAIZ / "inputs_clean" / "CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet"
FECHA = "2026-11-23"

# Posiciones de columna (nombres con caracteres especiales; se accede por índice)
I_FECHA_RESP = 5
I_NPS = 9
I_MOTIVO = 10
I_MICRO1 = 12
I_MACRO1 = 13
I_REPARADO = 33
I_VOLVERIA = 34
I_NOMBRE_SUC = 46
I_DES_MARCA = 53
DRIVERS = {
    22: "Acogida en sala de espera",
    23: "Atención de personal",
    24: "Claridad precios y costos",
    25: "Claridad reparación/mantenimiento",
    26: "Facilidad para comunicarse",
    27: "Fluidez general del proceso",
    28: "Tiempo de entrega del vehículo",
    29: "Calidad del servicio realizado",
}
SEGMENTOS = ["Detractor", "Pasivo", "Promotor"]
PALABRAS_MAX = 15


def pct(parte, total):
    return 100.0 * parte / total if total else float("nan")


def segmento(nps: pd.Series) -> pd.Series:
    return pd.cut(nps, bins=[-1, 6, 8, 10], labels=SEGMENTOS).astype(str)


def universos(df: pd.DataFrame) -> dict:
    suc = df.iloc[:, I_NOMBRE_SUC].fillna("").str.upper()
    return {
        "GRUPO_COMPLETO": pd.Series(True, index=df.index),
        # Regla de research/00_mapeo_portillo.md: PORT/PORTILLO al inicio de palabra.
        "PORTILLO_HIPOTESIS": suc.str.contains(r"\bPORT", regex=True),
    }


def bloque_nps(df: pd.DataFrame) -> None:
    nps = df.iloc[:, I_NPS]
    seg = segmento(nps)
    n = len(df)
    print(f"\n## 1. NPS (GRUPO_COMPLETO) n={n} fecha={FECHA}")
    for s in SEGMENTOS:
        k = int((seg == s).sum())
        print(f"  {s}: n={k} ({pct(k, n):.1f}%)")
    prom = pct(int((seg == "Promotor").sum()), n)
    det = pct(int((seg == "Detractor").sum()), n)
    print(f"  NPS={prom - det:.1f} media={nps.mean():.2f} mediana={nps.median():.0f} sd={nps.std():.2f}")
    dist = nps.value_counts().sort_index()
    print("  Distribución 0-10 (%): " + ", ".join(f"{int(i)}={pct(v, n):.1f}" for i, v in dist.items()))
    fechas = df.iloc[:, I_FECHA_RESP]
    print(f"  Fecha respuesta min={fechas.min()} max={fechas.max()}")


def bloque_drivers(df: pd.DataFrame) -> None:
    seg = segmento(df.iloc[:, I_NPS])
    print("\n## 2. Drivers por etapa: distribución 1-5 por segmento (GRUPO_COMPLETO)")
    for idx, nombre in DRIVERS.items():
        col = df.iloc[:, idx]
        print(f"\n  {nombre} [{df.columns[idx][:60]}]")
        for s in SEGMENTOS:
            v = col[seg == s].dropna()
            cuenta = v.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
            dist = " ".join(f"{k}={pct(c, len(v)):.1f}" for k, c in cuenta.items())
            print(f"    {s} n={len(v)} media={v.mean():.2f} | {dist} | <=3: {pct((v <= 3).sum(), len(v)):.1f}%")


def bloque_reparacion(df: pd.DataFrame) -> None:
    seg = segmento(df.iloc[:, I_NPS])
    rep = df.iloc[:, I_REPARADO].fillna("(vacío)")
    vol = df.iloc[:, I_VOLVERIA].fillna("(vacío)")
    print("\n## 3. Reparado a la primera y volvería (valores crudos)")
    print("  reparado:", rep.value_counts().to_dict())
    print("  volvería:", vol.value_counts().to_dict())
    print("\n  Reparado = No, por segmento:")
    for s in SEGMENTOS:
        m = seg == s
        k_no = int((rep[m] == "No").sum())
        print(f"    {s}: {k_no} de {int(m.sum())} ({pct(k_no, int(m.sum())):.1f}%)")
    print("\n  Detractores: cruce reparado x volvería")
    det = seg == "Detractor"
    tab = pd.crosstab(rep[det], vol[det])
    print(tab.to_string())
    print("  Detractores: % volvería por reparado")
    for r in tab.index:
        fila = tab.loc[r]
        tot = int(fila.sum())
        print(f"    reparado={r}: n={tot} " + ", ".join(f"{c}={pct(v, tot):.1f}%" for c, v in fila.items()))
    print("\n  Promotores: cruce reparado x volvería")
    pro = seg == "Promotor"
    print(pd.crosstab(rep[pro], vol[pro]).to_string())


def bloque_motivos(df: pd.DataFrame) -> None:
    seg = segmento(df.iloc[:, I_NPS])
    macro = df.iloc[:, I_MACRO1].fillna("(sin categoría)")
    micro = df.iloc[:, I_MICRO1].fillna("(sin categoría)")
    print("\n## 4. Motivos: Macrocategoría 1 por segmento (% sobre categorizados, y sobre segmento)")
    print("  Nota: solo se usa Macrocategoría 1 / Microcategoría 1.")
    for s in SEGMENTOS:
        m = seg == s
        cat = macro[m][macro[m] != "(sin categoría)"]
        vc = cat.value_counts()
        tot_seg = int(m.sum())
        print(f"  {s} (segmento n={tot_seg}, categorizados n={len(cat)}, sin categoría={tot_seg - len(cat)} = {pct(tot_seg - len(cat), tot_seg):.1f}%)")
        for k, v in vc.items():
            print(f"    {k}: n={v} ({pct(v, len(cat)):.1f}% de categorizados)")
    print("\n  Microcategoría 1, top 8 por segmento (% sobre categorizados)")
    for s in ["Detractor", "Promotor"]:
        m = seg == s
        cat = micro[m][micro[m] != "(sin categoría)"]
        print(f"  {s} (categorizados n={len(cat)}):")
        for k, v in cat.value_counts().head(8).items():
            print(f"    {k}: n={v} ({pct(v, len(cat)):.1f}%)")


def bloque_miedos(df: pd.DataFrame) -> None:
    seg = segmento(df.iloc[:, I_NPS])
    rep = df.iloc[:, I_REPARADO].fillna("")
    macro = df.iloc[:, I_MACRO1].fillna("")
    det = seg == "Detractor"
    print("\n## 5. Conteos para candidatos a miedo (detractores, n de segmento)")
    print(f"  Detractores totales: {int(det.sum())}")
    print(f"  Reparación fallida (reparado=No): {int((det & (rep == 'No')).sum())}")
    for cat in ["Atención", "Calidad del servicio", "Precios y costos", "Comunicación con el cliente", "Tiempo de entrega del vehículo"]:
        print(f"  Macro '{cat}' (todos los detractores): {int((det & (macro == cat)).sum())}")
    fallo_o_precio = det & ((rep == "No") | (macro == "Precios y costos"))
    print(f"  Detractores con reparación fallida O macro precios: {int(fallo_o_precio.sum())}")
    print(f"  Detractores con reparación fallida y sin volverías=Sí: {int((det & (rep == 'No')).sum())} (ver sección 3)")


def bloque_portillo(df: pd.DataFrame) -> None:
    rep = df.iloc[:, I_REPARADO].fillna("")
    nps = df.iloc[:, I_NPS]
    print("\n## 6. Universos")
    for nombre, mask in universos(df).items():
        sub = df[mask.values]
        seg = segmento(sub.iloc[:, I_NPS])
        n = len(sub)
        det = pct(int((seg == "Detractor").sum()), n)
        pro = pct(int((seg == "Promotor").sum()), n)
        print(f"  {nombre}: n={n} ({pct(n, len(df)):.1f}%) NPS={pro - det:.1f} det={det:.1f}% "
              f"reparado=No={pct(int((rep[mask.values] == 'No').sum()), n):.1f}%")
    suc = df.iloc[:, I_NOMBRE_SUC].fillna("").str.upper()
    print(f"  Sucursal vacía: {int((suc == '').sum())} ({pct(int((suc == '').sum()), len(df)):.1f}%)")
    print(f"  Sucursales distintas (excluye vacío): {suc[suc != ''].nunique()}")


def citas(df: pd.DataFrame, ruta_salida: Path) -> None:
    seg = segmento(df.iloc[:, I_NPS])
    texto = df.iloc[:, I_MOTIVO].fillna("")
    filtro = ~texto.str.contains(r"\d|@|http|www\.", regex=True)
    filtro &= texto.str.split().str.len().between(1, PALABRAS_MAX)
    filtro &= texto.str.split().str[1:].apply(lambda w: not any(p[:1].isupper() for p in w) if isinstance(w, list) else True)
    filas = []
    for s in ["Detractor", "Promotor"]:
        m = (seg == s) & filtro
        muestra = df[m].head(40)
        print(f"  Citas candidatas {s}: {int(m.sum())} pasan el filtro (se escriben 40 a {ruta_salida.name})")
        for idx, r in muestra.iterrows():
            filas.append(f"{s}\t{r.iloc[0]}\t{int(r.iloc[I_NPS])}\t{r.iloc[I_MOTIVO]}")
    ruta_salida.write_text("\n".join(filas) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--citas-out", type=Path, default=None,
                    help="ruta FUERA del proyecto para citas candidatas (no se imprimen)")
    args = ap.parse_args()

    df = pd.read_parquet(ARCHIVO)
    print(f"Archivo: CR_2025-Mecánica (filas={len(df)}, columnas={df.shape[1]}) fecha={FECHA}")
    bloque_nps(df)
    bloque_drivers(df)
    bloque_reparacion(df)
    bloque_motivos(df)
    bloque_miedos(df)
    bloque_portillo(df)
    if args.citas_out:
        print("\n## 7. Citas")
        citas(df, args.citas_out)


if __name__ == "__main__":
    main()
