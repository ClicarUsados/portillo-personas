"""
1A - Voz del comprador (ventas): motivos NPS, etapas del proceso y verbatim.

Fuentes (solo inputs_clean/):
  - CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f6b8ef__sin_segmento.parquet
  - CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet
Fecha de extracción de los archivos: 2026-11-23.

Universos:
  - GRUPO_COMPLETO: todas las filas.
  - PORTILLO_HIPOTESIS: nombre_concesionario contiene la palabra PORT o PORTILLO
    (ver research/00_mapeo_portillo.md). Asignación a Portillo = [HIPÓTESIS], bloqueada
    hasta confirmación de Beto / Iván Balaguera.

Segmentos NPS: promotor 9-10, pasivo 7-8, detractor 0-6.
Detractor de etapa (criterio de este script, no estándar): puntuación 1-2 en escala 1-5.
Polarización (criterio de este script): media >= 4,0 y % de 1-2 >= 10 %.

Salida: solo conteos y porcentajes. No imprime filas, verbatim ni identificadores.

Cómo reproducirlo: python3 analisis/1A_voz_ventas.py
"""
from pathlib import Path
import glob

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
FECHA = "2026-11-23"
NPS = ("En base a tu última experiencia de compra, ¿qué tan probable es que "
       "recomiendes #empresa# a un familiar o amigo?")
SEGMENTOS = ["promotor", "pasivo", "detractor"]
ETAPAS = [
    "Acogida en sala de ventas",
    "Atención del vendedor",
    "Claridad de precios y opciones de financiamiento",
    "Facilidad de comunicación con vendedor",
    "Fluidez general del proceso",
]

# Bloques de verbatim por sufijo de columna de codificación (Macrocategoría N<sufijo>).
# El sufijo "" es el bloque inmediatamente posterior a la pregunta NPS.
# Los sufijos ".1" y ".2" se identifican por POSICIÓN en el archivo, no por nombre semántico.
ARCHIVOS = {
    "Nuevo": {
        "prefijo": "CR_2025-Venta-Nuevo",
        "verbatim": {
            "": "¿Qué te motiva a dar esa puntuación?",
            ".1": "¿Nos contarías por qué?",  # tras Fluidez (bloque de etapas)
            ".2": "¿Nos contarías por qué?.1",  # tras Vehículo en parte de pago
        },
        "puntajes": ETAPAS + ["Información proporcionada por vendedor", "Vehículo en parte de pago"],
    },
    "Usados": {
        "prefijo": "CR_2025-Venta-Usados",
        "verbatim": {
            "": "¿Qué te motiva a dar esa puntuación?",
            ".1": "¿Qué te motivó a otorgar esta calificación?",  # tras Vehículo en parte de pago
            ".2": "¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor?",  # tras Proceso de Entrega
        },
        "puntajes": ETAPAS + ["Vehículo en parte de pago", "Proceso de Entrega"],
    },
}


def cargar(prefijo):
    ruta = glob.glob(str(RAIZ / "inputs_clean" / f"{prefijo}*.parquet"))[0]
    df = pd.read_parquet(ruta)
    df["nps"] = pd.to_numeric(df[NPS], errors="coerce")
    # pd.cut etiqueta de menor a mayor: (-1,6]=detractor, (6,8]=pasivo, (8,10]=promotor.
    df["segmento"] = pd.cut(df["nps"], [-1, 6, 8, 10], labels=["detractor", "pasivo", "promotor"]).astype(object)
    return df


def universo(df, nombre):
    if nombre == "GRUPO_COMPLETO":
        return df
    mascara = df["nombre_concesionario"].astype(str).str.contains(r"\bPORT", case=False, regex=True)
    return df[mascara]


def con_texto(serie):
    return serie.notna() & (serie.astype(str).str.strip() != "")


def pct(parte, total):
    return f"{100 * parte / total:.1f}%" if total else "n/a"


def imprimir_segmentos(df, titulo):
    print(f"\n### {titulo}: n={len(df)}")
    print(f"  NPS sin dato: {df['nps'].isna().sum()}")
    for seg in SEGMENTOS:
        print(f"  {seg}: {(df['segmento'] == seg).sum()} ({pct((df['segmento'] == seg).sum(), df['nps'].notna().sum())})")


def ranking_macro(df, sufijo, verbatim_col, titulo):
    macro = f"Macrocategoría 1{sufijo}"
    print(f"\n### Ranking macro1 ({macro}) - {titulo}")
    for seg in SEGMENTOS:
        s = df[df["segmento"] == seg]
        codificadas = s[macro].notna()
        print(f"  [{seg}] filas={len(s)} con_verbatim={con_texto(s[verbatim_col]).sum()} "
              f"codificadas={codificadas.sum()} sin_codificar_con_verbatim="
              f"{(con_texto(s[verbatim_col]) & ~codificadas).sum()}")
        for cat, n in s.loc[codificadas, macro].value_counts().items():
            print(f"     {cat}: {n} ({pct(n, codificadas.sum())} de codificadas)")


