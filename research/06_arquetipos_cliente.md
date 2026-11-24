# 06 · Arquetipos de cliente (marco Momentos de la Verdad), versión corregida

**USO INTERNO.** Cifras de CRM (leads, encuestas post-venta, servicio técnico). No publicable.
Fecha: 2026-11-23. Fuentes: `research/01_zmot.md`, `02_fmot.md`, `03_smot.md`, `04_umot_demografia.md`, `05_contexto_web.md`. Scripts en `analisis/` (solo lectura de `inputs_clean/`). No se abrió `inputs_raw/`.
Revisión: incorpora las decisiones de coordinación sobre la auditoría MdV (G): fusión de personas, base de C-05, hipótesis C-09b y C-13, y limitación de independencia.

## 1. Regla aplicada

- Se juntan los candidatos a miedo de ZMOT, FMOT, SMOT y UMOT en familias por **objeto del miedo**.
- Una familia cuenta como **momento con [DATO]** si tiene al menos una métrica [DATO] que mide ese objeto. Una métrica que solo mide una opción de pedido de información o una palabra clave cuenta como [HIPÓTESIS].
- La familia es **candidata a persona** si tiene [DATO] en al menos 3 de 4 MdV.
- **Limitación explícita:** la regla cuenta **momentos**, no **personas independientes**. UMOT es un pool que repite a los respondentes de FMOT (venta) y SMOT (taller). Por eso "3 de 4" puede significar 2 poblaciones. El solapamiento se mide en la sección 4 (script `analisis/7G_solapamiento_personas.py`).
- Comparación **por tasa dentro de cada MdV**, no por n absoluto. Los n de UMOT son ítems-respondentes y no se suman entre MdV.
- Máximo 5 personas.

**Lectura de la regla de decisión (coordinación):** se adopta la propuesta de G: P2 absorbe P4 y P5 (fusión, con el solapamiento como evidencia). P1 y P3 pasan a hipótesis, fuera de persona. El resultado es **una persona (F)** y **dos hipótesis de proceso (H1, H2)**.

## 2. Tabla de candidatos

Bases: ZMOT = 1.003 leads. Dentro de ZMOT, **431 respondieron la pregunta de contacto** (base de C-05); 558 con texto "¿Por qué?"; 138 con texto y evaluación 1-2. FMOT = Venta-Nuevo 6.458 (detractores 348) y Venta-Usados 4.103 (detractores 313). SMOT = Mecánica 27.516 (detractores 2.497). UMOT = pool de ítems ≤2 (Mecánica 3.399; Venta-Nuevo 614; Venta-Usados 413; Clicar 70). Fecha de extracción 2026-11-23.

Columnas: ID · MdV · métrica · n / base · tasa · etiqueta · fuente (script, columna, filtro).

### Familia F-SIL · silencio y falta de respuesta

| ID | MdV | Métrica | n / base | Tasa | Etiqueta | Fuente |
|---|---|---|---|---|---|---|
| C-05 | ZMOT | "No" a "¿Ha sido contactado por nuestro equipo de ventas luego de su solicitud de cotización?" | 60 / 431 respondidos | **13,9 %** | [DATO] | `zmot_leads.py`; Lead-Portillo. Base corregida (v1 usaba 1.003; ver nota de año) |
| C-05-año | ZMOT | Mismo "No", por año de fecha de respuesta: 2024 · 2025 · 2026 | 13 / 265 · 28 / 119 · 19 / 47 | 4,9 % · 23,5 % · 40,4 % | [DATO] | `analisis/8H_c05_por_anio.py`, columna de contacto, por `fecha respuesta`; reproducido con la base de C-05. 2023 (294 leads) no tiene respuesta a la pregunta. Con n=47 en 2026 es una señal, no una tasa |
| C-05b | ZMOT | Motivo "Sin respuesta o sin contacto" (palabras clave) | 39 / 558 | 7,0 % | [HIPÓTESIS] | `zmot_leads.py`. v1 = 61 (no reproducible con el script actual) |
| C-06 | FMOT | Facilidad de comunicación con vendedor, detractores 1-2: Nuevo / Usados | 98 / 348 · 84 / 313 | 28,2 % · 26,8 % | [DATO] | `fmot_mapa_empatia.py`. Mide facilidad, no respuesta |
| C-07 | SMOT | Facilidad para comunicarse con el servicio técnico, nota ≤3 en detractores | 1.620 / 2.497 | 64,9 % | [DATO] | `smot_mecanica.py`. Proxy de fricción de comunicación, no silencio observado |
| C-08 | UMOT | Ítem "Comunicación" ≤2 en pool (etiqueta del script: "Miedo a quedar sin respuesta"): Mecánica / vendedor Nuevo / vendedor Usados / Clicar | 1.189 / 3.399 · 103 / 614 · 87 / 413 · 35 / 70 | 35,0 % · 16,8 % · 21,1 % · 50,0 % | [DATO] | `umot_02_miedos_umot.py`. El ítem mide comunicación, la palabra "sin respuesta" es del script |

