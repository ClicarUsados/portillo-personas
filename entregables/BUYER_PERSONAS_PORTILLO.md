# Buyer personas Portillo: arquetipos de cliente por Momentos de la Verdad (versión 3, corregida)

**Fecha de corte:** 2026-11-23. **USO INTERNO.** Contiene cifras de CRM (leads, encuestas post-venta, servicio técnico). **No es publicable.**
**Estado:** borrador para Beto y jefatura. Asignación a Portillo **BLOQUEADA** (Beto / Iván Balaguera). Marca del seminuevo (Portillo o Clicar) **BLOQUEADA** (Beto / Iván Balaguera / equipo comercial Portillo).
**Sustituye a la v2** (archivada en `entregables/v1_pre_MdV/`). Tabla de candidatos, regla y solapamiento en `research/06_arquetipos_cliente.md`.

---

## 0. Resultado y cómo leer

**Resultado:** **una persona (P2, fusión F)** y **tres hipótesis fuera de persona (H1, H2, H3)**.

**Estado de la persona:** una persona confirmada; hipótesis H1-H3 pendientes de la guía de entrevista.
La coordinación pidió "3 personas". Con la fusión de G, P1 y P3 pasan a hipótesis, así que el número de **personas** es 1. Si comité quiere contar las hipótesis como personas, deben ser 4 en total (una persona y tres hipótesis de proceso). Esto se confirma en la respuesta.

**Etiquetas.**
- **[DATO C-xx]**: cifra de `research/06_arquetipos_cliente.md`, fila C-xx. Cada fila indica archivo, columna, filtro, n, base, fecha 2026-11-23 y script.
- **[WEB]**: URL y fecha de consulta 2026-11-23 (`research/05_contexto_web.md`).
- **[HIPÓTESIS]**: inferencia, codificación por palabras clave, pedido de información o propuesta. A validar.
- **NO VERIFICADO**: sin dato. No se rellena.
- **BLOQUEADO**: depende de una decisión o archivo de una persona nombrada.

**Reglas aplicadas en esta versión** (decisiones de coordinación):
1. Fusión: P2 absorbe P4 y P5. P1 y P3 pasan a hipótesis, fuera de persona. El solapamiento de respondentes es evidencia de la fusión (sección 4 de research/06).
2. C-05 usa la base de **431 respondidos (13,9 %)**, no 1.003. Incluye la desagregación por año.
3. Denominadores de evidencia: **sin NO VERIFICADO**, contados por `analisis/6F_recuentos_correccion.py` (regex corregida: cuenta `[HIPÓTESIS C-…]`).
4. C-09b y C-13 pasan a [HIPÓTESIS]: pedidos de información, no miedos.
5. Cita de lead `#662` con la ortografía de la fuente: "trasparente".
6. Marco legal: SERNAC sin fuente primaria: **NO VERIFICADO** (ver §7).
7. Solapamiento de Mecánica: 78,5 % de los respondentes aparecen en al menos dos personas previas. Es una limitación explícita (§5).

**Restricciones que se respetan.** Leads, compradores y clientes de taller son poblaciones distintas. **No hay clave verificada lead→venta**: no hay conversión ni tasa de cierre. Sin PII. Citas de 15 palabras o menos, con row_id. "Seminuevo" en premium.

---

## 1. Persona P2 (fusión F): "El que no recibe respuesta, explicación ni buen trato"

