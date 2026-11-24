"""
3C - Retención y fricciones de postventa (servicio técnico, NPS CR_2025-Mecánica).

Cómo reproducirlo: python3 analisis/3C_retencion_mecanica.py

Fuente: inputs_clean/CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet
Fecha de extracción de los archivos: 2026-11-23.
Solo lee inputs_clean/ (nunca inputs_raw/). No escribe archivos.

Universos:
  GRUPO_COMPLETO     : todas las filas del archivo.
  PORTILLO_HIPOTESIS : nombre_sucursal con 'PORT' al inicio de palabra
                       (regla de research/00_mapeo_portillo.md). [HIPÓTESIS] bloqueada:
                       depende de Beto / Iván Balaguera.

Salida: solo conteos, porcentajes y citas textuales anonimizadas (<=15 palabras, con row_id).
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "inputs_clean" / "CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet"

NPS = ("En base a tu última experiencia en servicio técnico, "
       "¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?")
MOTIVO = "¿Qué te motiva a dar esa puntuación?"
MACRO = "Macrocategoría 1"
MICRO = "Microcategoría 1"
VUELVE = "Dada tu reciente experiencia en el servicio técnico, ¿Volverías al servicio técnico de #empresa#?"
REPARA = "¿El vehículo fue reparado correctamente la primera vez?"
SUCURSAL = "nombre_sucursal"
MARCA = "des_marca"

DRIVERS = {
    "Tiempo de entrega del vehículo": "Tiempo de entrega del vehículo",
    "Claridad de precios y costos": "Claridad de precios y costos",
    "Claridad sobre la reparación o mantenimiento": "Claridad sobre la reparación o mantenimiento realizado",
    "Facilidad para comunicarse con servicio técnico": "Facilidad para comunicarse con servicio técnico",
    "Fluidez general del proceso": "Fluidez general del proceso",
    "Acogida en la sala de espera": "Acogida en la sala de espera",
    "Atención de personal": "Atención de personal",
    "Calidad del servicio realizado": "Calidad del servicio realizado",
}

NOTA_BAJA = 3       # escala 1-5: nota baja = 1..3 (se reporta también <=2)
UMBRAL_MARCA = 200  # n mínimo para desglose por marca
UMBRAL_SUC = 100    # n mínimo para mostrar sucursal (solo descriptivo)

# Cifras de diccionario (research/00_diccionario_datos.md) para contrastar.
DICC = {"filas": 27516, "nulos_sucursal": 619, "nulos_sentimiento": 7248,
        "nulos_macro1": 9810, "toyota": 3744, "chevrolet": 3513}


def pct(part, total):
    return round(100.0 * part / total, 1) if total else float("nan")


def seg_of(score):
    if score <= 6:
        return "DETRACTOR"
    if score <= 8:
        return "PASIVO"
    return "PROMOTOR"


def nps_score(s):
    if len(s) == 0:
        return float("nan")
    return round(100.0 * ((s >= 9).mean() - (s <= 6).mean()), 1)


def titulo(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def seccion_nps(df, nombre):
    titulo(f"1. Distribución NPS y segmentos - universo {nombre}")
    n = len(df)
    seg = df[NPS].map(seg_of)
    print(f"n = {n}")
    for s in ["DETRACTOR", "PASIVO", "PROMOTOR"]:
        k = int((seg == s).sum())
        print(f"  {s:10s} n={k:6d}  {pct(k, n)}%")
    print(f"  NPS (%prom - %det) = {nps_score(df[NPS])}")
    print(f"  Media = {df[NPS].mean():.2f} | Desv. est. = {df[NPS].std():.2f} | Mediana = {df[NPS].median()}")
    print("  Distribución completa 0..10 (n, %):")
    vc = df[NPS].value_counts().sort_index()
    print("   " + " | ".join(f"{int(k)}: {int(v)} ({pct(v, n)}%)" for k, v in vc.items()))
    extremos = int(((df[NPS] == 0) | (df[NPS] == 10)).sum())
    medios = int(df[NPS].between(4, 6).sum())
    print(f"  Polarización: extremos 0 y 10 = {extremos} ({pct(extremos, n)}%) | "
          f"zona 4-6 = {medios} ({pct(medios, n)}%) | zona 7-8 = {pct(int(df[NPS].between(7, 8).sum()), n)}%")
    return seg


def seccion_drivers(df, seg):
    titulo("2. Drivers por etapa: % con nota baja (<=3 y <=2) entre promotores vs detractores - GRUPO_COMPLETO")
    print(f"Escala de drivers 1-5. Nota baja = <={NOTA_BAJA}. Promotores n y detractores n varían por driver (NaN excluidos).")
    print(f"{'driver':50s} {'nP':>6s} {'nD':>6s} {'%P<=3':>7s} {'%D<=3':>7s} {'%P<=2':>7s} {'%D<=2':>7s} {'Δ<=3 pp':>9s}")
    for label, col in DRIVERS.items():
        ok = df[col].notna()
        p = df.loc[ok & (seg == "PROMOTOR"), col]
        d = df.loc[ok & (seg == "DETRACTOR"), col]
        p3, d3 = pct((p <= 3).sum(), len(p)), pct((d <= 3).sum(), len(d))
        p2, d2 = pct((p <= 2).sum(), len(p)), pct((d <= 2).sum(), len(d))
        print(f"{label:50s} {len(p):6d} {len(d):6d} {p3:7.1f} {d3:7.1f} {p2:7.1f} {d2:7.1f} {d3 - p3:9.1f}")


def seccion_categorias(df, seg):
    titulo("3. Macro y microcategorías de motivo por segmento NPS - GRUPO_COMPLETO")
    for s in ["DETRACTOR", "PASIVO", "PROMOTOR"]:
        sub = df[seg == s]
        con = sub[MACRO].notna()
        print(f"\n[{s}] n={len(sub)} | con Macrocategoría 1: {int(con.sum())} ({pct(con.sum(), len(sub))}%) | "
              f"sin categoría: {int((~con).sum())} ({pct((~con).sum(), len(sub))}%)")
        print("  Macrocategoría 1 (n, % sobre los categorizados):")
        for k, v in sub.loc[con, MACRO].value_counts().items():
            print(f"    {k:35s} {int(v):6d}  {pct(v, con.sum())}%")
        print("  Microcategoría 1 top 8 (n, % sobre los categorizados):")
        mic = sub[MICRO].notna()
        for k, v in sub.loc[mic, MICRO].value_counts().head(8).items():
            print(f"    {k:45s} {int(v):6d}  {pct(v, mic.sum())}%")


def seccion_friccion(df, seg):
    titulo("4. Fricciones vs recompra y recomendación (advocacy) - GRUPO_COMPLETO")
    for s in ["DETRACTOR", "PASIVO", "PROMOTOR"]:
        sub = df[seg == s]
        print(f"\n[{s}] n={len(sub)}")
        print("  Volverías al servicio técnico:")
        for k, v in sub[VUELVE].value_counts(dropna=True).items():
            print(f"    {k:10s} {int(v):6d}  {pct(v, len(sub))}%")
        print("  ¿Reparado correctamente la primera vez?:")
        for k, v in sub[REPARA].value_counts(dropna=True).items():
            print(f"    {k:10s} {int(v):6d}  {pct(v, len(sub))}%")

    det = df[seg == "DETRACTOR"]
    print("\nCruce DETRACTORES: reparado a la primera x volverías")
    tab = pd.crosstab(det[REPARA], det[VUELVE], margins=True)
    print(tab.to_string())
    print("\nCruce DETRACTORES: % que NO volvería (No) según reparado a la primera")
    for r in ["Sí", "No"]:
        sub = det[det[REPARA] == r]
        print(f"  reparado={r}: n={len(sub)} | No volvería={pct((sub[VUELVE] == 'No').sum(), len(sub))}% | "
              f"No sé={pct((sub[VUELVE] == 'No sé').sum(), len(sub))}% | Sí={pct((sub[VUELVE] == 'Sí').sum(), len(sub))}%")

    friccion = det[(det[REPARA] == "No") | (det[VUELVE] != "Sí")]
    print(f"\nDetractores con alguna señal de fricción de recompra (reparado=No o volvería != Sí): "
          f"n={len(friccion)} ({pct(len(friccion), len(det))}% de detractores)")
    print("  Macrocategoría 1 entre detractores con reparado=No (n, % sobre categorizados):")
    sub = det[det[REPARA] == "No"]
    con = sub[MACRO].notna()
    for k, v in sub.loc[con, MACRO].value_counts().items():
        print(f"    {k:35s} {int(v):6d}  {pct(v, con.sum())}%")
    print(f"    (sin categoría: {int((~con).sum())} de {len(sub)})")

    prom = df[seg == "PROMOTOR"]
    print("\nPromotores: % que NO volvería o No sé, según reparado a la primera")
    for r in ["Sí", "No"]:
        sub = prom[prom[REPARA] == r]
        print(f"  reparado={r}: n={len(sub)} | No={pct((sub[VUELVE] == 'No').sum(), len(sub))}% | "
              f"No sé={pct((sub[VUELVE] == 'No sé').sum(), len(sub))}%")


def seccion_desgloses(df, seg):
    titulo(f"5a. Desglose por marca (des_marca) con n >= {UMBRAL_MARCA} - GRUPO_COMPLETO")
    marcas = df[MARCA].fillna("<vacío>").value_counts()
    print(f"{'marca':18s} {'n':>6s} {'NPS':>7s} {'%DET':>7s} {'%PRO':>7s} {'Volv.Sí%':>9s} {'Rep.No%':>8s}")
    omitidas = 0
    for m, n in marcas.items():
        if n < UMBRAL_MARCA:
            omitidas += 1
            continue
        sub = df[df[MARCA].fillna("<vacío>") == m]
        sg = seg[sub.index]
        print(f"{m:18s} {n:6d} {nps_score(sub[NPS]):7.1f} {pct((sg == 'DETRACTOR').sum(), n):7.1f} "
              f"{pct((sg == 'PROMOTOR').sum(), n):7.1f} {pct((sub[VUELVE] == 'Sí').sum(), n):9.1f} "
              f"{pct((sub[REPARA] == 'No').sum(), n):8.1f}")
    print(f"Marcas con n < {UMBRAL_MARCA} omitidas: {omitidas} de {len(marcas)} valores distintos.")

    titulo(f"5b. Sucursal (nombre_sucursal) - SOLO DESCRIPTIVO, n >= {UMBRAL_SUC}, no es ranking")
    nulos = int(df[SUCURSAL].isna().sum())
    print(f"Filas con nombre_sucursal vacío: {nulos} de {len(df)} ({pct(nulos, len(df))}%). "
          f"NPS de esas filas: {nps_score(df.loc[df[SUCURSAL].isna(), NPS])} (n={nulos}).")
    print(f"Sucursales distintas: {df[SUCURSAL].nunique()}")
    conteo = df[SUCURSAL].value_counts()
    for suc, n in conteo.items():
        if n < UMBRAL_SUC:
            continue
        sub = df[df[SUCURSAL] == suc]
        sg = seg[sub.index]
        print(f"  {suc[:40]:40s} n={n:6d} NPS={nps_score(sub[NPS]):7.1f} "
              f"%DET={pct((sg == 'DETRACTOR').sum(), n):5.1f}")


def seccion_contraste_diccionario(df):
    titulo("Contraste con research/00_diccionario_datos.md (si no calza, se reporta, no se corrige)")
    checks = {
        "filas": (len(df), DICC["filas"]),
        "nombre_sucursal vacío": (int(df[SUCURSAL].isna().sum()), DICC["nulos_sucursal"]),
        "sentimiento nulo": (int(df["sentimiento"].isna().sum()), DICC["nulos_sentimiento"]),
        "Macrocategoría 1 nulo": (int(df[MACRO].isna().sum()), DICC["nulos_macro1"]),
        "des_marca TOYOTA": (int((df[MARCA] == "TOYOTA").sum()), DICC["toyota"]),
        "des_marca CHEVROLET": (int((df[MARCA] == "CHEVROLET").sum()), DICC["chevrolet"]),
    }
    for k, (obs, dic) in checks.items():
        estado = "CALZA" if obs == dic else "NO CALZA"
        print(f"  {k:25s} parquet={obs:6d} diccionario={dic:6d}  {estado}")


PII_RE = re.compile(r"[@\d]|https?:|www\.", re.IGNORECASE)


def es_cita_segura(texto):
    """Filtro anti-PII: <=15 palabras, sin dígitos/@/URL, sin palabras capitalizadas tras la primera (posibles nombres)."""
    palabras = texto.split()
    if not palabras or len(palabras) > 15:
        return False
    if PII_RE.search(texto):
        return False
    for p in palabras[1:]:
        limpia = p.strip(".,;:!?¡¿()\"'")
        if limpia[:1].isupper():
            return False
    return True


def seccion_verbatim(df, seg):
    titulo("6. Verbatim '¿Qué te motiva...?' anonimizado (<=15 palabras, con row_id)")
    print("Filtro: <=15 palabras; sin dígitos, @ ni URL; sin mayúsculas tras la primera palabra (evita nombres).")
    txt = df[MOTIVO].dropna()
    for s in ["DETRACTOR", "PROMOTOR"]:
        ids = txt.index[seg[txt.index] == s]
        seguras = [i for i in ids if es_cita_segura(str(df.at[i, MOTIVO]))]
        print(f"\n[{s}] con texto: {len(ids)} | pasan filtro: {len(seguras)} ({pct(len(seguras), len(ids))}%)")
        for i in seguras[:4]:
            texto = " ".join(str(df.at[i, MOTIVO]).split()[:15])
            print(f"  row_id={df.at[i, 'row_id']} | NPS={int(df.at[i, NPS])} | \"{texto}\"")


def seccion_notas(df, seg):
    titulo("7. Notas de calidad de datos")
    print(f"Motivo (texto) no vacío: {int(df[MOTIVO].notna().sum())} de {len(df)} "
          f"({pct(df[MOTIVO].notna().sum(), len(df))}%)")
    print(f"Macrocategoría 1 vacía: {int(df[MACRO].isna().sum())} ({pct(df[MACRO].isna().sum(), len(df))}%)")
    for label, col in DRIVERS.items():
        print(f"  NaN en '{label}': {int(df[col].isna().sum())}")


def main():
    df = pd.read_parquet(PARQUET)
    titulo(f"Archivo: {PARQUET.name} | filas={len(df)} | extracción 2026-11-23")
    seccion_contraste_diccionario(df)

    mask_port = df[SUCURSAL].fillna("").str.contains(r"(?i)\bPORT", regex=True)
    print(f"\nPORTILLO_HIPOTESIS por nombre_sucursal: n={int(mask_port.sum())} "
          f"({pct(mask_port.sum(), len(df))}%) [HIPÓTESIS BLOQUEADA]")

    seg = df[NPS].map(seg_of)
    seccion_nps(df, "GRUPO_COMPLETO")
    seccion_nps(df[mask_port], "PORTILLO_HIPOTESIS [HIPÓTESIS]")
    seccion_drivers(df, seg)
    seccion_categorias(df, seg)
    seccion_friccion(df, seg)
    seccion_desgloses(df, seg)
    seccion_verbatim(df, seg)
    seccion_notas(df, seg)


if __name__ == "__main__":
    main()
