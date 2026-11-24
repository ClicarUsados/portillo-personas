"""8H - C-05 y cortes por año (Lead-Portillo, pregunta de contacto de ventas).

Auditoría MdV final, 2026-11-23. Reproduce:
  - base correcta: respondidos (Sí o No) = 431; "No" = 60; tasa = 13,9 %.
  - cortes por año de fecha de respuesta (2023 no tiene respuestas a la pregunta).
Solo lee inputs_clean/. Imprime conteos.
Cómo reproducirlo: python3 analisis/8H_c05_por_anio.py
"""
import glob
import os

import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL = "¿Ha sido contactado por nuestro equipo de ventas luego de su solicitud de cotización?"


def main():
    rutas = glob.glob(os.path.join(RAIZ, "inputs_clean", "CR_Lead-Portillo_*"))
    if len(rutas) != 1:
        raise SystemExit(f"Se esperaba 1 archivo de leads, hay {len(rutas)}")
    df = pd.read_parquet(rutas[0])
    resp = df[COL].astype("string").str.strip()
    anio = pd.to_datetime(df["fecha respuesta"], errors="coerce").dt.year
    print("8H - C-05 | extracción 2026-11-23")
    print(f"filas={len(df)} | sin respuesta a la pregunta={int(resp.isna().sum())}")
    respondidos = resp.isin(["Sí", "No"])
    no = int((resp == "No").sum())
    si = int((resp == "Sí").sum())
    base = int(respondidos.sum())
    print(f"base respondidos={base} (Sí={si}, No={no}) | 'No' sobre respondidos = {100 * no / base:.1f} %")
    print(f"'No' sobre el total de filas = {100 * no / len(df):.1f} % (denominador incorrecto; no usar)")
    print("\nCortes por año de fecha de respuesta:")
    for y in sorted(anio.dropna().unique()):
        m = anio == y
        r = resp[m]
        b = int(r.isin(["Sí", "No"]).sum())
        n_no = int((r == "No").sum())
        tasa = f"{100 * n_no / b:.1f} %" if b else "sin base"
        print(f"  {int(y)}: filas={int(m.sum())} | respondidos={b} | 'No'={n_no} | tasa={tasa}")
    m23 = anio == 2023
    print(f"  2023: filas={int(m23.sum())} | respondidos={int(resp[m23].isin(['Sí', 'No']).sum())} (la pregunta no tiene respuestas en 2023)")


if __name__ == "__main__":
    main()
