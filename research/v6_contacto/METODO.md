# METODO · v6 universo de puntos de contacto [HIPÓTESIS-ML]
Corte: 2026-11-24. Intención: que Beto pueda explicar, reproducir y criticar cada paso. Todo lo que sale de estos modelos es hipótesis hasta validarse (ver `entregables/v6_contacto/PLAN_VALIDACION.md`).

## Entorno
- `.venv_v5` (Python 3.x con sentence-transformers 6.3.0, umap-learn, hdbscan, keybert, scipy, sklearn, transformers 5.24, torch 2.15). No se creó `.venv_v6`: no hizo falta.
- Modelos locales en caché HF: `paraphrase-multilingual-MiniLM-L12-v2` (ya estaba), `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (descargado en esta corrida). Los datos no salen a APIs externas; solo se descargaron las taxonomías públicas.

## Fase 0 · semillas (`analisis/v6_contacto/00b_semillas.py`)
- Conceptos del v5 con peso ≥ 30, sin clusters de ruido y sin nombres de comuna. Peso = peso/100 × 0,5.
- Rasgos del perfil (uso, detonante, cómo llega, valora, teme), peso 0,2 a 0,6. Los rasgos de estilo de vida son HIPÓTESIS y el peso es más bajo. Ver SESGOS.md §3 sobre rasgos ILUSTRATIVOS.
- Sin género ni nombre. La comuna no entra como semilla; solo en el contrafactual.

## Fase 1 · universo (`analisis/v6_contacto/00_universo.py`)
- Fuente principal: IAB Content Taxonomy 3.1, descargada de github.com/InteractiveAdvertisingBureau/Taxonomies (ruta `Content Taxonomies/Content Taxonomy 3.1.tsv`, copia en `fuentes/`). Se eligieron 49 nodos de estilo de vida, viajes, deportes, hogar, comida, auto y medios. Se usa la columna Name para el nombre.
- Candidatos locales y de calendario: 16 con URL consultada 2026-11-24 (chile.travel, The Clinic, Encancha, El Mostrador, CNN Chile, La Tercera, ESPN Run, Meteored, padelfip.com, alairelibre.cl).
- Google Ads: 5 categorías de afinidad de ejemplo tomadas de support.google.com/google-ads/answer/2497941 (verificado por WebFetch).
- Sin URL: 6 filas marcadas `verificado=NO` (intereses de Meta, radios, podcasts, newsletters, cuentas locales, escapada al sur). No entran al ranking.
- Re-ejecutar: borrar `universo_candidatos.csv` (el script usa modo "x") y correr `.venv_v5/bin/python analisis/v6_contacto/00_universo.py`.

## Fase 2 · modelos de afinidad (`analisis/v6_contacto/01_afinidad.py`)
M1. Similitud semántica. Persona = promedio ponderado de semillas normalizado. Candidato = "nombre. categoría. subcategoría". Score = coseno. Modelo MiniLM multilingüe. Supuesto: el coseno entre texto corto captura algo de afinidad temática (es débil con textos de 2 a 4 palabras).

M2. Zero-shot NLI. Premisa = 8 semillas de mayor peso unidas. Hipótesis = "A esta persona le interesa {candidato}." Modelo mDeBERTa xnli. Score = probabilidad de entailment (multi_label). Supuesto: que el NLI pueda juzgar interés a partir de una lista de semillas. Resultado: satura cerca de 1 y correlaciona poco con M1 y M3 (ver SESGOS.md §4).

M3. Grafo con PageRank personalizado. Nodos: semillas, candidatos y categorías. Aristas: semilla–candidato si coseno > 0,25 (peso = coseno); candidato–candidato si coseno > 0,50; candidato–categoría con peso 0,5 (jerarquía de la taxonomía). PageRank con α = 0,85, 100 iteraciones, vector de personalización = pesos de las semillas. Supuesto: la ruta semilla→candidato→categoría o candidato vecino cubre dos o tres saltos.

M4. Filtro colaborativo. NO CORRIÓ. No hay dataset público confiable de co-ocurrencia de intereses; no se fabricó.

Ensamble. Percentil de cada método (1 = mejor). Score final = media de percentiles de los métodos disponibles (emb, PPR, NLI). RRF con k = 60 en la columna `rrf`. Kendall entre métodos en `metodo_resultados.json`.
- Robusto: top 14 (20 %) en todos los métodos disponibles (3 de 3, no 3 de 4).
- Estable: rango del bootstrap entre el percentil 5 y el 95 ≤ 30 puestos. Bootstrap de 100 remuestreos de semillas, recalculando emb y PPR (no NLI).
- score_cf = NA: el filtro colaborativo no corrió.

## Fase 3 · territorios (`analisis/v6_contacto/02_territorios_html.py`)
- Top 50 de la unión de rankings. Embeddings MiniLM, UMAP (n_neighbors = 8, cosine), HDBSCAN (min_cluster_size = 4, min_samples = 2). Ruido = "sin territorio".
- Nombre con c-TF-IDF sobre los nombres de cada cluster, con stopwords en español.
- Alcance: compartido si ≥ 50 % de los miembros está en el top 20 de ambas personas; propio si ≥ 50 % en una y < 25 % en la otra; si no, mixto.
- Limitación: los clusters son pequeños (4 a 20 candidatos) y los nombres de IAB son cortos. Los territorios son orientativos.

## Fase 4 · sesgo (`analisis/v6_contacto/01_afinidad.py`, `03_sensibilidad_lexica.py`)
- Contrafactual de género y comuna con emb+PPR. Criterio: |Δ| > 20 puestos. Resultado: ninguno marcado. Detalle en SESGOS.md.
- Prueba de fuga léxica: ranking de Antonia solo con semillas de estilo de vida.

## Re-ejecutar (en orden)
```
.venv_v5/bin/python analisis/v6_contacto/00_universo.py      # borrar universo_candidatos.csv antes
.venv_v5/bin/python analisis/v6_contacto/00b_semillas.py     # borrar semillas_*.csv antes
.venv_v5/bin/python analisis/v6_contacto/01_afinidad.py      # borrar ranking_*, sesgos_detalle_*, metodo_resultados.json antes; ~5 min
.venv_v5/bin/python analisis/v6_contacto/02_territorios_html.py  # borrar territorios.csv y UNIVERSO_CONTACTO.html antes
.venv_v5/bin/python analisis/v6_contacto/03_sensibilidad_lexica.py  # borrar sensibilidad_lexica_antonia.csv antes
```
Las semillas están en `semillas_*.csv` y se pueden editar a mano; re-ejecutar 01 y 02 después.
