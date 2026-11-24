"""v3B - Dolores de COMPRA y POSTVENTA de detractores de Venta-Usados (cliente ideal seminuevo premium).

Subagente B, v3 "Cliente ideal de Seminuevos Portillo Zona Oriente". Extracción 2026-11-23.
Fuente única: inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet (4.103 filas).

Universos (se reportan los cuatro, cada uno con su regla):
  PORT_CAMP  : campaña "2025 - Venta Usados Portillo" (regla principal, n=114) [DATO]
  PORT_SUC   : nombre_concesionario empieza con "PORT" (n=108) [HIPÓTESIS de mapeo, BLOQUEADO Beto / Iván Balaguera]
  PORT_BPORT : nombre_concesionario contiene "\\bPORT" (n=145). INCLUYE 37 filas "USADOS SAN BDO AV PORTALES"
               que NO son Portillo (falso positivo de "PORT" en "PORTALES"). Se reporta solo para contraste.
  GRUPO      : todas las filas de Venta-Usados (4.103). Referencia de mercado, NO es universo Portillo.

Definiciones:
  Detractor = NPS 0-6 ; Promotor = 9-10 (pregunta "¿qué tan probable es que recomiendes...?").
  "Ítem <=2" = puntaje 1 o 2 en la escala 1-5 del ítem, sobre respondentes que contestaron ese ítem.
  Parte de pago: se evalúa solo donde no es "No aplica".
  Códigos Microcategoría / Macrocategoría: los asigna la encuesta (conteo de filas con al menos un código).
  Palabras clave: regex sobre texto libre de detractores; es conteo de filas, NO codificación manual.

Limitación: en PORT_CAMP hay pocos detractores (ver salida). Con n tan bajo los % son frágiles;
no se interpretan cortes con n < MIN_N. Solo conteos; nunca filas ni texto libre.
Asociaciones descriptivas, no causales. No es conversión lead -> venta.

Cómo reproducirlo: python3 analisis/v3B_dolores_seminuevo.py
"""
import re
import pandas as pd

RUTA = ("/Users/betosanchez/portillo-personas/inputs_clean/"
        "CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet")
NPS = "En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?"
ITEMS_COMPRA = {
    "Acogida en sala de ventas": "Acogida en sala (compra)",
    "Atención del vendedor": "Atención del vendedor (compra)",
    "Facilidad de comunicación con vendedor": "Comunicación con vendedor (compra)",
    "Claridad de precios y opciones de financiamiento": "Claridad de precio y financiamiento (compra)",
    "Fluidez general del proceso": "Fluidez del proceso (compra)",
}
ITEM_PARTE = "Vehículo en parte de pago"
ITEM_ENTREGA = "Proceso de Entrega"
TXT = {
    "motiva": "¿Qué te motiva a dar esa puntuación?",
    "motivo2": "¿Qué te motivó a otorgar esta calificación?",
    "entrega": "¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor?",
}
KEYWORDS = {  # regex sobre texto libre; conteo de filas
    "garantía": r"garant",
    "tasación / parte de pago": r"tasa|parte de pago|permuta|mi auto|mi vehículo",
    "precio / financiamiento / cuota": r"precio|financ|cuota|crédito|credito|cotiz",
    "estado del auto": r"estado|golpe|rayón|rayon|mecánic|mecanic|falla|detalle|condición|condicion",
    "respuesta / comunicación": r"respond|contest|llam|comunic|informa",
    "trato / atención": r"trato|atenci|amable|vendedor",
    "entrega / postventa": r"entrega|postventa|post venta|servicio|acuerdo",
    "documentación / permiso": r"permiso|papel|document|transfer|inscrip",
}
MIN_N = 10


def universos(df):
    camp = df["campaña o sensor"].fillna("").str.contains("Venta Usados Portillo")
    con = df["nombre_concesionario"].fillna("")
    return {
        "PORT_CAMP": camp,
        "PORT_SUC": con.str.match(r"^PORT"),
        "PORT_BPORT": con.str.contains(r"\bPORT"),
        "GRUPO": pd.Series(True, index=df.index),
    }