### Ficha (Target + ICP)
- **Miedo dominante:** después de pedir algo (una cotización, una explicación, una atención), no recibe respuesta, no sabe qué se hizo o no lo tratan bien. Son tres quejas de la misma persona en distinto momento: **silencio** (ZMOT), **información** (FMOT, SMOT, UMOT) y **trato** (FMOT, SMOT, UMOT).
- **Target:** quien pide algo a la empresa en venta (nuevo o seminuevo) o en taller, o quien cotiza y espera.
- **ICP:** leads de Lead-Portillo (1.003 filas; 431 respondieron la pregunta de contacto); clientes de Venta-Nuevo (6.458), Venta-Usados (4.103) y Mecánica (27.516). Origen de leads: WEB 60,7 %, SALON 28,3 % [DATO, `research/01_zmot.md` §4].
- **Edad / género:** NO VERIFICADO. Única fuente demográfica: seguridad vial (n=709; clientes de auto nuevo; 2025-10-22 a 2025-10-29) [DATO, `umot_03_demografia_seguridad_vial.py`]. No cruza con ninguna familia.
- **Ingreso, pie, financiamiento, zona, quién decide:** NO VERIFICADO.
- **Fecha de corte de leads:** 2026-01-23. Casi 10 meses antes de la extracción. Si es corte de exportación: NO VERIFICADO (Beto).

### Detonante y contexto de uso
- Detonante: pide una cotización, una respuesta o una explicación, y la espera.
- Contexto: el cliente decide si sigue o se va según la respuesta. En taller o en entrega, la espera se suma a la duda sobre lo que se hizo [HIPÓTESIS].

### Mapa de empatía (consolidado)
- **Piensa y siente** [HIPÓTESIS]: siente que no le hacen caso, que lo dejan esperando y que no le explican nada. Lectura de fricción en venta: 1-2 en facilidad de comunicación con el vendedor, 28,2 % de detractores de Nuevo y 26,8 % de Usados [DATO C-06].
- **Oye:** "Se suponía que me contactarían y no ha pasado nada" — `CR_Lead-Portillo_202#4` [DATO C-05, cita]. "Mala respuesta para la fecha de entrega y cero comunicación" — `CR_2025-Venta-Nuevo_#6271` [DATO C-08, cita]. Lo que oye de la empresa en general: NO VERIFICADO.
- **Ve:** el silencio como estado. De 431 leads que respondieron, 60 dicen que ventas no los ha contactado: **13,9 %** [DATO C-05]. En 2026 la cifra es 40,4 % (19 de 47) y en 2024 es 4,9 % (13 de 265) [DATO C-05-año]. En taller, la información sobre la reparación con nota ≤3 en 69,5 % de detractores [DATO C-15].
- **Dice y hace:** "Solicite cotización y nadie me ha contactado hasta el momento" — `CR_Lead-Portillo_202#5` [DATO C-05, cita]. "Nunca me enviaron nada, solo me llego un mensaje automático por WhatsApp" — `CR_Lead-Portillo_202#555` [DATO, `research/01_zmot.md` §8, cita]. Cuántas veces insiste: NO VERIFICADO.
- **Esfuerzos, miedos, objeciones:** "No me han entregado el auto y no responde el vendedor" — `CR_2025-Venta-Nuevo_#1879` [DATO C-06, cita]. "Vendedor inoperante, poco profesional, cero compromiso de venta, comunicación deficiente, mala experiencia" — `CR_2025-Venta-Usados#159` [DATO C-18, cita]. "Abollaron mi automóvil y no me informaron a la salida del servicio técnico" — `CR_2025-Mecánica_202#661` [DATO C-15, cita].
- **Resultados / medida de éxito:** que le respondan, le expliquen y lo traten bien, en un plazo que pueda contar. [HIPÓTESIS]. El plazo de respuesta: NO VERIFICADO.

### Recorrido por los 4 MdV

