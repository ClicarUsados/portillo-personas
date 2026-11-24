"""
2B_leads_cotizacion.py - Subagente B: leads y proceso de cotizacion (CR_Lead-Portillo).

Fuente: inputs_clean/CR_Lead-Portillo_*.parquet (1.003 filas, 2023-06-08 a 2026-01-23).
Fecha de extraccion de los archivos: 2026-11-23.
Universos: GRUPO_COMPLETO (todo el archivo) y PORTILLO_HIPOTESIS
(nombre_sucursal contiene PORT o PORTILLO; [HIPOTESIS] bloqueada, ver research/00_mapeo_portillo.md).

Codificacion manual (HIPOTESIS del subagente B):
- Opcion "otros" de la pregunta de necesidades: tabla OTROS_CODIGO por row_id.
- Motivo "Por que?": reglas por palabra clave, multietiqueta (THEMES).
Las citas verbatim se toman de una lista fija (QUOTES), se verifican en el dato
y se imprimen anonimizadas, con row_id y maximo 15 palabras.

Cómo reproducirlo: python3 analisis/2B_leads_cotizacion.py

Solo imprime conteos y porcentajes, mas las pocas citas de QUOTES. No imprime filas crudas.
"""

import glob
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FECHA_EXTRACCION = "2026-11-23"
MIN_N = 30  # por debajo de este n, la cifra no es concluyente

Q_PROC = "¿Cómo evaluaría el proceso de cotización?"
Q_CONT = "¿Ha sido contactado por nuestro equipo de ventas luego de su solicitud de cotización?"
Q_CAL = "¿Cómo evaluaría la calidad del contacto?"
Q_NEED = "¿Qué necesita para seguir con su proceso de cotización?"
Q_WHY = "¿Por qué?"
Q_OTROS = "Texto opción otros"
Q_MARCA = "des_marca"
Q_TIPO = "tipo_oportunidad"
Q_SUC = "nombre_sucursal"
Q_ORIGEN = "origen"
Q_FECHA = "fecha respuesta"

# Codificacion manual de "Texto opcion otros" (57 filas). Solo codigos, sin texto.
OTROS_CODIGO = {
    # Declara compra ya realizada (autodeclaracion en texto libre, no verificada contra ventas)
    **{rid: "Declara compra ya realizada" for rid in [
        "CR_Lead-Portillo_202#3", "CR_Lead-Portillo_202#90", "CR_Lead-Portillo_202#149",
        "CR_Lead-Portillo_202#150", "CR_Lead-Portillo_202#153", "CR_Lead-Portillo_202#160",
        "CR_Lead-Portillo_202#161", "CR_Lead-Portillo_202#163", "CR_Lead-Portillo_202#164",
        "CR_Lead-Portillo_202#185", "CR_Lead-Portillo_202#187", "CR_Lead-Portillo_202#188",
        "CR_Lead-Portillo_202#213", "CR_Lead-Portillo_202#228", "CR_Lead-Portillo_202#241",
        "CR_Lead-Portillo_202#250", "CR_Lead-Portillo_202#255", "CR_Lead-Portillo_202#263",
        "CR_Lead-Portillo_202#268", "CR_Lead-Portillo_202#279", "CR_Lead-Portillo_202#311",
        "CR_Lead-Portillo_202#315", "CR_Lead-Portillo_202#323", "CR_Lead-Portillo_202#325",
        "CR_Lead-Portillo_202#326", "CR_Lead-Portillo_202#328", "CR_Lead-Portillo_202#333",
        "CR_Lead-Portillo_202#339", "CR_Lead-Portillo_202#340", "CR_Lead-Portillo_202#351",
        "CR_Lead-Portillo_202#360", "CR_Lead-Portillo_202#364", "CR_Lead-Portillo_202#372",
        "CR_Lead-Portillo_202#374", "CR_Lead-Portillo_202#376", "CR_Lead-Portillo_202#377",
        "CR_Lead-Portillo_202#380", "CR_Lead-Portillo_202#385", "CR_Lead-Portillo_202#401",
        "CR_Lead-Portillo_202#409", "CR_Lead-Portillo_202#424", "CR_Lead-Portillo_202#427",
    ]},
    "CR_Lead-Portillo_202#181": "En proceso de compra o con asesor",
    "CR_Lead-Portillo_202#274": "En proceso de compra o con asesor",
    "CR_Lead-Portillo_202#165": "Espera de contacto o lentitud",
    "CR_Lead-Portillo_202#194": "Espera de contacto o lentitud",
    "CR_Lead-Portillo_202#24": "Sigue evaluando alternativas",
    "CR_Lead-Portillo_202#65": "Sigue evaluando alternativas",
    "CR_Lead-Portillo_202#30": "No continuara con el proceso",
    "CR_Lead-Portillo_202#71": "Financiamiento o parte de pago",
    "CR_Lead-Portillo_202#386": "Satisfaccion sin barrera",
    "CR_Lead-Portillo_202#83": "Sin contenido o ambiguo",
    "CR_Lead-Portillo_202#103": "Sin contenido o ambiguo",
    "CR_Lead-Portillo_202#156": "Sin contenido o ambiguo",
    "CR_Lead-Portillo_202#273": "Sin contenido o ambiguo",
    "CR_Lead-Portillo_202#362": "Sin contenido o ambiguo",
    "CR_Lead-Portillo_202#399": "Sin contenido o ambiguo",
}