def menciones_cualquiera(df, sufijo, titulo):
    cols = [f"Macrocategoría {i}{sufijo}" for i in range(1, 6)]
    print(f"\n### Menciones en cualquier macro 1-5 (sufijo '{sufijo}') - {titulo}")
    for seg in SEGMENTOS:
        s = df[df["segmento"] == seg]
        base = s[cols].notna().any(axis=1).sum()
        print(f"  [{seg}] filas_con_alguna_macro={base}")
        cats = pd.unique(s[cols].values.ravel())
        conteos = {c: s[cols].eq(c).any(axis=1).sum() for c in cats if isinstance(c, str)}
        for cat, n in sorted(conteos.items(), key=lambda kv: -kv[1]):
            print(f"     {cat}: {n} ({pct(n, base)} de filas codificadas)")


def top_micro_detractores(df, sufijo, titulo):
    micro = f"Microcategoría 1{sufijo}"
    s = df[df["segmento"] == "detractor"]
    print(f"\n### Top microcategoría 1 entre detractores ({micro}) - {titulo}")
    codificadas = s[micro].notna().sum()
    for cat, n in s[micro].value_counts().head(10).items():
        print(f"  {cat}: {n} ({pct(n, codificadas)} de codificadas; {pct(n, len(s))} de detractores)")


def puntajes(df, columnas, titulo):
    print(f"\n### Etapas: promedio y distribución (escala 1-5) - {titulo}")
    for col in columnas:
        if col not in df.columns:
            print(f"  {col}: columna no existe")
            continue
        sc = pd.to_numeric(df[col], errors="coerce")
        validos = sc.notna()
        n = validos.sum()
        media = sc[validos].mean()
        bajos = (sc.between(1, 2)).sum()
        medios = (sc == 3).sum()
        altos = (sc >= 4).sum()
        cinco = (sc == 5).sum()
        bandera = "POLARIZACIÓN: media alta con cola baja" if (media >= 4.0 and bajos / n >= 0.10) else ""
        print(f"  {col}: n={n} media={media:.2f} 1-2={pct(bajos, n)} 3={pct(medios, n)} "
              f"4-5={pct(altos, n)} (5={pct(cinco, n)}) {bandera}")
        for seg in SEGMENTOS:
            ss = sc[(df["segmento"] == seg) & validos]
            if len(ss):
                print(f"      [{seg}] n={len(ss)} media={ss.mean():.2f} 1-2={pct((ss <= 2).sum(), len(ss))}")


def conteo_verbatim(df, verbatim, macro_fmt, titulo):
    print(f"\n### Trazabilidad de verbatim y codificación - {titulo}")
    for sufijo, col in verbatim.items():
        if col not in df.columns:
            print(f"  bloque '{sufijo}': columna no existe")
            continue
        texto = con_texto(df[col])
        macro = df[macro_fmt.format(sufijo)].notna() if macro_fmt.format(sufijo) in df.columns else pd.Series(False, index=df.index)
        print(f"  bloque '{sufijo}' [{col}]: con_texto={texto.sum()} codificado_macro1={macro.sum()} "
              f"con_texto_sin_codificar={(texto & ~macro).sum()} codificado_sin_texto={(macro & ~texto).sum()}")


def main():
    print(f"Fecha de extracción: {FECHA}. Fuente: inputs_clean/ (parquet).")
    for etiqueta, cfg in ARCHIVOS.items():
        base = cargar(cfg["prefijo"])
        for nombre_univ in ["GRUPO_COMPLETO", "PORTILLO_HIPOTESIS"]:
            df = universo(base, nombre_univ)
            titulo = f"{etiqueta} / {nombre_univ}"
            print(f"\n==================== {titulo} ====================")
            imprimir_segmentos(df, titulo)
            ranking_macro(df, "", cfg["verbatim"][""], titulo)
            menciones_cualquiera(df, "", titulo)
            top_micro_detractores(df, "", titulo)
            conteo_verbatim(df, cfg["verbatim"], "Macrocategoría 1{}", titulo)
            puntajes(df, cfg["puntajes"], titulo)
            for sufijo in [".1", ".2"]:
                ranking_macro(df, sufijo, cfg["verbatim"][sufijo], f"{titulo} bloque '{sufijo}'")


if __name__ == "__main__":
    main()
