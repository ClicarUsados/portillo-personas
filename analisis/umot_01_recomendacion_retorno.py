"""UMOT 01 - Recomendación (NPS) y retorno declarado ("¿Volverías...?") por encuesta.

Subagente D (UMOT + demografía), Portillo (Grupo Americar, Chile). Extracción 2026-11-23.
Fuentes (solo inputs_clean/*.parquet):
  - CR_2025-Mecánica        : NPS "En base a tu última experiencia en servicio técnico..." + "¿Volverías al servicio técnico...?"
  - CR_2025-Venta-Nuevo     : NPS "...experiencia de compra..." + "¿Volverías a comprar...?"
  - CR_2025-Venta-Usados    : idem Venta-Nuevo
  - CR_Clicar               : "¿Recomendarías Clicar...?" + "¿Volverías a vender tú auto en Clicar?"
  - CR_Encuesta-funcionalidades-Web : columna `nps` (solo valores 9 y 10; NO es la pregunta NPS completa -> se reporta, no se usa para NPS)
Excluidas (sin pregunta NPS ni "¿Volverías?"): Seguridad vial (ver umot_03), Lead-Portillo (no aplica).

Definiciones:
  Promotor = 9-10 ; Pasivo = 7-8 ; Detractor = 0-6 ; NPS = %Promotor - %Detractor.
  "Sí" / "No sé" / "No" sobre volver = retorno DECLARADO (intención), no retorno observado.

Universos:
  GRUPO_COMPLETO   : todas las filas.
  PORTILLO_HIPOTESIS: sucursal/concesionario que contiene "PORT" como palabra (\\bPORT),
                      según research/00_mapeo_portillo.md. BLOQUEADO: asignación pendiente de Beto / Iván Balaguera.
  PORT_CAMPAÑA_CHECK: campaña o sensor contiene "Portillo" (etiqueta [DATO], solo cruce de control).

Imprime conteos y porcentajes agregados; nunca filas ni texto libre.
Asociaciones descriptivas, no causales. Cortes con n < MIN_N no se interpretan.

Cómo reproducirlo: python3 analisis/umot_01_recomendacion_retorno.py
"""
import glob
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "2026-11-23"
MIN_N = 30

NPS_COL = {
    "Mecanica": "En base a tu última experiencia en servicio técnico, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?",
    "VentaNuevo": "En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?",
    "VentaUsados": "En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?",
    "Clicar": "¿Recomendarías Clicar a un familiar o amigo?",
}
VOLVER_COL = {
    "Mecanica": "Dada tu reciente experiencia en el servicio técnico, ¿Volverías al servicio técnico de #empresa#?",
    "VentaNuevo": "Dada tu reciente experiencia de compra, ¿Volverías a comprar en #empresa#?",
    "VentaUsados": "Dada tu reciente experiencia de compra, ¿Volverías a comprar en #empresa#?",
    "Clicar": "Dada tu reciente experiencia, ¿Volverías a vender tú auto en Clicar?",
}
SUC_COL = {
    "Mecanica": "nombre_sucursal", "VentaNuevo": "nombre_concesionario",
    "VentaUsados": "nombre_concesionario", "Clicar": "nombre_sucursal",
    "Web": "nombre_concesionario",
}
# Items de escala 1-5 por encuesta (para "qué separa")
ITEMS = {
    "Mecanica": {"Acogida sala espera": "Acogida en la sala de espera",
                 "Claridad precios": "Claridad de precios y costos",
                 "Claridad reparación": "Claridad sobre la reparación o mantenimiento realizado",
                 "Comunicación": "Facilidad para comunicarse con servicio técnico",
                 "Fluidez": "Fluidez general del proceso",
                 "Calidad servicio": "Calidad del servicio realizado"},
    "VentaNuevo": {"Acogida sala": "Acogida en sala de ventas",
                   "Claridad precios/financ.": "Claridad de precios y opciones de financiamiento",
                   "Comunicación vendedor": "Facilidad de comunicación con vendedor",
                   "Fluidez": "Fluidez general del proceso"},
    "VentaUsados": {"Acogida sala": "Acogida en sala de ventas",
                    "Claridad precios/financ.": "Claridad de precios y opciones de financiamiento",
                    "Comunicación vendedor": "Facilidad de comunicación con vendedor",
                    "Fluidez": "Fluidez general del proceso"},
    "Clicar": {"Facilidad vender": "Facilidad para vender tu auto en Clicar",
               "Claridad oferta final": "Claridad en la oferta final del vehículo",
               "Comunicación": "Facilidad para comunicarte con Clicar",
               "Rapidez": "Rapidez del proceso"},
}
TEMA_COL = {  # Macrocategoría 1 = primer código temático del motivo del NPS
    "Mecanica": "Macrocategoría 1", "VentaNuevo": "Macrocategoría 1",
    "VentaUsados": "Macrocategoría 1",
}


