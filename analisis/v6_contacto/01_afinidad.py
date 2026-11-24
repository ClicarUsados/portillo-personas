"""Fase 2 y 4: modelos de afinidad, ensamble, estabilidad (bootstrap) y contrafactual de sesgo.
Salidas en research/v6_contacto/: ranking_{antonia,tomas}.csv, sesgos_detalle.csv, metodo_resultados.json
Métodos: M1 embeddings (MiniLM multilingüe, local), M2 NLI zero-shot (mDeBERTa xnli, local, puede fallar),
M3 grafo con PageRank personalizado (semillas -> candidatos -> categorías IAB/Google),
M4 filtro colaborativo: NO CORRE (no hay dataset público de co-ocurrencia; ver METODO.md)."""
import csv, json, math, pathlib, traceback
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.stats import kendalltau

OUT = pathlib.Path("/Users/betosanchez/portillo-personas/research/v6_contacto")
EMB_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
NLI_MODEL = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
SIM_SEED_CAND, SIM_CAND_CAND = 0.25, 0.50   # umbrales de arista del grafo
ALPHA, ITERS = 0.85, 100
TOP_FRAC, STAB_MAX_SPREAD, CF_MAX_SHIFT, N_BOOT = 0.20, 30, 20, 100
GENERO = {"antonia": "mujer", "tomas": "hombre"}
COMUNA_DIRECTA = {"antonia": "La Dehesa", "tomas": "Providencia"}
COMUNA_CRUZADA = {"antonia": "Providencia", "tomas": "La Dehesa"}
PERSONAS = ["antonia", "tomas"]

def read_seeds(p):
    with open(OUT/f"semillas_{p}.csv", encoding="utf-8") as f:
        return [dict(texto=r["texto"], peso=float(r["peso"]), tipo=r["tipo_semilla"]) for r in csv.DictReader(f)]

def read_cands():
    with open(OUT/"universo_candidatos.csv", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["verificado"] == "SI"]

def ctext(r):
    return f"{r['nombre']}. {r['categoria']}. {r['subcategoria']}".replace(" .", "").strip()

def pct(scores):
    """Percentil de ranking: 1 = mejor, 0 = peor. Mayor score = mejor."""
    order = np.argsort(-scores, kind="stable")
    rank = np.empty(len(scores), int); rank[order] = np.arange(1, len(scores)+1)
    return rank, 1 - (rank-1)/(len(scores)-1)

def ppr(seed_vec_w, S_idx_n, E, Cc, cat_of, n_c, cats, sims_sc, sims_cc):
    """PageRank personalizado sobre: semillas (m) + candidatos (n) + categorias (k)."""
    m, n, k = len(seed_vec_w), n_c, len(cats)
    N = m + n + k
    W = np.zeros((N, N))
    for s in range(m):
        for c in range(n):
            if sims_sc[s, c] > SIM_SEED_CAND:
                W[s, m+c] = W[m+c, s] = sims_sc[s, c]
    for i in range(n):
        for j in range(n):
            if i != j and sims_cc[i, j] > SIM_CAND_CAND:
                W[m+i, m+j] = sims_cc[i, j]
    for i in range(n):
        ci = cats.index(cat_of[i]); W[m+i, m+n+ci] = W[m+n+ci, m+i] = 0.5
    rs = W.sum(1, keepdims=True); rs[rs == 0] = 1
    P = W / rs
    v = np.zeros(N); v[:m] = seed_vec_w / seed_vec_w.sum()
    x = v.copy()
    for _ in range(ITERS):
        x = ALPHA * (x @ P) + (1-ALPHA) * v
    return x[m:m+n]

def run_methods(model, seeds_txt, seeds_w, E, cands, cat_of, cats, sims_cc, nli=None, cat_nli=None, want_nli=False):
    S = model.encode(seeds_txt, normalize_embeddings=True)
    w = np.asarray(seeds_w, float); pv = (w[:, None]*S).sum(0); pv /= np.linalg.norm(pv)
    s_emb = E @ pv
    sims_sc = S @ E.T
    s_ppr = ppr(w, None, E, None, cat_of, len(cands), cats, sims_sc, sims_cc)
    out = dict(emb=s_emb, ppr=s_ppr, sims_sc=sims_sc, S=S)
    if want_nli and nli is not None:
        top = np.argsort(-w)[:8]; summ = ". ".join(seeds_txt[i] for i in top) + "."
        labels = [f"A esta persona le interesa {c['nombre']}." for c in cands]
        res = nli(summ, candidate_labels=labels, hypothesis_template="{}", multi_label=True)
        d = dict(zip(res["labels"], res["scores"]))
        out["nli"] = np.array([d[l] for l in labels])
    return out

def ensemble(parts, keys):
    """Media de percentiles de los metodos disponibles y RRF."""
    pcts = [pct(parts[k])[1] for k in keys]
    final = np.mean(pcts, axis=0)
    rrf = np.zeros(len(final))
    for k in keys:
        rank, _ = pct(parts[k]); rrf += 1/(60+rank)
    return final, rrf

