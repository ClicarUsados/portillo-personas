"""4D - Intención y funcionalidades web + demografía de seguridad vial.

Subagente D del estudio de mercado Portillo (Grupo Americar).
Fuentes (solo inputs_clean/*.parquet, extracción 2026-11-23):
  - CR_Encuesta-funcionalidades-Web_*  (n=324, 2025-07-18..2025-08-23)
  - CR_Encuesta-de-seguridad-vial-en-Chile_* (n=709, 2025-10-22..2025-10-29, solo clientes de autos nuevos)
Imprime solo conteos y porcentajes agregados; nunca filas crudas ni PII.

Universos: GRUPO_COMPLETO (todas las filas) y PORTILLO_HIPOTESIS (PORT/PORTILLO en
nombre_concesionario; ver research/00_mapeo_portillo.md). Asignación bloqueada: Beto / Iván Balaguera.

Cómo reproducirlo: python3 analisis/4D_intencion_funcionalidades.py
"""
import glob
import os
import re
import sys

import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA_EXTRACCION = "2026-11-23"
MIN_N = 30  # n mínimo para reportar cortes; por debajo solo se muestra conteo, sin conclusión
ZW = "​"
PORT_RE = re.compile(r"\bPORT(ILLO)?\b", re.IGNORECASE)


def cargar(patron):
    rutas = glob.glob(os.path.join(ROOT, "inputs_clean", patron))
    if len(rutas) != 1:
        sys.exit(f"ERROR: se esperaba 1 archivo para {patron}, hay {len(rutas)}")
    return pq.read_table(rutas[0]).to_pydict()


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "n/a"