| MdV | Canal | Evidencia |
|---|---|---|
| ZMOT | Formulario web o salón; leads que cotizan | "No" a que ventas los haya contactado: **60 de 431 = 13,9 %** [DATO C-05]. Por año: 2024 4,9 % (13/265), 2025 23,5 % (28/119), 2026 40,4 % (19/47) [DATO C-05-año]. Motivo "sin respuesta" por palabras clave: 39 de 558 = 7,0 % [HIPÓTESIS C-05b; v1 = 61, no reproducible]. Opción "Mayor información del vehículo": 10 de 431 = 2,3 % [HIPÓTESIS C-13: pedido de información] |
| FMOT | Sala y ejecutivo | Facilidad de comunicación con el vendedor, 1-2 en detractores: 28,2 % Nuevo, 26,8 % Usados [DATO C-06]. Información del vendedor, 1-2: 31,0 % de detractores de Nuevo [DATO C-14]. Atención del vendedor, 1-2: 21,3 % Nuevo, 26,8 % Usados. Acogida en sala, 1-2: 12,4 % Nuevo, 23,3 % Usados [DATO C-18] |
| SMOT | Taller: recepción, llamada, salida | Facilidad para comunicarse con nota ≤3: 64,9 % de detractores (proxy de fricción, no de silencio) [DATO C-07]. Claridad sobre la reparación con nota ≤3: 69,5 % [DATO C-15]. Atención de personal con nota ≤3: 46,5 %. Acogida en sala de espera con nota ≤3: 51,4 % [DATO C-19] |
| UMOT | Recomendación y retorno declarado | Ítem "Comunicación" ≤2 en pool: Mecánica 35,0 %, vendedor Nuevo 16,8 %, Usados 21,1 %, Clicar 50,0 % [DATO C-08]. Reparación no explicada: 35,6 % [DATO C-16]. Acogida ≤2: Mecánica 18,3 %, Nuevo 7,3 %, Usados 18,4 % [DATO C-20] |

**Límites de la familia:**
- C-07 y C-08 miden facilidad o comunicación, no respuesta observada. El nombre "sin respuesta" es del script.
- C-14 solo existe en Nuevo. En Usados no hay columna equivalente.
- "Atención" es el motivo dominante de promotores (82 % Venta; 76,9 % Mecánica) [DATO, `research/02_fmot.md` §2.4, `smot_mecanica.py`]. Las tasas de detractores (18-51 %) la hacen un miedo; el archivo no tiene tasa de promotores con ≤2 para comparar.
- La cita `CR_2025-Venta-Usados#314` ("Vehículo con muchos detalles que no se informo por parte del vendedor") es de Usados. La métrica C-14 es de Nuevo. Se usa como ilustración, no como prueba de C-14.

### Bajada de comunicación
- **Arquetipo:** "el que espera una respuesta y una explicación".
- **Tono:** cercano y directo, sin tecnicismos, sin promesas de tiempo.
- **Pilares:** (1) alguien responde, aunque sea para decir cuándo; (2) se explica antes de hacer, con lo que se hizo y lo que falta; (3) el trato no depende de la compra.
- **TOFU** [HIPÓTESIS]: "Recibimos tu solicitud. Te decimos cuándo te contactamos." Solo con un plazo de respuesta confirmado (NO VERIFICADO; BLOQUEADO: Beto / equipo comercial Portillo).
- **MOFU** [HIPÓTESIS]: "Qué se hizo, qué falta y quién lo sigue." Aplica a cotización, reparación y entrega.
- **BOFU** [HIPÓTESIS]: "Tu ejecutivo y tu técnico, con nombre, y tu próximo paso." Requiere asignación confirmada de personal (NO VERIFICADO).
- **Funcionalidades que pide** (proxy de compradores de nuevo, no de leads ni de visitantes; [DATO, `zmot_funcionalidades.py`; D-N6]): comparar formas de pago (43,5 % top-3); contenido educativo (42,0 %); opiniones de clientes (40,4 %); historial del vehículo y documentos en app (89,8 % de acuerdo); asistente virtual que acompañe la visita (60,8 % de acuerdo). Escala de acuerdo NO VERIFICADA; muestra con sesgo de campaña (Salazar Israel 63,3 %).

### Tarjeta de evidencia
Ver sección 6.

---

## 2. Hipótesis H1 · Proceso largo o sin fecha (fuera de persona)