def main():
    model = SentenceTransformer(EMB_MODEL)
    cands = read_cands()
    txt = [ctext(c) for c in cands]
    E = model.encode(txt, normalize_embeddings=True)
    sims_cc = E @ E.T
    cat_of = [c["categoria"] for c in cands]; cats = sorted(set(cat_of))
    meta = {"n_candidatos_verificados": len(cands), "emb_model": EMB_MODEL}

    nli, nli_err = None, None
    try:
        from transformers import pipeline
        nli = pipeline("zero-shot-classification", model=NLI_MODEL)
        meta["nli_status"] = "OK"
    except Exception as e:
        nli_err = f"{type(e).__name__}: {str(e)[:300]}"
        meta["nli_status"] = "FALLO: " + nli_err
    rng = np.random.default_rng(42)
    result = {}
    for p in PERSONAS:
        seeds = read_seeds(p)
        stxt = [s["texto"] for s in seeds]; sw = [s["peso"] for s in seeds]
        base = run_methods(model, stxt, sw, E, cands, cat_of, cats, sims_cc, nli=nli, want_nli=nli is not None)
        keys = ["emb", "ppr"] + (["nli"] if "nli" in base else [])
        final, rrf = ensemble(base, keys)
        n = len(cands); top_n = math.ceil(TOP_FRAC*n)
        top_sets = {k: pct(base[k])[0] <= top_n for k in keys}
        robusto = np.all([top_sets[k] for k in keys], axis=0)
        # bootstrap de semillas (emb+ppr; NLI no se re-ejecuta 100 veces)
        boot_ranks = np.zeros((N_BOOT, n))
        probs = np.asarray(sw)/np.sum(sw)
        for b in range(N_BOOT):
            idx = rng.choice(len(stxt), size=len(stxt), p=probs)
            cnt = np.bincount(idx, minlength=len(stxt)).astype(float)
            bw = cnt*np.asarray(sw)
            bb = run_methods(model, stxt, bw, E, cands, cat_of, cats, sims_cc)
            fb, _ = ensemble(bb, ["emb", "ppr"])
            boot_ranks[b] = pct(fb)[0]
        spread = np.percentile(boot_ranks, 95, axis=0) - np.percentile(boot_ranks, 5, axis=0)
        estable = spread <= STAB_MAX_SPREAD
        # semillas que lo explican: top-3 por similitud coseno
        rows = []
        for i, c in enumerate(cands):
            top3 = np.argsort(-base["sims_sc"][:, i])[:3]
            expl = " | ".join(f"{stxt[j]} ({base['sims_sc'][j, i]:.2f})" for j in top3)
            rows.append(dict(rank=0, candidato=c["nombre"], id=c["id"], tipo=c["tipo"],
                 score_emb=round(float(base["emb"][i]),4), score_nli=(round(float(base["nli"][i]),4) if "nli" in base else "NA"),
                 score_ppr=round(float(base["ppr"][i]),5), score_cf="NA (M4 no corrio)",
                 score_final=round(float(final[i]),4), rrf=round(float(rrf[i]),5),
                 robusto="SI" if robusto[i] else "NO", estable="SI" if estable[i] else "NO",
                 spread_bootstrap=int(spread[i]), semillas_que_lo_explican=expl, fuente=c["url"]))
        rows.sort(key=lambda r: -r["score_final"])
        for r_i, r in enumerate(rows, 1): r["rank"] = r_i
        with open(OUT/f"ranking_{p}.csv", "x", newline="", encoding="utf-8") as f:
            w_ = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w_.writeheader(); w_.writerows(rows)
        # Kendall entre metodos
        tau = {}
        for a in range(len(keys)):
            for b_ in range(a+1, len(keys)):
                t, _ = kendalltau(pct(base[keys[a]])[0], pct(base[keys[b_]])[0]); tau[f"{keys[a]}-{keys[b_]}"] = round(float(t),3)
        result[p] = dict(metodos=keys, kendall=tau, robusto_criterio=f"top {top_n} en todos los metodos disponibles ({len(keys)}/3; CF no corrio)",
                         n_robusto=int(robusto.sum()), n_estable=int(estable.sum()))
        # Contrafactual (solo emb+ppr, misma base de comparacion)
        base_ens, _ = ensemble(base, ["emb","ppr"]); base_rank = pct(base_ens)[0]
        cf_rows = []
        variants = [("genero_directo", GENERO[p]), ("genero_cruzado", GENERO["tomas" if p=="antonia" else "antonia"]),
                    ("comuna_directa", COMUNA_DIRECTA[p]), ("comuna_cruzada", COMUNA_CRUZADA[p])]
        for vname, extra in variants:
            ex_txt = stxt + [extra]; ex_w = sw + [0.3]
            v = run_methods(model, ex_txt, ex_w, E, cands, cat_of, cats, sims_cc)
            ve, _ = ensemble(v, ["emb","ppr"]); vr = pct(ve)[0]
            for i, c in enumerate(cands):
                d = int(vr[i]-base_rank[i])
                cf_rows.append(dict(persona=p, variante=vname, atributo_agregado=extra, candidato=c["nombre"], id=c["id"],
                                    rank_base=int(base_rank[i]), rank_variante=int(vr[i]), delta=d, flag_mayor_20=("SI" if abs(d) > CF_MAX_SHIFT else "NO")))
        with open(OUT/f"sesgos_detalle_{p}.csv","x",newline="",encoding="utf-8") as f:
            w_ = csv.DictWriter(f, fieldnames=list(cf_rows[0].keys())); w_.writeheader(); w_.writerows(cf_rows)
        result[p]["cf_flags"] = sorted({r["candidato"] for r in cf_rows if r["flag_mayor_20"]=="SI"})
    meta.update(result)
    with open(OUT/"metodo_resultados.json","x",encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(json.dumps(meta, ensure_ascii=False, indent=1)[:3000])

if __name__ == "__main__":
    main()
