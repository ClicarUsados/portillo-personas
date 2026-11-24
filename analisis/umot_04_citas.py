"""UMOT 04 - Citas candidatas (<=15 palabras, anonimizadas) del pool UMOT con sentimiento Negative.

Imprime row_id + hasta 15 palabras con correos, teléfonos, patentes y números normalizados a [X].
Uso: revisión manual para elegir citas; las citas finales se copian a research/04_umot_demografia.md.
Fuentes: inputs_clean/*.parquet. Pool UMOT = Detractor (NPS 0-6) o volver No / No sé.

Cómo reproducirlo: python3 analisis/umot_04_citas.py
"""
import re
import sys
import os

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from umot_01_recomendacion_retorno import NPS_COL, VOLVER_COL, categoria_nps, cargar  # noqa: E402

PII = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[CORREO]"),
    (re.compile(r"\+?\d[\d\s-]{6,}\d"), "[NUM]"),
    (re.compile(r"\b[A-Z]{2,4}[-\s]?\d{2,4}\b"), "[PATENTE]"),
    (re.compile(r"\d+"), "[X]"),
]
TEXTO = {
    "Mecanica": "¿Qué te motiva a dar esa puntuación?",
    "VentaNuevo": "¿Nos contarías por qué?",
    "VentaUsados": "¿Qué te motivó a otorgar esta calificación?",
    "Clicar": "¿Tienes alguna otra recomendación o sugerencia? Tus comentarios son valiosos para nosotros.",
}
N_POR_ENCUESTA = 3


def limpiar(texto: str) -> str:
    for rx, rep in PII:
        texto = rx.sub(rep, texto)
    return " ".join(texto.split()[:15])


def main() -> None:
    fuentes = {"Mecanica": "CR_2025-Mecánica_*", "VentaNuevo": "CR_2025-Venta-Nuevo_*",
               "VentaUsados": "CR_2025-Venta-Usados_*", "Clicar": "CR_Clicar_*"}
    for enc, patron in fuentes.items():
        df = cargar(patron)
        cat = categoria_nps(df[NPS_COL[enc]])
        pool = (cat == "Detractor") | df[VOLVER_COL[enc]].astype(str).isin(["No", "No sé"])
        neg = pool & (df["sentimiento"] == "Negative") if "sentimiento" in df.columns else pool
        txt = df[TEXTO[enc]].fillna("").astype(str)
        cand = df.loc[neg & (txt.str.len() > 0), ["row_id"]].assign(t=txt)
        print(f"\n### {enc}: candidatos con texto={len(cand)}")
        for _, r in cand.sample(min(N_POR_ENCUESTA, len(cand)), random_state=7).iterrows():
            print(f"  row_id={r['row_id']} | \"{limpiar(r['t'])}\"")


if __name__ == "__main__":
    main()