# Reglas de palabra clave para "Por que?" (multietiqueta, sobre texto sin tildes y en minusculas).
THEMES = {
    "Sin respuesta o sin contacto": r"nadie|nunca (me )?(contact|llam|respond|enviaron|llego|llegó)|no (me )?(contact|llam|respond|enviaron|llego|han contest)|ni me (llam|respond)|sin respuesta|no tuve respuesta|no responden|no hubo comunicacion|aun no|no recib|no me dieron bola|no me contest|ni una sola",
    "Lentitud o tiempos": r"lent|tard|demora|tiempo de respuesta|rapidez|agil|esperando|semana en responder|respuesta lenta|respondiendo antes|en responder",
    "Precio o transparencia": r"transpar|precio|valor|honest|engan|costo|mentir|bajaron mucho|publicidad enga",
    "Financiamiento, credito o parte de pago": r"credito|financ|tasa|parte de pago|tasacion|tasar|dicom|liquidaci|cero pie",
    "Reserva o devolucion de dinero": r"reserva|devolu|devuelv|plata",
    "Stock o disponibilidad del vehiculo": r"stock|no hay autos|vendio|vendió|vendido|no tienen el auto|no tenian|no tenían|disponible|no aun cotizan",
    "Informacion o documentacion": r"informaci|papeles|document|detall|no me (dieron|enviaron|entregan)|no entregan|respuestas? (que|a|de)|contestar|consultas|poca info|no me dieron",
    "Trato o atencion del ejecutivo": r"trato|amable|pesim|horrible|mala atencion|muy mala|malo|respetuos|distante|consecuente|no me dieron bola|no me daban soluciones|no fue de mucha ayuda|sin animo",
}

# Citas fijas: deben existir textualmente en el dato, <=15 palabras, anonimizadas.
QUOTES = [
    "Solicite cotización y nadie me ha contactado hasta el momento",
    "Nunca me enviaron nada, solo me llego un mensaje automático por WhatsApp",
    "No me respondieron nada sobre valores, opciones de pago y financiamiento.",
    "Ser más trasparente con el costo establecido en la cotización",
    "Se suponía que me contactarían y no ha pasado nada",
    "No tienen el auto para verlo",
]


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "NA"


def strip_acc(s):
    if not isinstance(s, str):
        return None
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper().strip()


def tipo_norm(s):
    t = strip_acc(s)
    if t in ("VEHICULO NUEVOS", "NUEVOS"):
        return "nuevo"
    if t in ("VEHICULOS USADOS", "USADOS"):
        return "usado"
    return "SIN DATO"


def load():
    paths = glob.glob(str(ROOT / "inputs_clean" / "CR_Lead-Portillo_*.parquet"))
    assert len(paths) == 1, paths
    return pd.read_parquet(paths[0])


def dist(series, base_label, base_n):
    vc = series.value_counts(dropna=False).sort_index()
    for k, v in vc.items():
        print(f"  {str(k):<70} n={v:<5} {pct(v, base_n)} ({base_label})")


def group_table(df, col):
    total = len(df)
    print(f"  {col} | n total={total}")
    print(f"  {'valor':<34}{'n':>6}{'%total':>9}{'top2(4-5)':>11}{'bottom2(1-2)':>14}{'contact_n':>10}{'contact_Si%':>13}  nota")
    for k, g in df.groupby(col, dropna=False):
        n = len(g)
        q = g[Q_PROC]
        top2 = int((q >= 4).sum())
        bot2 = int((q <= 2).sum())
        cont = g[Q_CONT].dropna()
        si = int((cont == "Sí").sum())
        nota = "NO CONCLUYENTE (n<%d)" % MIN_N if n < MIN_N else ""
        print(f"  {str(k):<34}{n:>6}{pct(n, total):>9}{pct(top2, n):>11}{pct(bot2, n):>14}{len(cont):>10}{pct(si, len(cont)):>13}  {nota}")


