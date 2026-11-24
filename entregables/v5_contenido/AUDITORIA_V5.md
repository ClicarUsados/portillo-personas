# Auditoría red-team · Proyecto v5 · Antonia y Tomás Pascual

USO INTERNO · 2026-11-24 · Auditor: agente red-team (lectura, sin cambios en entregables).
Restricciones respetadas: no se abrió inputs_raw/, no hay commit, no se borró nada, no se crearon tareas en Asana ni se publicó en redes.

Etiquetas: [DATO] (archivo, columna/filtro, n, row_id) · [PLAN] (página) · [WEB] · [ILUSTRATIVO] · [HIPÓTESIS] · NO VERIFICADO.

---

## 0. Veredicto

| Persona | Veredicto | Motivo corto |
|---|---|---|
| **Antonia** | **Cae** como estrategia de persona | Su perfil es Javiera con otro nombre (similitud de tokens 0,967). Ninguno de sus 4 pilares tiene cluster propio estable con n suficiente: P1 apoya en A2 (0,59, bajo umbral) y en A0 (0,68, n = 6, concepto genérico). P2 y P4 no tienen dato propio. P3 es dato del grupo, no de Antonia. |
| **Tomás** | **Cae** como estrategia de persona | n = 19 (bajo 20). Su lenguaje de valor es el de Antonia (6 de 9 conceptos repetidos). Su pilar señal P1, que es el 31 % de la parrilla, no tiene cluster. La única diferencia real es el dolor de ficha, que viene del grupo y no de sus textos. Hay una cifra de stock en una pieza pública. |

Lo que sobrevive como [DATO] es el contenido de **grupo**: entrega, precio o ficha que no calza, respuesta al aviso y tasación. Eso se puede usar como pilares de marca, no como estrategias separadas por persona.

**Porcentaje de pilares** (9 pilares en total: 4 de Antonia y 5 de Tomás):
- [DATO] con cluster propio estable (≥ 0,6) y n ≥ 20: **0 de 9 (0 %)**.
- [DATO] solo a nivel de grupo o con n < 20: **3 de 9 (33 %)**. Son P3 de Antonia (grupo D1), P2 de Tomás (T0, n = 19, exploratorio) y P4 de Tomás (T1, igual a Antonia).
- [HIPÓTESIS]: **6 de 9 (67 %)**.

---

## 1. Verificación por punto

### 1. Cada pilar y creatividad tiene concepto con dato

Confirmado en CSV y JSON (no en la prosa):
- `conceptos_antonia.csv`: atención A2 estabilidad 0,59 · excelente A0 0,68 (n = 6) · rapidez A3 0,55 · amable A1 0,16.
- `conceptos_tomas.csv`: excelente/atención T1 0,82 · vendedor/solución/compra T0 0,75 (n = 19).
- `resumen_ejecucion.json` coincide con las cifras del CSV (0,675 → 0,68; 0,161 → 0,16; 0,593 → 0,59; 0,555 → 0,55; 0,753 → 0,75; 0,824 → 0,82; dolor D1 0,874 → 0,87).

Hallazgos:
- Antonia P1 (el "ancla" de su estrategia) se apoya en A2 con 0,59. Está marcado [HIPÓTESIS] y el texto lo dice bien.
- Tomás P1 (31 % de la parrilla, 5 de 16 filas) dice "Sin cluster estable" y aun así es el pilar con más peso. Es la mayor incoherencia de la parrilla.
- Antonia P3 y Tomás P2 citan como "[DATO] cluster estable" el cluster D1 o T0. D1 es del grupo, no de la persona. T0 tiene n = 19.
- Caveat de D1: el cluster incluye "vehículo", que puede venir de la pregunta de parte de pago (el propio ESTRATEGIA_ANTONIA lo reconoce). No se resolvió.
- Creatividades: todas apuntan a un pilar. El concepto de origen es [HIPÓTESIS] en los territorios de Antonia (T1 sobre atención A2 0,59; T2 sin cluster; T3 sobre D1 del grupo) y en los de Tomás (T1 sin cluster; T2 sobre T0 con n = 19; T3 sin cluster). Ningún territorio tiene concepto propio estable y con n ≥ 20.

