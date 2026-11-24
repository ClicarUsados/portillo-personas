# Buyer personas Portillo — miedo dominante de compra (versión 2, corregida)

**Fecha de corte de los datos:** 2026-11-23 (extracción de `inputs_clean/*.parquet`).
**Clasificación:** USO INTERNO. Contiene cifras de CRM (encuestas post-venta, leads, servicio técnico). **No es publicable.**
**Estado:** borrador para Beto y jefatura. La asignación a Portillo sigue **BLOQUEADA** (depende de Beto / Iván Balaguera).

---

## 0. Qué cambió respecto de la versión 1 (2026-11-23)

Reglas de decisión tomadas por la coordinación, aplicadas aquí:

1. **Recuento de evidencia.** El denominador son solo las afirmaciones con etiqueta ([DATO], [WEB], [HIPÓTESIS]). NO VERIFICADO queda fuera y se cuenta aparte. El conteo lo hace `analisis/6F_recuentos_correccion.py` sobre las secciones de evidencia (Ficha a Journey). Las bajadas de comunicación y las tarjetas quedan fuera del conteo.
2. **Retención de P2.** Se quitó el 61,7 % de Usados. Era de otra población (`Proceso de Entrega`, Venta-Usados).
3. **P1 (leads).** Fecha de corte 2026-01-23, declarada como antigua (casi 10 meses). El "sin respuesta" (54 de 138) pasa a [HIPÓTESIS], con nota: codificación por palabras clave no validada. Al quedar sin miedo dominante con [DATO], **P1 se descarta como persona** (ver sección 2).
4. **P4.** El miedo "lo que no se ve" se reescribe. Los verbatims de "Condición del vehículo" apuntan a terminación posterior a la entrega, no a información oculta antes de comprar. El miedo a la tasación pasa a [HIPÓTESIS].
5. **P3.** Universo Portillo recalculado excluyendo PORTILLOLA y PORTILLOTALCA (marcadas como dudosas). La distribución de notas (72,6 % en 0 o 10) se muestra junto al NPS 73,5.
6. **Cifras.** Solo se usan cifras que reproduce un script de `analisis/`. Ver sección 8.4 para el estado de cada una.

**Resultado:** **3 personas** (antes 4). P2, P3 y P4 se mantienen con evidencia corregida. P1 se descarta.

Correspondencia con la auditoría: la lista de correcciones está en `entregables/AUDITORIA_Y_BRECHAS.md`, sección h (no hay una sección con ese título exacto). Los puntos 1 a 9 de h se atienden aquí. Los incidentes de proceso de la sección 0 de esa auditoría **siguen abiertos** y no se resuelven en este documento.

---

## 1. Convenciones

**Etiquetas**
- **[DATO]**: archivo + columna + filtro + extracción 2026-11-23. Cifra reproducida por un script de `analisis/`.
- **[WEB]**: URL + fecha de consulta 2026-11-23 (`research/05_mercado_externo_web.md`).
- **[HIPÓTESIS]**: inferencia o codificación propia, a validar.
- **NO VERIFICADO**: no hay dato en las fuentes. No se rellena.
- **BLOQUEADO**: depende de una decisión o archivo de una persona nombrada.

**Universos**
- **GRUPO_COMPLETO**: todas las filas del archivo, sin asignar a Portillo.
- **PORTILLO_HIPOTESIS**: filas que el mapeo asigna a Portillo. Bloqueado: depende de Beto / Iván Balaguera. Se muestran varias reglas (ver sección 8.4).

**Restricciones que este documento respeta**
- Leads y compradores se describen por separado. **No hay clave verificada lead→venta**: no hay tasa de conversión ni de cierre.
- Sin PII. Citas textuales de 15 palabras o menos, identificadas por row_id.
- Premium: "seminuevo", nunca "usado", en contenido de marca. "Usados" aparece solo como nombre de archivo o categoría del CRM.
- No se afirma ninguna garantía, plazo ni cobertura de inspección sin respaldo legal u operativo.

**Demografía.** La única fuente demográfica es la encuesta de seguridad vial: n=709, solo clientes de autos nuevos, 2025-10-22 a 2025-10-29 [DATO]. No representa a los compradores de seminuevos y no se cruza con ninguna persona (ver sección 7).

---

## 2. Por qué 3 personas y no 4 (descarte de P1)

**P1 "el cotizador que espera" se descarta como persona.** Motivo: no tiene un miedo dominante sostenido por [DATO].

