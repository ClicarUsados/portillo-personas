# Estrategia de contenido · Antonia (seminuevos premium, zona oriente)

USO INTERNO · 2026-11-24 · Borrador para Beto. No publicado. Sin tareas en Asana, sin commit, sin piezas enviadas a redes.
Contiene referencias a verbatims de clientes: no pegar en piezas públicas.

Etiquetas: [DATO] (archivo, columna/filtro, n, row_id) · [PLAN] (pág. de research/10_plan_premium.md) · [WEB] (URL, research/14 y 15) · [ILUSTRATIVO] · [HIPÓTESIS] · NO VERIFICADO · [BLOQUEO] (con responsable).

---

## 0. Estado de la evidencia (leer primero)

- **Análisis exploratorio.** Antonia tiene n = 31 textos (METODO §2). Cuatro clusters: A0 0,68 · A1 0,16 · A2 0,59 · A3 0,55 (conceptos_antonia.csv; resumen_ejecucion.json).
- **Regla aplicada:** un pilar solo queda como [DATO] si su cluster de origen tiene estabilidad ≥ 0,6. Con ese criterio:
  - El concepto central "atención" (peso 100) está en A2 con 0,59: por debajo del umbral. Su pilar es [HIPÓTESIS].
  - A0 (0,68) es el único cluster sobre el umbral. Su concepto principal, "excelente", aparece en 6 textos y es un elogio genérico. Tampoco alcanza para [DATO] sin validación.
  - El pilar de entrega se apoya en el cluster D1 del corpus de dolor (0,87). Ese corpus es del grupo, no de Antonia. Por eso queda como [DATO] en el cluster y [HIPÓTESIS] en el vínculo con Antonia.
- **Resultado:** de 4 pilares, 1 tiene cluster estable (entrega, D1) y el vínculo con Antonia es [HIPÓTESIS]. Los otros 3 son [HIPÓTESIS].
- **Asignación a persona** (ya soy cliente / recomendación / parte de pago → Antonia): [HIPÓTESIS], regla propia (METODO §2). Todo lo que depende de ella queda con esa etiqueta.
- **Antonia y Tomás comparten casi todos sus conceptos de valor** (METODO §7). La diferencia de esta estrategia está en tasación (P2) y en regreso (P4), y ambas son [HIPÓTESIS]. Fase 3 debe confirmar que no termina igual que la de Tomás. Este subagente no leyó conceptos_tomas.csv, por la regla de aislamiento.
- **Skills:** las skills del listado (content-pillars, hook-writer, carousel-writer, reels-script, content-calendar, etc.) están disponibles y no las invoqué. Apliqué sus criterios según PROMPT_v5 y METODO. Si Beto quiere la pasada con cada skill, se corre aparte.
- **Ficha de Antonia (PERFIL_ANTONIA_cliente_ideal.html):** según PROMPT_v5 es el perfil de Javiera renombrado. Pendiente confirmar. Sus cifras no se usan en piezas:
  - La ficha usa 60 promotores de la zona oriente. METODO usa 31 textos de Antonia y research/11 usa 95 promotores de la campaña. Son universos distintos.
  - "60 de 60 volverían" (ficha) contrasta con "94 de 95" (research/11 §3, regla A). Ambas cifras van lado a lado y ninguna entra en piezas.
  - El nombre, la edad, la imagen y el estilo de Antonia son [ILUSTRATIVO].

---

## 1. Pilares (2.1)