### 2. Diferenciación Antonia vs Tomás

Medido sobre los conceptos de valor (dolor e intención son compartidos y se excluyen):
- Conceptos de valor: Antonia 20 · Tomás 9 · compartidos 6 (atención, excelente, excelente atención, vendedor, auto, compra). Unión 23. **Jaccard = 0,26**.
- Top 3 de cada persona: Antonia {atención, excelente, excelente atención}; Tomás {excelente, vendedor, atención}. **Coinciden 2 de 3**.
- Pilares: no hay nombres repetidos, pero Antonia P1 ("Como siempre", atención) y Tomás P4 ("El trato que se nota", excelente/atención) son el mismo concepto con otro nombre. Antonia P2 (tasación) y Tomás P1 (ficha que es contrato) comparten el mismo dolor de grupo (tasación 39,6 % vs precio/ficha 39,9 %).
- Verbatims: **0 de 10** row_id compartidos entre los dos perfiles, y 0 entre las dos estrategias. Eso no basta para diferenciarlas: el mismo tema aparece en ambas con citas distintas.

Conclusión: **se diferencian en canal, dolor de llegada y mezcla de pilares, pero no en el valor que dicen tener**. "Lo que sostiene la diferencia" es un dato del grupo, no de cada persona. Si Beto quiere presentar dos personas, la evidencia que falta es:
1. Validar la regla de asignación (canal + parte de pago) contra una variable real del CRM. Hoy el código de "parte de pago" 1–5 no tiene diccionario.
2. Llegar a n ≥ 20 por persona con la misma regla en otra campaña o período.
3. Prueba de permutación: reasignar al azar las etiquetas Antonia/Tomás y ver si la diferencia de c-TF-IDF o de Jaccard aparece igual. Si aparece, la diferencia es ruido.
4. Un corte de dolor de llegada en el lead (no solo en la venta) que separe por canal con n suficiente.

### 3. Ninguna pieza pública trae términos prohibidos ni cifras internas

Escaneo de columnas hook, copy, CTA y formato de ambos CSV (32 filas) más las piezas de las estrategias:
- "usado", "cobertura mecánica hasta 12 meses", "garantía de excelencia", "satisfacción garantizada", "precio líder", "inspección de X puntos": **ninguna aparece en las piezas de los CSV**.
- **Incumplimiento**: PARRILLA_TOMAS, S3-2026-12-08, copy de landing: "Tres autos en stock con precio, cuota y año." Es una cifra de stock en pieza pública. Además contradice la propia fila que dice "Sin cifra de stock". Hay que quitar "Tres autos".
- **Riesgo**: el WhatsApp 56978532401 aparece en carrusel, reel y landing de Tomás. No está verificado que sea la línea comercial de Portillo y no un número personal. NO VERIFICADO. Confirmar con Beto antes de publicar.
- **Riesgo**: "Cupo de prueba sujeto a disponibilidad" (S2, promo) y "Autos publicados esta semana" con "disponibilidad NO VERIFICADO": promesa sin respaldo.
- **Riesgo**: "Inspección agendada al cotizar" (landing de Antonia) está como bracket, pero si sale en pieza es una promesa de inspección que el plan no confirma: solo 16 % de las tasaciones llega a inspección [PLAN p.02].
- "Usado" aparece solo en nombres de búsqueda y en la nota de canal "Portillo Usados", que no son pieza. Correcto.
- Cifras internas: no aparecen NPS, n, CRM ni margen en las piezas. Sí aparecen en las secciones de estrategia, que son internas.

### 4. Garantía: plazo en piezas