Lo que sí dicen los datos de leads (Lead-Portillo, n=1.003, GRUPO_COMPLETO):
- Contactado por ventas: Sí 371, No 60; sin respuesta a la pregunta 572 [DATO].
- Evaluación del proceso de cotización: 1-2 en 17,1 % (n=1.003). **Dirección de la escala NO VERIFICADA**: no está en el diccionario [DATO, dirección NO VERIFICADA].
- Barreras explícitas (opciones marcadas, sobre 431 respondidos): 68, es decir 15,8 % [DATO].
- Entre quienes evaluaron 1-2 (n=172), 124 no respondieron la pregunta de contacto [DATO].
- "Sin respuesta o sin contacto" como motivo: 54 de 138 textos con evaluación 1-2 (39,1 %). **[HIPÓTESIS]**: codificación por palabras clave, precisión no validada.
- Fecha de corte: última respuesta 2026-01-23 [DATO]. Casi 10 meses antes de la extracción. Si es corte de exportación o falta de datos posteriores: **NO VERIFICADO**.

**Por qué no se fusiona con otra persona.** Fusionarla con P2, P3 o P4 importaría evidencia de compradores o clientes de taller a una población que no tiene clave común con ellos. Tampoco hay un miedo [DATO] que comparta con ellas.

**Qué pasa con su material.** El "sin respuesta" queda como hipótesis a validar (dos codificadores ciegos sobre 138 textos). La pregunta de contacto (C13) queda en la sección 8.4. La fecha de corte queda en la sección 8.1.

---

## 3. Persona P2 — El que ya pagó y espera su auto nuevo

### Ficha (Target + ICP)
- **Miedo dominante:** que el auto, ya pagado, no llegue en el plazo y con el trámite que se acordó.
- **Target:** comprador de vehículo nuevo que completó la compra y espera la entrega.
- **ICP:** cliente de Venta-Nuevo (6.458 filas, GRUPO_COMPLETO). Persona natural: 88,4 % (5.711 de 6.458) [DATO].
- **Universo:** GRUPO_COMPLETO. PORTILLO_HIPOTESIS (1.311 filas, 20,3 %) tiene 81 detractores [DATO del conteo; asignación [HIPÓTESIS], bloqueada].
- **Edad / género:** NO VERIFICADO para esta persona.
- **Ingreso, pie, modalidad, zona, quién decide:** NO VERIFICADO. La fuente de Venta-Nuevo no trae pie ni financiamiento de la compra.

### Detonante y contexto de uso
- Detonante: compra de vehículo nuevo con pago y trámite ya realizados [DATO, verbatim].
- Contexto: espera la entrega. La demora se vive como incumplimiento de lo pagado [HIPÓTESIS].

### Mapa de empatía
- **Piensa y siente** [HIPÓTESIS]: siente que cumplió su parte y no recibe lo comprometido.
- **Oye** [DATO]: "No es posible que se demoran tanto en entregar un auto nuevo ya pagado" — `CR_2025-Venta-Nuevo_#612`.
- **Ve** [DATO]: la etapa "Fluidez general del proceso" es la que más castiga la nota de detractores (1-2 en 58,0 %, 202 de 348).
- **Dice y hace** [DATO]: "ya va un mes y aun no me lo entregan" — `CR_2025-Venta-Nuevo_#445`.
- **Esfuerzos** [DATO]: el texto no dice cuántas consultas hace: NO VERIFICADO.
- **Miedos / objeciones** [DATO]: "Es demasiado el tiempo de entrega" — `CR_2025-Venta-Nuevo_#414`. Documentos: factura (22 de 348 detractores, 6,3 %) y permiso de circulación (17, 4,9 %).
- **Resultados / medida de éxito:** que el auto llegue en el plazo acordado con sus documentos. El plazo acordado: NO VERIFICADO.

### Journey (5 etapas)

| Etapa | Canal | Fricción | Evidencia |
|---|---|---|---|
| Interés | NO VERIFICADO (Venta-Nuevo no trae origen) | NO VERIFICADO | NO VERIFICADO |
| Consideración | Web (encuesta de funcionalidades, de clientes de campaña) | Comparar formas de pago es la prioridad top-1 (43,5 % de n=324) [DATO, otra población, sesgo de campaña] | [DATO] |
| Compra (crédito, tasación, cierre) | Ejecutivo de venta y trámite de pago | Plazos de entrega: 64 de 348 detractores (18,4 %). Tasa de detractores dentro del tema "Rapidez del proceso": 28,6 % (n=224) [DATO] | [DATO] |
| Retención (entrega, documentos) | Entrega física y documentos | Fluidez general con 1-2 en 58,0 % de detractores de Nuevo [DATO]. Documentación: tasa de detractores 47,0 % (n=83) [DATO]. Factura y permiso: 6,3 % y 4,9 % de detractores [DATO] | [DATO] |
| Advocacy | Recomendación | Promotores 88,8 % de Nuevo [DATO]. "Atención" es el motivo dominante de promotores (82,0 % de codificadas) [DATO] | [DATO] |

