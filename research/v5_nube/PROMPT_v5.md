# PROMPT v5 — Nube de conceptos con ML → pilares, verticales, creatividades y parrilla
Antonia y Tomás Pascual (Seminuevos Premium Portillo). Copia de trabajo del prompt pegado el 2026-11-24.

## Rol y objetivo
Equipo de tres: Data Scientist de NLP, Estratega de Contenido y Director Creativo de retail automotriz chileno. Objetivo: nube de conceptos reproducible por persona, bajada a pilares, verticales, territorios creativos, esquemas por formato y parrilla de 4 semanas. Quien lo lee es Beto (Brand Digital, Americar Usados), que lo lleva a jefatura, comité y su Magíster de Data Science: cada paso debe quedar explicado y reproducible.

## Contexto (leer antes)
- Perfiles: entregables/cliente_ideal/PERFIL_ANTONIA_cliente_ideal.html (es el perfil de Javiera renombrado; confirmar) y PERFIL_TOMAS_PASCUAL_cliente_ideal.html.
- Investigación: research/10_plan_premium.md, 11_promotores_seminuevo.md, 12_dolores_seminuevo.md, 13_comunas_web.md, 14_competencia_premium.md, 15_busqueda_premium.md, 00_contradicciones.md, 10_contradicciones_plan.md.
- Script base: analisis/v3_oriente_promotores.py (promotores de sucursales Portillo zona oriente).
- Marca: entregables/cliente_ideal/assets/brand/BRANDBOOK_PORTILLO_USADOS_2026.pdf (Premium #212c35 y blanco; acentos #0082d1, #6bc1e9, #fda902).
- Datos: solo inputs_clean/. NUNCA abras inputs_raw/.

## Reglas no negociables
1. Datos reales o nada. Cada concepto, peso o cifra: archivo, columna, filtro, n, script. Si no hay dato: NO VERIFICADO.
2. Etiquetas: [DATO], [PLAN], [WEB], [ILUSTRATIVO], [HIPÓTESIS] en todo lo que no sea código.
3. Privacidad: los verbatims no salen de la máquina. Modelos locales (sentence-transformers); nunca APIs externas de embeddings ni LLM para textos de clientes. Sin PII ni nombres de vendedores: filtra nombres propios antes de vectorizar.
4. No afirmes conversión lead→venta.
5. "seminuevo", nunca "usado". Sin promesas de garantía, plazos, "inspección de X puntos", "precio líder", "satisfacción garantizada" ni "cobertura mecánica hasta 12 meses".
6. Piezas públicas sin cifras internas (CRM, stock, margen, NPS, n de encuestas).
7. Todo bloqueo nombra de quién depende.
8. Nada irreversible: sin git commit, sin tocar inputs_raw/, sin crear tareas en Asana ni publicar en redes. Si una skill propone crear tareas, déjalas en un archivo y pregunta.
9. Contradicciones: ambas cifras, lado a lado.

## Fase 0 — Corpus por persona (secuencial)
- Crea analisis/v5_nlp/ y research/v5_nube/.
- Corpus base: textos libres de inputs_clean/CR_2025-Venta-Usados_* (campaña "2025 - Venta Usados Portillo") de sucursales de la zona oriente (mismo filtro que v3_oriente_promotores.py).
- Asignación a persona (regla explícita, [HIPÓTESIS]):
  - Antonia: llegó como "ya soy cliente" o por recomendación, o usó parte de pago.
  - Tomás: llegó porque "el auto que quería estaba acá", por publicidad o redes, y no usó parte de pago.
  - Los textos que no caen en ninguna van a un corpus común.
- Reporta n de cada corpus. Si alguno tiene < 20 textos, dilo: el análisis por persona es exploratorio y pesa más el corpus común.
- Corpus de dolores (para "qué lo haría irse"): detractores de Venta-Usados del grupo (decláralo) y respuestas abiertas de CR_Lead-Portillo ("¿Qué necesita para seguir con su proceso de cotización?").
- Corpus de búsqueda (solo intención): términos de research/15_busqueda_premium.md, marcados [WEB].
- Limpieza en español chileno: minúsculas; sin tildes para el conteo (conservarlas para mostrar); stopwords en español más chilenismos de relleno ("igual", "po", "cachai"); lematización si spacy con es_core_news_sm está disponible. Elimina nombres propios de personas.

## Fase 1 — Modelado (subagente Data Scientist)
Archivo: analisis/v5_nlp/01_nube_conceptos.py, con funciones por paso y comentarios que expliquen por qué cada método.
- Términos: TF-IDF de 1 a 3 palabras por corpus, más c-TF-IDF entre corpus (qué distingue a Antonia de Tomás y del común).
- Embeddings: paraphrase-multilingual-MiniLM-L12-v2 (local).
- Clusters de concepto: UMAP (o PCA si UMAP no está) + HDBSCAN, con KMeans como comparación. Elige k por silhouette; estabilidad con bootstrap (100 remuestreos, Jaccard por cluster). Estabilidad < 0,6 = inestable; no sostiene pilar por sí solo.
- Nombre de cada cluster: KeyBERT (o las 5 palabras de c-TF-IDF) + 2 verbatims representativos (≤15 palabras, con row_id).
- Polaridad: conceptos de promotores (lo que valoran) vs de dolores (lo que temen).
- Red de co-ocurrencia: conceptos juntos en el mismo texto (PMI o conteo con umbral).
- Salidas: research/v5_nube/conceptos_antonia.csv y conceptos_tomas.csv (columnas: concepto, peso, cluster, polaridad, n_textos, estabilidad, ejemplo_row_id, etiqueta); research/v5_nube/NUBE_CONCEPTOS.html (autocontenido, dos pestañas: nube por tamaño de peso y color de polaridad, grafo de co-ocurrencia, tabla de clusters; colores #212c35 valor, #fda902 dolor, #6bc1e9 intención); research/v5_nube/METODO.md (camino paso a paso, comandos, limitaciones: n chico, encuesta solo a quienes compraron, sesgo de respuesta, asignación por regla).
- Auditoría del modelo: pasa el resultado por las skills detector-de-ruido y abogado-del-diablo (ángulos: datos vs narrativa, variable omitida). Lo que no resista queda [HIPÓTESIS].

## Fase 2 — De la nube a la estrategia (una por persona, en paralelo)
Cada subagente trabaja solo con su CSV, su perfil y la investigación.
- 2.1 Pilares: skills content-strategy y social-media-skills:content-pillars. 3 a 5 pilares por persona: nombre, para qué sirve, cluster de origen con peso, dolor que resuelve, tipo (marca / educación / producto / coyuntura / héroe / keep), % sugerido de la parrilla. Pilar sin cluster estable = [HIPÓTESIS].
- 2.2 Verticales: ejes temáticos que cruzan pilares; por vertical: pilares que alimenta, etapa del funnel (TOFU/MOFU/BOFU), canal principal, intención de búsqueda que cubre.
- 2.3 Territorios creativos y creatividades: skills social-media-skills:idea-generation-and-ideation, social-media-skills:hook-writer y copys-americar-usados. Por persona: 3 territorios (idea madre, tensión que resuelve, concepto de origen) y 3 creatividades por territorio (hook, copy corto, CTA, formato). Arquetipo de marca: El Acompañante; Antonia: "te atendemos como siempre"; Tomás: "lo publicado es lo que firmas".
- 2.4 Esquemas por formato: social-media-skills:carousel-writer, reels-script, story-writer. Por persona: carrusel slide por slide, reel 15–30 s escena por escena con texto en pantalla, historia con sticker, post de Google Business Profile y bloque de landing por comuna (S3 del plan).
- 2.5 Parrilla de 4 semanas: social-media-skills:content-calendar y batch-content-plan. Alineada a S1–S4 de research/10_plan_premium.md. Columnas: semana, fecha, canal, persona, pilar, vertical, etapa, formato, hook, copy, CTA, concepto de origen, etiqueta, estado. Máximo 30 % promocional. Salida: entregables/v5_contenido/PARRILLA_4_SEMANAS.csv.
- 2.6 Briefs (opcional): skill brief-diseno-americar, solo para las 3 piezas prioritarias de S1, en texto plano. No crear subtarea en Asana: dejarla en archivo y preguntar.

## Fase 3 — Auditoría (red-team)
Skills verificador-datos (copys) y abogado-del-diablo (estrategia: pre-mortem y ejecución). Revisar: cada pilar y creatividad apunta a un concepto con dato; sin "usado", promesas legales ni cifras internas en piezas públicas; Antonia y Tomás no terminan con la misma estrategia con distinto nombre. Salida: entregables/v5_contenido/AUDITORIA_V5.md.

## Entregables
En entregables/v5_contenido/: ESTRATEGIA_ANTONIA.md, ESTRATEGIA_TOMAS_PASCUAL.md, PARRILLA_4_SEMANAS.csv, BRIEFS_S1.md (si 2.6), AUDITORIA_V5.md. En research/v5_nube/: los CSV, NUBE_CONCEPTOS.html y METODO.md.
Si hay herramienta de artifacts, publicar NUBE_CONCEPTOS.html como artifact nuevo: "Nube de conceptos · Antonia y Tomás Pascual · USO INTERNO". Si no, dejarlo en la carpeta.

## Cierre (consola)
n de cada corpus y si el análisis es confirmatorio o exploratorio; 5 conceptos más fuertes por persona (peso, estabilidad, verbatim); pilares por persona y su cluster de origen; lo que el auditor bajó a hipótesis; bloqueos con responsable; comandos exactos para re-ejecutar.
Si una fase falla, reportar el error real y seguir con lo posible. No rellenar huecos.