- [PLAN] p.05 dice "3 meses de garantía" para Portillo. Confirmado en research/10_plan_premium.md.
- Brandbook con 12 meses (p. 19): **no re-verificado en esta auditoría**. Lo cita ESTRATEGIA_TOMAS; no abrí el PDF.
- En los CSV no hay ningún plazo de garantía. Confirmado.
- **Excepción**: ESTRATEGIA_TOMAS §5.5, bloque 2 de landing, dice "garantía con T&C (plazo pendiente de confirmar)". Mencionar la garantía sin plazo es copy público con promesa sin respaldo. Quitarla hasta tener T&C.
- Antonia V2 y Tomás V2 usan "seminuevo con garantía" como término de búsqueda. Es uso interno, no pieza. Correcto.

### 5. Parrilla: distribución real vs objetivo

Conteo sobre los CSV (no sobre el texto):

| Persona | P1 | P2 | P3 | P4 | P5 | Promo | Objetivo |
|---|---|---|---|---|---|---|---|
| Antonia (16 filas) | 4 (25 %) | 5 (31 %) | 4 (25 %) | 3 (19 %) | — | **0 %** | P1 30 · P2 25 · P3 25 · P4 20 |
| Tomás (16 filas) | 5 (31 %) | 4 (25 %) | 4 (25 %) | 1 (6 %) | 2 (12,5 %) | **12,5 %** | P1 30 · P2 25 · P3 20 · P4 15 · P5 10 |

- Confirmo la distribución del subagente de Tomás: 31/25/25/6/12. El redondeo de P5 es 12,5 %.
- **Error en ESTRATEGIA_TOMAS**: dice "Promocional: 10 %" y "2 de 16", pero 2/16 = 12,5 %. Corregir el número.
- El tope de 30 % se cumple en ambos (0 % y 12,5 %).
- Desviación de Tomás: P4 vale 6 % contra 15 % objetivo; P1 queda 31 % contra 30 % objetivo, pero P1 no tiene cluster.
- Antonia: 8 de 16 filas en estado "bloqueado" y las 8 restantes en "borrador". **Ninguna fila es publicable hoy**.
- Tomás: 16 de 16 en estado "propuesta". Tampoco hay ninguna publicable hoy.
- **Falta** PARRILLA_4_SEMANAS.csv combinado (lo pedía el PROMPT en Fase 2.5). Solo existen las dos parrillas por persona. Registrado como entregable incompleto.

### 6. Contradicciones (ambas cifras, sin resolver)

**6.1 Antonia/Javiera: "auto que quería estaba acá" o "ya cliente"**
- Ficha (PERFIL_ANTONIA y PERFIL_TOMAS): "El auto que quería estaba acá" 16 de 60 (27 %); "ya era cliente" 13 de 60 (22 %).
- research/11 §3 (n = 95): "auto que quería estaba acá" 22; "ya era cliente" 18.
- Lectura: el de 60 es la subcohorte de zona oriente (script v3). Sin cruzar la base canal × zona no se puede saber si concilian. La ficha no declara que 60 es subconjunto de 95. **Sin resolver**; el cruce está pendiente.

**6.2 Antonia: "volverían"**
- Ficha (Javiera/Antonia, journey "Advocacy"): "60 de 60 promotores de la zona dicen que sí".
- research/11 §3 (n = 95): "94 de 95 Sí", 1 "No sé".
- Son compatibles si los 60 son subconjunto de los 95 (34 de 35 fuera de zona habrían dicho sí). Pero la ficha presenta 60/60 como cifra de la zona sin mostrar el universo. **Sin resolver**; la ficha debe declarar el universo o no usar la cifra.

**6.3 Dolor "ejecutivo/contacto" inflado**
- Dolor pool: "ejecutivo" 306, "contacto" 279, "contacto ejecutivo" 276, cluster D2 estabilidad 0,96 [DATO, conceptos_*.csv].
- Origen: "Ya estoy en contacto con mi ejecutivo" = 275 de 431 leads (64 %) [METODO §2].
- research/00 #13: "60 leads con ¿Ha sido contactado? = No; 10 de ellos responden 'ya estoy en contacto'". Por eso el 13,9 % de Tomás (60/431) incluye 10 que dicen estar en contacto. Neto: **50/431 = 11,6 %**. Sin resolver.
- La estabilidad 0,96 de D2 no prueba nada: los textos repetidos inflan la estabilidad.