def main():
    df = load()
    total = len(df)
    print(f"Filas: {total} | columnas: {df.shape[1]} | fecha extraccion: {FECHA_EXTRACCION}")
    print(f"Rango fecha respuesta: {df[Q_FECHA].min()} a {df[Q_FECHA].max()}")
    years = pd.to_datetime(df[Q_FECHA]).dt.year.value_counts().sort_index()
    print("Filas por ano de fecha respuesta:", {int(k): int(v) for k, v in years.items()})

    print("\n== 1. Evaluacion del proceso de cotizacion (base: 1003) [DATO]")
    dist(df[Q_PROC], "sobre 1003", total)
    print("  NOTA: direccion de la escala (5 = mejor?) NO VERIFICADA; no aparece en el diccionario.")

    print("\n== 1b. Contacto por ventas (base: 1003) [DATO]")
    dist(df[Q_CONT], "sobre 1003", total)
    n_cont = int(df[Q_CONT].notna().sum())
    print(f"  Base respondida (contacto): {n_cont}")

    print("\n== 1c. Calidad del contacto (base respondida = 371 o la que indique el dato) [DATO]")
    cal = df[Q_CAL].dropna()
    print(f"  base respondida: {len(cal)} | sobre total {total}: {pct(len(cal), total)}")
    for k, v in cal.value_counts().sort_index().items():
        print(f"  calidad={int(k)}: n={v} {pct(v, len(cal))} (sobre respondidos)")

    print("\n== 1d. Cruce proceso x contacto (n) [DATO]")
    print(pd.crosstab(df[Q_PROC], df[Q_CONT].fillna("sin respuesta")).to_string())

    print("\n== 2. Que necesita para seguir (base respondida; 1003 total) [DATO]")
    need = df[Q_NEED].dropna()
    print(f"  base respondida: {len(need)} | sobre total {total}: {pct(len(need), total)}")
    for k, v in need.value_counts().items():
        print(f"  {k:<42} n={v:<5} {pct(v, len(need))} (sobre respondidos) | {pct(v, total)} (sobre total)")

    print("\n== 2b. Codificacion de 'Opcion otros' (HIPOTESIS del subagente B)")
    otros_ids = set(df.loc[df[Q_OTROS].notna(), "row_id"])
    codigos_ids = set(OTROS_CODIGO)
    assert otros_ids == codigos_ids, (len(otros_ids), len(codigos_ids), len(otros_ids ^ codigos_ids))
    cod = pd.Series(OTROS_CODIGO).value_counts()
    for k, v in cod.items():
        print(f"  {k:<42} n={v:<4} {pct(v, len(otros_ids))} (sobre 'otros' n={len(otros_ids)})")
    print(f"  Cruce: 'Opcion otros' vs contacto respondido -> "
          f"{pd.crosstab(df.loc[df[Q_OTROS].notna(), Q_CONT].fillna('sin respuesta'), 'n').to_string()}")

    print("\n== 3a. Universos")
    suc = df[Q_SUC].fillna("")
    mask_port = suc.str.upper().str.contains(r"\bPORT(?:ILLO)?\b", regex=True)
    print(f"  GRUPO_COMPLETO: n={total}")
    print(f"  PORTILLO_HIPOTESIS (nombre_sucursal con PORT/PORTILLO): n={int(mask_port.sum())} {pct(int(mask_port.sum()), total)} [HIPOTESIS bloqueada]")
    for label, sub in [("GRUPO_COMPLETO", df), ("PORTILLO_HIPOTESIS", df[mask_port]), ("RESTO (no PORT)", df[~mask_port])]:
        q = sub[Q_PROC]
        c = sub[Q_CONT].dropna()
        print(f"  {label:<20} n={len(sub):<5} top2={pct(int((q >= 4).sum()), len(sub))} "
              f"bottom2={pct(int((q <= 2).sum()), len(sub))} contacto_respondido={len(c)} "
              f"contacto_Si={pct(int((c == 'Sí').sum()), len(c))}")

    print("\n== 3b. Marca (des_marca normalizada: mayusculas y sin tildes)")
    df = df.assign(marca_norm=df[Q_MARCA].map(lambda s: strip_acc(s) if isinstance(s, str) else "SIN DATO"))
    group_table(df, "marca_norm")
    print("  NOTA: 'USADOS' es un valor de des_marca que indica usado, no una marca.")

    print("\n== 3c. Tipo de oportunidad (regla: 'Vehiculo Nuevos'/'NUEVOS' -> nuevo; 'Vehiculos Usados'/'USADOS' -> usado)")
    df = df.assign(tipo_norm=df[Q_TIPO].map(tipo_norm))
    group_table(df, "tipo_norm")

    print("\n== 3d. Sucursal (nombre_sucursal; vacio = SIN DATO)")
    df = df.assign(suc_norm=suc.where(suc != "", "SIN DATO"))
    counts = df["suc_norm"].value_counts()
    print(f"  sucursales distintas: {len(counts)} | con n>={MIN_N}: {int((counts >= MIN_N).sum())} | con n<{MIN_N}: {int((counts < MIN_N).sum())}")
    grandes = df[df["suc_norm"].isin(counts[counts >= MIN_N].index)]
    group_table(grandes, "suc_norm")
    print(f"  Sucursales con n<{MIN_N} agrupadas: n={int((counts[counts < MIN_N]).sum())} ({pct(int(counts[counts < MIN_N].sum()), total)})")

    print("\n== 4. Origen (canal de entrada; descriptivo, NO atribucion de venta) [DATO]")
    dist(df[Q_ORIGEN], "sobre 1003", total)

    print("\n== 5. Motivo 'Por que?' (base con texto; multietiqueta por palabra clave) [HIPOTESIS]")
    why = df[Q_WHY].dropna()
    why_low = df.loc[df[Q_WHY].notna() & (df[Q_PROC] <= 2), Q_WHY]
    print(f"  textos 'Por que?': {len(why)} sobre total {total} | con Q1 en 1-2: {len(why_low)}")
    norm = why.map(strip_acc).str.lower()
    norm_low = why_low.map(strip_acc).str.lower()
    for theme, pattern in THEMES.items():
        hits = int(norm.str.contains(pattern, regex=True).sum())
        hits_low = int(norm_low.str.contains(pattern, regex=True).sum())
        print(f"  {theme:<42} n={hits:<4} {pct(hits, len(why))} (sobre textos) | Q1 1-2: n={hits_low} {pct(hits_low, len(why_low))}")

    print("\n== 5b. Citas verbatim (verificadas en el dato, <=15 palabras)")
    for q in QUOTES:
        words = len(q.split())
        hits = df.loc[df[Q_WHY].fillna("").str.contains(q, regex=False), "row_id"].tolist()
        assert len(hits) == 1, (q, len(hits))
        assert words <= 15, (q, words)
        print(f"  [{hits[0]}] \"{q}\" ({words} palabras)")

    print("\n== 6. Chequeos de consistencia (no se corrige ninguna cifra)")
    n_cal = int(df[Q_CAL].notna().sum())
    print(f"  calidad respondida={n_cal} vs contacto Si={int((df[Q_CONT] == 'Sí').sum())} vs contacto respondido={n_cont}")
    print(f"  necesidad respondida={len(need)} vs contacto respondido={n_cont}")
    ya_contacto_no = int(((df[Q_CONT] == "No") & (df[Q_NEED] == "Ya estoy en contacto con mi ejecutivo")).sum())
    print(f"  Contacto=No pero necesidad='Ya estoy en contacto con mi ejecutivo': n={ya_contacto_no}")
    print(f"  Q_PROC no respondida: {int(df[Q_PROC].isna().sum())}")
    tu = df.loc[df[Q_TIPO].notna(), "tipo_norm"].value_counts().to_dict()
    print(f"  tipo_oportunidad tras normalizar: {tu} (sin dato en {int(df[Q_TIPO].isna().sum())} filas)")
    print(f"  des_marca=USADOS: n={int((df[Q_MARCA] == 'USADOS').sum())} vs tipo usado normalizado: {tu.get('usado', 0)}")
    print(f"  nombre_sucursal con PORT: n={int(mask_port.sum())} (mapeo 00_mapeo_portillo.md dice 140)")
    print(f"  marca (columna) vacia: {int(df['marca'].isna().sum())} de {total}")


if __name__ == "__main__":
    main()
