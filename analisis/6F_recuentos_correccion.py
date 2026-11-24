"""
6F - Recuentos de corrección para entregables/BUYER_PERSONAS_PORTILLO.md.

Cómo reproducirlo (desde la raíz del proyecto):
    python3 analisis/6F_recuentos_correccion.py

Qué hace:
  A. Mecánica (3C): universo PORT de 3C vs universo limpio (\\bPORTILLO\\b, excluye
     PORTILLOLA / PORTILLOTALCA). Muestra n, NPS, % detractores y % de notas en 0 o 10.
  B. Venta-Usados: 108 (prefijo PORT) vs 145 (\\bPORT) en nombre_concesionario.
  C. Encuesta de seguridad vial: filas con 'Portillo' en campaña o sensor.
  D. Conteo de etiquetas [DATO] / [WEB] / [HIPÓTESIS] / NO VERIFICADO en las secciones
     de evidencia (Ficha a Journey) de cada persona del entregable. Las bajadas de
     comunicación y la tarjeta de evidencia quedan fuera del conteo.

Solo lee inputs_clean/ y entregables/BUYER_PERSONAS_PORTILLO.md. No escribe archivos.
Nunca lee inputs_raw/.
"""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "inputs_clean"
DOC = ROOT / "entregables" / "BUYER_PERSONAS_PORTILLO.md"

MECANICA = CLEAN / "CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet"
USADOS = CLEAN / "CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet"
SEG_VIAL = CLEAN / "CR_Encuesta-de-seguridad-vial-en-Chile_2023-03-01_2026-11-23_ebe2e042__sin_segmento.parquet"

NPS = ("En base a tu última experiencia en servicio técnico, "
       "¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?")
SUCURSAL = "nombre_sucursal"


def nps_stats(s):
    n = len(s)
    if n == 0:
        return None
    prom = (s >= 9).mean() * 100
    det = (s <= 6).mean() * 100
    extremos = ((s == 0) | (s == 10)).mean() * 100
    return {"n": n, "nps": round(prom - det, 1), "det_pct": round(det, 1),
            "extremos_0_10_pct": round(extremos, 1)}


def fmt(nombre, st):
    if st is None:
        return f"  {nombre}: n=0"
    return (f"  {nombre}: n={st['n']} | NPS={st['nps']} | %detractores={st['det_pct']} "
            f"| %notas 0 o 10={st['extremos_0_10_pct']}")


def bloque_mecanica():
    print("A. Mecánica (3C): universos de Portillo")
    df = pd.read_parquet(MECANICA)
    suc = df[SUCURSAL].fillna("").astype(str)
    s_all = df[NPS].dropna()
    print(fmt("GRUPO_COMPLETO", nps_stats(s_all)))
    port3c = df.loc[suc.str.contains(r"(?i)\bPORT", regex=True), NPS].dropna()
    print(fmt("PORT 3C (regla original, \\bPORT)", nps_stats(port3c)))
    limpio = df.loc[suc.str.contains(r"(?i)\bPORTILLO\b", regex=True), NPS].dropna()
    print(fmt("PORTILLO limpio (\\bPORTILLO\\b, excluye PORTILLOLA/TALCA)", nps_stats(limpio)))
    gap = df.loc[suc.str.fullmatch(r"GAP PORTILLO SERVICIO"), NPS].dropna()
    print(fmt("GAP PORTILLO SERVICIO (solo esta sucursal)", nps_stats(gap)))
    dudosas = df.loc[suc.str.contains(r"(?i)PORTILLOLA|PORTILLOTALCA", regex=True), NPS].dropna()
    print(f"  filas PORTILLOLA / PORTILLOTALCA dentro del universo 3C: {len(dudosas)}")
    print()


def bloque_usados():
    print("B. Venta-Usados: universo Portillo por nombre_concesionario")
    df = pd.read_parquet(USADOS)
    con = df["nombre_concesionario"].fillna("").astype(str)
    print(f"  prefijo ^PORT: {int(con.str.match(r'(?i)PORT').sum())}")
    print(f"  \\bPORT en cualquier posición: {int(con.str.contains(r'(?i)\bPORT', regex=True).sum())}")
    print()


def bloque_seguridad_vial():
    print("C. Seguridad vial: campaña o sensor con 'Portillo'")
    df = pd.read_parquet(SEG_VIAL)
    camp = df["campaña o sensor"].fillna("").astype(str)
    print(f"  campaña o sensor contiene 'Portillo': {int(camp.str.contains('Portillo', case=False).sum())}")
    print()


BLOQUES_EVIDENCIA = re.compile(r"^## \d+\. (?:Persona|Hipótesis) (P\d|H\d)", re.MULTILINE)
CORTE_EVIDENCIA = ("### Bajada de comunicación", "### Tarjeta de evidencia")
ETIQUETAS = {
    "DATO": re.compile(r"\[DATO"),
    "WEB": re.compile(r"\[WEB"),
    # Cuenta también las etiquetas con referencia, p. ej. "[HIPÓTESIS C-01: ...]".
    "HIPÓTESIS": re.compile(r"\[HIPÓTESIS"),
    "NO VERIFICADO": re.compile(r"NO VERIFICADO"),
}


def secciones_evidencia(texto):
    """Devuelve {persona: texto} desde la ficha hasta antes de Bajada / Tarjeta."""
    out = {}
    partes = BLOQUES_EVIDENCIA.split(texto)
    # partes = [previo, 'P1', cuerpo1, 'P2', cuerpo2, ...]
    for i in range(1, len(partes), 2):
        persona, cuerpo = partes[i], partes[i + 1]
        corte = len(cuerpo)
        for marca in CORTE_EVIDENCIA + ("\n## ",):
            pos = cuerpo.find(marca)
            if pos != -1:
                corte = min(corte, pos)
        out[persona] = cuerpo[:corte]
    return out


def bloque_etiquetas():
    print("D. Conteo de etiquetas en secciones de evidencia (Ficha a Journey)")
    texto = DOC.read_text(encoding="utf-8")
    for persona, cuerpo in secciones_evidencia(texto).items():
        conteo = {k: len(rx.findall(cuerpo)) for k, rx in ETIQUETAS.items()}
        con_etiqueta = conteo["DATO"] + conteo["WEB"] + conteo["HIPÓTESIS"]
        partes = []
        for k in ("DATO", "WEB", "HIPÓTESIS"):
            pct = round(100 * conteo[k] / con_etiqueta, 1) if con_etiqueta else 0.0
            partes.append(f"{k}={conteo[k]} ({pct} %)")
        print(f"  {persona}: " + " | ".join(partes)
              + f" | denominador etiquetado={con_etiqueta} | NO VERIFICADO (fuera del denominador)={conteo['NO VERIFICADO']}")
    print()


def main():
    bloque_mecanica()
    bloque_usados()
    bloque_seguridad_vial()
    bloque_etiquetas()


if __name__ == "__main__":
    main()