**6.4 Tamaño de corpus de Tomás**
- Tomás = 19 textos. Común = 6. Ambos < 20. Confirmado en METODO §2 y resumen_ejecucion.json.
- Antonia = 31 (≥ 20). Su análisis es exploratorio igual, por el umbral de estabilidad.

### 7. Detector de ruido y abogado del diablo

Las dos skills cargaron y devolvieron sus instrucciones; no ejecutaron un análisis propio. Aplico sus criterios directamente sobre los archivos. Nota: METODO §7 dice que tampoco devolvieron resultados en la ejecución anterior. Esta auditoría repite el ejercicio por mi cuenta.

**Ruido que cambia decisiones (máximo 3):**
1. **Dolor de "ejecutivo" es un estado, no un dolor.** Hipótesis en competencia: (a) el lead quiere contacto y es un dolor real; (b) es una opción cerrada del formulario que se marcó por defecto. Prueba barata: recalcular el pool de dolor sin esa opción y ver si D1 (vehículo, entrega, información) sigue arriba. Cambia la decisión de P2 de Tomás. Confianza en "respuesta al aviso como dolor": baja.
2. **Antonia y Tomás son la misma persona en valor.** Hipótesis en competencia: (a) hay dos segmentos con la misma voz; (b) la regla de asignación no separa nada. Prueba: permutación de etiquetas (punto 2.3). Cambia si hay dos personas o una sola con dos canales. Confianza: moderada.
3. **La "Antonia" es Javiera.** Hipótesis en competencia: (a) es un renombre de la misma ficha y la persona no tiene datos propios; (b) dos perfiles construidos de forma independiente que casualmente coinciden en 41 años, La Dehesa, dos hijos, ingeniera comercial, y las mismas cifras de sucursal (13 y 11), RAV4 6 de 60 y "60 de 60". La (b) es casi imposible. Confianza en (a): alta.

**Ruidos menores:**
- Parte de pago 1–5 sin diccionario, y la asignación de Antonia usa "con parte de pago" como criterio. Si los códigos están invertidos, la asignación se invierte.
- "Parte de pago aplica a 40 de 95" (research/11) y "26 de 60 usaron parte de pago" (ficha Antonia) y "34 de 60 no usaron" (ficha Tomás): los números no son consistentes entre sí dentro de los mismos documentos.
- 6 filas de dolor son también promotores/corpus de persona: el solapamiento de corpus infla n.

**Abogado del diablo, pre-mortem y ejecución en piso:**
- Pre-mortem de Antonia: "Te atendemos como siempre" le dice a alguien que nunca fue cliente que ya lo conocemos. El primer comentario en redes es "yo nunca fui". Ruido de marca, no de datos.
- Pre-mortem de Tomás: la pieza "Escribe por el aviso" promete respuesta. Si el plazo no está confirmado y el vendedor tarda, la pieza es la primera queja del mes.
- Ejecución en piso: campaña de "Agenda tu tasación" lleva tráfico a un proceso donde solo 16 % llega a inspección [PLAN p.02]. Se llena el embudo en la parte que se cae.
- Ejecución en piso: "fecha de entrega confirmada por escrito" depende de la sucursal. El dolor más grande del grupo es entrega sin fecha (77,3 %). Si la sucursal no cumple, la pieza aumenta la queja.
- Variable omitida: precio, modelo y plazo no están en los textos. Un detractor puede serlo por el auto y no por la atención. No se controló.

**Lo que no resiste y pasa a [HIPÓTESIS]:** diferencia Antonia vs Tomás; narrativa "transparencia" de Tomás (no aparece entre sus conceptos); dolor "respuesta al aviso" como dolor de Tomás; clusters A1, A2 y A3; todo concepto de búsqueda (26 consultas redactadas a mano, sin volumen).

### 8. Re-verificación de row_id contra inputs_clean (solo lectura, sin imprimir texto)