def resumen(nombre, m, df):
    d = df[m]
    nps = pd.to_numeric(d[NPS], errors="coerce")
    det = d[nps <= 6]
    pro = d[nps >= 9]
    print(f"\n=== {nombre}: n={len(d)} | detractores={len(det)} | promotores={len(pro)} "
          f"| {'NO INTERPRETAR (n<MIN_N)' if len(det) < MIN_N else 'n suficiente'}")
    for col, lab in ITEMS_COMPRA.items():
        sc = pd.to_numeric(det[col], errors="coerce")
        print(f"  {lab}: <=2 en detractores {int((sc <= 2).sum())}/{int(sc.notna().sum())}"
              f" | <=2 en todos {int((pd.to_numeric(d[col], errors='coerce') <= 2).sum())}/"
              f"{int(pd.to_numeric(d[col], errors='coerce').notna().sum())}")
    pp = det[ITEM_PARTE].astype(str)
    app = pp[pp != "No aplica"]
    print(f"  Tasación / parte de pago (aplica): detractores <=2 {int(app.isin(['1', '2']).sum())}/{len(app)}"
          f" | todos <=2 {int(d[ITEM_PARTE].astype(str).isin(['1', '2']).sum())}/"
          f"{int((d[ITEM_PARTE].astype(str) != 'No aplica').sum())}")
    en = pd.to_numeric(det[ITEM_ENTREGA], errors="coerce")
    print(f"  POSTVENTA entrega: detractores <=2 {int((en <= 2).sum())}/{int(en.notna().sum())}"
          f" | todos <=2 {int((pd.to_numeric(d[ITEM_ENTREGA], errors='coerce') <= 2).sum())}/"
          f"{int(pd.to_numeric(d[ITEM_ENTREGA], errors='coerce').notna().sum())}")
    for lab, col in [("Micro-1", "Microcategoría 1"), ("Micro-2", "Microcategoría 2"),
                     ("Micro-3", "Microcategoría 3")]:
        vc = det[col].dropna().value_counts()
        if len(vc):
            print(f"  Códigos {lab} en detractores: {dict(vc)}")
    for clave, col in TXT.items():
        txt = det[col].fillna("").astype(str)
        print(f"  Texto '{clave}' no vacío en detractores: {int((txt.str.len() > 0).sum())}")
        for k, rx in KEYWORDS.items():
            c = int(txt.str.contains(rx, case=False, regex=True).sum())
            if c:
                print(f"     palabra clave [{k}]: {c} filas")


MICRO_COLS = [f"Microcategoría {i}" for i in range(1, 6)] + [f"Microcategoría {i}.1" for i in range(1, 6)] \
    + [f"Microcategoría {i}.2" for i in range(1, 6)]
# Mapeo dolor -> códigos de Microcategoría (asignación de esta sesión, documentada en research/12)
DOLOR_MICRO = {
    "Respuesta y trato en venta (COMPRA)": ["Atención del vendedor", "Respuesta de consultas", "Disponibilidad de contacto"],
    "Claridad de precio y financiamiento (COMPRA)": ["Diferencia de precios en relación a la cotización", "Claridad de cobros",
                                                     "Financiamiento", "Percepción de precios"],
    "Estado del auto (COMPRA)": ["Detalles del vehículo", "Calidad del producto", "Limpieza del vehículo"],
    "Proceso y tiempos de compra (COMPRA)": ["Rapidez proceso en general"],
    "Entrega: plazos y entrega de información (POSTVENTA)": ["Plazos de entrega", "Entrega de información"],
    "Atención post venta (POSTVENTA)": ["Atención post una venta de vehículo", "Cumplimiento de acuerdos"],
    "Documentación: permiso y factura (POSTVENTA)": ["Permiso de circulación", "Factura"],
}
# Ítem de encuesta <=2 asociado a cada dolor (primario, sin micro)
DOLOR_ITEM = {
    "Respuesta y trato en venta (COMPRA)": ["Acogida en sala de ventas", "Atención del vendedor",
                                            "Facilidad de comunicación con vendedor"],
    "Claridad de precio y financiamiento (COMPRA)": ["Claridad de precios y opciones de financiamiento"],
    "Proceso y tiempos de compra (COMPRA)": ["Fluidez general del proceso"],
    "Entrega: plazos y entrega de información (POSTVENTA)": ["Proceso de Entrega"],
}


def ranking(df, m):
    """Filas detractoras por dolor (unión de ítem <=2 y códigos de microcategoría). Base = detractores."""
    d = df[m]
    nps = pd.to_numeric(d[NPS], errors="coerce")
    det = d[nps <= 6]
    base = len(det)
    codes = det[MICRO_COLS].apply(lambda col: col.fillna("")).values
    print(f"\n--- Ranking dolores (base = detractores, n={base}) ---")
    for dolor in DOLOR_MICRO:
        mask = pd.Series(False, index=det.index)
        for c in DOLOR_MICRO[dolor]:
            mask |= det[MICRO_COLS].eq(c).any(axis=1)
        for c in DOLOR_ITEM.get(dolor, []):
            mask |= pd.to_numeric(det[c], errors="coerce") <= 2
        n = int(mask.sum())
        print(f"  {dolor}: {n}/{base} ({100 * n / base if base else 0:.1f} %)")
    garantia = det[TXT["motiva"]].fillna("").str.contains("garant", case=False) | \
        det[TXT["entrega"]].fillna("").str.contains("garant", case=False)
    print(f"  Garantía (palabra clave, sin código de encuesta): {int(garantia.sum())}/{base}")
    pp = det[ITEM_PARTE].astype(str)
    app = pp[pp != "No aplica"]
    print(f"  Tasación / parte de pago (ítem 1-2 sobre base que aplica): {int(app.isin(['1', '2']).sum())}/{len(app)}")


def main():
    df = pd.read_parquet(RUTA)
    print(f"Filas Venta-Usados: {len(df)}")
    for nombre, m in universos(df).items():
        resumen(nombre, m, df)
        ranking(df, m)


if __name__ == "__main__":
    main()
