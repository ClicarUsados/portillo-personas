# METODO · Nube de conceptos v5 (Fase 0 y Fase 1)

Fecha de ejecución: 2026-11-24 · USO INTERNO · contiene verbatims de clientes anonimizados: no publicar.
Etiquetas: [DATO] = inputs_clean/ con filtro explícito · [WEB] = research/15_busqueda_premium.md · [HIPÓTESIS] · NO VERIFICADO.

## 1. Reproducir

```bash
cd /Users/betosanchez/portillo-personas
./.venv_v5/bin/python analisis/v5_nlp/01_nube_conceptos.py
```

- Entorno: `.venv_v5/` (Python 3.14.6; pandas 3.0.3; scikit-learn 1.9.0; sentence-transformers 6.3.0; umap-learn 0.6.0; hdbscan 0.8.44; spacy 3.8.18 con `es_core_news_sm` 3.8.0; keybert 0.9.0 instalado pero no usado: ver §6).
- Modelo de embeddings: `paraphrase-multilingual-MiniLM-L12-v2`, descargado de Hugging Face y ejecutado en local. Ningún texto sale de la máquina.
- Semilla fija: 42. Bootstrap: 100 remuestreos.
- Entrada: solo `inputs_clean/`. `inputs_raw/` no se abrió. El script tiene un `assert` que rechaza cualquier ruta con `inputs_raw`.
- Salidas: `conceptos_antonia.csv`, `conceptos_tomas.csv`, `NUBE_CONCEPTOS.html`, `resumen_ejecucion.json`, y los corpus anonimizados en `analisis/v5_nlp/corpus/` (uso local).

## 2. Corpus (Fase 0)

| Corpus | Filtro / fuente | n textos | Fuente de datos |
|---|---|---|---|
| Antonia | `campaña o sensor` = "2025 - Venta Usados Portillo" (114 filas) y `nombre_concesionario` que contiene LA DEHESA, BILBAO, LAS CONDES, LUIS CARRERA, PADRE HURTADO, VITACURA o DELANO (71 filas; mismo regex que v3). Texto no vacío. | **31** | CR_2025-Venta-Usados |
| Tomás | Igual que arriba | **19** | CR_2025-Venta-Usados |
| Común (oriente) | Igual que arriba | **6** | CR_2025-Venta-Usados |
| Dolor | Detractores (NPS ≤ 6) de Venta-Usados **del grupo**, todas las campañas, con texto libre (298) + respuestas de `¿Qué necesita para seguir con su proceso de cotización?` de CR_Lead-Portillo (431) | **729** | CR_2025-Venta-Usados; CR_Lead-Portillo |
| Búsqueda | Consultas entre comillas en research/15_busqueda_premium.md, secciones §2 y §3 | **26** | [WEB] |

Notas de n:
- De las 71 filas oriente, 15 no tienen texto libre; quedan 56 textos (31 + 19 + 6).
- Antonia (31) alcanza el umbral de 20. Tomás (19) queda bajo 20: su análisis es **exploratorio**. Común (6) no se interpreta.
- En el corpus de dolor, 275 de 431 respuestas de Lead son la opción cerrada "Ya estoy en contacto con mi ejecutivo" (64 %). No es un dolor, es un estado.
- De los 298 detractores del grupo, solo 6 son de Portillo oriente. El resto son de las otras marcas del holding.
- 6 filas de dolor (detractores) también están en los corpus de persona. Los corpus se solapan parcialmente.

**Asignación a persona [HIPÓTESIS]** (regla de PROMPT_v5 Fase 0, implementada en `asignar_persona`):
- Tomás: canal "Porque el auto que quería estaba acá", "Porque vi publicidad en medios" o "Redes Sociales", y SIN parte de pago.
- Antonia: canal "Porque ya soy (o he sido) cliente" o "Por recomendaciones de conocidos", o CON parte de pago.
- Común: el resto ("Porque me queda cerca", "Otro").
- Parte de pago = `Vehículo en parte de pago` distinto de "No aplica". Los valores 1–5 no tienen diccionario en el archivo: NO VERIFICADO el significado; se usa solo como "usó parte de pago".
- La regla es exclusiva por construcción: no hay filas que caigan en dos personas.

## 3. Limpieza y anonimización

1. Textos libres de Venta-Usados por fila: `¿Qué te motiva a dar esa puntuación?`, `¿Qué faltó para que la entrega…?`, `Texto opción otros`. Se concatenan con ". ".
2. Anonimización antes de vectorizar (`procesar_textos`):
   - NER de spaCy `es_core_news_sm`: los tramos etiquetados PER se reemplazan por `PERSONA`.
   - Regex: correos, teléfonos y RUT se reemplazan por `DATO_PRIVADO` (4 casos, todos en el corpus de dolor).
   - Límite: el NER no detecta todos los nombres. No conocemos la lista de vendedores (la columna `vendedor` no trae nombres) y no se revisó a mano cada texto. Riesgo residual: nombres no reconocidos por el modelo.