- **Evidencia [DATO]:** fluidez 1-2 en detractores: 58,0 % Nuevo (202 de 348), 50,8 % Usados (159 de 313) [DATO C-02]. Proceso largo en pool: 35,0 % Mecánica, 35,3 % Nuevo, 41,2 % Usados [DATO C-04]. Tiempo de entrega ≤3 en detractores de taller: 60,9 % [DATO C-03]. Cita: "Mucha demora en entrega de factura y entrega de vehiculo" — `CR_2025-Venta-Nuevo_#143` [DATO C-02, cita].
- **Por qué no es persona:** tres momentos con [DATO], pero solo dos poblaciones independientes (venta y taller). UMOT repite a FMOT (93 %) y SMOT (86 %). En ZMOT, la lentitud es solo palabra clave (23,7 %, [HIPÓTESIS C-01]; v1 = 85).
- **Qué la confirmaría:** texto exacto de la pregunta de fluidez (NO VERIFICADO; Beto); tiempos reales de entrega del periodo (denominador NO VERIFICADO); codificación validada de "Lentitud" (dos codificadores ciegos, 100 textos).
- **Tarjeta:** sección 6.

## 3. Hipótesis H2 · Costo o financiamiento poco claro (fuera de persona)

- **Evidencia [DATO]:** claridad de precios y financiamiento con 1-2 en detractores: 20,1 % Nuevo (70 de 348), 25,2 % Usados (79 de 313) [DATO C-10]. Claridad de precios y costos con ≤3 en detractores de taller: 70,4 % [DATO C-11]. Costos poco claros en pool: 38,6 % Mecánica, 12,4 % Nuevo, 20,8 % Usados [DATO C-12].
- **Evidencia de leads [HIPÓTESIS]:** precio 40 y financiamiento 23 de 558, por palabras clave [HIPÓTESIS C-09]. Opción "Información de financiamiento": 14 de 431 = 3,2 % [HIPÓTESIS C-09b: pedido de información, no miedo].
- **Citas:** "Vendedora me dio un precio y despues lo subio" — `CR_2025-Venta-Nuevo_#476` [DATO C-10, cita]. "No me respondieron nada sobre valores, opciones de pago y financiamiento." — `CR_Lead-Portillo_202#61` [HIPÓTESIS C-09, cita]. "Ser más trasparente con el costo establecido en la cotización" — `CR_Lead-Portillo_202#662` [HIPÓTESIS C-09, cita; ortografía de la fuente].
- **Por qué no es persona:** tres momentos con [DATO] en venta y taller, pero el lado de leads es solo hipótesis, y su solapamiento con F no está medido en una base común.
- **Qué la confirmaría:** clasificar los motivos de leads de precio con codificación validada; medir precio y financiamiento en la misma base que F (NO VERIFICADO; Beto).
- **Tarjeta:** sección 6.

## 4. Hipótesis H3 · Reparación mal hecha (fuera de persona)

- **Evidencia [DATO]:** reparado a la primera = No en 43,9 % de detractores (1.097 de 2.497) [DATO, `smot_mecanica.py`]. Calidad del servicio con nota ≤3 en 78,2 % de detractores [DATO, `smot_mecanica.py`]. Trabajo mal hecho en pool de UMOT: 39,9 % (1.355 de 3.399) [DATO C-21].
- **Por qué no es persona:** solo dos momentos (SMOT y UMOT), misma encuesta de taller. ZMOT y FMOT no lo miden.
- **Solapamiento con F:** de los 1.735 detractores con claridad de reparación ≤3, 968 (55,8 %) tienen reparado = No [DATO, `smot_mecanica.py`; research/06 C-21]. La familia es casi la misma gente que F.
- **Qué la confirmaría:** una segunda MdV independiente, o los casos de CASOS_PBI (**BLOQUEADO**: depende de Beto).

---

## 5. Matriz persona × MdV × miedo

Leyenda: ● familia con [DATO] en ese MdV; ○ solo [HIPÓTESIS] o proxy; – sin dato o no medido (NO VERIFICADO).