**Veredicto F-SIL:** silencio directo [DATO] solo en ZMOT (C-05). En venta y taller se mide fricción de comunicación (C-06, C-07, C-08). Con la regla literal, cuatro momentos tienen [DATO]. Con la regla de "silencio" estricta, solo uno. Se acepta como fricción de comunicación en F.

### Familia F-INFO · no saber qué se hizo o qué pasa con el auto

| ID | MdV | Métrica | n / base | Tasa | Etiqueta | Fuente |
|---|---|---|---|---|---|---|
| C-13 | ZMOT | Opción "Mayor información del vehículo" | 10 / 431 | 2,3 % | [HIPÓTESIS] | `zmot_leads.py`. Es un pedido de información, no un miedo (decisión de coordinación) |
| C-13b | ZMOT | Motivo "Información o documentación" (palabras clave) | 71 / 558 | 12,7 % | [HIPÓTESIS] | `zmot_leads.py` |
| C-14 | FMOT | Información proporcionada por el vendedor, detractores 1-2 (solo Nuevo) | 108 / 348 | 31,0 % | [DATO] | `fmot_mapa_empatia.py`. No hay columna equivalente en Usados |
| C-15 | SMOT | Claridad sobre la reparación o mantenimiento, nota ≤3 en detractores | 1.735 / 2.497 | 69,5 % | [DATO] | `smot_mecanica.py` |
| C-16 | UMOT | Ítem "Claridad de reparación" ≤2 en pool de Mecánica (etiqueta del script: "reparación no explicada") | 1.210 / 3.399 | 35,6 % | [DATO] | `umot_02_miedos_umot.py` |

**Veredicto F-INFO:** [DATO] en FMOT, SMOT y UMOT (3 momentos). ZMOT solo [HIPÓTESIS]. **Candidata a persona.**

### Familia F-TRATO · trato, acogida y atención personal

| ID | MdV | Métrica | n / base | Tasa | Etiqueta | Fuente |
|---|---|---|---|---|---|---|
| C-17 | ZMOT | Motivo "Trato o atención del ejecutivo" (palabras clave) | 5 / 558 | 0,9 % | [HIPÓTESIS] | **Descartado por n.** No cuenta como momento |
| C-18 | FMOT | Atención del vendedor, detractores 1-2: Nuevo / Usados · acogida en sala: Nuevo / Usados | 74 / 348 · 84 / 313 · 43 / 348 · 73 / 313 | 21,3 % · 26,8 % · 12,4 % · 23,3 % | [DATO] | `fmot_mapa_empatia.py` |
| C-19 | SMOT | Atención de personal ≤3 en detractores · acogida en sala de espera ≤3 · motivo "Atención" (macro) | 1.162 / 2.497 · 51,4 % de 2.497 · 882 / 1.835 | 46,5 % · 51,4 % · 48,1 % | [DATO] | `smot_mecanica.py` |
| C-20 | UMOT | Ítem "Acogida en sala de espera" ≤2 en pool (etiqueta del script: "mal trato en recepción"): Mecánica / Nuevo / Usados | 621 / 3.399 · 45 / 614 · 76 / 413 | 18,3 % · 7,3 % · 18,4 % | [DATO] | `umot_02_miedos_umot.py`. Etiqueta "mal trato" no corresponde al ítem (D-A1) |

