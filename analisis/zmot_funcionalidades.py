"""ZMOT: funcionalidades pedidas en el sitio web (encuesta funcionalidades Web, 2025-07 a 2025-08).

Fuente unica: inputs_clean/CR_Encuesta-funcionalidades-Web_2023-03-01_2026-11-23_9f03c80b__sin_segmento.parquet
Universos: GRUPO_COMPLETO (324 filas). PORTILLO_HIPOTESIS = PORT/PORTILLO en nombre_concesionario [HIPOTESIS, bloqueada: Beto / Ivan Balaguera].
Advertencia: todas las filas son nombre_categoria_venta = NUEVO y traen fec_factura, es decir son compradores de vehiculo nuevo,
no visitantes en ZMOT. Estas cifras son lista de deseos post-venta, usada como proxy.
Imprime solo conteos y porcentajes.

Cómo reproducirlo: python3 analisis/zmot_funcionalidades.py
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = RAIZ / "inputs_clean" / "CR_Encuesta-funcionalidades-Web_2023-03-01_2026-11-23_9f03c80b__sin_segmento.parquet"
FECHA = "2026-11-23"
COL_CAMPANA = "campaña o sensor"
COL_CONCES = "nombre_concesionario"
PREFIJO_TOP3 = "Por favor, selecciona entre las siguientes funcionalidades"
NO_LIKERT = {"reinicio", "nps", "id_servicio", "vendedor"}


def etiqueta_top3(col: str) -> str:
    """Quita el prefijo de la pregunta y deja la opcion."""
    return col.split("-", 1)[-1].replace("​", "").replace(".", "").strip()


def main() -> None:
    df = pd.read_parquet(ARCHIVO)
    total = len(df)
    print(f"[ZMOT funcionalidades web] fecha de extraccion {FECHA} | filas={total}")

    print("\n== A. Compradores, no visitantes (contexto) ==")
    print(f"  nombre_categoria_venta NUEVO: {int((df['nombre_categoria_venta'] == 'NUEVO').sum())} de {total}")
    print(f"  fec_factura no vacio: {int(df['fec_factura'].notna().sum())} de {total}")
    fac = pd.to_datetime(df["fec_factura"], format="%d-%m-%Y", errors="coerce")
    resp = pd.to_datetime(df["fecha respuesta"], errors="coerce", dayfirst=False, format="mixed")
    dias = (resp - fac).dt.days
    print(f"  fec_factura parseable: {int(fac.notna().sum())} | rango año-mes factura: {fac.min():%Y-%m} a {fac.max():%Y-%m}")
    print(f"  dias entre factura y respuesta: mediana={dias.median():.0f}, n_negativos={int((dias < 0).sum())}")

    top3 = [c for c in df.columns if c.startswith(PREFIJO_TOP3)]
    seleccion = df[top3].notna() & (df[top3].astype(str).apply(lambda s: s.str.strip()) != "")
    total_marcas = int(seleccion.values.sum())
    completas = int((seleccion.sum(axis=1) == 3).sum())
    print(f"\n== B. Top-3 funcionalidades (base {total}) [DATO] ==")
    print(f"  opciones columnas={len(top3)} | marcas totales={total_marcas} (esperado {3*total}) | respondieron 3 completas={completas}")
    conteo = seleccion.sum().sort_values(ascending=False)
    for col, n in conteo.items():
        print(f"  {etiqueta_top3(col)[:70]}: {int(n)} ({100*n/total:.1f}%)")

    likert = [c for c in df.columns if df[c].dtype.kind in "iu" and c not in NO_LIKERT]
    print(f"\n== C. Niveles de acuerdo (escala 1-5, extremos NO VERIFICADOS) base {total} ==")
    for col in likert:
        serie = df[col]
        de = int((serie >= 4).sum())
        neu = int((serie == 3).sum())
        en = int((serie <= 2).sum())
        print(f"  {col.replace(chr(0x200b), '')[:70]}: de_acuerdo={100*de/total:.1f}% neutro={100*neu/total:.1f}% en_desacuerdo={100*en/total:.1f}%")

    print("\n== D. NPS (sin indicador: escala truncada) ==")
    print(f"  valores: {df['nps'].value_counts().sort_index().to_dict()}")

    print("\n== E. Campaña o sensor y universo PORTILLO ==")
    for valor, n in df[COL_CAMPANA].value_counts().items():
        print(f"  {valor}: {int(n)} ({100*n/total:.1f}%)")
    por_campana = int(df[COL_CAMPANA].str.contains("Portillo", case=False).sum())
    por_concesionario = int(df[COL_CONCES].fillna("").str.upper().str.contains(r"PORTILLO|\bPORT\b", regex=True).sum())
    print(f"  CONTRADICCION: campaña 'Portillo' = {por_campana} [DATO] | nombre_concesionario PORT/PORTILLO = {por_concesionario} [HIPOTESIS]")

    print("\n== F. Top-3 en subgrupo PORTILLO_HIPOTESIS (solo descriptivo, n<30 total) ==")
    mask = df[COL_CONCES].fillna("").str.upper().str.contains(r"PORTILLO|\bPORT\b", regex=True)
    print(f"  n={int(mask.sum())}")
    for col, n in seleccion[mask].sum().sort_values(ascending=False).items():
        print(f"  {etiqueta_top3(col)[:60]}: {int(n)}")


if __name__ == "__main__":
    main()