| Persona / hipótesis (miedo) | ZMOT | FMOT | SMOT | UMOT |
|---|---|---|---|---|
| **P2 · Silencio** (sin respuesta) | ● C-05 13,9 % (2026: 40,4 %) | ● C-06 28,2 % / 26,8 % | ○ C-07 proxy 64,9 % | ● C-08 35,0 % / 16,8 % / 21,1 % / 50,0 % |
| **P2 · Información** (no sé qué se hizo) | ○ C-13 [HIPÓTESIS] · C-13b [HIPÓTESIS] | ● C-14 31,0 % (solo Nuevo) | ● C-15 69,5 % | ● C-16 35,6 % |
| **P2 · Trato** (cómo me reciben) | – C-17 descartado por n | ● C-18 atención 21,3 % / 26,8 %; acogida 12,4 % / 23,3 % | ● C-19 atención 46,5 %; acogida 51,4 % | ● C-20 acogida 18,3 % / 7,3 % / 18,4 % |
| H1 · Proceso largo | ○ C-01 [HIPÓTESIS] | ● C-02 58,0 % / 50,8 % | ● C-03 60,9 % | ● C-04 35,0 % / 35,3 % / 41,2 % |
| H2 · Costo poco claro | ○ C-09, C-09b [HIPÓTESIS] | ● C-10 20,1 % / 25,2 % | ● C-11 70,4 % | ● C-12 38,6 % / 12,4 % / 20,8 % |
| H3 · Reparación mal hecha | – | – | ● 43,9 % (reparado = No); 78,2 % | ● C-21 39,9 % |

**Familias fuera de la matriz:** tasación o parte de pago (C-22; FMOT ● 21,8 % / 39,6 %; UMOT ● 65,7 % Clicar); terminación (C-23; FMOT ● 24,3 % Usados); documentación (C-24; FMOT ● 14,9 % / 11,2 %); cumplimiento de acuerdos (C-25; SMOT ● 17,5 %). Hipótesis, sin persona.

---

## 6. Tarjetas de evidencia

Conteo de `analisis/6F_recuentos_correccion.py` (sección D), con regex corregida (`[HIPÓTESIS` cuenta también las etiquetas con referencia). Denominador = [DATO] + [WEB] + [HIPÓTESIS] en la sección de evidencia de cada persona o hipótesis, hasta "### Bajada de comunicación". NO VERIFICADO fuera del denominador.

| Persona / hipótesis | [DATO] | [WEB] | [HIPÓTESIS] | Denominador etiquetado | NO VERIFICADO (fuera) | n que la respalda |
|---|---:|---:|---:|---:|---:|---|
| **P2 · fusión F** (silencio, información, trato) | 25 (83,3 %) | 0 (0,0 %) | 5 (16,7 %) | 30 | 6 | 1.003 leads y 431 respondidos (C-05, C-05-año); 348 y 313 detractores de venta (C-06, C-14, C-18); 2.497 de taller (C-07, C-15, C-19); pools de 3.399, 614, 413 y 70 (C-08, C-16, C-20) |
| H1 · Proceso largo | 6 (85,7 %) | 0 (0,0 %) | 1 (14,3 %) | 7 | 2 | 348 y 313 (C-02); 2.497 (C-03); pools de 3.399, 614 y 413 (C-04) |
| H2 · Costo poco claro | 6 (54,5 %) | 0 (0,0 %) | 5 (45,5 %) | 11 | 1 | 348 y 313 (C-10); 2.497 (C-11); pools de 3.399, 614 y 413 (C-12); 558 y 431 de leads (C-09, C-09b) |
| H3 · Reparación mal hecha | 5 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 5 | 0 | 2.497 (reparado = No, 43,9 %; calidad 78,2 %); pool 3.399 (C-21) |

Lectura: el conteo es de menciones etiquetadas en el texto, no de ítems únicos; una misma cifra puede repetirse. Sirve para comparar la forma de la evidencia, no como medida de solidez. La solidez por momento y por solapamiento está en `research/06_arquetipos_cliente.md` (secciones 3 y 4).

---

## 7. Qué NO sabemos