**Veredicto F-TRATO:** [DATO] en FMOT, SMOT y UMOT. ZMOT descartado por n. **Candidata a persona** (dentro de F).
**Límite de valencia:** "Atención" es el motivo dominante de promotores (82 % Venta; 76,9 % Mecánica). La familia mide un tema que también sostiene las notas altas. Las tasas de detractores (21-51 %) la hacen un miedo; no hay tasa de promotores con ≤2 en el archivo para comparar.

### Familia F-COST · costo o financiamiento poco claro (hipótesis H2)

| ID | MdV | Métrica | n / base | Tasa | Etiqueta | Fuente |
|---|---|---|---|---|---|---|
| C-09 | ZMOT | Motivo "Precio o transparencia" / "Financiamiento o parte de pago" (palabras clave) | 40 y 23 / 558 | 7,2 % y 4,1 % | [HIPÓTESIS] | `zmot_leads.py` |
| C-09b | ZMOT | Opción "Información de financiamiento" | 14 / 431 | 3,2 % | [HIPÓTESIS] | `zmot_leads.py`. Pedido de información, no miedo (decisión de coordinación) |
| C-10 | FMOT | Claridad de precios y financiamiento, detractores 1-2: Nuevo / Usados | 70 / 348 · 79 / 313 | 20,1 % · 25,2 % | [DATO] | `fmot_mapa_empatia.py` |
| C-11 | SMOT | Claridad de precios y costos, nota ≤3 en detractores | 1.757 / 2.497 | 70,4 % | [DATO] | `smot_mecanica.py` |
| C-12 | UMOT | Costos o precio/financiamiento poco claros (ítem ≤2 en pool): Mecánica / Nuevo / Usados | 1.311 / 3.399 · 76 / 614 · 86 / 413 | 38,6 % · 12,4 % · 20,8 % | [DATO] | `umot_02_miedos_umot.py` |

**Veredicto F-COST:** [DATO] en FMOT, SMOT y UMOT, con ZMOT solo [HIPÓTESIS]. Con la regla literal cumple 3 momentos. **Pasa a hipótesis H2 fuera de persona:** sus dos sustentos de leads (C-09, C-09b) son [HIPÓTESIS], y su solapamiento con F-INFO y F-SIL no está medido en la misma base. Ver sección 5.

### Familia F-DEM · demora y proceso lento (hipótesis H1)

| ID | MdV | Métrica | n / base | Tasa | Etiqueta | Fuente |
|---|---|---|---|---|---|---|
| C-01 | ZMOT | Motivo "Lentitud o tiempos" (palabras clave) | 132 / 558 | 23,7 % | [HIPÓTESIS] | `zmot_leads.py`. v1 = 85 (no reproducible) |
| C-02 | FMOT | Fluidez general del proceso, detractores 1-2: Nuevo / Usados | 202 / 348 · 159 / 313 | 58,0 % · 50,8 % | [DATO] | `fmot_mapa_empatia.py` |
| C-03 | SMOT | Tiempo de entrega del vehículo, nota ≤3 en detractores | 1.521 / 2.497 | 60,9 % | [DATO] | `smot_mecanica.py` |
| C-04 | UMOT | Proceso largo o desordenado (ítem ≤2 en pool): Mecánica / Nuevo / Usados | 1.191 / 3.399 · 217 / 614 · 170 / 413 | 35,0 % · 35,3 % · 41,2 % | [DATO] | `umot_02_miedos_umot.py` |

**Veredicto F-DEM:** [DATO] en FMOT, SMOT y UMOT (3 momentos). **Pasa a hipótesis H1 fuera de persona:** su evidencia de venta (C-02, C-04-venta) y de taller (C-03, C-04-taller) son dos poblaciones, y UMOT repite a los mismos respondentes de FMOT (93 %) y SMOT (86 %). Ver sección 4.

### Familias que no pasan la regla (hipótesis)

