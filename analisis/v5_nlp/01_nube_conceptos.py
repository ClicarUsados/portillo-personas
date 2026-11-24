#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fase 1 del PROMPT_v5: nube de conceptos por persona (Antonia y Tomás Pascual).

Reproducir (desde la raíz del proyecto):
    ./.venv_v5/bin/python analisis/v5_nlp/01_nube_conceptos.py

Entrada: SOLO inputs_clean/ (nunca inputs_raw/).
Salidas:
    research/v5_nube/conceptos_antonia.csv
    research/v5_nube/conceptos_tomas.csv
    research/v5_nube/NUBE_CONCEPTOS.html
    research/v5_nube/resumen_ejecucion.json
    analisis/v5_nlp/corpus/*.csv  (textos anonimizados por corpus, uso local)

Privacidad: todo corre en local (spaCy es_core_news_sm + MiniLM de sentence-transformers).
Antes de vectorizar se enmascaran nombres propios (NER tipo PER), correos, teléfonos y RUT.
"""
import glob
import html
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import hdbscan
import numpy as np
import pandas as pd
import spacy
import umap
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import adjusted_rand_score, silhouette_score

ROOT = Path(__file__).resolve().parents[2]
IN_DIR = ROOT / "inputs_clean"
OUT_DIR = ROOT / "research" / "v5_nube"
CORPUS_DIR = ROOT / "analisis" / "v5_nlp" / "corpus"
PLAN_BUSQUEDA = ROOT / "research" / "15_busqueda_premium.md"

SEED = 42
B_BOOT = 100            # remuestreos bootstrap para estabilidad
UMBRAL_ESTABLE = 0.6    # Jaccard medio < 0,6 = inestable
MODELO_EMB = "paraphrase-multilingual-MiniLM-L12-v2"

CAMPANA_VU = "2025 - Venta Usados Portillo"
ZONA_ORIENTE = r"LA DEHESA|BILBAO|LAS CONDES|LUIS CARRERA|PADRE HURTADO|VITACURA|DELANO"  # igual que v3
COL_NPS = ("En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes "
           "#empresa# a un familiar o amigo?")
COL_CANAL = "¿Cómo llegaste a #empresa# para comprar tu auto?"
COL_PAGO = "Vehículo en parte de pago"
COL_LIBRES_VU = [  # textos libres de Venta-Usados (se concatenan por fila)
    "¿Qué te motiva a dar esa puntuación?",
    "¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor?",
    "Texto opción otros",
]
COL_LEAD = "¿Qué necesita para seguir con su proceso de cotización?"

# Regla de asignación a persona [HIPÓTESIS] (PROMPT_v5, Fase 0)
CANAL_ANTONIA = {"Porque ya soy (o he sido) cliente", "Por recomendaciones de conocidos"}
CANAL_TOMAS = {"Porque el auto que quería estaba acá", "Porque vi publicidad en medios", "Redes Sociales"}

# Stopwords: español general (spaCy) + chilenismos de relleno + placeholders del CRM
STOP_EXTRA = {"igual", "po", "cachai", "osea", "altiro", "bueno", "nomas", "harto",
              "empresa", "americar", "persona", "dato_privado", "ser", "estar", "tener"}
PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d[\d\s-]{7,}\d|\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")


def sin_tildes(s):
    """Quita tildes para contar (ñ se conserva como n por la descomposición NFKD)."""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def unico_parquet(prefijo):
    """Devuelve la ruta única de inputs_clean/<prefijo>*.parquet; falla si hay 0 o >1."""
    rutas = sorted(glob.glob(str(IN_DIR / f"{prefijo}*.parquet")))
    assert len(rutas) == 1, f"{prefijo}: {rutas}"
    assert "inputs_raw" not in rutas[0]
    return rutas[0]


def textos_libres(df, columnas):
    """Une los textos libres de una fila (omite vacíos). Una fila = un texto."""
    def une(fila):
        partes = [str(x).strip() for x in fila if pd.notna(x) and str(x).strip()]
        return ". ".join(partes)
    return df[columnas].apply(une, axis=1)


def asignar_persona(canal, pago):
    """Regla [HIPÓTESIS]: Tomás = canal de 'auto acá / publicidad / redes' y SIN parte de pago.
    Antonia = canal de 'cliente / recomendación' O con parte de pago. Resto = común."""
    pago_usado = pd.notna(pago) and str(pago).strip() not in ("", "No aplica")
    if canal in CANAL_TOMAS and not pago_usado:
        return "Tomás"
    if canal in CANAL_ANTONIA or pago_usado:
        return "Antonia"
    return "común"


def cargar_corpus():
    """Construye los cinco corpus. Lee SOLO inputs_clean/ y el plan de búsqueda (research/)."""
    vu = pd.read_parquet(unico_parquet("CR_2025-Venta-Usados_"))
    vu["nps"] = pd.to_numeric(vu[COL_NPS], errors="coerce")
    vu["texto"] = textos_libres(vu, COL_LIBRES_VU)
    port = vu[vu["campaña o sensor"] == CAMPANA_VU].copy()
    port["oriente"] = port["nombre_concesionario"].fillna("").str.contains(ZONA_ORIENTE, regex=True)
    port["persona"] = [asignar_persona(c, p) for c, p in zip(port[COL_CANAL], port[COL_PAGO])]
    ori = port[port["oriente"] & (port["texto"] != "")]

    filas = []
    for _, r in ori.iterrows():  # corpus por persona (zona oriente, Portillo)
        filas.append(dict(id=f"VU-{r['row_id']}", corpus={"Antonia": "antonia", "Tomás": "tomas", "común": "comun"}[r["persona"]],
                          fuente="CR_2025-Venta-Usados (campaña Portillo, oriente)",
                          row_id=r["row_id"], nps=r["nps"], texto=r["texto"]))
    # Corpus de dolores: detractores (NPS<=6) de Venta-Usados DEL GRUPO (todas las campañas)
    det = vu[(vu["nps"] <= 6) & (vu["texto"] != "")]
    for _, r in det.iterrows():
        filas.append(dict(id=f"VU-{r['row_id']}", corpus="dolor",
                          fuente="CR_2025-Venta-Usados (grupo, NPS<=6)", row_id=r["row_id"],
                          nps=r["nps"], texto=r["texto"]))
    # Corpus de dolores: respuesta abierta de CR_Lead-Portillo
    lp = pd.read_parquet(unico_parquet("CR_Lead-Portillo_"))
    lp = lp[lp[COL_LEAD].notna() & (lp[COL_LEAD].astype(str).str.strip() != "")]
    for _, r in lp.iterrows():
        filas.append(dict(id=f"LP-{r['row_id']}", corpus="dolor", fuente="CR_Lead-Portillo",
                          row_id=r["row_id"], nps=np.nan, texto=str(r[COL_LEAD]).strip()))
    # Corpus de búsqueda: consultas candidatas de research/15 §2-§3 (tag [WEB])
    md = PLAN_BUSQUEDA.read_text(encoding="utf-8")
    seccion = md[md.index("## 2.") : md.index("## 4.")]
    consultas = sorted(set(q.strip() for q in re.findall(r'"([^"\n]{3,80})"', seccion)))
    for i, q in enumerate(consultas, 1):
        filas.append(dict(id=f"BQ-{i:03d}", corpus="busqueda", fuente="research/15_busqueda_premium.md §2-3 [WEB]",
                          row_id=f"BQ-{i:03d}", nps=np.nan, texto=q))

    df = pd.DataFrame(filas)
    stats = dict(
        vu_campana_filas=int((vu["campaña o sensor"] == CAMPANA_VU).sum()),
        vu_campana_oriente_filas=int(port["oriente"].sum()),
        vu_campana_oriente_sin_texto=int((port["oriente"] & (port["texto"] == "")).sum()),
        grupo_vu_detractores_con_texto=int(len(det)),
        grupo_vu_detractores_portillo_oriente=int(det["row_id"].isin(ori["row_id"]).sum()),
        lead_con_respuesta=int(len(lp)),
        busqueda_consultas=len(consultas),
    )
    return df, stats


def procesar_textos(textos, nlp):
    """Enmascara PII y lematiza. Devuelve (texto_enmascarado, lemas_sin_tildes_y_con_tildes)."""
    enmascarados, lemas = [], []
    for doc in nlp.pipe(textos, batch_size=64):
        # 1) NER: nombres de personas -> PERSONA (la lista de vendedores no se conoce; esto es la red)
        spans = [(e.start_char, e.end_char) for e in doc.ents if e.label_ == "PER"]
        masked = doc.text
        for s, e in sorted(spans, reverse=True):
            masked = masked[:s] + "PERSONA" + masked[e:]
        # 2) Regex: correos, teléfonos, RUT
        masked = PII.sub("DATO_PRIVADO", masked)
        # 3) Lemas de tokens alfabéticos, sin stopwords, fuera de entidades de persona
        toks = []
        for tok in doc:
            if any(s <= tok.idx < e for s, e in spans) or not tok.is_alpha:
                continue
            lema = tok.lemma_.lower()
            if tok.is_stop or len(lema) < 3 or sin_tildes(lema) in STOP_EXTRA or lema in STOP_EXTRA:
                continue
            toks.append(lema)
        enmascarados.append(masked)
        lemas.append(" ".join(toks))
    return enmascarados, lemas


def embeber(textos, modelo):
    """Embeddings MiniLM multilingüe, local. Normalizados (coseno = producto punto)."""
    return modelo.encode(textos, normalize_embeddings=True, show_progress_bar=False, batch_size=32)


def reducir(E):
    """UMAP (coseno) con n>=15; PCA si hay pocos textos (UMAP no es estable con muestras chicas)."""
    n = len(E)
    if n >= 15:
        return umap.UMAP(n_components=5, n_neighbors=min(15, n - 1), min_dist=0.0,
                         metric="cosine", random_state=SEED).fit_transform(E)
    return PCA(n_components=min(5, n - 1), random_state=SEED).fit_transform(E)


def estabilidad(Z, etiquetas, ajustar, B=B_BOOT):
    """Bootstrap con reemplazo: en cada remuestreo se reagrupa y, para cada cluster original,
    se toma el mejor Jaccard con un cluster del remuestreo. Estabilidad = media de esos Jaccard."""
    rng = np.random.default_rng(SEED)
    n = len(Z)
    clusters = [c for c in set(etiquetas) if c != -1]
    acum = {c: [] for c in clusters}
    for _ in range(B):
        idx = np.unique(rng.integers(0, n, n))
        try:
            lb = ajustar(Z[idx])
        except ValueError:
            lb = np.full(len(idx), -1)
        grupos_b = [set(idx[lb == d].tolist()) for d in set(lb) if d != -1]
        for c in clusters:
            miembros = set(idx[etiquetas[idx] == c].tolist())
            if not miembros:
                continue
            mejor = 0.0
            for g in grupos_b:
                mejor = max(mejor, len(miembros & g) / len(miembros | g))
            acum[c].append(mejor)
    return {c: (float(np.mean(v)) if v else float("nan")) for c, v in acum.items()}


def agrupar(Z):
    """HDBSCAN como método principal; KMeans (k por silhouette) como comparación.
    Si HDBSCAN no produce >=2 clusters, se usa KMeans y se dice en 'metodo'."""
    n = len(Z)
    if n < 8:
        return dict(labels=np.full(n, -1), metodo="no clusterizado (n<8)", stab={}, stab_km={},
                    ari=float("nan"), k=None, sil={})
    mcs = max(3, n // 10)
    ajuste_hdb = lambda X: hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=2).fit_predict(X)
    hdb = ajuste_hdb(Z)
    sil = {}
    for k in range(2, min(6, n // 4) + 1):
        lab = KMeans(k, n_init=10, random_state=SEED).fit_predict(Z)
        sil[k] = float(silhouette_score(Z, lab))
    k = max(sil, key=sil.get) if sil else 2
    ajuste_km = lambda X: KMeans(min(k, len(X)), n_init=10, random_state=SEED).fit_predict(X)
    km = ajuste_km(Z)
    if len(set(hdb) - {-1}) >= 2:
        labels, metodo, ajuste = hdb, "HDBSCAN", ajuste_hdb
    else:
        labels, metodo, ajuste = km, "KMeans (fallback: HDBSCAN con <2 clusters)", ajuste_km
    return dict(labels=labels, metodo=metodo, stab=estabilidad(Z, labels, ajuste),
                stab_km=estabilidad(Z, km, ajuste_km), ari=float(adjusted_rand_score(hdb, km)),
                k=k, sil=sil)


def ctfidf(Cm, grupos, nombres):
    """c-TF-IDF (BERTopic): W[g,t] = tf[g,t] * log(1 + A / f[t]); A = palabras medias por grupo."""
    TF = np.vstack([np.asarray(Cm[grupos == g].sum(axis=0)).ravel() for g in nombres])
    A = TF.sum() / len(nombres)
    f = TF.sum(axis=0)
    W = TF * np.log(1 + A / np.maximum(f, 1))
    return W


def verbatim(texto, max_pal=15):
    """Frase de <=15 palabras; si no hay, las primeras 15 palabras con '…'."""
    for fr in re.split(r"(?<=[.!?])\s+", texto):
        if 3 <= len(fr.split()) <= max_pal:
            return fr
    return " ".join(texto.split()[:max_pal]) + " …"


def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df, stats = cargar_corpus()
    nlp = spacy.load("es_core_news_sm")
    masked, lemas = procesar_textos(df["texto"].tolist(), nlp)
    df["texto_anon"] = masked
    df["lemas"] = lemas
    df = df[df["lemas"].str.strip() != ""].reset_index(drop=True)
    print("corpus:", df["corpus"].value_counts().to_dict())

    # Forma de visualización: palabra con tilde más frecuente para cada forma sin tildes
    forma = defaultdict(Counter)
    for l in df["lemas"]:
        for t in l.split():
            forma[sin_tildes(t)][t] += 1
    mostrar = {k: c.most_common(1)[0][0] for k, c in forma.items()}

    # Matriz de conteos 1-3 gramas (sobre lemas sin tildes), min_df=2 en el conjunto total
    vec = CountVectorizer(ngram_range=(1, 3), min_df=2, token_pattern=r"(?u)\b[^\W\d_]{3,}\b")
    Cm = vec.fit_transform([sin_tildes(x) for x in df["lemas"]]).tocsr()
    vocab = vec.get_feature_names_out()
    Bin = (Cm > 0).astype(int).tocsr()
    grupos_corpus = df["corpus"].to_numpy()
    nps = df["nps"].to_numpy()

    # Embeddings por texto (texto anonimizado, con tildes)
    modelo = SentenceTransformer(MODELO_EMB)
    E_all = embeber(df["texto_anon"].tolist(), modelo)

    # Clusters por corpus de interés: personas (oriente) y dolores
    resumen = dict(stats=stats, corpus_n={}, clusters={}, modelo_embeddings=MODELO_EMB)
    clust = {}  # corpus -> dict(idx, labels, E, Z, info)
    for corp in ["antonia", "tomas", "dolor"]:
        idx = np.where(grupos_corpus == corp)[0]
        resumen["corpus_n"][corp] = int(len(idx))
        info = agrupar(reducir(E_all[idx]))
        clust[corp] = dict(idx=idx, E=E_all[idx], info=info)
        print(corp, len(idx), info["metodo"], info["k"], info["ari"])

    # Nombre de cada cluster: 5 términos con mayor c-TF-IDF dentro del corpus
    def nombres_clusters(corp):
        d = clust[corp]
        lab = d["info"]["labels"]
        etiq = np.array([f"c{l}" if l != -1 else "ruido" for l in lab])
        Cc = Cm[d["idx"]]
        nombres = sorted(set(etiq))
        W = ctfidf(Cc, etiq, nombres)
        salida = {}
        for gi, g in enumerate(nombres):
            if g == "ruido":
                continue
            cand = [i for i in np.argsort(-W[gi]) if W[gi, i] > 0][:5]
            salida[g] = [mostrar.get(vocab[i], vocab[i]) for i in cand]
        return salida, etiq

    # Términos candidatos por pool
    def pool(grupo, n_top, min_df):
        mask = grupos_corpus == grupo
        grupos_all = grupos_corpus
        nombres = ["antonia", "tomas", "comun", "dolor", "busqueda"]
        W = ctfidf(Cm, grupos_all, nombres)
        gi = nombres.index(grupo)
        df_g = np.asarray(Bin[mask].sum(axis=0)).ravel()
        cand = [i for i in np.argsort(-W[gi]) if W[gi, i] > 0 and df_g[i] >= min_df][:n_top]
        return cand, W[gi], df_g

    filas_salida = {}
    concepto_info = {}
    for persona, slug in [("antonia", "antonia"), ("tomas", "tomas")]:
        cand, Wg, _ = pool(persona, 20, 2)
        filas = []
        mask_p = grupos_corpus == persona
        nps_p = nps[mask_p]
        cl = clust[persona]
        nombres_cl, etiq_p = nombres_clusters(persona)
        for i in cand:
            pres = np.asarray(Bin[mask_p][:, i].todense()).ravel() > 0
            n_prom = int(((nps_p >= 9) & pres).sum())
            n_det = int(((nps_p <= 6) & pres).sum())
            pol = "neutro" if n_prom + n_det == 0 else ("valor" if n_prom / (n_prom + n_det) >= 0.5 else "dolor")
            filas.append(dict(vocab_i=i, pool="persona", polaridad=pol, n=int(pres.sum()),
                              peso=float(Wg[i]), pres_idx=np.where(mask_p)[0][pres]))
        filas_salida[slug] = filas
        concepto_info[slug] = (cand, cl, etiq_p, nombres_cl)

    # Pool dolor (compartido) y pool búsqueda (intención)
    cand_d, Wd, _ = pool("dolor", 12, 3)
    cand_b, Wb, _ = pool("busqueda", 10, 1)
    mask_d = grupos_corpus == "dolor"
    mask_b = grupos_corpus == "busqueda"
    pool_d = [dict(vocab_i=i, pool="dolor", polaridad="dolor", n=int(np.asarray(Bin[mask_d][:, i].sum()).item()),
                   peso=float(Wd[i]), pres_idx=np.where(mask_d)[0][np.asarray(Bin[mask_d][:, i].todense()).ravel() > 0])
              for i in cand_d]
    pool_b = [dict(vocab_i=i, pool="busqueda", polaridad="intención", n=int(np.asarray(Bin[mask_b][:, i].sum()).item()),
                   peso=float(Wb[i]), pres_idx=np.where(mask_b)[0][np.asarray(Bin[mask_b][:, i].todense()).ravel() > 0])
              for i in cand_b]
    nombres_dolor, etiq_dolor = nombres_clusters("dolor")

    # Co-ocurrencia (PMI) entre conceptos seleccionados, sobre todos los textos
    seleccion = []
    for slug in ["antonia", "tomas"]:
        seleccion += [r["vocab_i"] for r in filas_salida[slug]]
    seleccion += [r["vocab_i"] for r in pool_d + pool_b]
    seleccion = list(dict.fromkeys(seleccion))
    Bs = Bin[:, seleccion].toarray()
    N = Bs.shape[0]
    Cab = Bs.T @ Bs
    pa = np.diag(Cab) / N
    arist = []
    for a in range(len(seleccion)):
        for b in range(a + 1, len(seleccion)):
            if Cab[a, b] < 2:
                continue
            pmi = np.log((Cab[a, b] / N) / (pa[a] * pa[b]))
            ta, tb = vocab[seleccion[a]], vocab[seleccion[b]]
            if pmi > 0 and ta not in tb and tb not in ta:
                arist.append(dict(a=ta, b=tb, pmi=round(float(pmi), 3), n=int(Cab[a, b])))
    print("aristas co-ocurrencia:", len(arist))

    # Construcción de tablas por persona
    def etiqueta_de(pool_name, n, cluster_stable):
        base = {"persona": "[DATO] VU oriente; [HIPÓTESIS] asignación por canal/parte de pago",
                "dolor": "[DATO] VU detractores grupo + CR_Lead-Portillo",
                "busqueda": "[WEB] research/15_busqueda_premium.md §2-3"}[pool_name]
        if n < 3:
            base += " · n<3 [HIPÓTESIS]"
        if cluster_stable is False:
            base += " · cluster inestable [HIPÓTESIS]"
        return base

    def fila_concepto(r, cluster_name, estab_val, nombre_c=None):
        return dict(concepto=" ".join(mostrar.get(t, t) for t in vocab[r["vocab_i"]].split()),
                    clave=vocab[r["vocab_i"]], peso=None, cluster=cluster_name,
                    polaridad=r["polaridad"], n_textos=r["n"],
                    estabilidad=("NA" if estab_val is None or np.isnan(estab_val) else round(estab_val, 2)),
                    ejemplo_row_id=None, etiqueta=None, _pres=r["pres_idx"], _peso=r["peso"], _pool=r["pool"])

    def cluster_dominante(pres_idx, idx_corp, etiq_corpus, stab, prefijo):
        """Cluster con mayor proporción de textos donde aparece el concepto."""
        pos = {g: j for j, g in enumerate(idx_corp)}
        ids = [pos[p] for p in pres_idx if p in pos]
        if not ids:
            return "ruido", None
        c = Counter(etiq_corpus[ids]).most_common()
        mejor = next(((g, n) for g, n in c if g != "ruido"), None)
        if mejor is None:
            return "ruido", None
        g = mejor[0]
        lab_num = int(g[1:])
        return f"{prefijo}{lab_num}", stab.get(lab_num)

    def ejemplo(pres_idx, cluster_key, corp):
        """Un row_id de ejemplo que contiene el concepto, preferentemente en su cluster y de ~12 palabras."""
        cand = [p for p in pres_idx]
        if not cand:
            return ""
        cand.sort(key=lambda p: abs(len(df.loc[p, "texto_anon"].split()) - 12))
        return df.loc[cand[0], "row_id"]

    tablas = {}
    for slug in ["antonia", "tomas"]:
        cl = clust[slug]
        nombres_cl, etiq_p = nombres_clusters(slug)
        stab_p = cl["info"]["stab"]
        pref = "A" if slug == "antonia" else "T"
        rows = []
        for r in filas_salida[slug]:
            cl_name, est = cluster_dominante(r["pres_idx"], cl["idx"], etiq_p, stab_p, pref)
            rr = fila_concepto(r, cl_name, est)
            rr["peso"] = round(r["peso"], 3)
            rr["ejemplo_row_id"] = ejemplo(r["pres_idx"], cl_name, slug)
            rows.append(rr)
        for r in pool_d:
            cl_name, est = cluster_dominante(r["pres_idx"], clust["dolor"]["idx"], etiq_dolor,
                                              clust["dolor"]["info"]["stab"], "D")
            rr = fila_concepto(r, cl_name, est)
            rr["peso"] = round(r["peso"], 3)
            rr["ejemplo_row_id"] = ejemplo(r["pres_idx"], cl_name, "dolor")
            rows.append(rr)
        for r in pool_b:
            rr = fila_concepto(r, "sin cluster (n<20 consultas)", None)
            rr["peso"] = round(r["peso"], 3)
            rr["ejemplo_row_id"] = ejemplo(r["pres_idx"], None, "busqueda")
            rows.append(rr)
        # Pesos normalizados 0-100 dentro de cada tabla; etiqueta; dedupe por concepto (prioridad persona>dolor>intención)
        # Normalización 0-100 POR POOL (persona, dolor, búsqueda): cada pool tiene su propia escala c-TF-IDF
        mx_pool = {p: max([x["peso"] for x in rows if x["_pool"] == p] or [1.0]) for p in {x["_pool"] for x in rows}}
        vistos, final = set(), []
        for x in rows:
            if x["clave"] in vistos:
                continue
            vistos.add(x["clave"])
            x["peso"] = round(100 * x["peso"] / mx_pool[x["_pool"]], 1)
            x["etiqueta"] = etiqueta_de(x["_pool"] if x["_pool"] != "persona" else "persona", x["n_textos"],
                                        None if x["cluster"].startswith("sin") or x["cluster"] == "ruido" else
                                        (not np.isnan(x["estabilidad"]) and x["estabilidad"] != "NA" and
                                         float(x["estabilidad"]) >= UMBRAL_ESTABLE))
            final.append(x)
        tablas[slug] = final

        cols = ["concepto", "peso", "cluster", "polaridad", "n_textos", "estabilidad", "ejemplo_row_id", "etiqueta"]
        pd.DataFrame([{c: x[c] for c in cols} for x in final]).to_csv(
            OUT_DIR / f"conceptos_{slug}.csv", index=False, encoding="utf-8")

    # Tabla de clusters (por corpus) con nombre, estabilidad y 2 verbatims (<=15 palabras, row_id)
    def tabla_clusters(corp, nombres, etiq, E, idx):
        info = clust[corp]["info"]
        out = []
        for g in sorted(set(etiq) - {"ruido"}, key=lambda s: int(s[1:])):
            num = int(g[1:])
            miembros = np.where(etiq == g)[0]
            cen = E[miembros].mean(axis=0)
            cen = cen / np.linalg.norm(cen)
            orden = miembros[np.argsort(-(E[miembros] @ cen))]
            verbs = []
            for m in orden[:2]:
                fila = df.loc[idx[m]]
                verbs.append(dict(row_id=fila["id"], texto=verbatim(fila["texto_anon"])))
            est = info["stab"].get(num)
            out.append(dict(cluster=g, nombre=", ".join(nombres.get(g, [])), n=int(len(miembros)),
                            estabilidad=("NA" if est is None or np.isnan(est) else round(est, 2)),
                            metodo=info["metodo"], verbatims=verbs))
        return out

    tc = {}
    for slug in ["antonia", "tomas"]:
        nombres_cl, etiq_p = nombres_clusters(slug)
        tc[slug] = tabla_clusters(slug, nombres_cl, etiq_p, clust[slug]["E"], clust[slug]["idx"])
    nombres_d, etiq_d = nombres_clusters("dolor")
    tc["dolor"] = tabla_clusters("dolor", nombres_d, etiq_d, clust["dolor"]["E"], clust["dolor"]["idx"])

    # Resumen de ejecución (JSON local, reproducible)
    for corp in ["antonia", "tomas", "dolor"]:
        info = clust[corp]["info"]
        resumen["clusters"][corp] = dict(metodo=info["metodo"], k_kmeans=info["k"],
                                         silhouette_k=info["sil"], ari_hdbscan_vs_kmeans=info["ari"],
                                         estabilidad_primario={f"c{k}": (None if np.isnan(v) else round(v, 3))
                                                               for k, v in info["stab"].items()},
                                         estabilidad_kmeans={f"c{k}": (None if np.isnan(v) else round(v, 3))
                                                             for k, v in info["stab_km"].items()})
    resumen["corpus_n"]["comun_oriente"] = int((grupos_corpus == "comun").sum())
    resumen["corpus_n"]["busqueda"] = int((grupos_corpus == "busqueda").sum())
    resumen["aristas_coocurrencia"] = len(arist)
    (OUT_DIR / "resumen_ejecucion.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")

    # Corpus anonimizados (uso local, NO publicar)
    for corp in df["corpus"].unique():
        df[df["corpus"] == corp][["id", "row_id", "fuente", "nps", "texto_anon"]].to_csv(
            CORPUS_DIR / f"corpus_{corp}.csv", index=False, encoding="utf-8")

    escribir_html(tablas, tc, arist, resumen)
    print(json.dumps(resumen["corpus_n"], ensure_ascii=False), "OK")


COLOR = {"valor": "#212c35", "dolor": "#fda902", "intención": "#6bc1e9", "neutro": "#888"}


def escribir_html(tablas, tc, arist, resumen):
    """HTML autocontenido: pestañas por persona; cada una con nube, grafo y clusters."""
    def nube(filas):
        spans = []
        for x in sorted(filas, key=lambda z: -z["peso"]):
            size = 13 + 30 * x["peso"] / 100
            titulo = f"n={x['n_textos']} · estabilidad={x['estabilidad']} · cluster={x['cluster']} · {x['etiqueta']}"
            spans.append(f'<span class="w" style="font-size:{size:.1f}px;color:{COLOR.get(x["polaridad"], "#888")}" '
                         f'title="{html.escape(titulo)}">{html.escape(x["concepto"])}</span>')
        return '<div class="nube">' + " ".join(spans) + "</div>"

    def grafo(filas, aristas):
        nombres = {x["clave"]: x for x in filas}
        nodos = list(nombres.keys())
        if not nodos:
            return "<p>Sin conceptos.</p>"
        W, H, R = 680, 500, 200
        pos = {}
        for i, k in enumerate(nodos):
            ang = 2 * np.pi * i / len(nodos)
            pos[k] = (W / 2 + R * np.cos(ang), H / 2 + R * np.sin(ang))
        lineas = []
        for a in aristas:
            if a["a"] in pos and a["b"] in pos:
                (x1, y1), (x2, y2) = pos[a["a"]], pos[a["b"]]
                lineas.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                              f'stroke="#9aa5b1" stroke-width="{min(4, 0.5 + a["pmi"]):.2f}" opacity=".7"/>')
        puntos = []
        for k in nodos:
            x, y = pos[k]
            r = 5 + nombres[k]["peso"] / 20
            col = COLOR.get(nombres[k]["polaridad"], "#888")
            lab = html.escape(nombres[k]["concepto"])
            puntos.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}"/>'
                          f'<text x="{x:.1f}" y="{y - r - 3:.1f}" font-size="11" text-anchor="middle" '
                          f'fill="#212c35">{lab}</text>')
        return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Grafo de co-ocurrencia">'
                + "".join(lineas) + "".join(puntos) + "</svg>")

    def tabla(filas):
        cab = ("<tr><th>Concepto</th><th>Peso</th><th>Cluster</th><th>Polaridad</th><th>n</th>"
               "<th>Estabilidad</th><th>row_id</th><th>Etiqueta</th></tr>")
        cuerpo = "".join(
            f"<tr><td>{html.escape(x['concepto'])}</td><td>{x['peso']}</td><td>{html.escape(str(x['cluster']))}</td>"
            f"<td>{x['polaridad']}</td><td>{x['n_textos']}</td><td>{x['estabilidad']}</td>"
            f"<td>{html.escape(str(x['ejemplo_row_id']))}</td><td>{html.escape(x['etiqueta'])}</td></tr>"
            for x in sorted(filas, key=lambda z: -z["peso"]))
        return f"<table>{cab}{cuerpo}</table>"

    def clusters_html(lista, titulo):
        if not lista:
            return f"<h3>{titulo}</h3><p>Sin clusters (ruido o n&lt;8).</p>"
        filas = []
        for c in lista:
            verbs = "<br>".join(f"<q>{html.escape(v['texto'])}</q> <small>[{html.escape(v['row_id'])}]</small>"
                                for v in c["verbatims"])
            filas.append(f"<tr><td>{c['cluster']}</td><td>{html.escape(c['nombre'])}</td><td>{c['n']}</td>"
                         f"<td>{c['estabilidad']}</td><td>{verbs}</td></tr>")
        return (f"<h3>{titulo}</h3><table><tr><th>Cluster</th><th>Términos (c-TF-IDF)</th><th>n</th>"
                f"<th>Estabilidad</th><th>Verbatims (≤15 palabras)</th></tr>{''.join(filas)}</table>")

    secciones = []
    for slug, nombre in [("antonia", "Antonia"), ("tomas", "Tomás")]:
        n_p = resumen["corpus_n"][slug]
        flag = " · exploratorio (n&lt;20)" if n_p < 20 else ""
        secciones.append(f"""
<section id="{slug}" class="panel{' on' if slug == 'antonia' else ''}">
  <h2>{nombre} <small>n={n_p} textos{flag}</small></h2>
  <p class="leyenda"><span style="color:#212c35">■ valor (promotor)</span> ·
     <span style="color:#fda902">■ dolor (detractor / Lead)</span> ·
     <span style="color:#6bc1e9">■ intención (búsqueda [WEB])</span> · tamaño = peso c-TF-IDF</p>
  <h3>Nube</h3>{nube(tablas[slug])}
  <h3>Grafo de co-ocurrencia (PMI, pares con ≥2 textos)</h3>{grafo(tablas[slug], arist)}
  {clusters_html(tc[slug], 'Clusters de ' + nombre)}
  {clusters_html(tc['dolor'], 'Clusters de dolores (compartidos)')}
  <h3>Tabla de conceptos</h3>{tabla(tablas[slug])}
</section>""")
    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nube de conceptos · Antonia y Tomás Pascual · USO INTERNO</title>
<style>
:root {{ --valor:#212c35; --dolor:#fda902; --intencion:#6bc1e9; --fondo:#ffffff; --texto:#212c35; }}
body {{ margin:0; padding:16px; font:15px/1.5 system-ui,sans-serif; background:var(--fondo); color:var(--texto); }}
h1 {{ font-size:22px; margin:0 0 4px; }} h2 {{ font-size:19px; }} h3 {{ font-size:16px; margin-top:24px; }}
.aviso {{ background:#fff4d6; border-left:4px solid var(--dolor); padding:8px 12px; font-size:13px; }}
.tabs button {{ border:1px solid var(--valor); background:#fff; padding:8px 14px; margin-right:6px; cursor:pointer; }}
.tabs button.on {{ background:var(--valor); color:#fff; }}
.panel {{ display:none; }} .panel.on {{ display:block; }}
.nube {{ display:flex; flex-wrap:wrap; gap:10px 16px; align-items:baseline; padding:12px; border:1px solid #e3e8ee; }}
.w {{ font-weight:600; line-height:1.1; }}
.leyenda {{ font-size:13px; }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th,td {{ border-bottom:1px solid #e3e8ee; padding:6px 8px; text-align:left; vertical-align:top; }}
th {{ background:#f3f6f9; }} q {{ display:block; margin:4px 0; }}
svg {{ width:100%; max-width:680px; height:auto; border:1px solid #e3e8ee; }}
footer {{ font-size:12px; color:#555; margin-top:32px; border-top:1px solid #e3e8ee; padding-top:8px; }}
@media (max-width:600px) {{ body {{ padding:16px; }} table {{ display:block; overflow-x:auto; }} }}
</style></head>
<body>
<h1>Nube de conceptos · Antonia y Tomás Pascual</h1>
<p class="aviso"><strong>USO INTERNO.</strong> Contiene verbatims de clientes (anonimizados, sin nombres). No publicar ni pegar en piezas públicas.
Fase 1 del PROMPT_v5 · método completo en research/v5_nube/METODO.md.</p>
<nav class="tabs"><button class="on" data-tab="antonia">Antonia</button><button data-tab="tomas">Tomás</button></nav>
{''.join(secciones)}
<footer>Corpus: Venta-Usados campaña Portillo, zona oriente (n={resumen['corpus_n'].get('antonia',0)+resumen['corpus_n'].get('tomas',0)+resumen['corpus_n'].get('comun_oriente',0)} textos);
dolores: detractores grupo + CR_Lead-Portillo (n={resumen['corpus_n'].get('dolor',0)}); búsqueda [WEB] (n={resumen['corpus_n'].get('busqueda',0)}).
Modelo de embeddings local: {html.escape(MODELO_EMB)}.</footer>
<script>
document.querySelectorAll('.tabs button').forEach(function(b){{
  b.addEventListener('click',function(){{
    document.querySelectorAll('.tabs button').forEach(function(x){{x.classList.remove('on');}});
    document.querySelectorAll('.panel').forEach(function(x){{x.classList.remove('on');}});
    b.classList.add('on'); document.getElementById(b.dataset.tab).classList.add('on');
  }});
}});
</script>
</body></html>"""
    (OUT_DIR / "NUBE_CONCEPTOS.html").write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