**Lectura.** La nota alta de los promotores viene de la atención (82 %). La demora pesa en quien tiene el auto pagado. Que la demora sea de la entrega física o de trámites de la compra no está resuelto: el texto exacto de la pregunta de fluidez es NO VERIFICADO [HIPÓTESIS sobre el nombre de la etapa].

### Bajada de comunicación
- **Arquetipo:** "el que ya pagó y espera".
- **Tono:** claro, respetuoso del tiempo ajeno, sin promesas de plazo no confirmadas.
- **Pilares:** (1) saber en qué punto va su auto; (2) documentos listos y explicados; (3) trato humano en la entrega.
- **TOFU** [HIPÓTESIS]: "Tu auto, paso a paso." Requiere un seguimiento de estado que no está confirmado: NO VERIFICADO.
- **MOFU** [HIPÓTESIS]: "Qué incluye tu entrega y qué documentos recibes."
- **BOFU** [HIPÓTESIS]: "Tu fecha de entrega y tu ejecutivo." Bloqueado hasta confirmar plazos internos (NO VERIFICADO; Beto / Iván Balaguera).
- **Contenidos que pide** (base Subagente D, traspasado como [HIPÓTESIS]): historial del vehículo y documentos, 89,8 % de acuerdo [DATO, encuesta web n=324, sesgo de campaña; escala con extremos NO VERIFICADOS].

### Tarjeta de evidencia (P2)
Ver sección 9 (conteo automático de `6F_recuentos_correccion.py`).

---

## 4. Persona P3 — El que vuelve al taller

### Ficha (Target + ICP)
- **Miedo dominante:** que la reparación no quede bien a la primera y que el costo final sea distinto al que se explicó.
- **Target:** cliente de servicio técnico (mecánica).
- **ICP:** cliente que llevó su vehículo a servicio. Marcas con más registros: TOYOTA 3.744, CHEVROLET 3.513, MG 2.140, NISSAN 1.983 [DATO, `des_marca`, GRUPO_COMPLETO]. Son 77 marcas en total [DATO].
- **Universo:** GRUPO_COMPLETO (27.516 filas) para todas las cifras generales.
- **Edad / género, ingreso, pie, modalidad, zona, quién decide:** NO VERIFICADO.

### Universo Portillo recalculado (regla 5)
Todas las cifras son [DATO] del conteo; la asignación a Portillo es [HIPÓTESIS] bloqueada (Beto / Iván Balaguera). Fuente: `6F_recuentos_correccion.py`, sección A.

| Universo (nombre_sucursal) | n | NPS | % detractores | % notas 0 o 10 |
|---|---:|---:|---:|---:|
| GRUPO_COMPLETO | 27.516 | 73,5 | 9,1 | 72,6 |
| PORT (regla original, `\bPORT`) | 245 | 68,2 | 11,4 | 72,7 |
| PORTILLO limpio (`\bPORTILLO\b`, excluye PORTILLOLA/TALCA) | 127 | 84,3 | 3,9 | 79,5 |

- Las 118 filas que salen son "PORTILLOLA FLORIDA SERVICIOS" (60) y "PORTILLOTALCA SERVICIOS" (58) [DATO del conteo]. **Marcadas como dudosas**: solo coinciden por prefijo y no están confirmadas como Portillo.
- Todo el universo limpio es "GAP PORTILLO SERVICIO" (127) [DATO].
- **Lectura:** la cifra de Portillo de la versión 1 (NPS 68,2) mezclaba la red de otras sucursales. Con el universo limpio, el NPS sube a 84,3. Ninguna de las dos cifras es de Portillo hasta confirmación.

### Distribución junto al NPS (regla 5)
GRUPO_COMPLETO [DATO, 03/3C]: 0 = 2,4 %; 1-3 = 2,7 %; 4-6 = 4,0 %; 7 = 2,9 %; 8 = 5,4 %; 9 = 12,4 %; 10 = 70,2 %. **NPS 73,5 con 72,6 % de notas en 0 o 10.** Un NPS alto con esa forma significa satisfechos o no, no necesariamente buen servicio.

### Detonante y contexto de uso
- Detonante: una falla o un mantenimiento que lleva el vehículo al taller. Motivo de ingreso: NO VERIFICADO (no hay campo).
- Contexto: vuelve si la primera reparación quedó bien; si no, la recompra se pierde [DATO, ver abajo].