| ID | Familia | Evidencia [DATO] por momento | Decisión |
|---|---|---|---|
| C-21 | Reparación mal hecha / trabajo mal hecho | SMOT: reparado = No en detractores 1.097 / 2.497 (43,9 %); calidad del servicio ≤3 1.953 / 2.497 (78,2 %). UMOT: trabajo mal hecho 1.355 / 3.399 (39,9 %) | **2 momentos, misma encuesta de taller → hipótesis.** Es la familia de mayor n en taller. De los 1.735 detractores con claridad de reparación ≤3, 968 (55,8 %) tienen reparado = No (solapamiento con F-INFO) |
| C-22 | Tasación / parte de pago | FMOT: parte de pago ≤2 en detractores Nuevo 27 / 124 (21,8 %), Usados 42 / 106 (39,6 %). UMOT: oferta baja o poco clara en Clicar 46 / 70 (65,7 %) | ZMOT solo [HIPÓTESIS]. Clicar 2023-06 a 2024-04, desactualizado. **Hipótesis** |
| C-23 | Terminación del vehículo entregado | FMOT: motivo "Condición del vehículo" detractores Usados 52 / 214 (24,3 %), Nuevo 32 / 261 (12,3 %) | SMOT: lavado sin distribución (**NO VERIFICADO**). **1 momento → hipótesis** |
| C-24 | Documentación / trámite | FMOT: motivo "Documentación" detractores Nuevo 39 / 261 (14,9 %), Usados 24 / 214 (11,2 %). UMOT: trámite complicado en Clicar 42 / 70 (60,0 %) | ZMOT solo [HIPÓTESIS]. **Hipótesis** |
| C-25 | Cumplimiento de lo acordado | SMOT: micro "Cumplimiento de acuerdos" 376 / 2.146 categorizados (17,5 %) | **1 momento → hipótesis** |
| C-26 | Stock / disponibilidad; reserva o devolución | ZMOT: keyword 12 / 558 (2,2 %) y 13 / 558 (2,3 %) | **Descartados** por n y por momento |

## 3. Resultado

**Persona (1):**

| Persona | Familias fusionadas | Momentos con [DATO] | Poblaciones |
|---|---|---|---|
| **F · El que no recibe respuesta, explicación ni buen trato** | F-SIL (fricción de comunicación), F-INFO, F-TRATO | ZMOT (C-05, solo silencio directo), FMOT, SMOT, UMOT: 4 momentos con [DATO] | leads, venta, taller |

**Hipótesis fuera de persona:**

| ID | Hipótesis | Momentos con [DATO] | Por qué no es persona |
|---|---|---|---|
| H1 | Proceso largo o sin fecha (F-DEM) | 3 (FMOT, SMOT, UMOT) | Dos poblaciones (venta y taller). UMOT repite FMOT (93 %) y SMOT (86 %). Sin ZMOT [DATO] |
| H2 | Costo o financiamiento poco claro (F-COST) | 3 (FMOT, SMOT, UMOT), con ZMOT solo [HIPÓTESIS] | Sustento de leads [HIPÓTESIS]. Solapa con F-INFO y F-TRATO |
| H3 | Reparación mal hecha (C-21) | 2 (SMOT, UMOT, misma encuesta) | Solo taller. La mayor familia de taller; sin ZMOT ni FMOT |

Y las familias C-22 a C-26 (sección 2).

**Por qué F es una sola persona y no tres.** F-INFO y F-TRATO tienen el mismo patrón de respondentes que F-SIL en venta y taller (sección 4). La separación en tres personas no aparece en la base de respondentes. La fusión se justifica por el solapamiento, no por la regla de 3 momentos.

## 4. Solapamiento de respondentes (script `analisis/7G_solapamiento_personas.py`)

Salida verificada (solo lectura; sin clave entre archivos, el solapamiento se mide dentro de cada archivo). Las personas son las de la fase previa (P1 a P5) y se usan como grupos de familias.

**Dentro de cada persona: FMOT o SMOT contra UMOT (mismos respondentes)**

| Persona previa | Archivo | FMOT / SMOT | UMOT | En ambos | % de UMOT en FMOT o SMOT |
|---|---|---:|---:|---:|---|
| P1 | Venta-Nuevo | 202 | 217 | 202 | 93 % |
| P2 | Venta-Nuevo | 98 | 103 | 98 | 95 % |
| P3 | Venta-Nuevo | 70 | 76 | 70 | 92 % |
| P1 | Venta-Usados | 159 | 170 | 159 | 94 % |
| P2 | Venta-Usados | 84 | 87 | 84 | 97 % |
| P3 | Venta-Usados | 79 | 86 | 79 | 92 % |
| P1 | Mecánica | 1.521 | 1.191 | 1.024 | 86 % |
| P2 | Mecánica | 1.620 | 1.189 | 1.097 | 92 % |
| P3 | Mecánica | 1.757 | 1.311 | 1.099 | 84 % |
| P4 | Mecánica | 1.735 | 1.210 | 1.170 | 97 % |
| P5 | Mecánica | 1.162 | 621 | 520 | 84 % |