def cargar(patron):
    rutas = glob.glob(os.path.join(ROOT, "inputs_clean", patron))
    if len(rutas) != 1:
        raise SystemExit(f"Se esperaba 1 archivo para {patron}, hay {len(rutas)}")
    return pd.read_parquet(rutas[0])


def cargar_todo():
    fuentes = {
        "Mecanica": cargar("CR_2025-Mecánica_*"),
        "VentaNuevo": cargar("CR_2025-Venta-Nuevo_*"),
        "VentaUsados": cargar("CR_2025-Venta-Usados_*"),
        "Clicar": cargar("CR_Clicar_*"),
        "Web": cargar("CR_Encuesta-funcionalidades-Web_*"),
    }
    return fuentes


def universos(df, enc):
    suc = df[SUC_COL[enc]].fillna("").astype(str)
    camp = df["campaña o sensor"].fillna("").astype(str)
    return {
        "GRUPO_COMPLETO": pd.Series(True, index=df.index),
        "PORTILLO_HIPOTESIS": suc.str.contains(r"\bPORT", case=False, regex=True),
        "PORT_CAMPAÑA_CHECK": camp.str.contains("portillo", case=False, regex=False),
    }


def categoria_nps(s):
    s = pd.to_numeric(s, errors="coerce")
    return pd.Series(
        pd.cut(s, bins=[-1, 6, 8, 10], labels=["Detractor", "Pasivo", "Promotor"]),
        index=s.index,
    )


def pct(a, b):
    return 0.0 if b == 0 else 100.0 * a / b


def bloque_nps(enc, df):
    print(f"\n### {enc} | filas totales {len(df)} | fecha {FECHA}")
    col_nps = NPS_COL[enc]
    col_vol = VOLVER_COL[enc]
    for uni_nombre, mask in universos(df, enc).items():
        sub = df[mask]
        cat = categoria_nps(sub[col_nps])
        valid = cat.notna()
        n = int(valid.sum())
        cnt = cat.value_counts()
        p, pa, d = (int(cnt.get(k, 0)) for k in ["Promotor", "Pasivo", "Detractor"])
        nps_score = pct(p, n) - pct(d, n)
        vol = sub[col_vol].astype(str).value_counts()
        nv = int(sub[col_vol].notna().sum())
        si, nosé, no = (int(vol.get(k, 0)) for k in ["Sí", "No sé", "No"])
        print(
            f"  [{uni_nombre}] n_NPS={n} | Prom={p} ({pct(p,n):.1f}%) Pas={pa} ({pct(pa,n):.1f}%) "
            f"Det={d} ({pct(d,n):.1f}%) | NPS={nps_score:+.1f} || "
            f"n_volver={nv} Sí={si} ({pct(si,nv):.1f}%) No sé={nosé} ({pct(nosé,nv):.1f}%) "
            f"No={no} ({pct(no,nv):.1f}%)"
            + ("  [n<MIN_N: no interpretar]" if n < MIN_N else "")
        )