| # | Pilar | Para qué sirve | Cluster de origen (peso, estabilidad) | Dolor que resuelve | Tipo | % sugerido | Etiqueta |
|---|---|---|---|---|---|---|---|
| P1 | **Como siempre** | Sostener la relación de quien ya fue bien atendido y dar el mismo trato a quien llega por recomendación | A2 "atención" (100; 0,59). A0 "excelente" (51; 0,68; n = 6) | Que la atención se prometa y no se cumpla. Riesgo real: "no se cumple en su totalidad lo que ofrece la persona que te atiende" (CR_2025-Venta-Usados#3904, matiz de promotor) | marca / keep | 30 % | [HIPÓTESIS]. Contexto [DATO] de research/11 §2: atención es el motivo del 53,7 % de promotores de la campaña (n = 95, regla A). No es Antonia. |
| P2 | **Tu auto, tasado sin sorpresas** | Explicar cómo se tasa el auto en parte de pago antes de que la persona llegue con él | Ninguno en la nube de Antonia. Tasación no aparece como concepto | Tasación que no coincide con la web: 42 de 106 detractores del grupo que aplican (39,6 %) [DATO research/12 D4]. Portillo: 1 de 2. Verbatim del grupo: "Los valores ofrecidos en la página web por vehículos en parte de pago no son" (CR_2025-Venta-Usados#2256) | educación / producto | 25 % | [HIPÓTESIS]. Parte de pago aplica a 40 de 95 promotores (42 %, research/11 §3, regla A). Ese dato depende de la regla de asignación. |
| P3 | **Entrega con fecha, papeles y auto listo** | Que la entrega sea una experiencia cumplida y no la parte que se recuerda mal | D1 "entregar / entrega / información" (vehículo 88, entregar 56, entrega 45; **0,87**). Corpus de dolor del grupo (n = 729) | Entrega sin fecha o con papeles pendientes: 77,3 % de detractores del grupo (base 313) [DATO research/12 P1]. En Portillo, 5 de 10. Verbatim de Portillo: "al entregarme no enciende porque se descargo la batería" (CR_2025-Venta-Usados#3477) | producto / postventa | 25 % | [DATO] cluster estable (grupo). Vínculo con Antonia: [HIPÓTESIS]. **Caveat:** "vehículo" puede venir de la pregunta de parte de pago. Revisarlo antes de usar el cluster como dolor de entrega. |
| P4 | **Vuelve y recomienda** | Convertir la compra en regreso y en recomendación, con el canal de la sucursal | Ninguno en la nube de Antonia | Que nadie la invite a reseñar, y que la reseña de Portillo siga en 3,0 ★ frente a 4,7–5,0 ★ de boutiques vecinas [PLAN p.05, NO VERIFICADO de forma independiente] | keep | 20 % | [HIPÓTESIS]. "Volvería a comprar" (94 de 95, research/11 §3) es [DATO] de la campaña, no de Antonia. |

Nota de asignación: 16 filas de la parrilla se reparten 4 / 5 / 4 / 3 (P1 / P2 / P3 / P4). Eso da 25 / 31 / 25 / 19 %. Las desviaciones frente al % sugerido se corrigen en la semana 2, cuando haya más piezas publicadas.

---

## 2. Verticales (2.2)

| Vertical | Pilares que alimenta | Etapa | Canal principal | Intención de búsqueda que cubre |
|---|---|---|---|---|
| **V1 Mi auto de hoy** (tasación y parte de pago) | P2, P1 | MOFU / BOFU | Landing premium con bloque de tasación; Google Business Profile | "tasación de mi auto para parte de pago" (research/15 §3, ejemplo redactado, sin volumen). Hay consultas de este tipo en [WEB] (The Clinic, research/15 §3). Portillo no aparece en orgánico en 0 de 8 búsquedas [PLAN p.02]; las 8 no están listadas: NO VERIFICADO |
| **V2 Familia en SUV** (espacio para colegio y viajes) | P1, P3 | TOFU | Reels en Instagram [NO VERIFICADO: cuenta y alcance]; fichas de Google | "seminuevos Vitacura", "autos usados inspeccionados Vitacura" (research/15 §2, [WEB] de búsqueda, 2026-11-23). **Decisión pendiente:** la gente busca "usados" y las piezas dicen "seminuevo". Los términos de búsqueda sí pueden aparecer en título y meta, si Beto lo autoriza |
| **V3 Sucursal de siempre** (entrega, regreso, reseña) | P3, P4, P1 | BOFU / retención | Google Business Profile; historias; QR de reseña en entrega [PLAN p.05] | "Portillo seminuevos Las Condes" / "Vitacura" (research/15 §3, [WEB] avisos Chileautos); "reseñas Portillo Google" |

---

## 3. Territorios y creatividades (2.3)

**Arquetipo:** El Acompañante (propuesto en research/11 y ficha; [HIPÓTESIS]). **Énfasis de Antonia:** "te atendemos como siempre".

**Límites de copy (aplican a todo):**
- Nunca "usado" en piezas. Usar "seminuevo".
- Sin "garantía de excelencia", "satisfacción garantizada", "precio líder", "oferta imperdible", "garantía total", "cobertura mecánica hasta 12 meses" ni cifras de inspección.
- Sin cifras internas (NPS, n, CRM, stock, margen).
- Garantía: solo con condiciones escritas, validadas. Ver bloqueo B-4.
- Ningún incentivo por reseñas. Google no lo permite, y la invitación debe ser abierta.
- Palabras bandera (ficha, [HIPÓTESIS]): cercano, claro, respaldo. Evitar "impecable" y "a tiempo" hasta tener el proceso verificado.

### T1 · "Ya nos conoces"
- **Idea madre:** la relación de regreso. Quien ya fue bien atendido vuelve con confianza.
- **Tensión que resuelve:** poco tiempo para visitar varias automotoras. La ficha lo expresa como "No tengo tiempo para recorrer diez automotoras" ([ILUSTRATIVO]).
- **Concepto de origen:** "atención" (A2, 0,59). **[HIPÓTESIS].**

| # | Hook | Copy corto | CTA | Formato |
|---|---|---|---|---|
| T1.1 | "Ya nos conoces." | "Si ya te atendimos bien, vuelve. Te atendemos como siempre." | Visita tu sucursal de siempre | Post Google Business Profile |
| T1.2 | "¿Quién te recomendó Portillo?" | "Cuéntanos quién te trajo y te respondemos." | Responde el sticker | Historia con sticker de pregunta |
| T1.3 | "Te atendemos como siempre." | "Si ya nos visitaste, sabes cómo te recibimos. Si es tu primera vez, te explicamos todo." | Escríbenos o visita tu sucursal | Carrusel de 4 slides (o post único) |

### T2 · "Tu tasación, explicada"
- **Idea madre:** tasar tu auto es un proceso que se entiende antes de llegar.
- **Tensión que resuelve:** la cifra de la web y la de la sucursal no coinciden. Dolor del grupo, 39,6 % de los que aplican.
- **Concepto de origen:** sin cluster en Antonia. Dolor de [DATO] del grupo (research/12 D4). **[HIPÓTESIS].**
- **Bloqueo B-1:** el proceso de tasación (criterios, qué cambia la cifra, plazos) no está documentado. Ninguna pieza de T2 sale sin él.

| # | Hook | Copy corto | CTA | Formato |
|---|---|---|---|---|
| T2.1 | "Tu auto vale algo. Te mostramos cómo se calcula." | "Cómo tasamos tu auto en parte de pago, paso a paso." | Agenda tu tasación | Carrusel de 7 slides (esquema 4.1) |
| T2.2 | "¿Te dieron una cifra y no entendiste de dónde salió?" | "Te explicamos de dónde sale la cifra de tu tasación, antes de firmar." | Pregunta por tu tasación | Reel de 25 s |
| T2.3 | "¿Sabes cuánto vale tu auto hoy?" | "Te explicamos cómo se calcula, paso a paso." | Vota y te mostramos cómo | Historia con encuesta |

### T3 · "La fecha que cumplimos"
- **Idea madre:** la entrega es lo que la gente recuerda. Llegar con fecha y papeles es lo que se valora.
- **Tensión que resuelve:** entrega sin fecha o con documentos pendientes. 77,3 % de los detractores del grupo.
- **Concepto de origen:** entrega (D1, 0,87). **[DATO] cluster estable; vínculo con Antonia [HIPÓTESIS].**
- **Bloqueo B-2:** "fecha de entrega confirmada por escrito" depende de un proceso que no está verificado. Hasta confirmarlo, las piezas quedan en borrador.

| # | Hook | Copy corto | CTA | Formato |
|---|---|---|---|---|
| T3.1 | "Tu auto, tu fecha, tus papeles." | "Entrega con fecha confirmada por escrito, con los papeles listos." | Pregunta tu fecha de entrega | Reel de 20 s |
| T3.2 | "Te confirmamos la fecha antes de firmar." | "Pregunta tu fecha de entrega en tu sucursal de siempre." | Pregunta por tu fecha | Post Google Business Profile (esquema 4.4) |
| T3.3 | "Qué recibes el día que retiras tu auto." | "Kit de entrega: qué incluye y cómo te lo entregamos." | Guárdalo para tu entrega | Carrusel de 5 slides |

---

## 4. Esquemas por formato (2.4)

### 4.1 Carrusel · T2.1 "Cómo tasamos tu auto en parte de pago" (7 slides)
1. **Hook:** "Tu auto vale algo. Te mostramos cómo se calcula."
2. **Qué es el parte de pago:** "Tu auto cuenta como parte del pago de otro. Así se usa." (texto plano, sin cifras)
3. **Qué miramos:** "[CRITERIOS DE TASACIÓN: BLOQUEO B-1, Beto / Iván Balaguera]"
4. **Por qué la cifra cambia:** "[CONDICIÓN DEL AUTO, DOCUMENTOS: BLOQUEO B-1]"
5. **Qué pasa después:** "Tasación, firma y entrega. Tasamos el fin de semana [PLAN p.05]."
6. **Lo que queda por escrito:** "[A CONFIRMAR: BLOQUEO B-1 y B-4]"
7. **CTA:** "Agenda tu tasación en tu sucursal de siempre."

Caption: sin cifras, sin "garantía", sin "usado". Publicar solo cuando los slides 3, 4 y 6 estén completos.

### 4.2 Reel · 20 s · V2 "Familia en SUV" (hook de T1 con ángulo de familia)
| Tiempo | Escena | Texto en pantalla | Audio |
|---|---|---|---|
| 0–3 s | Familia frente a un SUV, plano abierto | "Tu familia creció." | Música suave |
| 3–6 s | Plano corto: mano sobre el capó del SUV | "Tu auto tiene que alcanzar." | Sin voz |
| 6–12 s | Clienta conversa con asesora en sala, plano medio | "Te atendemos como siempre." | Voz natural, sin nombres |
| 12–16 s | Maletero abierto con espacio para colegio y viajes | "Ficha con precio y cuota." | Sonido ambiente |
| 16–20 s | Logo y CTA | "Visita tu sucursal de siempre." | Cierre musical |

Producción: personas reales con consentimiento escrito. No usar las imágenes generadas con IA de la ficha: son ficticias y [ILUSTRATIVO].

### 4.3 Historias con sticker
- **T1.2 (pregunta):** sticker "¿Quién te recomendó Portillo?". Respuesta automática: "Gracias. Te respondemos por el mismo canal."
- **T2.3 (encuesta):** "¿Sabes cuánto vale tu auto hoy?" Sí / No. Respuesta: "Te explicamos cómo se calcula. Toca para ver." Enlace a T2.1 cuando esté desbloqueado.

### 4.4 Post de Google Business Profile · T3.2 (texto completo)
> Tu entrega, con fecha. Te confirmamos la fecha de entrega por escrito antes de firmar, y te explicamos qué papeles recibes. Pregunta por tu fecha en tu sucursal de siempre.

Botón: "Llamar" o "Cómo llegar" a la sucursal. **Bloqueo B-2**: no publicar hasta confirmar que la fecha se entrega por escrito.

### 4.5 Bloques de landing por comuna (S3)
**Bloque A · Lo Barnechea y La Dehesa** (row 9 de la parrilla)
- H2: "Tu auto en parte de pago, tasado en tu sucursal de siempre."
- Bajada: "Tasamos el fin de semana y te explicamos cada paso."
- Tres puntos: "Te explicamos de dónde sale la cifra" · "Agenda tu tasación" · "[Inspección agendada al cotizar: PLAN p.05, confirmar]"
- CTA: "Agenda tu tasación."
- Nota: en la búsqueda de La Dehesa no hubo consultas verificadas (research/15 §2, NO VERIFICADO). Medir antes de escalar.

**Bloque B · Vitacura y Padre Hurtado** (row 12)
- H2: "Ya nos conoces: te atendemos como siempre."
- Bajada: "Tu sucursal de siempre te recibe igual que la primera vez."
- Tres puntos: "Tasación explicada" · "Entrega con fecha confirmada [BLOQUEO B-2]" · "Visita sin compromiso [A CONFIRMAR]"
- CTA: "Agenda tu visita."
- Nota: el mapeo entre las sucursales del plan y las de la base no está verificado (B-3).

---

## 5. Parrilla de 4 semanas (2.5)

Archivo: `entregables/v5_contenido/PARRILLA_ANTONIA.csv`. Solo filas de Antonia; el CSV combinado lo arma el otro proceso.

- **16 filas**, cuatro por semana. Las fechas siguen S1–S4 de research/10_plan_premium.md [PLAN p.02]. S1 empieza hoy, 24-nov (el plan dice 23–29 nov).
- **0 de 16 filas son promocionales (0 %, tope 30 %).** No hay ofertas de precio en esta parrilla.
- **Estado:** 8 en borrador y 8 bloqueadas (filas 3, 6, 8, 9, 10, 12, 13 y 14). Nada está publicado.
- **Canales:** Google Business Profile, Instagram (cuenta y alcance: NO VERIFICADO) y landing premium.

Bloqueos de la parrilla:

| ID | Bloqueo | Responsable | Afecta |
|---|---|---|---|
| B-1 | Proceso y criterios de tasación de parte de pago | Beto / Iván Balaguera | T2, bloque A, filas 6, 8, 9, 10 |
| B-2 | Fecha de entrega confirmada por escrito y kit de entrega | Beto / Iván Balaguera | T3, filas 3, 13, 14 y post de 4.4 |
| B-3 | Mapeo de sucursales del plan (p.06) a las de la base | Beto / Iván Balaguera | Bloque B, fila 12 |
| B-4 | Condiciones de garantía por escrito (la web dice 3 meses; el plan también; Kavak está en contradicción: 7 días / 300 km en su web vs. 12 meses en el plan, research/14) | Beto + área legal de Americar (responsable NO VERIFICADO) | Cualquier mención de garantía |
| B-5 | Cuenta de Instagram de Portillo Seminuevos, alcance y formatos | Beto | Canal Instagram de todas las filas |
| B-6 | Decidir si los términos de búsqueda "usados" van en título y meta | Beto | V2, SEO |
| B-7 | Confirmar que Antonia es el perfil de Javiera renombrado; reconciliar 60 vs. 31 vs. 95 | Beto | Toda la estrategia de Antonia |
| B-8 | Diccionario de "Vehículo en parte de pago" (valores 1–5) | Beto / CRM | P2 y la regla de asignación |
| B-9 | Autorizar publicar NUBE_CONCEPTOS (tiene verbatims) | Beto | Artifact de la nube |

---

## 6. Qué no hice, y por qué

- **No publiqué** ningún artifact con esta estrategia. Contiene verbatims de clientes, y PROMPT_v5 pide que los verbatims no salgan de la máquina. Si Beto quiere un artifact, debe autorizarlo y decidir qué se muestra (B-9).
- **No abrí inputs_raw/.** No re-verifiqué los row_id contra inputs_clean/: los tomé de METODO, de la ficha y de research/11 y 12. Antes de publicar cualquier verbatim, hay que verificarlos.
- **No leí conceptos_tomas.csv ni NUBE_CONCEPTOS.html**, por la regla de aislamiento.
- **No invoqué las skills** listadas (ver §0).
- **No creé tareas en Asana, no hice commit y no publiqué en redes.**
