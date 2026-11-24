"""ZMOT: barreras, calidad del contacto y evaluacion de la cotizacion (leads Portillo).

Fuente unica: inputs_clean/CR_Lead-Portillo_2023-03-01_2026-11-23_216d73e0__sin_segmento.parquet
Universos: GRUPO_COMPLETO (1.003 filas) y PORTILLO_HIPOTESIS (PORT/PORTILLO en nombre_sucursal) [HIPOTESIS, bloqueada: Beto / Ivan Balaguera].
Imprime solo conteos y porcentajes. No imprime textos libres ni filas.
Los leads NO son compradores: no se calcula ninguna tasa lead->venta.

Cómo reproducirlo: python3 analisis/zmot_leads.py
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = RAIZ / "inputs_clean" / "CR_Lead-Portillo_2023-03-01_2026-11-23_216d73e0__sin_segmento.parquet"
FECHA = "2026-11-23"

COL_PROCESO = "¿Cómo evaluaría el proceso de cotización?"
COL_CONTACTO = "¿Ha sido contactado por nuestro equipo de ventas luego de su solicitud de cotización?"
COL_CALIDAD = "¿Cómo evaluaría la calidad del contacto?"
COL_NECESIDAD = "¿Qué necesita para seguir con su proceso de cotización?"
COL_OTROS = "Texto opción otros"
COL_POR_QUE = "¿Por qué?"


def normalizar(texto: str) -> str:
    """Minusculas y sin tildes, para reglas de palabras clave."""
    if not isinstance(texto, str):
        return ""
    sin_tilde = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sin_tilde.lower()


# Reglas de palabras clave. Multietiqueta. [HIPOTESIS]: no validadas con muestra etiquetada.
REGLAS_POR_QUE = {
    "Sin respuesta o sin contacto": r"nadie|nunca (me|han|nos)|no (me|nos) (han |ha )?(contact|respond|llam|escrib)|sin respuesta|no ha pasado nada|automatic",
    "Lentitud o tiempos": r"demor|lent|tard|espera|dias|semanas|urgen|pronto|rapido",
    "Precio o transparencia": r"precio|costo|valor|transpar|cobro|tarifa|sobreprecio",
    "Financiamiento, credito o parte de pago": r"financ|credito|cuota|banco|parte de pago|pie\b|tasa",
    "Trato o atencion del ejecutivo": r"\btrato\b|mala atencion|no atendi|grosero|maltrato",
    "Informacion o documentacion": r"informac|document|detalle|opciones|respuesta sobre|dudas",
    "Stock o disponibilidad": r"stock|disponib|no tienen|no hay|agotad",
    "Reserva o devolucion de dinero": r"reserva|devol|devuel|dinero|plata",
}
REGLA_OTROS_COMPRA = r"compr|ya (lo|la) (tom|adquir)|ya tengo|ya me"


def fmt(n: int, base: int) -> str:
    pct = 100 * n / base if base else 0.0
    return f"{n} ({pct:.1f}%)"


def main() -> None:
    df = pd.read_parquet(ARCHIVO)
    total = len(df)
    es_portillo = df["nombre_sucursal"].fillna("").str.upper().str.contains(r"PORTILLO|\bPORT\b", regex=True)
    print(f"[ZMOT leads] fecha de extraccion {FECHA} | archivo filas={total}")
    print(f"GRUPO_COMPLETO n={total} | PORTILLO_HIPOTESIS n={int(es_portillo.sum())} (declarado en 00_mapeo_portillo: 140)")

    print("\n== A. Evaluacion del proceso (base GRUPO_COMPLETO) ==")
    for valor, n in df[COL_PROCESO].value_counts().sort_index().items():
        print(f"  {valor}: {fmt(int(n), total)}")
    top2 = int((df[COL_PROCESO] >= 4).sum())
    bot2 = int((df[COL_PROCESO] <= 2).sum())
    print(f"  top-2 (4-5): {fmt(top2, total)} | bottom-2 (1-2): {fmt(bot2, total)} | direccion de escala NO VERIFICADA")
    bajo = df[COL_PROCESO] <= 2
    print(f"  cruce proceso 1-2 (n={int(bajo.sum())}) x contacto: No={int((bajo & (df[COL_CONTACTO] == 'No')).sum())} "
          f"| Si={int((bajo & (df[COL_CONTACTO] == 'Sí')).sum())} "
          f"| sin respuesta={int((bajo & df[COL_CONTACTO].isna()).sum())}")

    print("\n== B. Contacto por ventas (base GRUPO_COMPLETO) ==")
    contacto = df[COL_CONTACTO].fillna("(sin respuesta)")
    for valor, n in contacto.value_counts().items():
        print(f"  {valor[:40]}: {fmt(int(n), total)}")
    respondidos = int(df[COL_CONTACTO].notna().sum())
    print(f"  respondidos: {respondidos} ({100*respondidos/total:.1f}%)")

    print("\n== C. Calidad del contacto (base: contacto = Si) ==")
    si = df[COL_CONTACTO] == "Sí"
    base_si = int(si.sum())
    print(f"  base Si = {base_si}; calidad respondida = {int(df.loc[si, COL_CALIDAD].notna().sum())}")
    for valor, n in df.loc[si, COL_CALIDAD].value_counts().sort_index().items():
        print(f"  {int(valor)}: {fmt(int(n), base_si)}")

    print("\n== D. Que necesita para seguir (base: respondidos) ==")
    necesidad = df[COL_NECESIDAD].dropna()
    base_nec = len(necesidad)
    for valor, n in necesidad.value_counts().items():
        print(f"  {valor[:60]}: {fmt(int(n), base_nec)} | sobre 1.003: {100*n/total:.1f}%")

    print("\n== E. Texto 'otros' (codificacion por palabras clave, [HIPOTESIS]) ==")
    otros = df[COL_OTROS].dropna()
    base_otros = len(otros)
    compra = int(otros.map(normalizar).str.contains(REGLA_OTROS_COMPRA, regex=True).sum())
    print(f"  base = {base_otros}; declaran compra ya realizada (autodeclaracion, NO verificada contra ventas) = {compra}")
    print(f"  resto sin marca de compra = {base_otros - compra}")

    print("\n== F. Motivo '¿Por que?' (multietiqueta, palabras clave, [HIPOTESIS]) ==")
    texto = df[COL_POR_QUE].map(normalizar)
    con_texto = df[COL_POR_QUE].notna() & (df[COL_POR_QUE].astype(str).str.strip() != "")
    base_txt = int(con_texto.sum())
    print(f"  base con texto = {base_txt} ({100*base_txt/total:.1f}%)")
    proceso_bajo = df[COL_PROCESO] <= 2
    print(f"  base con texto y proceso 1-2 = {int((con_texto & proceso_bajo).sum())}")
    for tema, patron in REGLAS_POR_QUE.items():
        marca = texto.str.contains(patron, regex=True)
        n_total = int((marca & con_texto).sum())
        n_bajo = int((marca & con_texto & proceso_bajo).sum())
        print(f"  {tema}: {fmt(n_total, base_txt)} | con proceso 1-2: {n_bajo}")

    print("\n== G. Origen (canal de entrada, descriptivo, no atribucion de venta) ==")
    for valor, n in df["origen"].fillna("(vacio)").value_counts().items():
        print(f"  {valor}: {fmt(int(n), total)}")

    print("\n== H. Contradicciones (ambas cifras, sin corregir) ==")
    no_contacto = df[COL_CONTACTO] == "No"
    en_contacto = df[COL_NECESIDAD] == "Ya estoy en contacto con mi ejecutivo"
    print(f"  Contacto = No: {int(no_contacto.sum())} | 'Ya estoy en contacto con mi ejecutivo': {int(en_contacto.sum())}")
    print(f"  Cruce Contacto = No y 'Ya estoy en contacto': {int((no_contacto & en_contacto).sum())}")
    print(f"  Usado: des_marca USADOS = {int((df['des_marca'] == 'USADOS').sum())} | tipo_oportunidad usado tras normalizar = "
          f"{int(df['tipo_oportunidad'].fillna('').str.upper().str.contains('USADO').sum())}")

    print("\n== I. Universo PORTILLO_HIPOTESIS (base respondidos) ==")
    for etiqueta, mascara in [("PORTILLO_HIPOTESIS", es_portillo), ("Resto", ~es_portillo)]:
        sub = df[mascara]
        resp = int(sub[COL_CONTACTO].notna().sum())
        si_n = int((sub[COL_CONTACTO] == "Sí").sum())
        print(f"  {etiqueta}: n={len(sub)} | contacto respondido={resp} | contacto Si={si_n}")

    print("\n== J. Verificacion de citas (sin imprimir texto) ==")
    citas = {
        "CR_Lead-Portillo_202#5": "Solicite cotización y nadie me ha contactado hasta el momento",
        "CR_Lead-Portillo_202#4": "Se suponía que me contactarían y no ha pasado nada",
        "CR_Lead-Portillo_202#555": "Nunca me enviaron nada, solo me llego un mensaje automático por WhatsApp",
        "CR_Lead-Portillo_202#61": "No me respondieron nada sobre valores, opciones de pago y financiamiento.",
        "CR_Lead-Portillo_202#662": "Ser más trasparente con el costo establecido en la cotización",
    }
    for rid, cita in citas.items():
        fila = df.loc[df["row_id"] == rid, COL_POR_QUE]
        ok = bool(len(fila)) and cita in str(fila.iloc[0])
        print(f"  {rid}: subcadena_verbatim={ok} | palabras={len(cita.split())}")


if __name__ == "__main__":
    main()
