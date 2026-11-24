"""Fase 4 (prueba de ruido lexico): ranking de Antonia usando SOLO semillas de estilo de vida (HIPOTESIS),
sin conceptos de compra ni palabras automotrices. Compara top 10 con el ranking base (emb+ppr).
Salida: research/v6_contacto/sensibilidad_lexica_antonia.csv"""
import csv, importlib.util, pathlib
import numpy as np
spec = importlib.util.spec_from_file_location("af", "/Users/betosanchez/portillo-personas/analisis/v6_contacto/01_afinidad.py")
af = importlib.util.module_from_spec(spec); spec.loader.exec_module(af)
from sentence_transformers import SentenceTransformer
OUT = af.OUT
model = SentenceTransformer(af.EMB_MODEL)
cands = af.read_cands(); txt=[af.ctext(c) for c in cands]
E = model.encode(txt, normalize_embeddings=True); sims_cc = E@E.T
cat_of=[c["categoria"] for c in cands]; cats=sorted(set(cat_of))
seeds = af.read_seeds("antonia")
# semillas de estilo de vida: no tienen 'estilo' en el tipo
life = [s for s in seeds if "estilo" in s["tipo"]]
base_rank = None
res = af.run_methods(model, [s["texto"] for s in life], [s["peso"] for s in life], E, cands, cat_of, cats, sims_cc)
fin, _ = af.ensemble(res, ["emb","ppr"])
order = np.argsort(-fin)
rows=[]
for r_i,i in enumerate(order,1):
    rows.append(dict(rank=r_i, candidato=cands[i]["nombre"], tipo=cands[i]["tipo"], score_sens=round(float(fin[i]),4)))
with open(OUT/"sensibilidad_lexica_antonia.csv","x",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("semillas de estilo usadas:", len(life))
for r in rows[:10]: print(r["rank"], r["candidato"][:40], r["tipo"], r["score_sens"])
base = list(csv.DictReader(open(OUT/"ranking_antonia.csv",encoding="utf-8")))
top_base=[r["candidato"] for r in base[:10]]; top_sens=[r["candidato"] for r in rows[:10]]
print("solapamiento top10 base vs sensibilidad:", len(set(top_base)&set(top_sens)))
print("en base top10 y no en sensibilidad:", [c[:30] for c in top_base if c not in top_sens])