3. Lematización con spaCy. Se quitan stopwords de spaCy, tokens de menos de 3 letras, no alfabéticos y: `igual, po, cachai, osea, altiro, bueno, nomas, harto, empresa, americar, persona, dato_privado, ser, estar, tener`.
4. Tildes: para contar se usan formas sin tildes. Para mostrar se usa la forma con tilde más frecuente.

## 4. Términos (TF-IDF y c-TF-IDF)

- `CountVectorizer` de 1 a 3 gramas sobre lemas sin tildes, `min_df = 2` en el conjunto total.
- **c-TF-IDF** (BERTopic): `W[g,t] = tf[g,t] · log(1 + A / f[t])`. `A` = promedio de palabras por grupo. Grupos: antonia, tomas, comun, dolor, busqueda.
- Pools por corpus:
  - Persona (valor/dolor): top 20 de c-TF-IDF de la persona, con `df ≥ 2` dentro de la persona.
  - Dolor: top 12 de c-TF-IDF del corpus de dolor, con `df ≥ 3`. Es compartido por las dos personas.
  - Intención: top 10 de c-TF-IDF de búsqueda, con `df ≥ 1`. Es compartido.
- `peso` = c-TF-IDF normalizado a 0–100 **dentro de cada pool**. Los pesos de un pool no se comparan con los de otro.
- Dedupe por concepto: prioridad persona > dolor > intención.

## 5. Embeddings, clusters y estabilidad

