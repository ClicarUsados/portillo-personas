"""UMOT 03 - Demografía (edad y género) de la encuesta de seguridad vial.

Fuente: inputs_clean/CR_Encuesta-de-seguridad-vial-en-Chile_*.parquet (n=709, 2025-10-22 a 2025-10-29).
SESGO DECLARADO: solo clientes de autos NUEVOS, un mes, no representa a seminuevos (Venta-Usados).
Columnas: 'Rango de edad', 'Género', 'campaña o sensor', 'nombre_concesionario'.
Cruce de control: 'campaña o sensor' con 'Portillo' ([DATO]) y PORTILLO_HIPOTESIS
(\\bPORT en nombre_concesionario, [HIPÓTESIS]; BLOQUEADO: Beto / Iván Balaguera).
Imprime conteos y porcentajes; sin filas.

Cómo reproducirlo: python3 analisis/umot_03_demografia_seguridad_vial.py
"""
import glob
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "2026-11-23"


def pct(a: float, b: float) -> float:
    return 0.0 if b == 0 else 100.0 * a / b


def tabla(serie: pd.Series, etiqueta: str, total: int) -> None:
    nn = int(serie.notna().sum())
    print(f"  {etiqueta}: válidos={nn} de {total} ({pct(nn, total):.1f}%), faltantes={total - nn}")
    for k, v in serie.value_counts(dropna=True).items():
        print(f"    {k}: n={int(v)} | {pct(int(v), total):.1f}% del total | {pct(int(v), nn):.1f}% de válidos")


def main() -> None:
    rutas = glob.glob(os.path.join(ROOT, "inputs_clean", "CR_Encuesta-de-seguridad-vial*"))
    if len(rutas) != 1:
        raise SystemExit("Archivo de seguridad vial no encontrado de forma única")
    df = pd.read_parquet(rutas[0])
    total = len(df)
    print(f"UMOT 03 - Demografía seguridad vial | extracción {FECHA} | n={total}")
    print("  SESGO: solo clientes de autos nuevos; 2025-10-22..2025-10-29; no representa seminuevos.")
    tabla(df["Rango de edad"], "Rango de edad", total)
    tabla(df["Género"], "Género", total)
    camp = df["campaña o sensor"].fillna("").astype(str)
    print("\n  Campañas [DATO]:")
    for c, n in camp.value_counts().items():
        print(f"    {c}: n={int(n)}")
    portillo_camp = camp.str.contains("portillo", case=False, regex=False)
    suc = df["nombre_concesionario"].fillna("").astype(str)
    porte = suc.str.contains(r"\bPORT", case=False, regex=True)
    print(f"  Campaña 'Portillo' [DATO]: n={int(portillo_camp.sum())}")
    print(f"  PORTILLO_HIPOTESIS [HIPÓTESIS]: n={int(porte.sum())}")
    tabla(df.loc[portillo_camp, "Rango de edad"], "Rango de edad (campaña Portillo)", int(portillo_camp.sum()))
    tabla(df.loc[portillo_camp, "Género"], "Género (campaña Portillo)", int(portillo_camp.sum()))


if __name__ == "__main__":
    main()