### Mapa de empatía
- **Piensa y siente** [HIPÓTESIS]: desconfía de que le digan lo que se hizo realmente.
- **Oye** [DATO, verbatim]: "bajo nivel tecnico para solucionar fallas" — `CR_2025-Mecánica_202#4` (NPS 0). Lo opuesto en promotores: "La buena atención" — `CR_2025-Mecánica_202#10`.
- **Ve** [WEB]: reclamos públicos sobre calidad de reparaciones y demoras de taller. Son casos individuales, complemento sin valor de tendencia (https://www.reclamos.cl/empresa/automotora_portillo, consulta 2026-11-23).
- **Dice y hace** [DATO]: califica "Calidad del servicio realizado" con 3 o menos en el 78,2 % de sus detractores. El 43,9 % de detractores (1.097) responde que el vehículo no quedó reparado a la primera.
- **Esfuerzos** [DATO]: volver al taller a reparar lo que no quedó bien. Cuántas veces: NO VERIFICADO (no hay identificador de vehículo en la fuente).
- **Miedos / objeciones** [DATO]: "Cumplimiento de acuerdos" es el 17,5 % de los micro-motivos de detractores; "Percepción de precios", 4,3 %. Verbatim: "Podria ver si se cambian o no los componentes" — `CR_2025-Mecánica_202#145` (NPS 6).
- **Resultados / medida de éxito** [DATO]: que la reparación quede bien a la primera. Entre quienes no quedó bien, el 55,4 % dice que no volvería.

### Journey (5 etapas)

| Etapa | Canal | Fricción | Evidencia |
|---|---|---|---|
| Interés | Búsqueda y reclamos públicos | Demoras y calidad de taller en reclamos públicos | [WEB] (complemento, no tendencia) |
| Consideración | Agendar hora, llamada | Facilidad para comunicarse con 3 o menos en 64,9 % de detractores [DATO]. Promotor: "facil agendamiento de hora" — `CR_2025-Mecánica_202#6` [DATO] | [DATO] |
| Compra (presupuesto y cobro) | Asesor de servicio | Claridad de precios y costos con 3 o menos en 70,4 % de detractores (8,2 % de promotores) [DATO]. "Precios y costos" 9,2 % del motivo de detractores [DATO] | [DATO] |
| Retención (servicio técnico, garantía) | Taller | Calidad del servicio realizado con 3 o menos en 78,2 % de detractores [DATO]. "Reparado a la primera: No" en 43,9 % de detractores [DATO]. Garantía: NO VERIFICADO | [DATO]; garantía NO VERIFICADO |
| Advocacy | Recomendación | Promotores que dicen "Volvería" 98,7 % [DATO]. Si la reparación falló, "No sé" sube a 6,1 % frente a 1,1 % [DATO] | [DATO] |

**Límites**
- La pregunta de reparación: no sabemos si se refiere a reparación o a mantenimiento. Su definición es NO VERIFICADA. Una parte del "No" puede no medir falla técnica [HIPÓTESIS].
- "No volvería" es intención declarada, no conducta. No hay retención real: NO VERIFICADO.
- El archivo CASOS_PBI (reclamos y reincidencia) no está en el proyecto. **BLOQUEADO: depende de Beto (entregar el archivo).**

### Bajada de comunicación
- **Arquetipo:** "el que vuelve con desconfianza".
- **Tono:** explicativo, sin jerga, con el detalle de lo hecho.
- **Pilares:** (1) explicar qué se hizo, qué se cambió y qué falta; (2) precio explicado antes de intervenir; (3) cumplir lo acordado.
- **TOFU** [HIPÓTESIS]: "Qué revisar antes de llevar tu auto al taller." Sin promesas de inspección: "inspección de 200+ puntos" está prohibido sin respaldo legal.
- **MOFU** [HIPÓTESIS]: "Presupuesto explicado antes de intervenir."
- **BOFU** [HIPÓTESIS]: "Tu reparación: qué se hizo, qué se cambió y qué sigue."
- **Contenidos que pide** (base Subagente D, traspasado como [HIPÓTESIS]): contenido educativo sobre mantenimiento, parte de un ítem con 42,0 % top-3 [DATO, encuesta web n=324, sesgo de campaña].
- **Restricción legal:** "garantía" solo con respaldo legal confirmado: NO VERIFICADO.

### Tarjeta de evidencia (P3)
Ver sección 9.

---

## 5. Persona P4 — El que compra o vende un seminuevo

### Ficha (Target + ICP)
- **Miedo dominante (reescrito, regla 4):** que el vehículo entregado no quede como se acordó en su terminación y en el proceso de entrega. [HIPÓTESIS]. La lectura de terminación se basa en dos verbatims; ver Dice y hace.
- **Target:** comprador de seminuevo que recibe el auto, y persona que entrega su auto en parte de pago.
- **ICP:** cliente de Venta-Usados (4.103 filas, GRUPO_COMPLETO). Persona natural: 91,9 % (3.771 de 4.103) [DATO]. Marcas: CHEVROLET 407, MG 286, PEUGEOT 277, NISSAN 263 [DATO, `des_marca`; describe la muestra, no el comprador].
- **Universo Portillo** [HIPÓTESIS, bloqueada]: 145 filas con `\bPORT` (regla 1A) o 108 con prefijo PORT (regla 02). Ambas cifras reproducen con `6F_recuentos_correccion.py`, sección B. De ellas, 11 detractores: no hay base para inferencias [DATO].
- **Edad / género, ingreso, pie, zona, financiamiento, quién decide:** NO VERIFICADO.
- **Marca bajo la que se vende el seminuevo** [BLOQUEADO]: la web comunica el usado de Portillo bajo CLICAR [WEB]. Depende de Beto / Iván Balaguera.

### Detonante y contexto de uso
- Detonante: necesita cambiar de auto y considera un seminuevo. Puede entregar su auto en parte de pago [HIPÓTESIS: existe la pregunta, no el motivo].
- Contexto: compara seminuevos y revisa el estado del auto antes de decidir [HIPÓTESIS].

### Mapa de empatía
- **Piensa y siente** [HIPÓTESIS]: quiere que el auto que recibe esté como se le prometió; no quiere sorpresas después de entregado.
- **Oye** [WEB]: Clicar, "Ingresas patente y kilometraje, y recibes una oferta en minutos" (https://www.clicar.cl, 2026-11-23). Kavak, "Compra y venta de autos. Fácil y seguro" (https://www.kavak.com/cl, 2026-11-23). Son voces de competidores, no de compradores.
- **Ve** [DATO]: "Condición del vehículo" es motivo de 52 de 214 detractores codificados (24,3 %) [DATO]. Su tasa de detractores dentro del tema es 17,2 % (n=302) [DATO].
- **Dice y hace** [DATO, verbatim, terminación posterior a la entrega]: "no se preocupan de entregar un producto de calidad" — `CR_2025-Venta-Usados#41`. "Pintaron los parachoques de otro color no igual al del vehículo" — `CR_2025-Venta-Usados#86`. Que estos casos sean terminación posterior y no información oculta es [HIPÓTESIS] basada en estos dos textos. Clasificar los 52 textos: NO VERIFICADO.
- **Esfuerzos** [DATO]: revisar la entrega y reclamar. Cuánto tiempo: NO VERIFICADO.
- **Miedos / objeciones** [DATO]: calidad del producto (22 de 313 detractores, 7,0 %) y detalles del vehículo (26, 8,3 %).
- **Resultados / medida de éxito** [DATO parcial]: entrega completa con la terminación esperada. La medida "tasación justa" queda en la siguiente fila.

**Miedo a la tasación (HIPÓTESIS).** La pregunta "Vehículo en parte de pago" tiene 1-2 en 39,6 % de detractores (42 de 106) [DATO]. Qué mide exactamente (tasación, rapidez o trámite): NO VERIFICADO. Por eso el miedo "me paguen poco" es [HIPÓTESIS] y no un miedo dominante demostrado.

### Journey (5 etapas)

| Etapa | Canal | Fricción | Evidencia |
|---|---|---|---|
| Interés | Marketplaces y comparadores de seminuevos | Competencia: Kavak, compra directa a particulares y garantía 7 días o 300 km [WEB, benchmark, no propuesta de Portillo] | [WEB] |
| Consideración | Web, opiniones | Opiniones de otros clientes: 40,4 % en top-3 [DATO, encuesta web, sesgo de campaña] | [DATO] |
| Compra (tasación/parte de pago, cierre) | Asesor, tasación | Parte de pago: 1-2 en 39,6 % de detractores (42 de 106) [DATO]. En total, 6,3 % con 1-2 (n=1.525) [DATO]. Condición del vehículo: 17,2 % de tasa de detractores (n=302) [DATO] | [DATO]; significado de parte de pago NO VERIFICADO |
| Retención (entrega, terminación, garantía) | Entrega y taller | Entrega como bloque: 61,7 % de detractores con 1-2 en el proceso de entrega de Usados (193 de 313) [DATO] | [DATO]; garantía de Portillo NO VERIFICADO |
| Advocacy | Recomendación | Promotores 86,4 % de Venta-Usados [DATO]. La atención es el motivo de 82,3 % de promotores codificados [DATO] | [DATO] |

### Bajada de comunicación
- **Arquetipo:** "el que quiere ver el auto antes de decidir".
- **Tono:** transparente y verificable. Nada de "garantía" ni de "inspección" sin respaldo.
- **Pilares:** (1) estado y terminación del seminuevo, explicados en detalle; (2) entrega sin sorpresas, con lo que se acordó; (3) opiniones de clientes reales y verificables.
- **TOFU** [HIPÓTESIS]: "Qué mirar antes de comprar un seminuevo."
- **MOFU** [HIPÓTESIS]: "Qué incluye la entrega de tu seminuevo." Bloqueado hasta confirmar el estándar de entrega (NO VERIFICADO).
- **MOFU para parte de pago** [HIPÓTESIS]: "Cómo tasamos tu auto para parte de pago." **BLOQUEADO** hasta confirmar el método (Beto / Iván Balaguera).
- **BOFU** [HIPÓTESIS]: "Opiniones de clientes y el historial del auto." Solo con reseñas reales y verificables. Nunca fabricar reseñas.
- **Contenidos que pide** (base Subagente D, traspasado como [HIPÓTESIS]): opiniones (40,4 %), alertas de mejor momento para vender (35,5 %) y herramienta para comparar formas de pago (43,5 %) [DATO, encuesta web n=324, sesgo de campaña].
- **Marca:** "seminuevo" en premium. La marca que habla (Portillo o Clicar): BLOQUEADA.

### Tarjeta de evidencia (P4)
Ver sección 9.

---

## 6. Matriz persona × dolor × etapa

Leyenda: ● dolor principal con [DATO]; ○ secundario o [HIPÓTESIS]; – sin evidencia (NO VERIFICADO).

| Persona | Dolor | Interés | Consideración | Compra | Retención | Advocacy |
|---|---|---|---|---|---|---|
| P2 | Plazo de entrega | – | – | ● plazos 18,4 % de detractores | ● fluidez 58,0 % con 1-2 | ○ promotores valoran la atención |
| P2 | Documentos (factura, permiso) | – | – | ○ 6,3 % y 4,9 % | ● tasa de detractor en Documentación 47,0 % | – |
| P3 | Reparación no quedó bien | – | – | – | ● calidad del servicio con 3 o menos 78,2 % | ● "no volvería" 55,4 % |
| P3 | Costo distinto al explicado | – | ○ comunicación 64,9 % | ● claridad de precios con 3 o menos 70,4 % | ○ precios 9,2 % | – |
| P4 | Terminación del vehículo entregado | – | – | – | ○ condición del vehículo, tasa 17,2 % [DATO]; lectura de terminación [HIPÓTESIS] | ○ atención 82,3 % de promotores |
| P4 | Proceso de entrega de Usados | – | – | ○ | ● 61,7 % de detractores con 1-2 | – |
| P4 | Parte de pago (significado NO VERIFICADO) | – | ○ alerta de venta 35,5 % | ● 39,6 % de detractores con 1-2 | – | – |
| Transversal | Precio y financiamiento (no es persona) | – | – | ○ detractores 5,7 % en Nuevo y 4,2 % en Usados (bases pequeñas) | – | – |
| Descartada | Sin respuesta tras cotizar (P1) | – | ○ [HIPÓTESIS], codificación sin validar | ○ 15,8 % de barreras explícitas | – | – |

---

## 7. Demografía: una sola fuente, sin cruce

- **Fuente única:** encuesta de seguridad vial, n=709, solo clientes de autos nuevos, 2025-10-22 a 2025-10-29 [DATO, USO INTERNO].
- **Rango de edad** [DATO]: 60 o más 26,2 %; 50-59 25,8 %; 40-49 24,7 %; 30-39 14,5 %; 18-29 5,1 %; vacío 3,7 %.
- **Género** [DATO]: masculino 61,2 %; femenino 32,4 %; prefiere no decir 1,3 %; vacío 5,1 %.
- **Sesgo:** clientes de auto nuevo, un solo mes, un solo canal. No se usa para inferir perfil de P2 a P4.
- **Cruce persona × edad o género:** NO VERIFICADO. La encuesta web no tiene edad ni género.

---

## 8. Qué NO sabemos

### 8.1 Variables que no existen en los datos
- **Ingreso:** NO VERIFICADO en todas las fuentes.
- **Pie / enganche real:** NO VERIFICADO. [WEB] portillo.cl ofrece "cuotas con pie de 40 % a 36 cuotas" (oferta pública, no dato de clientes).
- **Financiamiento (tipo, plazo, bancos):** NO VERIFICADO. [WEB] el financiamiento en la web es "solo implícito". Stock de crédito automotriz: NO VERIFICADO.
- **Zona de la persona:** NO VERIFICADO (solo nombres de sucursal).
- **Quién decide:** NO VERIFICADO.
- **Edad y género por persona:** NO VERIFICADO.
- **Fecha de corte de leads (2026-01-23):** NO VERIFICADO si es exportación o falta de datos. Dependencia: Beto. Esta fecha invalida la vigencia de cualquier conclusión de leads.

### 8.2 Cruces que no se pueden hacer
- **Lead → venta:** no existe clave verificada. **No hay conversión ni tasa de cierre.** Dependencia: Beto / Iván Balaguera.
- **Venta → servicio:** no verificado. Mecánica y Venta son fuentes separadas.
- **Persona × demografía:** NO VERIFICADO.

### 8.3 Bloqueos y a quién dependen

| Bloqueo | Depende de |
|---|---|
| Asignación de sucursales y marcas a Portillo (PORTILLO_HIPOTESIS) | Beto / Iván Balaguera |
| Marca que habla por el seminuevo: Clicar o Portillo (C11) | Beto / Iván Balaguera |
| Regla para PORTILLO (`\bPORT` o `\bPORTILLO\b`; C7, C15) | Beto / Iván Balaguera |
| Archivo CASOS_PBI: no está en el proyecto | Beto (entregar archivo) |
| Libro de códigos y responsable de macrocategorías | Beto |
| Dirección de la escala de evaluación (leads y encuesta web) | Beto (diccionario de datos) |
| Fecha de corte de leads (2026-01-23) | Beto |
| Definición de la pregunta de reparación (Mecánica) | Beto |
| Texto exacto de la pregunta de fluidez (Nuevo) | Beto |
| Método de tasación de parte de pago (P4) | Beto / Iván Balaguera |
| Garantía, cobertura de inspección, plazos de entrega (cualquier mensaje) | Beto (validación legal y operativa; NO VERIFICADO) |
| Clasificación de los 52 textos de "Condición del vehículo" (P4) | Beto (o quien codifica) |

### 8.4 Contradicciones y recuentos (las 15, sin corregir)

Numeración según `research/00_contradicciones.md` (#1 a #15). Estado de reproducción por `6F_recuentos_correccion.py` (sección A-C) y por los scripts de `analisis/` (1A, 2B, 3C, 4D).

| # | Tema | Cifra A | Cifra B | Reproducción y uso en este documento |
|---|---|---|---|---|
| 1 | Ventana Lead-Portillo | Brief 2023-06 a 2026-01 | Datos 2023-06-08 a 2026-01-23 | Coincide. Fecha de corte NO VERIFICADA (8.1) |
| 2 | Ventana Clicar | Brief 2023-06 a 2024-04 | Datos 2023-06-30 a 2024-04-08 (223 filas) | Coincide. Clicar no entra en las personas |
| 3 | Etiqueta Portillo | `empresa` = Grupo Americar | Nombre de archivo y sucursales dicen PORTILLO | Real. Todas las cifras de Portillo son [HIPÓTESIS] |
| 4 | Sucursal en Venta-Usados | Vacía | `nombre_concesionario` poblado (149 valores) | Coincide. P4 usa `nombre_concesionario` |
| 5 | Hoja1 de CASOS_PBI | Brief: con datos en 0.0 | Archivo no presente | BLOQUEADO (Beto). P3 sin capa de casos |
| 6 | Número de .xlsx | Brief: 8 | 7 | Ligado a 5. Sin efecto en personas |
| 7 | Prefijos en Mecánica | Brief sin mención | GAP, ACSA, DENALI conviven con PORTILLOLA y PORTILLOTALCA | **Reproducida.** 118 de 245 filas dudosas. Universo limpio: 127 filas, NPS 84,3 (6F, A) |
| 8 | Marca en Mecánica | `des_marca` 77 valores | `marca` 78; `marca_sucursal` 62 | Se usa `des_marca` en P3 |
| 9 | Portillo en encuesta web | 72 por `campaña o sensor` | 30 por `nombre_concesionario` | **Reproducida:** 72 en 4D (5b). 30 en 4D. No se usa ninguna como cifra de Portillo |
| 10 | Portillo en seguridad vial | 142 por `campaña o sensor` | 102 por `nombre_concesionario` | **142: reproducida por 6F (C), no por 4D.** 4D no imprime esa cifra. Se muestra como contradicción; no se usa en personas. 102 reproducida por 4D |
| 11 | Usado de Portillo | Mapeo: "PORT USADOS" es Portillo | Web: el usado se comunica como CLICAR [WEB] | BLOQUEADO. P4 sin marca definida |
| 12 | Plantilla de Portillo 2025 | 3.389 a 2.973 empleados [WEB, secundaria] | Sin cifra interna | No se usa en ninguna persona ni mensaje |
| 13 | Contacto vs necesidad | 60 leads con "No" al contacto | 275 "Ya estoy en contacto"; 10 coinciden | Reproducida por 2B. Motivo de descarte de P1 |
| 14 | Leads usados | `des_marca` = USADOS: 326 | `tipo_oportunidad` usado: 327 | Diferencia de 1 fila. Sin efecto |
| 15 | Universo PORTILLO en Venta-Usados | Prefijo PORT: **108** | `\bPORT`: **145** | **Ambas reproducidas por 6F (B).** Se muestran las dos. 11 detractores: no concluyente |

### 8.5 Otras limitaciones
- **Sesgo de campaña en la encuesta web:** 63,3 % de las respuestas viene de la campaña "Salazar Israel" [DATO].
- **Encuesta web sin NPS útil:** todos los valores son 9 o 10 [DATO]. No se calcula NPS.
- **Sin pruebas estadísticas:** las diferencias son descriptivas, no efectos.
- **Sin causalidad:** las brechas por etapa son asociaciones.
- **Fechas distintas por fuente:** Leads hasta 2026-01-23; Nuevo y Usados hasta 2026-11-23; Mecánica desde 2025-03-04; encuesta web 2025-07-18 a 2025-08-23; seguridad vial 2025-10-22 a 2025-10-29.
- **Codificación de motivos:** sin libro de códigos. Quién codificó: NO VERIFICADO.
- **Verbatims:** de 15 palabras o menos, con row_id. Dos ajustes de forma: "trasparente" en la fuente (la cita de leads usa la forma corregida; no se cita en esta versión). El filtro de Mecánica no garantiza ausencia de PII en minúscula; revisar antes de cualquier uso externo.
- **Auditoría de URLs WEB:** pendiente. Las URLs de `research/05` no se volvieron a abrir en esta corrección.

---

## 9. Tarjetas de evidencia (conteo automático)

Conteo de `analisis/6F_recuentos_correccion.py`, sección D. Denominador = afirmaciones etiquetadas en Ficha a Journey (DATO + WEB + HIPÓTESIS). NO VERIFICADO fuera del denominador.

| Persona | [DATO] | [WEB] | [HIPÓTESIS] | Denominador etiquetado | NO VERIFICADO (fuera del denominador) |
|---|---:|---:|---:|---:|---:|
| P2 | 19 (86,4 %) | 0 (0,0 %) | 3 (13,6 %) | 22 | 8 |
| P3 | 24 (82,8 %) | 2 (6,9 %) | 3 (10,3 %) | 29 | 6 |
| P4 | 22 (71,0 %) | 4 (12,9 %) | 5 (16,1 %) | 31 | 6 |

Lectura: el conteo es de menciones etiquetadas en el texto, no de ítems únicos; una misma cifra puede repetirse. Por eso la proporción sirve para comparar la forma de la evidencia entre personas, no como medida de solidez. Las cifras de n que respaldan cada persona están en la sección 10.

---

## 10. Resumen de trazabilidad

| Persona | Miedo dominante (versión 2) | n base | Estado |
|---|---|---|---|
| P2 | Plazo y trámite de la entrega (Nuevo) | 6.458 (348 detractores) | Sostenida por [DATO], con nombre de etapa [HIPÓTESIS] |
| P3 | Reparación no bien hecha y costo distinto al explicado | 27.516 (2.497 detractores); universo Portillo limpio 127 | Sostenida a nivel grupo; Portillo bloqueado |
| P4 | Terminación del vehículo entregado (Usados) | 4.103 (313 detractores) | Tasa de detractores 17,2 % [DATO]; lectura de terminación [HIPÓTESIS]; miedo a la tasación [HIPÓTESIS] |
| P1 | Descartada | 1.003 leads | Datos movidos a 8.1 y 8.4 |

**Versión publicable:** ninguna. Todas las cifras son USO INTERNO.

*Script de apoyo: `analisis/6F_recuentos_correccion.py` (recuentos y conteo de etiquetas). Fuentes de cifras: `research/01` a `04`, con scripts `analisis/1A_voz_ventas.py`, `2B_leads_cotizacion.py`, `3C_retencion_mecanica.py`, `4D_intencion_funcionalidades.py`.*
