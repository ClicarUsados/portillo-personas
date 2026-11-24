"""Fase 3: territorios (UMAP + HDBSCAN sobre top 50 de la union de rankings, nombre con c-TF-IDF),
y UNIVERSO_CONTACTO.html autocontenido (dos pestañas: Antonia, Tomás).
Salidas: research/v6_contacto/territorios.csv, research/v6_contacto/UNIVERSO_CONTACTO.html"""
import csv, html, json, pathlib
import numpy as np
import hdbscan, umap
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
OUT = pathlib.Path("/Users/betosanchez/portillo-personas/research/v6_contacto")
COL = {"ink":"#212c35","blue":"#0082d1","sky":"#6bc1e9","sun":"#fda902","gray":"#8a939b"}
TERR_COLORS = ["#0082d1","#fda902","#6bc1e9","#212c35","#8a939b","#2e7d5b","#b5485d"]

def read(p):
    return list(csv.DictReader(open(OUT/f"ranking_{p}.csv", encoding="utf-8")))

def ctext(r):
    return r["candidato"]  # texto de candidato = nombre (la categoria va en la tabla)

def main():
    R = {p: read(p) for p in ["antonia","tomas"]}
    names_all = {}
    for p in R:
        for r in R[p]: names_all.setdefault(r["candidato"], r)
    cands = list(names_all.values())
    top50 = set()
    for p in R:
        for r in R[p][:50]: top50.add(r["candidato"])
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    E = model.encode([ctext(r) for r in cands], normalize_embeddings=True)
    idx50 = [i for i,r in enumerate(cands) if r["candidato"] in top50]
    Xu = umap.UMAP(n_neighbors=8, min_dist=0.15, metric="cosine", random_state=42).fit_transform(E)
    lab = hdbscan.HDBSCAN(min_cluster_size=4, min_samples=2).fit_predict(E[idx50])
    cluster = {cands[i]["candidato"]: int(l) for i,l in zip(idx50, lab)}
    # c-TF-IDF: un documento por territorio (concatenar nombres), terminos distintivos
    docs = {}
    for c,l in cluster.items(): docs.setdefault(l, []).append(c)
    labels_k = [k for k in docs if k != -1]
    cv = CountVectorizer(lowercase=True, token_pattern=r"(?u)\b\w\w+\b", stop_words=["de","y","en","la","el","los","las","para","del","por","con","una","un","a","al","o","s"])
    corpus = [" ".join(docs[k]) for k in labels_k]
    tf = cv.fit_transform(corpus).toarray().astype(float)
    tfidf_c = tf / np.maximum(tf.sum(1, keepdims=True),1)
    idf = np.log((1+len(corpus))/(1+(tf>0).sum(0)))+1
    ctfidf = tfidf_c*idf
    vocab = cv.get_feature_names_out()
    tname = {}
    for j,k in enumerate(labels_k):
        top_terms = [vocab[t] for t in np.argsort(-ctfidf[j])[:3] if ctfidf[j][t]>0]
        tname[k] = " · ".join(top_terms) if top_terms else f"territorio {k}"
    tname[-1] = "sin territorio (ruido HDBSCAN)"
    # propio / compartido
    top20 = {p: set(r["candidato"] for r in R[p][:20]) for p in R}
    rows = []
    for k in sorted(docs, key=lambda x:(x==-1,x)):
        mem = docs[k]
        # alcance por proporcion de miembros en el top 20 de cada persona
        fa = sum(1 for c in mem if c in top20["antonia"])/len(mem)
        ft = sum(1 for c in mem if c in top20["tomas"])/len(mem)
        if fa>=0.5 and ft>=0.5: alcance = "compartido"
        elif fa>=0.5 and ft<0.25: alcance = "propio de Antonia"
        elif ft>=0.5 and fa<0.25: alcance = "propio de Tomás"
        else: alcance = "mixto (sin dominio claro)"
        rows.append(dict(territorio=tname[k], cluster=k, n_candidatos=len(mem), alcance=alcance,
                         candidatos=" | ".join(mem)))
    with open(OUT/"territorios.csv","x",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    color_of = {}
    for k in sorted(docs):
        color_of[k] = TERR_COLORS[(k if k>=0 else len(TERR_COLORS)-1) % len(TERR_COLORS)] if k!=-1 else COL["gray"]
    # ---- HTML ----
    def score_px(s): return 6 + 14*float(s)
    def scatter(p):
        W,H,pad=640,420,30
        xs,ys=Xu[:,0],Xu[:,1]
        def sx(x): return pad+(x-xs.min())/(xs.max()-xs.min()+1e-9)*(W-2*pad)
        def sy(y): return pad+(y-ys.min())/(ys.max()-ys.min()+1e-9)*(H-2*pad)
        sc={r["candidato"]:r for r in R[p]}
        out=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mapa UMAP de candidatos {p}" style="width:100%;height:auto;background:#fff;border:1px solid #e4e1da;border-radius:10px">']
        for i,c in enumerate(cands):
            name=c["candidato"]; r=sc.get(name)
            s=float(r["score_final"]) if r else 0.0
            col=color_of[cluster.get(name,-1)] if name in top50 else "#cfd4d9"
            stroke = "#212c35" if (r and r["robusto"]=="SI") else "#ffffff"
            sw = 2.5 if (r and r["robusto"]=="SI") else 1
            op = 1.0 if r else 0.35
            out.append(f'<circle cx="{sx(xs[i]):.1f}" cy="{sy(ys[i]):.1f}" r="{score_px(s)/2:.1f}" fill="{col}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"><title>{html.escape(name)} (score {s:.2f}{", robusto" if r and r["robusto"]=="SI" else ""})</title></circle>')
        out.append('</svg>')
        return "".join(out)
    def graph(p):
        top=R[p][:20]; W,H=640,520; cx=W/2; cy=H/2; Rr=200
        nodes=[]; out=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Grafo persona a top 20" style="width:100%;height:auto;background:#fff;border:1px solid #e4e1da;border-radius:10px">']
        for j,r in enumerate(top):
            ang=2*np.pi*j/len(top)-np.pi/2; x=cx+Rr*np.cos(ang); y=cy+Rr*np.sin(ang)
            w=float(r["score_final"]); col=color_of[cluster.get(r["candidato"],-1)] if r["candidato"] in top50 else "#cfd4d9"
            out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#8a939b" stroke-opacity="{0.2+0.8*w:.2f}" stroke-width="{1+3*w:.1f}"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{col}" stroke="{"#212c35" if r["robusto"]=="SI" else "#fff"}" stroke-width="2"><title>{html.escape(r["candidato"])} {w:.2f}</title></circle>')
            tx=cx+(Rr+22)*np.cos(ang); ty=cy+(Rr+22)*np.sin(ang)
            anchor="start" if np.cos(ang)>0.2 else ("end" if np.cos(ang)<-0.2 else "middle")
            out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="11" text-anchor="{anchor}" fill="#212c35">{html.escape(r["candidato"][:28])}</text>')
        label = "Antonia" if p=="antonia" else "Tomás"
        out.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#212c35"/><text x="{cx}" y="{cy+4}" font-size="13" fill="#fff" text-anchor="middle">{label}</text></svg>')
        return "".join(out)
    def table(p):
        trs=[]
        for r in R[p]:
            trs.append("<tr><td>"+str(r["rank"])+"</td><td>"+html.escape(r["candidato"])+"</td><td>"+r["tipo"]+"</td><td>"+r["score_final"]+"</td><td>"+r["robusto"]+"</td><td>"+r["estable"]+"</td><td>"+html.escape(r["semillas_que_lo_explican"])+"</td></tr>")
        return "".join(trs)
    legend="".join(f'<span class="sw" style="background:{color_of[k]}"></span>{html.escape(tname[k])}' for k in sorted(docs))
    def pane(p, title):
        return f'''<section class="pane" id="{p}">
<h2>{title} [HIPÓTESIS-ML]</h2>
<p class="note">Ranking de hipótesis generadas por modelos. No es evidencia: validar con PLAN_VALIDACION.md antes de usar.</p>
<div class="grid">{scatter(p)}{graph(p)}</div>
<div class="leg">{legend}</div>
<input id="f_{p}" class="filt" placeholder="Filtrar por nombre, tipo o semilla" oninput="filt('{p}',this.value)">
<div class="tw"><table><thead><tr><th>#</th><th>Candidato</th><th>Tipo</th><th>Score final</th><th>Robusto</th><th>Estable</th><th>Semillas que lo explican</th></tr></thead><tbody id="b_{p}">{table(p)}</tbody></table></div>
</section>'''
    doc=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Universo de contacto v6</title>
<style>
:root{{--ink:#212c35;--blue:#0082d1;--sky:#6bc1e9;--sun:#fda902;--mute:#5d6470;--line:#e4e1da;--paper:#faf8f4}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
header{{background:var(--ink);color:#fff;padding:18px 16px}} header h1{{margin:0;font-size:22px}}
.bar{{height:6px;background:linear-gradient(90deg,var(--sky) 50%,var(--sun) 50%)}}
nav{{display:flex;gap:8px;padding:12px 16px}} nav button{{border:1px solid var(--ink);background:#fff;padding:8px 14px;border-radius:20px;cursor:pointer}}
nav button.on{{background:var(--ink);color:#fff}}
main{{padding:0 16px 40px;max-width:1100px;margin:0 auto}} .pane{{display:none}} .pane.on{{display:block}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} @media (max-width:760px){{.grid{{grid-template-columns:1fr}}}}
.note{{color:var(--mute);font-size:13px}} .leg{{font-size:12px;color:var(--mute);margin:10px 0;display:flex;flex-wrap:wrap;gap:6px 14px}}
.sw{{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:5px;vertical-align:middle}}
.filt{{width:100%;max-width:420px;padding:9px;border:1px solid var(--line);border-radius:8px;margin:6px 0}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:13px;min-width:700px;background:#fff}}
th,td{{text-align:left;padding:7px;border-top:1px solid var(--line);vertical-align:top}} th{{color:var(--mute);font-size:12px}}
@media (prefers-color-scheme:dark){{:root{{--paper:#17181b;--ink:#ece9e2;--mute:#a7a59f;--line:#34363b}} body{{background:var(--paper);color:var(--ink)}} table,svg{{background:#202226!important}}}}
</style></head><body>
<header><h1>Universo de puntos de contacto · v6 [HIPÓTESIS-ML]</h1><div>Uso INTERNO · no publicar · corte 2026-11-24</div></header><div class="bar"></div>
<nav><button class="on" onclick="tab('antonia',this)">Antonia</button><button onclick="tab('tomas',this)">Tomás</button></nav>
<main>{pane("antonia","Antonia")}{pane("tomas","Tomás")}</main>
<script>
function tab(p,b){{document.querySelectorAll('.pane').forEach(e=>e.classList.remove('on'));document.getElementById(p).classList.add('on');document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));b.classList.add('on');}}
function filt(p,q){{q=q.toLowerCase();document.querySelectorAll('#b_'+p+' tr').forEach(tr=>{{tr.style.display=tr.textContent.toLowerCase().includes(q)?'':'none'}});}}
</script></body></html>'''
    (OUT/"UNIVERSO_CONTACTO.html").write_text(doc, encoding="utf-8")
    print("clusters:", {tname[k]:len(docs[k]) for k in docs})
if __name__=="__main__": main()