def bloque_separa(enc, df):
    """Qué separa a Promotores de Detractores (y Sí vs No en volver), grupo completo."""
    print(f"\n### Qué separa ({enc}, GRUPO_COMPLETO)")
    cat = categoria_nps(df[NPS_COL[enc]])
    prom = df[cat == "Promotor"]
    det = df[cat == "Detractor"]
    print(f"  n Promotor={len(prom)} | n Detractor={len(det)}")
    for etiqueta, col in ITEMS[enc].items():
        def bajo(d):
            v = pd.to_numeric(d[col], errors="coerce").dropna()
            return (int((v <= 2).sum()), len(v))
        bp, np_ = bajo(prom)
        bd, nd = bajo(det)
        print(f"  Item '{etiqueta}': <=2 Promotores {pct(bp,np_):.1f}% (n={np_}) | "
              f"Detractores {pct(bd,nd):.1f}% (n={nd})")
    if "sentimiento" in df.columns:
        for nombre, g in [("Promotores", prom), ("Detractores", det)]:
            s = g["sentimiento"].value_counts(dropna=True)
            tot = int(s.sum())
            print(f"  sentimiento (motivo NPS) {nombre}: " +
                  ", ".join(f"{k}={pct(int(v),tot):.1f}% (n={int(v)})" for k, v in s.items()))
    if enc in TEMA_COL:
        tc = TEMA_COL[enc]
        for nombre, g in [("Promotores", prom), ("Detractores", det)]:
            s = g[tc].value_counts(dropna=True)
            tot = int(s.sum())
            top = ", ".join(f"{k}={pct(int(v),tot):.1f}% (n={int(v)})" for k, v in s.head(5).items())
            print(f"  tema Macrocategoría 1 {nombre} (n con código={tot}): {top}")
    # volver: Sí vs No
    sí = df[df[VOLVER_COL[enc]] == "Sí"]
    no = df[df[VOLVER_COL[enc]] == "No"]
    print(f"  volver: n Sí={len(sí)} | n No={len(no)}")
    for etiqueta, col in ITEMS[enc].items():
        def bajo(d):
            v = pd.to_numeric(d[col], errors="coerce").dropna()
            return (int((v <= 2).sum()), len(v))
        bs, ns = bajo(sí)
        bn, nn = bajo(no)
        print(f"  volver Item '{etiqueta}': <=2 en Sí {pct(bs,ns):.1f}% (n={ns}) | en No {pct(bn,nn):.1f}% (n={nn})")


def bloque_web(df):
    print("\n### Web (columna nps; NO es la pregunta NPS completa, NO VERIFICADO como NPS)")
    vc = df["nps"].astype(str).value_counts()
    print("  valores nps:", {k: int(v) for k, v in vc.items()}, f"| total={len(df)}")
    print("  Nota: solo valores 9 y 10 -> sin detractores observables; no calcular NPS.")


def main():
    print(f"UMOT 01 - NPS y retorno declarado | extracción {FECHA}")
    fuentes = cargar_todo()
    for enc in ["Mecanica", "VentaNuevo", "VentaUsados", "Clicar"]:
        bloque_nps(enc, fuentes[enc])
    bloque_web(fuentes["Web"])
    # Control de la discrepancia #15 (00_contradicciones.md): regla prefijo ^PORT vs \bPORT
    u = fuentes["VentaUsados"]
    suc = u["nombre_concesionario"].fillna("").astype(str)
    print(f"\nControl #15 Venta-Usados: \\bPORT={int(suc.str.contains(r'\bPORT', case=False, regex=True).sum())} | "
          f"prefijo ^PORT={int(suc.str.contains(r'^PORT', case=False, regex=True).sum())} (filas, sin filtrar por NPS)")
    for enc in ["Mecanica", "VentaNuevo", "VentaUsados", "Clicar"]:
        bloque_separa(enc, fuentes[enc])


if __name__ == "__main__":
    main()
