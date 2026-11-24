# PROMPT v6 — Universo de puntos de contacto con ML (Antonia y Tomás Pascual)
Copia de trabajo del prompt pegado el 2026-11-24. Esto es generación de HIPÓTESIS, no evidencia: todo lo que salga del modelo va [HIPÓTESIS-ML] hasta validarse.

## Objetivo
Generar un universo ordenado de hipótesis de puntos de contacto (intereses, actividades, lugares, momentos, medios y comunidades) para cada persona, rankearlos, proponer cómo validarlos y bajarlos a un calendario por punto de contacto y mes. Quien lo lee es Beto (Brand Digital, Americar Usados), que lo usa en su Magíster: explicar cada algoritmo, por qué se eligió y cómo reproducirlo.

## Insumos
- Perfiles: entregables/cliente_ideal/PERFIL_ANTONIA_cliente_ideal.html (Javiera renombrada, por confirmar) y PERFIL_TOMAS_PASCUAL_cliente_ideal.html.
- Conceptos: research/v5_nube/conceptos_antonia.csv y conceptos_tomas.csv.
- Contexto: research/10_plan_premium.md, 13_comunas_web.md, 14_competencia_premium.md, 15_busqueda_premium.md.
- Datos: solo inputs_clean/. NUNCA abras inputs_raw/.

## Reglas
- Etiquetas: [DATO], [PLAN], [WEB] (URL y fecha), [ILUSTRATIVO], [HIPÓTESIS-ML]. Ningún punto de contacto se presenta como hecho sin validación.
- Privacidad: verbatims fuera de APIs externas; embeddings con modelos locales (sentence-transformers).
- Control de estereotipos: género y comuna NO son variables del modelo (ver Fase 4).
- Marca: "seminuevo", nunca "usado". Sin promesas de garantía, plazos ni ganchos sin respaldo legal. Piezas públicas sin cifras internas.
- No afirmes conversión lead→venta.
- Nada irreversible: sin git commit, sin tocar inputs_raw/, sin crear campañas, audiencias ni tareas en Asana/Meta/GA4/Google.
- Bloqueos con responsable.

## Fase 0 — Semillas
research/v6_contacto/semillas_{persona}.csv: conceptos del v5 con su peso; rasgos del perfil (uso del auto, detonante, cómo llega, qué valora, qué teme); contexto de movilidad y hogares de la comuna desde 13_comunas_web.md [WEB]. Excluye género y nombre. La comuna entra solo como contexto de movilidad y entorno.

## Fase 1 — Universo de candidatos
Taxonomías públicas con URL: IAB Content Taxonomy 3.x; categorías de afinidad y de público en el mercado de Google Ads; lista pública de intereses de Meta Ads (si no hay, NO VERIFICADO). Candidatos locales [WEB] con URL: deportes y actividades de Santiago oriente (trekking cajón del Maipo, esquí Valle Nevado o Farellones, ciclismo urbano, running parque Bicentenario, pádel), escapadas (costa central, sur), momentos (verano, invierno, Fiestas Patrias, vuelta a clases) y medios (radios, podcasts, newsletters, cuentas locales). No inventar.
Salida: research/v6_contacto/universo_candidatos.csv con columnas id, nombre, categoria, subcategoria, tipo (interes|actividad|lugar|momento|medio|comunidad), fuente, url.

## Fase 2 — Modelos de afinidad (cuatro métodos independientes)
Script: analisis/v6_contacto/01_afinidad.py.
1. Similitud semántica: paraphrase-multilingual-MiniLM-L12-v2. Persona = promedio ponderado de semillas; candidato = nombre + descripción. Score = coseno.
2. Zero-shot NLI: modelo multilingüe local (p. ej. MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7). Hipótesis: "A esta persona le interesa {candidato}" sobre un resumen de semillas. Score = probabilidad de entailment.
3. Grafo: nodos = semillas y candidatos; aristas = similitud sobre umbral y jerarquía de la taxonomía. PageRank personalizado desde las semillas de cada persona (candidatos a dos o tres saltos).
4. Filtro colaborativo (opcional): solo con un dataset público confiable de co-ocurrencia de intereses; si no existe, saltarlo y decirlo. No fabricar datos.
Ensamble: rank percentil y Reciprocal Rank Fusion. Correlación de Kendall entre métodos. "Robusto" = top 20 % en al menos 3 de 4 métodos.
Estabilidad: bootstrap de semillas, 100 remuestreos. Puesto que varía más de 30 lugares = inestable.
Salida: research/v6_contacto/ranking_{persona}.csv (candidato, tipo, score_emb, score_nli, score_ppr, score_cf, score_final, robusto, estable, semillas_que_lo_explican).

