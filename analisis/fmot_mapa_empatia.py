#!/usr/bin/env python3
"""FMOT (sala de ventas): datos para el mapa de empatía (Subagente B).

Cómo reproducirlo: python3 analisis/fmot_mapa_empatia.py
Lee solo inputs_clean/*.parquet (Venta-Nuevo, Venta-Usados, Clicar).
Imprime conteos, medias y distribuciones. Las citas (≤15 palabras, con row_id)
se imprimen solo en la sección 6 y pasan filtro anti-PII. Fecha de extracción: 2026-11-23.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DIR_CLEAN = RAIZ / "inputs_clean"
NPS = ("En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes "
       "#empresa# a un familiar o amigo?")
CLICAR_NPS = "¿Recomendarías Clicar a un familiar o amigo?"
CLICAR_OFERTA = "Claridad en la oferta final del vehículo"

ETAPAS_NUEVO = [
    "Acogida en sala de ventas",
    "Atención del vendedor",
    "Información proporcionada por vendedor",
    "Claridad de precios y opciones de financiamiento",
    "Facilidad de comunicación con vendedor",
    "Fluidez general del proceso",
    "Vehículo en parte de pago",
]
ETAPAS_USADOS = [
    "Acogida en sala de ventas",
    "Atención del vendedor",
    "Claridad de precios y opciones de financiamiento",
    "Facilidad de comunicación con vendedor",
    "Fluidez general del proceso",
    "Vehículo en parte de pago",
    "Proceso de Entrega",  # SMOT: se reporta como contexto, no es FMOT
]
# Bloques de verbatim por posición de columna (ver research/v1_pre_MdV/01_*)
BLOQUES_NUEVO = {
    "NPS (¿Qué te motiva…?)": ("¿Qué te motiva a dar esa puntuación?", "Macrocategoría 1"),
    "Etapa Fluidez (¿Nos contarías por qué?)": ("¿Nos contarías por qué?", "Macrocategoría 1.1"),
    "Etapa Parte de pago (¿Nos contarías por qué?.1)": ("¿Nos contarías por qué?.1", "Macrocategoría 1.2"),
}
BLOQUES_USADOS = {
    "NPS (¿Qué te motiva…?)": ("¿Qué te motiva a dar esa puntuación?", "Macrocategoría 1"),
    "Etapa Parte de pago (¿Qué te motivó…?)": ("¿Qué te motivó a otorgar esta calificación?", "Macrocategoría 1.1"),
    "Entrega (¿Qué faltó…?)": ("¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor?", "Macrocategoría 1.2"),
}


def cargar(prefijo: str) -> pd.DataFrame:
    rutas = sorted(DIR_CLEAN.glob(f"{prefijo}*.parquet"))
    if len(rutas) != 1:
        raise SystemExit(f"Se esperaba 1 archivo para {prefijo}, hay {len(rutas)}")
    return pd.read_parquet(rutas[0])


def segmento(df: pd.DataFrame, col: str) -> pd.Series:
    v = pd.to_numeric(df[col], errors="coerce")
    return pd.Series(
        np.select([v >= 9, v >= 7, v <= 6], ["promotor", "pasivo", "detractor"], default=""),
        index=df.index,
    ).where(v.notna(), "")


def universos(df: pd.DataFrame) -> dict[str, pd.Series]:
    conc = df["nombre_concesionario"].fillna("").str.upper()
    camp = df["campaña o sensor"].fillna("")
    return {
        "GRUPO_COMPLETO": pd.Series(True, index=df.index),
        "PORTILLO_HIPOTESIS (prefijo PORT en nombre_concesionario)": conc.str.match(r"PORT"),
        "SENSIBILIDAD \\bPORT en cualquier posición": conc.str.contains(r"\bPORT", regex=True),
        "SENSIBILIDAD campaña o sensor contiene Portillo": camp.str.contains("portillo", case=False),
    }


def resumen_score(s: pd.Series) -> dict:
    v = pd.to_numeric(s, errors="coerce").dropna()
    n = len(v)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "media": round(v.mean(), 2),
        "1-2 %": round(100 * (v <= 2).mean(), 1),
        "3 %": round(100 * (v == 3).mean(), 1),
        "4-5 %": round(100 * (v >= 4).mean(), 1),
        "dist 1..5": [int((v == k).sum()) for k in range(1, 6)],
    }


def seccion(titulo: str) -> None:
    print(f"\n{'=' * 8} {titulo} {'=' * 8}")


def sec1_universos_y_segmentos(nuevo: pd.DataFrame, usados: pd.DataFrame) -> None:
    seccion("1. Tamaños por universo y segmento NPS (fecha 2026-11-23)")
    for nombre, df in [("Venta-Nuevo", nuevo), ("Venta-Usados", usados)]:
        seg = segmento(df, NPS)
        print(f"[{nombre}] filas={len(df)} sin NPS={int((seg == '').sum())}")
        for uni, m in universos(df).items():
            s = seg[m]
            cnt = s.value_counts()
            print(f"  {uni}: n={int(m.sum())} | P={cnt.get('promotor', 0)} "
                  f"Pa={cnt.get('pasivo', 0)} D={cnt.get('detractor', 0)}")


def sec2_macros_nps(nuevo: pd.DataFrame, usados: pd.DataFrame) -> None:
    seccion("2. Macrocategorías por segmento (bloque NPS, Macrocategoría 1)")
    for nombre, df in [("Venta-Nuevo", nuevo), ("Venta-Usados", usados)]:
        seg = segmento(df, NPS)
        mac = df["Macrocategoría 1"]
        for uni in ["GRUPO_COMPLETO", "PORTILLO_HIPOTESIS (prefijo PORT en nombre_concesionario)"]:
            m = universos(df)[uni]
            print(f"[{nombre} | {uni.split(' ')[0]}]")
            for s_nom in ["promotor", "pasivo", "detractor"]:
                mm = m & (seg == s_nom) & mac.notna()
                base = int(mm.sum())
                vc = mac[mm].value_counts()
                top = {k: f"{v} ({100 * v / base:.1f}%)" for k, v in vc.head(6).items()} if base else {}
                print(f"  {s_nom} codificadas={base}: {top}")


def sec3_macros_etapas(nuevo: pd.DataFrame, usados: pd.DataFrame) -> None:
    seccion("3. Macrocategorías de los bloques por etapa (GRUPO_COMPLETO; base = detractores codificados)")
    for nombre, df, bloques in [("Venta-Nuevo", nuevo, BLOQUES_NUEVO), ("Venta-Usados", usados, BLOQUES_USADOS)]:
        seg = segmento(df, NPS)
        for bloque, (_verb, mcol) in bloques.items():
            if bloque.startswith("NPS"):
                continue
            mac = df[mcol]
            print(f"[{nombre}] {bloque}: codificadas={int(mac.notna().sum())}")
            for s_nom in ["promotor", "pasivo", "detractor"]:
                mm = (seg == s_nom) & mac.notna()
                vc = mac[mm].value_counts()
                print(f"   {s_nom} codificadas={int(mm.sum())}: {dict(vc.head(5))}")


def sec4_etapas(nuevo: pd.DataFrame, usados: pd.DataFrame) -> None:
    seccion("4. Etapas: distribución y polarización (escala 1-5; 'No aplica' excluido)")
    for nombre, df, etapas in [("Venta-Nuevo", nuevo, ETAPAS_NUEVO), ("Venta-Usados", usados, ETAPAS_USADOS)]:
        seg = segmento(df, NPS)
        det = seg == "detractor"
        pro = seg == "promotor"
        print(f"[{nombre}]")
        for col in etapas:
            tot = resumen_score(df[col])
            d = resumen_score(df.loc[det, col])
            p = resumen_score(df.loc[pro, col])
            print(f"  {col}")
            print(f"    total n={tot['n']} media={tot.get('media')} 1-2={tot.get('1-2 %')}% "
                  f"3={tot.get('3 %')}% 4-5={tot.get('4-5 %')}% dist={tot.get('dist 1..5')}")
            print(f"    detractores n={d['n']} media={d.get('media')} 1-2={d.get('1-2 %')}% dist={d.get('dist 1..5')}")
            print(f"    promotores  n={p['n']} media={p.get('media')} 1-2={p.get('1-2 %')}%")
        # Mismo cálculo en PORTILLO_HIPOTESIS (prefijo PORT), solo totales
        mport = universos(df)["PORTILLO_HIPOTESIS (prefijo PORT en nombre_concesionario)"]
        print(f"  -- {nombre} PORTILLO_HIPOTESIS (n={int(mport.sum())}), total y detractores --")
        for col in etapas:
            t = resumen_score(df.loc[mport, col])
            dd = resumen_score(df.loc[mport & det, col])
            print(f"    {col}: total n={t['n']} media={t.get('media')} 1-2={t.get('1-2 %')}% | "
                  f"detractores n={dd['n']} 1-2={dd.get('1-2 %')}%")
        # Pesos: quién aporta los 1-2 de Fluidez
        if "Fluidez general del proceso" in df:
            v = pd.to_numeric(df["Fluidez general del proceso"], errors="coerce")
            low = v <= 2
            print(f"  Fluidez: de los 1-2 totales ({int(low.sum())}), "
                  f"detractores={int((low & det).sum())}, pasivos={int((low & (seg == 'pasivo')).sum())}, "
                  f"promotores={int((low & pro).sum())}")


def sec5_clicar() -> None:
    seccion("5. CR_Clicar (solo oferta final; desactualizado 2023-06 a 2024-04)")
    c = cargar("CR_Clicar")
    seg = segmento(c, CLICAR_NPS)
    print(f"n={len(c)} | fecha respuesta {c['fecha respuesta'].min()} a {c['fecha respuesta'].max()}")
    print(f"NPS Clicar (0-10): P={int((seg == 'promotor').sum())} Pa={int((seg == 'pasivo').sum())} "
          f"D={int((seg == 'detractor').sum())}")
    print(f"Oferta final resumen: {resumen_score(c[CLICAR_OFERTA])}")
    for s_nom in ["promotor", "pasivo", "detractor"]:
        print(f"   oferta {s_nom}: {resumen_score(c.loc[seg == s_nom, CLICAR_OFERTA])}")
    print(f"Parte de pago como puntaje: columnas con 'pago' = "
          f"{[x for x in c.columns if 'pago' in x.lower()]}")
    fpa = c["fecha_pa"].dropna()
    iso = fpa.str.match(r"^\d{4}-\d{2}-\d{2}$").sum()
    print(f"fecha_pa: no nulos={len(fpa)}, formato ISO={int(iso)} (resto: formato no interpretable, NO VERIFICADO)")
    print(f"origen: {c['origen'].value_counts(dropna=False).to_dict()}")


PII = re.compile(r"@|\d{3,}|https?:|www\.|\b(rut|fono|teléfono|telefono|celular|whatsapp)\b", re.I)


def pasa_pii(texto: str) -> bool:
    if PII.search(texto):
        return False
    tokens = texto.split()
    # nombres propios: mayúscula en posición >0 que no sea sigla
    for t in tokens[1:]:
        limpio = t.strip(".,;:!?¡¿\"'()")
        if limpio[:1].isupper() and not limpio.isupper():
            return False
    return True


def sec6_citas(nuevo: pd.DataFrame, usados: pd.DataFrame) -> None:
    seccion("6. Citas candidatas (detractores, ≤15 palabras, anti-PII; row_id + texto)")
    temas = {
        "Fluidez/plazo": r"demor|tiempo|plazo|esper|demasiad|lent",
        "Vendedor": r"vendedor|ejecutivo|atenc",
        "Precio/financiamiento": r"precio|financ|cuota|tasa|crédito|credito",
        "Parte de pago": r"parte de pago|mi auto|usado|tasaci|peritaj",
        "Acogida": r"acogi|recib|sala|llegu",
    }
    for nombre, df, prefijo_col in [("Venta-Nuevo", nuevo, "¿Nos contarías por qué?"),
                                    ("Venta-Usados", usados, "¿Qué te motiva a dar esa puntuación?")]:
        seg = segmento(df, NPS)
        texto = df["¿Qué te motiva a dar esa puntuación?"].fillna("")
        for tema, rx in temas.items():
            m = (seg == "detractor") & texto.str.contains(rx, case=False, regex=True)
            cand = [(rid, t) for rid, t in zip(df.loc[m, "row_id"], texto[m])
                    if len(t.split()) <= 15 and pasa_pii(t)]
            print(f"[{nombre} | {tema}] candidatas={int(m.sum())} válidas={len(cand)}")
            for rid, t in cand[:3]:
                print(f"   {rid} | {len(t.split())}p | {t}")


if __name__ == "__main__":
    nuevo = cargar("CR_2025-Venta-Nuevo")
    usados = cargar("CR_2025-Venta-Usados")
    sec1_universos_y_segmentos(nuevo, usados)
    sec2_macros_nps(nuevo, usados)
    sec3_macros_etapas(nuevo, usados)
    sec4_etapas(nuevo, usados)
    sec5_clicar()
    sec6_citas(nuevo, usados)