- **Solapamiento en Mecánica (limitación de independencia):** 78,5 % de los respondentes de taller (2.105 de 2.681) aparecen en al menos dos personas previas [DATO, `analisis/7G_solapamiento_personas.py`]. La regla de "3 de 4 momentos" cuenta momentos, no personas independientes. Por eso la fusión en P2 es la decisión, no la regla. Clave de respondente entre archivos: NO VERIFICADO (Beto).
- **Visitantes que no cotizan (ZMOT real):** no hay datos. Dependencia: Beto (analítica web).
- **C-05 por año:** 2023 (294 leads) no tiene respuesta a la pregunta de contacto. La subida de 4,9 % a 40,4 % puede venir de un cambio de captura. Dependencia: Beto (fecha en que empezó a capturarse el campo).
- **Fecha de corte de leads (2026-01-23):** NO VERIFICADO si es de exportación. Dependencia: Beto.
- **Escala de cotización y de calidad del contacto:** dirección NO VERIFICADA. Dependencia: Beto.
- **Palabras clave (ZMOT):** C-01, C-05b, C-09, C-13b y C-24 dependen de una regla no validada. Dependencia: Beto (codificación).
- **Cruce lead→venta:** no hay clave verificada. Dependencia: Beto / Iván Balaguera. No hay conversión ni tasa de cierre.
- **Recompra y retorno real:** solo intención declarada ("volvería"). Dependencia: Beto (historial de visitas; el identificador de vehículo fue anonimizado).
- **Plazos de respuesta y de entrega:** NO VERIFICADOS. Dependencia: equipo comercial Portillo y Beto.
- **Tasación y parte de pago (C-22):** significado de la pregunta. Dependencia: Beto.
- **Terminación del vehículo (C-23):** clasificar los 52 textos de "Condición del vehículo". Dependencia: Beto.
- **Portillo:** toda cifra de Portillo depende de la asignación (Beto / Iván Balaguera). Ver §8.
- **Clicar:** datos 2023-06-30 a 2024-04-08, desactualizados. Dependencia: Beto.
- **Marca del seminuevo:** BLOQUEADA (Beto / Iván Balaguera / equipo comercial Portillo).
- **Demografía por persona:** NO VERIFICADO. Única fuente: seguridad vial, sin cruce.
- **Marco legal de garantías (voluntarias y en usados):** NO VERIFICADO. No hay fuente primaria leída (circular SERNAC, Res. Ex. N° 923). Las fuentes consultadas son prensa y un análisis jurídico, que no se usan como base. **Dependencia: validación legal (Beto).**
- **C-14:** solo existe en Nuevo; no hay equivalente en Usados.

## 8. Contradicciones que afectan a esta versión

Numeración según `research/00_contradicciones.md`. Se muestran ambas cifras sin corregir. Detalle y reproducción en esa sección, "Fase 1 (marco MdV)".