def vacio(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


def conteo(valores):
    out = {}
    for v in valores:
        k = "<vacío>" if vacio(v) else v
        out[k] = out.get(k, 0) + 1
    return out


def imprimir_conteo(titulo, valores, total):
    print(f"  {titulo}:")
    for k, n in sorted(conteo(valores).items(), key=lambda x: -x[1]):
        print(f"    {k}: n={n} ({pct(n, total)})")


def grupo_frecuencia(txt):
    if vacio(txt):
        return "<vacío>"
    return txt


def main():
    web = cargar("CR_Encuesta-funcionalidades-Web_*.parquet")
    n_web = len(web["row_id"])
    print(f"[DATO] inputs_clean/CR_Encuesta-funcionalidades-Web_* | filas={n_web} | "
          f"fecha respuesta {min(web['fecha respuesta'])[:10]}..{max(web['fecha respuesta'])[:10]} | extracción {FECHA_EXTRACCION}")

    # 1) Top-3 (selección múltiple): valor no vacío = opción marcada
    print("\n## 1. Top-3 funcionalidades (cada persona elige 3)")
    cols_top3 = [c for c in web if c.startswith("Por favor, selecciona")]
    print(f"  columnas de opciones: {len(cols_top3)} | total selecciones esperado = 3 x {n_web} = {3 * n_web}")
    filas = []
    for c in cols_top3:
        marcados = sum(1 for v in web[c] if not vacio(v))
        etiqueta = c.split("-", 1)[-1].replace(ZW, "").strip().rstrip(".")
        filas.append((marcados, etiqueta))
    print(f"  suma de selecciones observada = {sum(m for m, _ in filas)}")
    for m, e in sorted(filas, reverse=True):
        print(f"  [DATO] [WEB-col top3] n={m} ({pct(m, n_web)}) | {e}")
    resp_top3 = sum(1 for i in range(n_web) if any(not vacio(web[c][i]) for c in cols_top3))
    print(f"  respondientes con top-3 completo: {resp_top3} ({pct(resp_top3, n_web)})")

    # 2) Niveles de acuerdo: escala observada 1-5 (dirección asumida: 5 = muy de acuerdo) -> NO VERIFICADO
    print("\n## 2. Niveles de acuerdo (escala 1-5 observada; etiquetas de extremos NO VERIFICADAS, sin diccionario de escala)")
    excluir = set(cols_top3) | {"nps", "reinicio", "vendedor", "id_servicio", "empresa.1", "encuesta.1",
                                "Por favor, selecciona entre las siguientes funcionalidades o contenidos, las tres más importantes o relevantes para ti y que te gustaría ver en el sitio web de #empresa#:"}
    likert = [c for c in web if c not in excluir and c not in {"nps", "reinicio", "vendedor", "id_servicio"}
              and isinstance(next((v for v in web[c] if v is not None), None), int)]
    print(f"  columnas de acuerdo detectadas: {len(likert)}")
    for c in likert:
        vals = [v for v in web[c] if v is not None]
        n = len(vals)
        cnt = conteo(vals)
        acuerdo = sum(cnt.get(k, 0) for k in (4, 5))
        desacuerdo = sum(cnt.get(k, 0) for k in (1, 2))
        neutro = cnt.get(3, 0)
        etiqueta = c.replace(ZW, "").strip()
        print(f"  [DATO] [WEB-col {etiqueta[:85]}] n={n} | de acuerdo(4-5)={acuerdo} ({pct(acuerdo, n)}) | "
              f"neutro(3)={neutro} ({pct(neutro, n)}) | en desacuerdo(1-2)={desacuerdo} ({pct(desacuerdo, n)})")

    # 3) NPS y cobertura
    print("\n## 3. NPS y cobertura de respuesta")
    nps = [v for v in web["nps"] if v is not None]
    print(f"  [DATO] nps: n_valido={len(nps)} de {n_web} ({pct(len(nps), n_web)}); valores={conteo(nps)}")
    imprimir_conteo("[DATO] encuesta (texto)", web["encuesta"], n_web)
    imprimir_conteo("[DATO] campaña o sensor", web["campaña o sensor"], n_web)
    imprimir_conteo("[DATO] canal", web["canal"], n_web)
    print("  Vacíos por columna (solo las con vacíos):")
    for i, c in enumerate(web):
        n_v = sum(1 for v in web[c] if vacio(v))
        if n_v:
            print(f"    col#{i} {c.replace(ZW, '')[:50]!r}: {n_v} ({pct(n_v, n_web)})")

    # 4) Cruce con des_marca (GRUPO_COMPLETO) y PORTILLO_HIPOTESIS
    print("\n## 4. Cruce top-3 con des_marca [DATO] (GRUPO_COMPLETO)")
    ev_col = next(c for c in cols_top3 if "vehículos eléctricos" in c)
    por_marca = {}
    for i, m in enumerate(web["des_marca"]):
        por_marca.setdefault("<vacío>" if vacio(m) else m, []).append(i)
    for m, idx in sorted(por_marca.items(), key=lambda x: -len(x[1])):
        n = len(idx)
        if n < MIN_N:
            print(f"  {m}: n={n} | bajo umbral n<{MIN_N}, sin conclusión")
            continue
        ev = sum(1 for i in idx if not vacio(web[ev_col][i]))
        print(f"  {m}: n={n} | pide sección EV en top-3: {ev} ({pct(ev, n)})")

    print("\n## 5. Universo PORTILLO_HIPOTESIS [HIPÓTESIS, bloqueado: Beto / Iván Balaguera]")
    idx_p = [i for i, n in enumerate(web["nombre_concesionario"]) if n and PORT_RE.search(n)]
    print(f"  [HIPÓTESIS] n={len(idx_p)} ({pct(len(idx_p), n_web)}) de {n_web}; n<{MIN_N}: solo descriptivo, sin conclusión")
    for c in cols_top3:
        m = sum(1 for i in idx_p if not vacio(web[c][i]))
        if m:
            etiqueta = c.split("-", 1)[-1].replace(ZW, "").strip().rstrip(".")
            print(f"    {etiqueta[:70]}: {m}")

    print("\n## 5b. Campaña o sensor (etiqueta de origen) vs PORTILLO_HIPOTESIS [DATO vs HIPÓTESIS]")
    camp_port = sum(1 for c in web["campaña o sensor"] if c and "portillo" in c.lower())
    print(f"  [DATO] campaña o sensor contiene 'Portillo': n={camp_port} ({pct(camp_port, n_web)})")
    print(f"  [HIPÓTESIS] nombre_concesionario PORT/PORTILLO: n={len(idx_p)} ({pct(len(idx_p), n_web)})")
    print(f"  NO CALZAN: {camp_port} vs {len(idx_p)}. No se corrige; ambas cifras se reportan.")

    # 6) Seguridad vial
    sv = cargar("CR_Encuesta-de-seguridad-vial-en-Chile_*.parquet")
    n_sv = len(sv["row_id"])
    print(f"\n## 6. Seguridad vial [DATO] inputs_clean/CR_Encuesta-de-seguridad-vial-en-Chile_* | filas={n_sv} | "
          f"fecha respuesta {min(sv['fecha respuesta'])[:10]}..{max(sv['fecha respuesta'])[:10]}")
    print("  SESGO: encuesta de un solo mes; solo clientes de autos NUEVOS; NO representa al comprador de seminuevos.")
    col_edad, col_gen = "Rango de edad", "Género"
    col_frec = "¿Con qué frecuencia conduces un vehículo, ya sea para trabajar o desplazarte?"
    col_estr = "En una escala del 1 al 5, ¿cuánto estrés sientes al conducir en la ciudad?"
    imprimir_conteo("Rango de edad", sv[col_edad], n_sv)
    imprimir_conteo("Género", sv[col_gen], n_sv)
    imprimir_conteo("Frecuencia de conducción", sv[col_frec], n_sv)

    # Estrés por frecuencia y por edad (escala 1-5; dirección 5 = más estrés asumida, NO VERIFICADA)
    print("  Estrés (escala 1-5) por cortes [DATO]:")
    for titulo, col in (("frecuencia", col_frec), ("edad", col_edad)):
        grupos = {}
        for i in range(n_sv):
            g = "<vacío>" if vacio(sv[col][i]) else sv[col][i]
            e = sv[col_estr][i]
            if e is not None:
                grupos.setdefault(g, []).append(e)
        for g, es in sorted(grupos.items(), key=lambda x: -len(x[1])):
            media = sum(es) / len(es)
            aviso = "" if len(es) >= MIN_N else f" (n<{MIN_N}, sin conclusión)"
            print(f"    por {titulo} | {g}: n={len(es)} media={media:.2f}{aviso}")

    # Frecuencia por edad (tabla n)
    print("  Frecuencia x edad (n) [DATO]:")
    tabla = {}
    for i in range(n_sv):
        tabla.setdefault("<vacío>" if vacio(sv[col_edad][i]) else sv[col_edad][i], {}).setdefault(
            "<vacío>" if vacio(sv[col_frec][i]) else sv[col_frec][i], 0)
        tabla[sv[col_edad][i] if not vacio(sv[col_edad][i]) else "<vacío>"][
            sv[col_frec][i] if not vacio(sv[col_frec][i]) else "<vacío>"] += 1
    for edad, fila in sorted(tabla.items()):
        print(f"    {edad}: " + ", ".join(f"{k}={v}" for k, v in sorted(fila.items())))

    # Portillo hipotético en seguridad vial (solo descriptivo)
    idx_sv = [i for i, n in enumerate(sv["nombre_concesionario"]) if n and PORT_RE.search(n)]
    print(f"  [HIPÓTESIS] PORTILLO_HIPOTESIS en seguridad vial: n={len(idx_sv)} ({pct(len(idx_sv), n_sv)})")


if __name__ == "__main__":
    main()