## Fase 3 — Explicar y agrupar
- Explicabilidad: para el top 30, semillas que más pesan y la ruta del grafo.
- Clustering del top 50 (embeddings + HDBSCAN) en territorios de vida (familia y escapadas, ciudad a pie, bienestar, diseño y casa...). Nombre con c-TF-IDF.
- Diferencial: territorios propios de Antonia, de Tomás y compartidos.
- research/v6_contacto/UNIVERSO_CONTACTO.html: autocontenido, dos pestañas; mapa 2D (UMAP) coloreado por territorio, tamaño = score final, borde = robustez; grafo persona → top 20; tabla filtrable. Colores #212c35, #0082d1, #6bc1e9, #fda902.

## Fase 4 — Sesgo y solidez
- Contrafactual de estereotipos: volver a correr el ensamble agregando solo "mujer" (Antonia) o "hombre" (Tomás), y luego intercambiarlos. Si un candidato sube o baja más de 20 puestos solo por ese cambio: sacarlo del top y listarlo en research/v6_contacto/SESGOS.md. Igual con la comuna (La Dehesa ↔ Providencia).
- Revisar el ranking con las skills detector-de-ruido y abogado-del-diablo (si no responden, aplicar sus criterios y decirlo).
- Lista de candidatos con respaldo [WEB] de contexto chileno vs solo similitud semántica.

## Fase 5 — Plan de validación
Para el top 15 de cada persona, cómo pasar de [HIPÓTESIS-ML] a [DATO]:
- Encuesta corta a compradores de sucursales de la zona oriente: 3 preguntas de selección múltiple y análisis posterior (FP-Growth con soporte, confianza y lift).
- GA4 (intereses de visitantes de la landing premium) y Meta Ads (tamaño de audiencia por interés en comunas de la zona): qué reporte y cómo calcular el índice de afinidad. No ejecutar ni crear nada en esas plataformas.
- Google Trends por región: términos y estacionalidad esperada.
- Criterio de validación: por ejemplo, lift > 1,2 con n ≥ 30.
Salida: entregables/v6_contacto/PLAN_VALIDACION.md.

## Fase 6 — Calendario por punto de contacto
Skills: social-media-skills:seasonal-and-moment-marketing, content-calendar, idea-generation-and-ideation.
- Matriz punto de contacto × mes (diciembre 2026 a noviembre 2027). Estacionalidad de Chile con fuente [WEB] (esquí junio a agosto, playa enero y febrero, Fiestas Patrias septiembre, vacaciones de invierno julio, vuelta a clases marzo).
- Para meses de mayor calce: ideas donde el auto acompaña la vida de la persona (el punto de contacto es el contexto; el seminuevo resuelve). Cada idea: persona, territorio, pilar, etapa del funnel, formato, canal y la hipótesis que la sostiene.
- Marcar qué ideas se pueden lanzar como prueba chica A/B por interés y cuáles esperan validación.
Salida: entregables/v6_contacto/CALENDARIO_PUNTOS_DE_CONTACTO.csv y entregables/v6_contacto/PLAN_PUNTOS_DE_CONTACTO.md.

## Entregables
- research/v6_contacto/: universo_candidatos.csv, ranking_antonia.csv, ranking_tomas.csv, UNIVERSO_CONTACTO.html, SESGOS.md, METODO.md (cada algoritmo explicado, por qué, supuestos y cómo re-ejecutarlo).
- entregables/v6_contacto/: PLAN_PUNTOS_DE_CONTACTO.md, CALENDARIO_PUNTOS_DE_CONTACTO.csv, PLAN_VALIDACION.md.
- Artifact de UNIVERSO_CONTACTO.html: NO publicar sin autorización de Beto (contiene verbatims derivados y el método interno).

## Cierre (consola)
Tamaño del universo y sus fuentes; top 10 de cada persona con score final, robustez, estabilidad y semillas que lo explican; territorios propios y compartidos; candidatos eliminados por sesgo; 3 hipótesis a validar primero y cómo; comandos para re-ejecutar.
Si un método falla (modelo que no descarga, taxonomía no encontrada), reportar el error real y seguir con los que funcionen. No rellenar huecos.