1. Embeddings MiniLM multilingüe (384 dimensiones, normalizados) sobre el texto anonimizado con tildes.
2. Reducción: UMAP (5 componentes, coseno, `n_neighbors = min(15, n-1)`) si n ≥ 15; PCA (5 componentes) si n < 15.
3. Método principal: **HDBSCAN** (`min_cluster_size = max(3, n // 10)`, `min_samples = 2`).
4. Comparación: **KMeans** con k elegido por silhouette en 2..min(6, n//4). Se comparan los dos con ARI.
5. Si HDBSCAN no da al menos 2 clusters, el método pasa a KMeans y queda anotado. No pasó en ningún corpus.
6. **Estabilidad**: bootstrap con reemplazo, 100 remuestreos. En cada remuestreo se reagrupa y, para cada cluster original, se toma el mejor Jaccard con un cluster del remuestreo. Estabilidad = media. Umbral: < 0,6 = inestable.
7. **Nombre de cluster**: top 5 términos por c-TF-IDF dentro del cluster frente al resto de su corpus. No se usó KeyBERT: el `keybert` de la venv no se llama en el script.
8. **Verbatims**: los 2 textos más cercanos al centroide (coseno). Se muestra una frase de ≤15 palabras o las primeras 15 palabras con "…". Cada uno lleva su `row_id`.

Resultados (fuente: `research/v5_nube/resumen_ejecucion.json`):

| Corpus | n | Método | k KMeans (silhouette) | ARI HDBSCAN vs KMeans | Clusters y estabilidad (HDBSCAN) |
|---|---|---|---|---|---|
| Antonia | 31 | HDBSCAN | 3 (0,41) | 0,54 | A0 0,68 · A1 **0,16** · A2 0,59 · A3 0,55 |
| Tomás | 19 | HDBSCAN | 2 (0,47) | 0,79 | T0 0,75 · T1 0,82 |
| Dolor | 729 | HDBSCAN | 6 (0,96, tope de la búsqueda) | 0,85 | D0 0,56 · D1 0,87 · D2 0,96 |

Lectura: en Antonia ningún cluster es estable con holgura (A1 0,16 es inestable; A2 y A3 quedan en el límite). En Tomás los dos clusters son estables. En dolor, la estabilidad alta de D2 no es evidencia fuerte: D2 contiene los duplicados de la opción cerrada. KMeans en dolor da estabilidad 1,0 en todos los clusters porque el corpus tiene muchos textos idénticos.

## 6. Polaridad y co-ocurrencia

- **Persona (valor vs dolor)**: para cada concepto del pool de persona se cuentan los textos con NPS ≥ 9 (promotor) y NPS ≤ 6 (detractor) donde aparece. Si la proporción de promotores es ≥ 0,5, la polaridad es **valor**; si no, **dolor**. Sin textos de ninguno de los dos extremos: neutro.
- **Dolor** → polaridad dolor. **Búsqueda** → intención [WEB].
- **Co-ocurrencia**: sobre todos los textos. Se cuentan los textos donde aparecen dos conceptos seleccionados. Se conserva el par si hay ≥ 2 textos y PMI > 0, y si ninguno contiene al otro. Resultado: 160 aristas.
- `keybert` está instalado pero no se usa. Se usó c-TF-IDF para nombrar clusters, como permitía el PROMPT.

## 7. Auditoría del modelo (criterios de detector-de-ruido y abogado-del-diablo)

Las dos skills se cargaron, pero **no devolvieron resultados en esta ejecución**. Lo que sigue aplica sus criterios directamente, no lo que dijeron las skills.

**Ruido detectado (detector-de-ruido):**
1. **Dolor inflado por una opción cerrada.** Los conceptos top del pool de dolor (`ejecutivo`, `contacto`, `contacto ejecutivo`: n=306, 279, 276; cluster D2) salen de "Ya estoy en contacto con mi ejecutivo" (275 de 431 leads). Esa respuesta describe un estado del lead, no un dolor. Hipótesis que compiten: (a) el lead quiere contacto y es un dolor real; (b) es una opción de formulario sin contenido. La prueba más barata: recalcular el pool de dolor sin esa opción y ver si `vehículo`, `entrega`, `información` (cluster D1) siguen arriba. Confianza en "dolor del Lead" sin ese ajuste: baja.
2. **Antonia y Tomás comparten casi todos sus conceptos valor** (atención, excelente, vendedor, excelente atención). La diferencia entre personas es de tamaño y no de contenido. Con 31 y 19 textos, la diferencia puede ser ruido. La regla de asignación ([HIPÓTESIS]) no está validada.
3. **Clusters inestables**: A1 (0,16) y A2/A3 cerca del límite. Los conceptos apoyados solo en esos clusters no sostienen pilar.

**Abogado del diablo (ángulos: datos vs narrativa, variable omitida):**
- La narrativa "Antonia cree en la atención personal; Tomás en la transparencia" no sale de los datos: en el corpus de Tomás no aparece "transparencia" entre los conceptos top. Esa narrativa queda como [HIPÓTESIS] y no debe usarse en piezas.
- El corpus de dolor mezcla marcas. Si el dolor es de otras concesionarias del holding, no describe a los clientes de Portillo. Hay que filtrar a Portillo para decir algo sobre Portillo; con solo 6 detractores de Portillo oriente no se puede.
- Variable omitida: no hay dato de precio, modelo ni plazo de venta por texto. Un detractor puede serlo por el auto y no por la atención. No se controló por modelo.
- Búsqueda: son 26 consultas candidatas redactadas a mano, sin volumen. La intención "premium" es un supuesto del plan, no un hallazgo.

**Lo que no resiste → [HIPÓTESIS]**: diferencias Antonia vs Tomás; narrativa de transparencia; dolor del Lead ("ejecutivo"); los clusters A1, A2 y A3; cualquier concepto de búsqueda.

## 8. Limitaciones

- n chico: Antonia 31, Tomás 19, común 6, Portillo oriente con texto 56. Análisis **exploratorio** por persona.
- Encuesta solo a quienes compraron (Venta-Usados) y a leads que cotizaron. Hay sesgo de respuesta y de supervivencia.
- Asignación a persona por regla propia [HIPÓTESIS], no por una variable del CRM.
- NPS ≥ 9 / ≤ 6 como proxy de valor/dolor: es una simplificación.
- Anonimización por NER: no garantiza borrar todos los nombres. Revisar antes de cualquier uso fuera del equipo.
- Lematización con `es_core_news_sm`: puede fallar en chilenismos.
- Silhouette en dolor sigue subiendo hasta el tope k = 6; no se exploró más allá.
- Co-ocurrencia con PMI sobre pocos textos: los pares con ≥ 2 apariciones son frágiles.
- **Conversión**: no hay ningún cálculo de conversión lead→venta. No se afirma.

## 9. Bloqueos

- Diccionario de `Vehículo en parte de pago` (valores 1–5): responsable Beto / CRM.
- Confirmar la regla de asignación a persona antes de usarla en la estrategia: responsable Beto.
- Confirmar si la opción "Ya estoy en contacto con mi ejecutivo" debe contar como dolor: responsable Beto.
- Autorizar el artefacto de publicación: el PROMPT pide publicarlo como artifact, pero el HTML contiene verbatims de clientes. Esto contradice la regla de que los verbatims no salen de la máquina. **No se publicó.** Si Beto quiere un artifact, debe autorizarlo y decidir qué se muestra.