**Entre personas previas: respondentes únicos y solapamiento (Jaccard = |A∩B| / |A∪B|)**

| Archivo | Respondentes en ≥2 personas | Pares con más solapamiento |
|---|---|---|
| Venta-Nuevo (detractores 348) | 148 de 256 (58 %) | P2-P4 53 %, P4-P5 56 %, P2-P5 52 % |
| Venta-Usados (detractores 313) | 122 de 219 (56 %) | P2-P5 52 %, P1-P5 44 % |
| Mecánica (detractores 2.497) | **2.105 de 2.681 (78,5 %)** | P2-P4 63 %, P1-P2 63 %, P3-P4 61 %, P1-P4 60 % |

Lectura: ninguna pareja es la misma gente (máximo 63 %). Pero en taller la mayoría de los detractores aparecen en varias familias. La fusión en F es el resultado natural de ese solapamiento.

## 5. Qué NO sabemos y pruebas pendientes

- **Solapamiento de Mecánica:** 78,5 % (2.105 de 2.681 respondentes) aparecen en al menos dos personas previas. Es la limitación más fuerte para decir que son grupos distintos. Dependencia: Beto (clave de respondente en CRM, si existe).
- **ZMOT real:** no hay datos de visitantes que no cotizaron. Dependencia: Beto (analítica web).
- **C-05 por año:** 2023 no tiene respuesta a la pregunta de contacto (294 leads). La subida de 4,9 % a 40,4 % puede venir de un cambio de captura. Prueba: CRM debe dar la fecha en que empezó a capturarse el campo. Dependencia: Beto.
- **Fecha de corte de leads (2026-01-23):** NO VERIFICADO si es de exportación. Dependencia: Beto.
- **Escala de cotización y de calidad del contacto:** dirección NO VERIFICADA. Dependencia: Beto.
- **Palabras clave (ZMOT):** C-01, C-05b, C-09, C-13b y C-24 dependen de una regla no validada. Prueba: dos codificadores ciegos sobre 100 textos. Dependencia: Beto.
- **C-07 y C-08:** miden facilidad de comunicación, no respuesta. Prueba: CRM con tiempo de primera respuesta. Dependencia: Beto / equipo comercial Portillo.
- **C-14:** solo existe en Nuevo. En Usados no hay columna equivalente.
- **C-21 (reparación mal hecha):** la mayor familia de taller, fuera de persona. Prueba: segunda MdV independiente o CASOS_PBI (**BLOQUEADO**, depende de Beto).
- **C-22 (tasación):** significado de la pregunta de parte de pago. Dependencia: Beto.
- **C-23 (terminación):** clasificar los 52 textos de "Condición del vehículo". Dependencia: Beto (codificación).
- **Portillo:** toda cifra de Portillo depende de la asignación (Beto / Iván Balaguera). Ver D-N1 a D-N7 en `research/00_contradicciones.md`, sección Fase 1.
- **Clicar:** datos 2023-06-30 a 2024-04-08, desactualizados. Dependencia: Beto.
- **Cruce lead→venta:** no hay clave verificada. Dependencia: Beto / Iván Balaguera. No se afirma conversión.
- **Demografía:** solo seguridad vial (n=709; clientes de auto nuevo; 2025-10-22 a 2025-10-29). No cruza con ninguna familia. NO VERIFICADO por persona.

## 6. Cifras reproducidas y no reproducidas

- **Reproducidas por script:** todas las de la tabla salvo las marcadas abajo.
- **No reproducibles con el script actual:** cifras de v1 (C-01 "85", C-05b "61"). Solo contexto.
- **Consulta directa a `inputs_clean/` (sin línea de script):** 163 (campaña "Venta Usados Clicar", D-N2) y 1.313 (campaña "Venta Nuevo Portillo", D-N3, bruto). Se muestran en contradicciones con esa marca.
- **C-05-año:** `analisis/8H_c05_por_anio.py` (solo lectura de `inputs_clean/CR_Lead-Portillo`), coincide con la base de C-05 (431 respondidos; 60 "No").