Tres row_id tomados al azar de `analisis/v5_nlp/corpus/corpus_antonia.csv`, comparados contra `inputs_clean/CR_2025-Venta-Usados_*.parquet` (columna `row_id`, texto = concatenación de las tres columnas libres):

| row_id | Existe en inputs_clean | Campaña "2025 - Venta Usados Portillo" | Solapamiento de tokens con el corpus anonimizado |
|---|---|---|---|
| CR_2025-Venta-Usados#3591 | Sí (1 fila) | Sí | 1,00 |
| CR_2025-Venta-Usados#3409 | Sí (1 fila) | Sí | 0,83 |
| CR_2025-Venta-Usados#3762 | Sí (1 fila) | Sí | 0,91 |

Lectura: los tres coinciden. El solapamiento menor a 1,00 es esperable porque el NER reemplazó nombres por PERSONA. Veredicto: **confirmado en 3 de 3**. Esto no valida los 56 textos del corpus; solo muestra que el mapeo row_id → fila es correcto.

Nota: el propio row_id de la ficha (#3764, #3290, #3514, #2256, #3477, #3803, #4103, #3604, #3915, #3361) no fue re-verificado. Pendiente antes de cualquier publicación.

### 9. ¿Antonia es Javiera renombrada?

**Sí, con alta confianza.**
- Javiera Correa, 41 años, La Dehesa/Lo Barnechea, casada, dos hijos, ingeniera comercial. Antonia Correa, 41 años, La Dehesa/Lo Barnechea, casada, dos hijos, ingeniera comercial.
- Mismas sucursales de referencia (La Dehesa 13, Padre Hurtado 11), mismo RAV4 6 de 60, mismo "60 de 60", mismo journey, mismos verbatims (#3764, #3290, #3514, #2256, #3477).
- Similitud de tokens entre los dos HTML: **0,967**. Diferencias: el nombre, y la línea "zona definida por Beto" que solo está en Javiera.
- Bloqueo B-7 ya lo reconoce. Sin respuesta de Beto.

Consecuencia: la ficha de Antonia no es una persona nueva con datos propios. Es el mismo perfil. Si Beto quiere mantener dos perfiles, Antonia debe reconstruirse desde su corpus (n = 31), o declararse como ILUSTRATIVO compuesto.

### 10. Afirmaciones débiles y qué las cerraría

| Afirmación | Dónde | Qué la cerraría |
|---|---|---|
| "Atención es el motivo principal de la zona" | ESTRATEGIA_ANTONIA P1; ficha | Doble codificación de 56 textos por dos codificadores ciegos; kappa reportado |
| "Antonia cree en la atención personal" (narrativa) | ESTRATEGIA_ANTONIA §3 | No hay dato. Se cierra con prueba de permutación (punto 2) |
| "Tomás: transparencia" | ESTRATEGIA_TOMAS §1; ficha | Conteo de "transparencia", "lo que firmas", "publicado" en corpus de Tomás. Hoy no aparece en top |
| P2 de Tomás: "respuesta al aviso" como dolor | ESTRATEGIA_TOMAS | Tiempos de respuesta del CRM por lead de aviso; hoy sin dato |
| 13,9 % "sin contacto de ventas" | ESTRATEGIA_TOMAS; ficha | Neto de los 10 que dicen estar en contacto (50/431); ver 6.3 |
| "Entrega con fecha" como dolor de Antonia (P3) | ESTRATEGIA_ANTONIA | Dato del grupo ya existe (77,3 %). Lo que falta es si pasa en Portillo: 5 de 10 detractores, n chico |
| "Nunca me dejaron probar el auto" (P3 de Tomás) | ESTRATEGIA_TOMAS | Conteo de menciones de prueba de manejo en los 729 de dolor. Hoy es un verbatim |
| "Leads siguen al stock, r = 0,90" (P5) | [PLAN] p.06 | Tabla de stock (vacía) y export leads por auto. Bloqueo de responsable de stock |
| "Garantía 3 meses" como ventaja | ficha Tomás; plan | T&C escritos. Brandbook dice 12 (no re-verificado aquí) |
| "Kavak 12 meses" vs "7 días / 300 km" | ficha Tomás; research/10_contradicciones P6 | Captura fechada de la web de Kavak; plan sin fuente |
| 26 términos de búsqueda como intención | research/15; conceptos_*.csv | Volumen de búsqueda (Search Console o planificador) |
| "Volvería a comprar 94 de 95" | research/11 §3 | Recompra real en el CRM. Hoy es autoreporte, sin conversión |
| 0,9 % landing vs 2,3 % resto | [PLAN] p.02 | Sesiones y leads por landing. No se afirma conversión lead→venta |

---

## 2. Qué debe corregirse antes de comité

1. Quitar "Tres autos en stock" del landing de Tomás (cifra de stock en pieza pública).
2. Corregir "Promocional 10 %" a 12,5 % en ESTRATEGIA_TOMAS.
3. Quitar "garantía con T&C" del bloque 2 de landing hasta tener T&C.
4. Confirmar que 56978532401 es la línea comercial de Portillo. Si no lo es, reemplazar en todas las piezas.
5. Declarar el universo en la ficha: "60 de 60" y "16 de 60" son subconjunto de los 95 de research/11. Mostrar ambas cifras lado a lado, como pide el PROMPT (punto 9).
6. Reportar "60 sin contacto" neto de los 10 que dicen "ya estoy en contacto" (50/431). Recalcular el pool de dolor sin la opción cerrada.
7. Reescribir la parrilla de Tomás: P1 (31 %) no tiene dato. O se marca como hipótesis a validar con una pieza de prueba, o se baja a 20 %.
8. Decidir sobre Antonia: se reconstruye desde su corpus, o se declara compuesta e ILUSTRATIVA. No se publican las dos fichas como "construidas desde 60 promotores" sin aclarar que son el mismo perfil.
9. "Te atendemos como siempre" no se usa con quien llega por primera vez (Antonia). Cambiar el hook de GBP y de la historia.
10. Quitar "Inspección agendada" de piezas hasta confirmar que la sucursal la hace. Hoy solo 16 % llega a inspección.
11. Antes de cualquier verbatim público: verificar los 10 row_id de las fichas (solo 3 verificados aquí) y quitar los que nombran vendedores.
12. Crear PARRILLA_4_SEMANAS.csv combinado (pedido por el PROMPT, no existe).

---

## 3. Bloqueos con responsable

| Bloqueo | Responsable |
|---|---|
| Diccionario de "Vehículo en parte de pago" (códigos 1–5) y regla de asignación | Beto / CRM |
| Confirmar si Antonia es Javiera renombrada y qué hacer con ella | Beto |
| Cruce canal × zona (16/60 vs 22/95; 60/60 vs 94/95) | Beto / Iván Balaguera |
| Mapeo de sucursales del plan a las de la base | Beto / Iván Balaguera |
| T&C de garantía y plazo (3 vs 12 meses) | Beto + área legal de Americar (responsable NO VERIFICADO) |
| Plazo de respuesta al aviso y horario de prueba de manejo | Beto y jefatura de ventas; sucursal Bilbao |
| Tabla de stock por sucursal (plan p.06, vacía) | responsable de stock |
| Export de ventas ene–oct 2026 | Beto |
| Confirmar número de WhatsApp 56978532401 | Beto |
| Autorizar publicación de NUBE_CONCEPTOS (tiene verbatims) | Beto |
| Brandbook (12 meses) no re-verificado por el auditor | Beto |

---

## 4. Limitaciones de esta auditoría

- No abrí el brandbook ni la captura de Kavak; las cifras de garantía de competidor y de brandbook quedan sin re-verificar.
- Re-verifiqué 3 row_id de 56 y 0 de 10 de las fichas.
- Las skills detector-de-ruido y abogado-del-diablo se cargaron, pero no devolvieron un análisis propio: apliqué sus criterios manualmente.
- No se calculó conversión lead→venta. No se afirma.