| # | Tema | Cifra A | Cifra B | Impacto |
|---|---|---|---|---|
| D-N1 | Mecánica Portillo | 7.881 por campaña "Mecánica Portillo" [DATO] · NPS +71,6 | 245 por `\bPORT` en sucursal [HIPÓTESIS] · NPS +68,2; sin PORTILLOLA/TALCA: 127, NPS +84,3, detractores 3,9 % | Tamaño del universo de taller. Abierta |
| D-N2 | Usados por campaña | 114 "Venta Usados Portillo" [DATO] · NPS +74,6 | 163 "Venta Usados Clicar" [DATO; consulta directa] | Marca del seminuevo. Abierta (BLOQUEADO) |
| D-N3 | Venta-Nuevo Portillo | 1.313 por campaña [DATO, bruto]; 1.312 con NPS válido | 1.311 por prefijo PORT [HIPÓTESIS] · NPS +81,5 | 1-2 filas. Sin efecto |
| D-N4 | Lentitud (regla de codificación) | 132 de 558 (versión 2) [HIPÓTESIS] | 85 de 558 (versión 1) [HIPÓTESIS; no reproducible] | H1 (ZMOT). Rango 85-132 |
| D-N5 | Sin respuesta (regla de codificación) | 39 de 558 (versión 2) [HIPÓTESIS] | 61 de 558 (versión 1) [HIPÓTESIS; no reproducible] | Soporte de F en ZMOT. Solo hipótesis |
| D-N6 | Marco de la encuesta web | Brief: funcionalidades pedidas por el **visitante** | Datos: 324 de 324 son **compradores de vehículo nuevo con factura** (2024-01 a 2025-05; mediana 262 días) [DATO] | Las funcionalidades son proxy post-venta, no necesidad de visitante. Abierta |
| D-N7 | Seguridad vial, campaña Portillo | 142 por `campaña o sensor` [DATO; reproducido por `umot_03`] | 102 por `\bPORT` en concesionario [HIPÓTESIS] | Sin efecto en personas |
| D-B1 | Universo Portillo en Usados | 108 por prefijo `^PORT` [HIPÓTESIS] · 145 por `\bPORT` [HIPÓTESIS] | 114 por campaña "Venta Usados Portillo" [DATO] | Ninguna cifra única. Abierta |
| D-E1 | Marca del usado de Portillo | Aviso de Chileautos "PORTILLO \| USADOS VITACURA 6875" y "PORTILLO \| USADOS PADRE HURTADO NORTE 1246" [WEB, consultado 2026-11-23] | Usado bajo la marca Clicar [WEB, fuente de empleo; portillo.cl] | Bloquea la marca que habla por el seminuevo. Abierta (BLOQUEADO) |
| #13 | Contacto vs necesidad | 60 "No" al contacto [DATO] | 275 "ya en contacto" [DATO]; 10 coinciden | Cambia la lectura de C-05 |
| #15 | Universo Portillo en Venta-Usados | 108 por prefijo | 145 por `\bPORT` | Ver D-B1 |
| D-A1 | Etiqueta vs ítem (UMOT Mecánica) | "Miedo a mal trato en recepción" (script): 621 | Ítem "Acogida en sala de espera" | Se usa "acogida" en esta versión |

**Nota sobre C-05:** la cifra de la versión anterior (6,0 % de 1.003) usaba un denominador equivocado. La base correcta es 431 respondidos (13,9 %).

## 9. Arquetipo de marca (solo bajada de comunicación)

Este arquetipo es de **marca**. No se mezcla con la persona P2 ni con las hipótesis.

- **Arquetipo propuesto:** "El Acompañante": cumple lo que promete, explica antes de hacer y responde. [HIPÓTESIS].
- **Base en datos:** la atención es el motivo dominante de promotores (82 % Venta; 76,9 % Mecánica) [DATO, `research/02_fmot.md` §2.4, `smot_mecanica.py`]. La información y la respuesta son las quejas de la persona P2 (C-08, C-15, C-16).
- **Tono:** cercano, claro, cumplidor. Nada de tono de promoción.
- **Pilares:** (1) lo que se dice, se cumple; (2) se explica antes de hacer; (3) se responde.
- **Prohibido sin respaldo primario:** garantías, plazos, "inspección de X puntos", cifras de cobertura. Ver el marco legal como NO VERIFICADO (§7).
- **Competidores (referencia, [WEB] 2026-11-23):** Pompeyo, "El camino que da confianza", con seminuevos "inspeccionados, con garantía" [WEB, pompeyo.cl; término de competidor, no se usa en la marca]. Kavak, "7 días o 300 km" de prueba [WEB, kavak.com/cl]. Derco, cuotas con CAE visible [WEB, derco.cl].
- **Marca que habla:** BLOQUEADA (Portillo o Clicar para el seminuevo; Beto / Iván Balaguera / equipo comercial Portillo).

---

*Fuentes: `research/06_arquetipos_cliente.md` (C-01 a C-26; solapamiento en sección 4), `research/01_zmot.md`, `02_fmot.md`, `03_smot.md`, `04_umot_demografia.md`, `05_contexto_web.md`, `00_contradicciones.md` (Fase 1). Scripts: `zmot_leads.py`, `zmot_funcionalidades.py`, `fmot_mapa_empatia.py`, `smot_mecanica.py`, `umot_01_recomendacion_retorno.py`, `umot_02_miedos_umot.py`, `umot_03_demografia_seguridad_vial.py`, `7G_solapamiento_personas.py`, `6F_recuentos_correccion.py`.*
