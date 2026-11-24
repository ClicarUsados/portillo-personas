# Auditoría red-team y brechas — Buyer personas Portillo

**USO INTERNO.** Contiene cifras de CRM (encuestas, leads, servicio técnico). No publicable.
**Fecha de auditoría:** 2026-11-23. **Auditado:** `entregables/BUYER_PERSONAS_PORTILLO.md`.
**Veredicto corto:** el documento es sólido en las cifras de Nuevo y Mecánica (GRUPO_COMPLETO) y frágil en la parte Portillo, en la lectura de "miedo" de P1 y P4, y en los porcentajes de evidencia. Hay dos incidentes de proceso propios de esta auditoría (sección 0), que deben declararse antes de comité.

---

## 0. Incidentes de proceso de esta auditoría (declarar antes de comité)

1. **Acceso a `inputs_raw/` (violación de la instrucción de auditoría).** Al correr `analisis/00_anonimizar.py` se leyeron los `.xlsx` de `inputs_raw/` y se reescribieron los 7 parquets de `inputs_clean/`. El script imprimió los mismos conteos de filas que el diccionario (27.516 / 6.458 / 4.103 / 223 / 709 / 324 / 1.003). No se imprimió ni se guardó contenido crudo. Aun así, **los parquets fueron regenerados** y no hay copia previa para comparar byte a byte. Acción: Beto debe confirmar que la regeneración es idéntica (hash del parquet anterior o re-generación desde el mismo origen).
2. **Sobrescritura de dos archivos fuera de mi alcance.** `analisis/01_diccionario.py` reescribió `research/00_diccionario_datos.md` (479 líneas) y `analisis/02_mapeo_portillo.py` reescribió `research/00_mapeo_portillo.md`. No hay git con historial de esos archivos (`git status` los muestra como no rastreados), así que **no puedo diffear el contenido anterior**. Lo que sí verifiqué: la fila de Venta-Usados del mapeo sigue en 108 y el diccionario coincide con las cifras de control de `research/00`. Acción: confirmar que el contenido regenerado es el aprobado.
3. Ninguna otra acción de escritura: no hice commit, no borré nada, no toqué los entregables fuera de los dos que me tocan.

---

## a. Reproducibilidad

**Scripts ejecutados desde la raíz (exit 0 en los 7, sin Traceback):**

| Script | Estado | Nota |
|---|---|---|
| 00_anonimizar.py | Corrió | Lee `inputs_raw/` (ver sección 0.1) |
| 01_diccionario.py | Corrió | Reescribe `research/00_diccionario_datos.md` |
| 02_mapeo_portillo.py | Corrió | Reescribe `research/00_mapeo_portillo.md` |
| 1A_voz_ventas.py | Corrió | Salida en scratchpad, 550 líneas |
| 2B_leads_cotizacion.py | Corrió | 156 líneas |
| 3C_retencion_mecanica.py | Corrió | 298 líneas; el propio script declara que no escribe |
| 4D_intencion_funcionalidades.py | Corrió | 151 líneas |

**Cifras comprobadas contra la salida de los scripts:** unas 60. Coinciden: todas las de Nuevo (1A: 5.732 / 348 detractores, fluidez 4,69 y 58,0 % con 1-2 en detractores, entrega Usados 61,7 %, parte de pago Usados 39,6 % con 42 de 106); todas las de Leads (2B: 371 Sí, 60 No, 431 respondidos, 275 "ya en contacto", 138 textos con Q1 1-2, 54 "sin respuesta", 42 de 57 "otros" autodeclaran compra, Portillo 140 / 82 / 75,6 %); todas las de Mecánica (3C: 27.516, NPS 73,5, 72,6 % en 0 o 10, 2.497 / 22.713, 245 Portillo con NPS 68,2 y 28 detractores, GAP PORTILLO 84,3 / 3,9 %, 78,2 %, 43,9 % (1.097), 55,4 %, 98,7 %); todas las de Web y Seguridad vial que se citan (4D: 324, Salazar Israel 63,3 %, Portillo 72 en campaña, 43,5 %, 40,4 %, 35,5 %, 89,8 %, n=102 Portillo seguridad vial, edad 60+ 26,2 %, género 61,2 %).

**Diferencias exactas:**
- **"142" Portillo en seguridad vial por `campaña o sensor`** (cifra en `research/04` §5c y en contradicción C10). **No aparece en la salida de 4D.** Solo sale el 102 por concesionario. Esta cifra no es reproducible desde el script. Usar solo el 102 o corregir el script.
- **"108" Portillo en Venta-Usados por prefijo PORT.** Sale del mapeo (02), no del 1A, que usa 145 (`\bPORT`). El documento lo declara (C15), así que no es un error, pero el 1A no reproduce el 108 y ninguna tabla de personas dice de dónde sale.
- Las cifras de control del diccionario (6 valores de Mecánica) sí calzan, según la salida 3C.

**Lo que no pude reproducir por diseño:** cualquier cifra de CASOS_PBI (archivo ausente; BLOQUEADO).

---

## b. Afirmaciones sin etiqueta, cifra ni fuente

Estas frases del documento no tienen etiqueta, o tienen una cifra sin base o sin fuente:

1. **Sección 1:** "Los datos sostienen cuatro grupos distintos y significativos". Ninguna prueba de significancia; "significativos" es un juicio, no un test. Sin etiqueta.
2. **P1, Ficha:** "Target: persona que cotizó en línea o en salón". La definición de "en línea" no está en la fuente; es una lectura del campo `origen`. Sin etiqueta.
3. **P1, Empatía, "Piensa y siente":** tiene [HIPÓTESIS], pero la frase "la espera genera desconfianza, más que enojo directo" no tiene ningún dato de tono ni de enojo. Es suposición sin marca de cuánta.
4. **P2, Empatía, "Resultados":** "que el auto llegue en plazo y con documentos" está etiquetado [DATO parcial], pero el plazo no existe en los datos. La etiqueta debería ser HIPÓTESIS.
5. **P3, Ficha:** "marcas con más registros: TOYOTA 3.744..." es correcto, pero "Target: cliente de servicio técnico de la red del grupo" no está en los datos (no hay campo de red). Sin etiqueta.
6. **P4, Empatía, "Piensa y siente":** "no puede verificar la condición del auto antes de decidir; teme... recibir poco por el suyo" está marcado [HIPÓTESIS] en una frase, pero la frase "no puede verificar la condición" se presenta como hecho del journey. Sin etiqueta en la tabla de journey, donde "Condición del vehículo" aparece como fricción [DATO] (es la tasa de detractores, no una medida de "no poder verificar").
7. **Bajadas de comunicación (todas):** los pilares y ejemplos de TOFU/MOFU/BOFU son propuestas. Están marcados [HIPÓTESIS] en su mayoría; los que no lo están (P1 "Cotizaste. Te decimos cuándo te contactamos") ya tienen el NO VERIFICADO del plazo, bien.
8. **P2, Journey, "Consideración":** "Comparar formas de pago es la prioridad top-1" se cita como [DATO] de "otra población". Está bien etiquetado, pero el documento habla de "clientes web" sin decir que son clientes de la campaña "Salazar Israel" (63 % de la muestra). Dato sin contexto de sesgo.
9. **P4, Ficha:** "Marcas: CHEVROLET 407, MG 286, PEUGEOT 277, NISSAN 263" es correcto, pero la marca más vendida no es un perfil de comprador: sin etiqueta de que describe la muestra, no al comprador.

---

## c. Sesgos de muestra

- **Solo responden quienes ya compraron o cotizaron.** Ninguna de las cuatro personas representa al no comprador. El documento lo dice en §0 y §1, pero las cuatro fichas hablan de "el comprador" como si fuera el mercado. Riesgo alto para jefatura.
- **Cobertura por marca:** 3C muestra marcas con NPS de 55 a 85 (PEUGEOT 55,6; CITROËN 59,2; OPEL 56,0 frente a CHERY 84,9). Esas diferencias mezclan marca y red de sucursales. El documento lo dice en §5 pero no lo aplica a P3, que sí usa "marca" para decir "cobro sorpresa".
- **Encuesta por email:** Mecánica tiene 27.514 de 27.516 por email. El documento no dice que el canal excluye a quien no tiene correo o no abre mensajes. Sin etiqueta de sesgo en P3.
- **Encuesta web con 63 % de una campaña:** 205 de 324 son "Salazar Israel". El documento lo declara (§8.5), pero P2 y P4 usan esa encuesta como "lo que pide el comprador" y P4 la usa para "opiniones 40,4 %". Es la fuente más débil del documento para P2 y P4 y aparece como respaldo de la fila de Consideración (P2) y de la de Interés/Consideración (P4), así como en la bajada de P2 y P4.
- **Seguridad vial, un solo mes y solo nuevos:** 2025-10-22 a 2025-10-29, solo clientes de autos nuevos, 709 respuestas. El documento lo limita a §6 y "no se usa para inferir perfil de P1 a P4". Correcto. Pero la sección 6 abre con "Rango de edad" y "Género" como cifras de cliente, y P2/P3 las usan implícitamente en la Ficha ("Edad / género: NO VERIFICADO" está bien). Sin contradicción, pero la demografía no tiene uso en ninguna persona: es decoración.
- **Fechas distintas:** Leads termina 2026-01-23, hace 10 meses. P1 se presenta como vigente. Ver P1 abajo.

---

## d. Violaciones de reglas

| Regla | Hallazgo | Severidad |
|---|---|---|
| Sin conversión lead→venta | Limpio. El documento lo niega en §0, §8.2 y en P1 ("Dato a no usar como conversión"). No encontré frases que lo insinúen. | Ninguna |
| "Usado" en lenguaje premium | Limpio en bajadas de comunicación. P4 dice "seminuevo". "Usado" aparece solo como dato o nombre de categoría. Revisar la línea 225 ("cliente de Venta-Usados") y los títulos de archivo: son CRM, correcto. | Ninguna |
| Cifras internas sin USO INTERNO | El encabezado marca todo el documento como USO INTERNO. Las secciones de personas no repiten la etiqueta. Es aceptable para uso interno, pero si una bajada se copia a otro documento, pierde la marca. | Baja |
| PII | No encontré correos, RUT ni teléfonos de clientes en el documento ni en `research/`. Los teléfonos de `research/05` (600 088 0016, *5005) son públicos de la empresa. Verbatims: 15 palabras o menos, con row_id. Pero el filtro de Mecánica no elimina nombres en minúscula (nota de §8.5). Sin revisión humana de cada verbatim, no puedo garantizar ausencia de PII. | Media |
| Legal (garantía, inspección) | Bien tratado: "garantía" y "inspección de 200+ puntos" quedan prohibidas o NO VERIFICADO. P4 menciona la garantía de Kavak como [WEB] de competidor: correcto, pero no verifiqué esa URL en esta auditoría. | Baja |
| Cita fiel | P1 cita "Ser más transparente con el costo establecido en la cotización" (row 662). La fuente dice "trasparente". Es una corrección ortográfica, no de contenido, pero el documento afirma ser "textual". Corregir o decir "con ortografía corregida". | Baja |

---

## e. Promedios que esconden distribuciones polarizadas

1. **NPS de Mecánica 73,5.** Esconde 72,6 % de notas en 0 o 10 y solo 4,0 % en 4-6. Un NPS alto con esa forma es "satisfechos o no", no "buen servicio". El documento no muestra la distribución en ningún lado; solo aparece en la fuente de §5 del 3C. **Corregir:** mostrar la distribución junto al NPS si se cita.
2. **Fluidez Nuevo 4,69.** Esconde que 58,0 % de los detractores (202 de 348) puntúa 1-2, mientras 93,6 % del total puntúa 4-5. P2 lo usa bien, pero la media de la tabla de etapas (1A) sí aparece en research; el documento no cita la media, solo el 58 %. Correcto. Riesgo: el 58 % depende de que la pregunta sea sobre entrega. Ver sección f.
3. **Entrega Usados 61,7 % de detractores con 1-2** (media 2,24). Es la etapa más castigada de todo el archivo y el documento la usa en P2 con población equivocada (ver sección f).
4. **Parte de pago Usados.** Media total 4,45 pero 39,6 % de los detractores con 1-2 (42 de 106). Se castiga poco en la media general y mucho en un subgrupo de 106. El documento lo marca como "Límite" (§P4). Bien.
5. **Macro "Atención" 82 % en promotores.** Es el tema dominante en ambos lados (37,4 % en detractores de Usados, 29,5 % en Nuevo). El documento lo dice ("es un tema, no una valencia"), pero P2 y P4 lo usan como "pilar de atención" sin separar que el mismo tema sostiene promotores y detractores.
6. **Mecánica por marca.** Promedio de 77 marcas. CHERY NPS 84,9 y PEUGEOT 55,6 están a 30 puntos. Promedio global esconde marcas malas. El documento lo cita en §5 pero no lo lleva a P3.

---

## f. Evidencia de persona: porcentajes y denominadores

El documento calcula cada porcentaje sobre "los ítems de evidencia que listó" (12, 11, 11, 10). Esto **infla la solidez**, por tres razones que verifiqué contra el texto:

1. **Las etiquetas del cuerpo no coinciden con la tarjeta.** Conté las etiquetas en el texto de cada persona (sección por sección):

| Persona | [DATO] en texto | [WEB] en texto | [HIPÓTESIS] en texto | NO VERIFICADO en texto | Tarjeta declara (DATO/WEB/HIP) |
|---|---:|---:|---:|---:|---|
| P1 | 13 | 3 | 11 | 16 | 9 / 1 / 2 (12) |
| P2 | 14 | 1 | 8 | 11 | 10 / 0 / 1 (11) |
| P3 | 14 | 3 | 10 | 8 | 9 / 1 / 1 (11) |
| P4 | 13 | 5 | 10 | 10 | 7 / 2 / 1 (10) |

   Los conteos de texto son etiquetas, no ítems: una misma cifra puede repetirse. Aun así, la tarjeta de P1 dice 2 [HIPÓTESIS] y el texto tiene 11. Esto significa que la tarjeta cuenta solo las **cifras** que sostienen el miedo y no todo lo que el documento afirma. Esa es la elección que infla los porcentajes.

2. **Lo que no entra en el denominador.** Las celdas "NO VERIFICADO" de los journeys (16 en P1, 11 en P2) no están en el 12 ni en el 11. Una persona con 16 huecos declarados sale con "75 % DATO". El 75 % de P1 es sobre lo que se pudo medir, no sobre lo que se necesita para la persona.

3. **Denominador ajeno.** P1 tiene 9 de 12 "DATO" pero el DATO más pesado de P1 (el 39,1 % de "sin respuesta") es [HIPÓTESIS] de codificación por palabras clave: 54 de 138. Ese ítem cuenta como DATO en la base y como HIPÓTESIS en el texto. Si se recalcula, P1 queda con menos de la mitad de su miedo medido.

**Efecto neto:** los porcentajes de la tabla de trazabilidad (§9) dan impresión de solidez que no corresponde. Recomiendo reemplazar esa tabla por: "cifras DATO que sostienen el miedo, n de la base, y huecos NO VERIFICADO" sin porcentaje.

---

## g. Tres formas en que cada persona puede estar equivocada, y la prueba que lo mostraría

### P1 — El cotizador que espera
1. **"Sin respuesta" es un artefacto de codificación por palabras clave.** 54 de 138 textos con evaluación 1-2 se codificaron por palabras clave (precisión no validada). *Prueba:* dos codificadores ciegos, sobre una muestra de 138 textos. Si el acuerdo (kappa) es menor a 0,7, el 39,1 % no se usa como cifra.
2. **La pregunta "¿Ha sido contactado?" está mal leída o mal capturada.** 60 leads dicen No, pero 275 dicen "Ya estoy en contacto con mi ejecutivo". Si el "No" es un campo no contestado, P1 cambia de "sin respuesta" a "sin registro". *Prueba:* pedir a CRM la definición del campo y el flujo de captura; contar cuántos "No" tienen fecha de primer contacto registrada.
3. **P1 es una foto de 2023-2024, no de hoy.** Los leads van de 2023-06 a 2026-01 (2023: 294, 2024: 543, 2025: 119, 2026: 47). Si la tasa de "sin respuesta" cambió por año, la persona es de una época. *Prueba:* repetir el 39,1 % por año de respuesta; si varía más de 10 puntos entre 2023 y 2025, la persona no describe el presente.
- Plus: la escala de "evaluación del proceso" tiene dirección NO VERIFICADA. Si 5 significa "peor", el 65 % de "5" invierte la lectura. Confirmar con el diccionario antes de comité.

### P2 — El que ya pagó y espera su auto nuevo
1. **La "demora de entrega" no es la etapa que midió Nuevo.** La columna que castiga es "Fluidez general del proceso", no un campo de entrega física. Si fluidez incluye financiamiento y trámite, P2 describe la compra, no la entrega. *Prueba:* leer el texto exacto de la pregunta de fluidez; clasificar los 202 detractores con 1-2 por microcategoría (Plazos de entrega 64, Factura 22, Permiso 17 sobre 348 detractores: si la mayoría cae en "aprobación/crédito", P2 se equivoca de nombre).
2. **P2 mezcla poblaciones.** La fila de Retención usa "61,7 % de detractores con 1-2 en Usados" para describir a comprador de auto nuevo. Ese dato es de Usados (`Proceso de Entrega`, n=313). *Prueba:* eliminar la cifra de Usados de P2; si la historia de "entrega" depende de ella, P2 queda con 58 % de fluidez, no con 61,7 %, y la afirmación de entrega física se debilita.
3. **Sobrevivencia de la encuesta.** Solo responde quien ya recibió el auto. Los que siguen esperando no están en la base, y la demora extrema queda fuera. *Prueba:* el denominador de entregas del periodo (OT o facturas) no está en los archivos (NO VERIFICADO). Pedirlo a Beto; si la tasa de respuesta es baja, la cifra de 58 % es una cota inferior de la insatisfacción y el mensaje de P2 debe ser más fuerte, no más suave.

### P3 — El que vuelve al taller
1. **La mitad de la subpoblación Portillo no es Portillo.** 118 de 245 filas son PORTILLOLA o PORTILLOTALCA, que solo coinciden por prefijo. *Prueba:* recalcular NPS y detractores solo con GAP PORTILLO SERVICIO (127). Si el NPS 84,3 se mantiene y los 28 detractores caen a menos, el perfil "Portillo" de P3 es de otra red. Hoy el documento ya lo marca como [HIPÓTESIS]; aun así, P3 usa "cobro sorpresa" como miedo, y el dato de precios no está desagregado por sucursal.
2. **"Reparado a la primera: No" tiene base mal definida.** 43,9 % de detractores (1.097) responde no. Si la pregunta se contestó también en OT de mantenimiento (no reparación), el "No" no mide falla técnica. *Prueba:* cruzar "reparado" con microcategoría de motivo; si los "No" con motivo de precio o trato no tienen "Calidad del servicio", la persona "reparación mal hecha" está inflada.
3. **"No volvería" es intención, no conducta, y puede ser causa invertida.** 55,4 % "no volvería" entre quien no reparó bien. Podría ser que el cliente ya no volvía por otra razón. *Prueba:* contar visitas repetidas por vehículo (no hay identificador: `patente_vin` fue eliminado en la anonimización). Sin ese dato, la persona no puede afirmar retención. NO VERIFICADO.

### P4 — El que compra o vende un seminuevo
1. **El miedo "lo que no se ve" no es el que aparecen los verbatims.** Las 52 filas de detractores con "Condición del vehículo" incluyen "Pintaron los parachoques de otro color", "Calidad del producto", "Detalles del vehículo". Son defectos de terminación visibles después de la compra, no información oculta antes. *Prueba:* clasificar las 52 filas por verbatim en "oculto antes de comprar" versus "terminación después de entregar". Si menos de la mitad es "oculto", la persona cambia de miedo.
2. **"Me paguen poco" en parte de pago no está medido.** La pregunta de parte de pago tiene 106 detractores, y el documento no sabe si mide tasación, rapidez o transparencia. *Prueba:* leer el texto exacto de la pregunta de "Vehículo en parte de pago" y la de comentario (`¿Nos contarías por qué?.1`, 26 codificadas de 57 con texto). Si el comentario casi no tiene texto, el miedo a la tasación es HIPÓTESIS pura.
3. **La voz del comprador en P4 es de competidores, no de compradores.** La celda "Oye" usa textos de Clicar y Kavak (marketing de otros). Además, la encuesta web (opiniones 40,4 %) tiene 63 % de una campaña. *Prueba:* entrevistar a 5 compradores o vendedores de Usados (la guía de entrevista lo permite). Si no aparece el miedo a "lo que no se ve", P4 no tiene voz propia. Además, el universo Portillo tiene 11 detractores y 108 vs 145 filas: no es base para una persona específica de Portillo.

---

## h. Qué corregir antes de comité (orden de prioridad)

1. **Declarar y resolver los incidentes de la sección 0.** Confirmar que los parquets regenerados son idénticos a los anteriores y que los dos `research/*.md` regenerados son los aprobados. Sin esto, cualquier cifra del documento tiene una cadena de custodia rota.
2. **Quitar el "142" de seguridad vial** o reproducirlo en 4D. Hoy aparece en C10 y `research/04` como cifra oficial y no sale del script.
3. **Rehacer la tabla de trazabilidad (§9) y las tarjetas de evidencia.** Usar recuento de etiquetas reales, no ítems elegidos. Mostrar los NO VERIFICADO como denominador.
4. **Sacar la cifra de Usados (61,7 %) de la fila de Retención de P2**, o marcarla como de otra población.
5. **P1: marcar la fecha de corte como problema, no como dato.** Leads hasta 2026-01-23, hace 10 meses. Antes de decir "el cotizador espera", confirmar con Beto si el corte es de exportación. Dirección de la escala de evaluación: confirmar.
6. **P1: validar el 39,1 % "sin respuesta"** con dos codificadores ciegos sobre 138 textos.
7. **P4: reescribir el miedo "lo que no se ve"** según la clasificación de las 52 filas de "Condición del vehículo".
8. **P3: recalcular la subpoblación Portillo sin PORTILLOLA y PORTILLOTALCA** antes de decir nada de Portillo en P3.
9. **NPS: mostrar la distribución** (72,6 % en 0/10) siempre que se cite el 73,5.
10. **Fidelidad de citas:** corregir "transparente" a "trasparente" o declarar la corrección. Revisar todos los verbatims de Mecánica por PII en minúscula antes de cualquier uso externo.
11. **Verificar las URLs WEB** citadas (Kavak, Pompeyo, Derco, reclamos.cl) con una nueva consulta; esta auditoría no las volvió a abrir.
12. **Confirmar con Beto** los bloqueos ya listados en §8.3 (Portillo/PORTILLO_HIPOTESIS, marca del usado, CASOS_PBI, codificación de macrocategorías). Sin ellos, P3 y P4 no deben circular como personas de Portillo.

---

## Veredicto por persona

- **P1 — no sobrevive tal como está.** Su núcleo ("sin respuesta") depende de codificación por palabras clave sobre 138 textos, de una fecha de corte de hace 10 meses y de una pregunta de contacto contradictoria. Puede sobrevivir como hipótesis a validar.
- **P2 — sobrevive en Nuevo, con corrección.** La señal de fluidez (58 % de detractores con 1-2) es real en la base, pero el nombre "demora de entrega" no está probado y la cifra de Usados debe salir.
- **P3 — sobrevive a nivel grupo (GRUPO_COMPLETO).** Las cifras de Mecánica son las más sólidas del documento. Lo que no sobrevive es cualquier afirmación específica de Portillo, que depende de 118 filas de dudosa asignación y no tiene capa de casos (CASOS_PBI).
- **P4 — no sobrevive en su formulación de miedo.** La mayoría de los verbatims de "Condición del vehículo" son de terminación posterior a la entrega, no de información oculta antes de comprar. El miedo a la tasación es HIPÓTESIS. Las voces de "Oye" son de competidores.

---

## Trazabilidad de esta auditoría

- Scripts: `analisis/00_anonimizar.py`, `01_diccionario.py`, `02_mapeo_portillo.py`, `1A_voz_ventas.py`, `2B_leads_cotizacion.py`, `3C_retencion_mecanica.py`, `4D_intencion_funcionalidades.py`. Salidas en `/private/tmp/claude-501/-Users-betosanchez/24be6daf-63e5-47fe-9340-aa059ab3e68f/scratchpad/` (`out_*.txt`, `1A_out.txt`).
- Archivos leídos: `entregables/BUYER_PERSONAS_PORTILLO.md`, `research/00_*.md`, `research/01` a `05`. No se abrió `inputs_raw/` directamente; sí se ejecutó el script que lo lee (sección 0.1).
- Cifras no verificadas por esta auditoría: las URLs WEB de `research/05` y los valores de CMF/ANAC.

---

## Re-auditoría v2 (2026-11-23)

**Objeto:** `entregables/BUYER_PERSONAS_PORTILLO.md` versión 2 (corregida por F). Esta sección no reemplaza la auditoría anterior; corrige lo que cambió. **USO INTERNO.**

### 1. Estado del 142 (seguridad vial, campaña)

**Reproducido, con corrección.** En la auditoría anterior lo marqué "no reproducible". Era un error mío: busqué "142" en la salida de `4D`, que no lo imprime, y no revisé la lógica de otros scripts. `analisis/6F_recuentos_correccion.py` (sección C) lo reproduce: **142 filas** de `CR_Encuesta-de-seguridad-vial-en-Chile_*` donde `campaña o sensor` contiene "Portillo", sin distinguir mayúsculas (`str.contains('Portillo', case=False)`). La regla es de substring, no de palabra completa. La cifra del 102 por `nombre_concesionario` sí sale de 4D. Ambas quedan como contradicción C10, sin uso en personas.

### 2. Verificación de los puntos pedidos

**1. 6F corre y reproduce.** Exit 0, sin escritura, sin lectura de `inputs_raw/`. Reproduce: 142 (C), 245 / 127 / 118 (A), 108 / 145 (B) y los recuentos de etiquetas (D). La salida está en el scratchpad (`out_6F.txt`).

**2. P3 sin PORTILLOLA/TALCA: confirmado.** `\bPORTILLO\b` sobre `nombre_sucursal` da **n=127, NPS 84,3, detractores 3,9 %, notas 0 o 10 = 79,5 %**. Es idéntico a `GAP PORTILLO SERVICIO` solo. Las 118 filas excluidas son PORTILLOLA (60) y PORTILLOTALCA (58). Con el universo `\bPORT` (245): NPS 68,2, 11,4 % detractores, 72,7 % en 0/10.
   - Matiz que el documento no dice: el "universo limpio" es **una sola sucursal**. Sirve para mostrar que la cifra de v1 venía de otra red, no para afirmar un perfil Portillo. Con n=127 y 5 detractores, la tasa de detractores (3,9 %) tiene un intervalo muy amplio (NO VERIFICADO: no se calculó intervalo). Esto debe leerse como [HIPÓTESIS].

**3. Denominadores de evidencia: confirmados.** 6F sección D cuenta desde cada encabezado de persona hasta "Bajada de comunicación" o "Tarjeta de evidencia". Eso incluye Ficha, Mapa, Journey, Límites y Distribución, y deja fuera las bajadas y la tarjeta. NO VERIFICADO queda fuera del denominador y se cuenta aparte.

| Persona | DATO | WEB | HIPÓTESIS | Denominador (DATO+WEB+HIP) | NO VERIFICADO aparte |
|---|---:|---:|---:|---:|---:|
| P2 | 19 (86,4 %) | 0 | 3 (13,6 %) | 22 | 8 |
| P3 | 24 (82,8 %) | 2 (6,9 %) | 3 (10,3 %) | 29 | 6 |
| P4 | 22 (73,3 %) | 4 (13,3 %) | 4 (13,3 %) | 30 | 6 |

   Los porcentajes son de **menciones etiquetadas**, no de ítems únicos. El documento lo dice en §9. El denominador ya no es "lo que listé" como en la v1, pero sigue siendo una cuenta de texto: sirve para comparar la forma de la evidencia entre personas, no para declarar solidez.

**4. P1 descartada: confirmado, con dos restos a vigilar.** §2 la descarta y dice por qué. No aparece como persona vigente en §6 (fila "Descartada"), §10 ("Descartada") ni en las bajadas. Restos que siguen en el documento: (a) §2 conserva sus cifras (371/60, 17,1 %, 68, 54 de 138) con etiqueta de descarte; no aparecen como miedo de ninguna persona. (b) §8.1 conserva la fecha de corte. Ambos son aceptables porque van como descarte. Recomiendo no citar P1 en ningún resumen para jefatura.

**5. PII, "usado" y conversión: sin hallazgos.**
- PII: solo aparecen URLs públicas (clicar.cl, kavak.com/cl, reclamos.cl) y nombres internos (Beto, Iván Balaguera). Sin correos, RUT, teléfonos, patentes ni nombres de clientes.
- "usado" en lenguaje de marca: no aparece. Las ocurrencias son la regla de §1, un nombre de archivo o categoría, la nota BLOQUEADA de P4 y la tabla de contradicciones.
- Conversión lead→venta: solo aparece para negarla (§0, §1, §8.2). La palabra "cierre" aparece como nombre de etapa del journey, no como tasa.

### 3. Veredicto por persona (v2)

- **P2 — sobrevive.** La fluidez de 58,0 % con 1-2 en detractores de Nuevo es [DATO]. El nombre de la etapa es [HIPÓTESIS] y lo dice el documento. La cifra de Usados salió de la retención.
- **P3 — sobrevive a nivel grupo.** Las cifras generales son [DATO] y reproducen. Lo específico de Portillo no sobrevive a la prueba de la sucursal única: queda como [HIPÓTESIS] con n=127.
- **P4 — sobrevive solo como hipótesis.** La tasa de 17,2 % es [DATO]; la lectura de "terminación posterior" se basa en dos textos ([HIPÓTESIS] en el documento). §10 dice "sostenida por [DATO]", lo que sobrestima. Debe decir "tasa [DATO], lectura [HIPÓTESIS]".
- **P1 — descartada.** Correcto.

### 4. Desalineaciones que encontré en v2

1. **§6, fila P4 "terminación":** marca ● (dolor principal con [DATO]) sobre una interpretación que el propio texto marca [HIPÓTESIS]. Cambiar a ○.
2. **§10, P4:** "Sostenida por [DATO]" sobrestima. Ver veredicto.
3. **§4, "Lectura" del universo limpio:** "la cifra de Portillo de la versión 1 mezclaba la red de otras sucursales" es una interpretación sin etiqueta. Marcar [HIPÓTESIS].
4. **§4, universo limpio:** es una sola sucursal (GAP PORTILLO SERVICIO). Debe decirse en la tabla, no solo en la lectura.
5. **Incidentes de la sección 0 de la auditoría anterior:** siguen abiertos (regeneración de `inputs_clean/` y sobrescritura de dos `research/*.md`). v2 no los resuelve, como declara su propio §0.

### 5. Cifras corregidas respecto de v1

| Cifra | v1 | v2 (reproducida) |
|---|---|---|
| Portillo en Mecánica | 245, NPS 68,2 | Se mantiene como `\bPORT` (245). Universo limpio: 127, NPS 84,3 |
| Portillo en seguridad vial, campaña | "142 no reproducible" (mía) | **142, reproducida por 6F (C)** |
| Evidencia P2 / P3 / P4 | 11, 11, 10 ítems | 22, 29, 30 menciones etiquetadas |
| Retención P2 | 61,7 % de Usados | Quitada (fluidez 58,0 % de Nuevo) |

### 6. Guía de entrevista

Actualizada. La P3 (stock del lead) cerraba un hueco de P1, que está descartada. La reemplacé por una pregunta sobre preparación y terminación del seminuevo, que cierra el hueco de P4. Las demás preguntas siguen alineadas con P2 y P4.

---

## Auditoría MdV (Fase 3, 2026-11-23)

**Objeto:** `entregables/BUYER_PERSONAS_PORTILLO.md` (versión MdV, P1 a P5), contra `research/06_arquetipos_cliente.md`, `01_zmot.md`, `02_fmot.md`, `03_smot.md`, `04_umot_demografia.md`, `05_contexto_web.md` y `00_contradicciones.md` (sección Fase 1 MdV). La v2 está archivada en `entregables/v1_pre_MdV/` y no se audita como vigente. **USO INTERNO.**

### 0. Reproducibilidad y alcance

- Scripts ejecutados (exit 0, sin Traceback): `zmot_leads.py`, `zmot_funcionalidades.py`, `fmot_mapa_empatia.py`, `smot_mecanica.py`, `umot_01_recomendacion_retorno.py`, `umot_02_miedos_umot.py`, `umot_03_demografia_seguridad_vial.py`, `umot_04_citas.py`, `6F_recuentos_correccion.py`. Salidas en el scratchpad (`mdv_*.txt`).
- Script nuevo de esta auditoría: `analisis/7G_solapamiento_personas.py` (solo lectura de `inputs_clean/`, imprime conteos). Mide el solapamiento de respondentes. Se creó porque la pregunta de independencia no se puede responder sin medir filas compartidas.
- No se re-corrió `00_anonimizar.py`. No se abrió `inputs_raw/`. Las citas se verificaron leyendo `inputs_clean/` y reportando solo True/False y el nombre de columna.
- **Limitación:** no hay clave de respondente entre archivos. El solapamiento se mide solo dentro de cada archivo (Nuevo, Usados, Mecánica).

### 1. Cifras C-xx contra la salida de los scripts

Coinciden, con el número de la tabla de `research/06`: C-02 (202/348 y 159/313), C-03 (1.521), C-04 (1.191; 217; 170), C-05b (39), C-06 (98 y 84), C-07 (1.620), C-08 (1.189; 103; 87; 35), C-10 (70 y 79), C-11 (1.757), C-12 (1.311; 76; 86), C-14 (108), C-15 (1.735), C-16 (1.210), C-18 (74 y 84; acogida 43 y 73), C-19 (1.162; acogida ≤3 51,4 %; 882), C-20 (621; 45; 76), C-21 (1.097 y 1.953; 1.355), C-25 (376/2.146), C-26 (12 y 13), C-17 (5), C-13b (71), C-09 (40 y 23).

**Errores o cifras que no reproducen:**
1. **C-05 tiene el denominador equivocado.** "No" a contacto = 60, pero el 6,0 % usa 1.003 como base. La base correcta es 431 respondidos, es decir **13,9 %**. Los 572 sin respuesta incluyen los 294 de 2023, que no tienen ninguna respuesta a la pregunta (la pregunta no existe en 2023 en el archivo). Por año de respuesta: 2024: 13 de 265 (4,9 %); 2025: 28 de 119 (23,5 %); 2026: 19 de 47 (40,4 %). **La cifra sube con los años.** Con n=47 en 2026 es una señal, no una tasa. Esto cambia la lectura de P2: el silencio aparece en los registros más recientes, no en los antiguos.
2. **C-01 (85) y C-05b (61)** son cifras de v1 y no reproducen. Se muestran como contexto, con esa marca. Bien.
3. **D-N3:** el script da 1.312 filas con NPS válido en Venta-Nuevo (PORT_CAMPAÑA_CHECK); la cifra "1.313" es el conteo bruto (consulta directa). Diferencia de una fila sin NPS. Ambas deben mostrarse.
4. **D-N2:** 114 (campaña Venta Usados Portillo) reproduce en `umot_01`. El 163 de "Venta Usados Clicar" viene de consulta directa, no de script. Se debe marcar así.
5. **D-N6:** confirmado por `zmot_funcionalidades.py`: 324 de 324 son NUEVO con factura (2024-01 a 2025-05), mediana 262 días entre factura y respuesta. La encuesta web es post-venta, no de visitantes.

### 2. Regla "3 de 4 MdV con DATO": verificación de cada evidencia

Regla literal: cada persona necesita [DATO] en al menos 3 de 4 MdV. Lo que verifiqué es si el DATO es real y si las MdV son poblaciones distintas.

| Persona | ZMOT | FMOT | SMOT | UMOT | MdV con DATO (literal) | Poblaciones independientes con DATO |
|---|---|---|---|---|---|---|
| P1 | HIP (C-01) | C-02 DATO real | C-03 DATO real | C-04 DATO real | 3 | **2** (venta, taller) |
| P2 | C-05 DATO real (base corregida: 13,9 %) | C-06 DATO real (mide facilidad, no silencio) | C-07 proxy (fricción de comunicación, no silencio) | C-08 DATO real (etiqueta "sin respuesta" es del script) | 3 sin contar proxy | **3** (leads, venta, taller), pero "silencio" solo se mide en leads |
| P3 | C-09b DATO **mal clasificado** (3,2 % pidió información; no es miedo) | C-10 DATO real | C-11 DATO real | C-12 DATO real | 3 si se acepta C-09b; 2 sin él | **2** (venta, taller) |
| P4 | C-13 DATO **mal clasificado** (2,3 % pidió más información) | C-14 DATO real (solo Nuevo) | C-15 DATO real, pero 56 % de sus detractores también tiene reparado = No (C-21) | C-16 DATO real | 3 sin ZMOT | **2** (venta Nuevo, taller) |
| P5 | descartado | C-18 DATO real | C-19 DATO real | C-20 DATO real con etiqueta "mal trato" (D-A1) | 3 | **2** (venta, taller) |

**Hallazgos:**
- **P1, P3, P4 y P5 pasan la regla solo contando MdV.** Sus tres DATO vienen de dos poblaciones de respondentes: venta y taller. ZMOT no tiene DATO de miedo para ellas.
- **Los DATO de UMOT no son una cuarta fuente.** UMOT es un pool que contiene a todo detractor más quien respondió "No" o "No sé" a volver. Por eso repite a los mismos respondentes de FMOT y SMOT (ver sección 3).
- **C-09b (P3) y C-13 (P4) son DATO de una opción marcada, no de un miedo.** "Información de financiamiento" y "Mayor información del vehículo" son pedidos de información. Como evidencia de un miedo son [HIPÓTESIS] disfrazada. Su etiqueta debe bajar a [HIPÓTESIS].
- **La matriz de §7 contradice el recorrido de P3:** en ZMOT marca ○ (hipótesis) para C-09, pero en el recorrido cita [DATO C-09b]. Hay que unificar.
- **C-08 (UMOT, "Miedo a quedar sin respuesta")** y **C-07 (SMOT)** miden el ítem "Facilidad para comunicarse", no respuesta. El nombre del miedo es de script; el DATO es real. La etiqueta "silencio" es [HIPÓTESIS] en venta y taller.

### 3. Solapamiento entre respondentes (7G)

**Dentro de cada persona: FMOT o SMOT contra UMOT**

| Persona | Archivo | FMOT/SMOT | UMOT | En ambos | Solapamiento |
|---|---|---:|---:|---:|---|
| P1 | Venta-Nuevo | 202 | 217 | 202 | 93 % de UMOT ya está en FMOT |
| P2 | Venta-Nuevo | 98 | 103 | 98 | 95 % |
| P3 | Venta-Nuevo | 70 | 76 | 70 | 92 % |
| P1 | Venta-Usados | 159 | 170 | 159 | 94 % |
| P2 | Venta-Usados | 84 | 87 | 84 | 97 % |
| P3 | Venta-Usados | 79 | 86 | 79 | 92 % |
| P1 | Mecánica | 1.521 | 1.191 | 1.024 | 86 % de UMOT está en SMOT |
| P2 | Mecánica | 1.620 | 1.189 | 1.097 | 92 % |
| P3 | Mecánica | 1.757 | 1.311 | 1.099 | 84 % |
| P4 | Mecánica | 1.735 | 1.210 | 1.170 | 97 % |
| P5 | Mecánica | 1.162 | 621 | 520 | 84 % |

Para P5 en Venta-Usados, la acogida de UMOT (76) está casi entera en la acogida de FMOT (73 de 76). Es decir, UMOT no agrega respondentes; repite FMOT.

**Entre personas, respondentes únicos y pares (Jaccard = |A∩B| / |A∪B|):**

| Archivo | Personas únicas (unión de sus MdV) | Respondentes en ≥2 personas | Pares con más solapamiento (Jaccard) |
|---|---|---|---|
| Venta-Nuevo (detractores 348) | P1 217, P2 103, P3 76, P4 108, P5 88 | 148 de 256 (58 %) | P2-P4 53 %, P4-P5 56 %, P2-P5 52 % |
| Venta-Usados (detractores 313) | P1 170, P2 87, P3 86, P5 113 | 122 de 219 (56 %) | P2-P5 52 %, P1-P5 44 % |
| Mecánica (detractores 2.497) | P1 1.688, P2 1.712, P3 1.969, P4 1.775, P5 1.263 | 2.105 de 2.681 (79 %) | P2-P4 63 %, P1-P2 63 %, P3-P4 61 %, P1-P4 60 % |

- **Ninguna pareja es la misma gente**: el máximo es 63 % (Mecánica). Pero en taller las cinco personas son, en buena parte, los mismos detractores que puntúan bajo en ítems distintos.
- **El conjunto P2 + P4 + P5 es el más compacto**: en Nuevo, sus pares van de 52 % a 56 %. Sumado, cubre 148 de 348 detractores de Nuevo, 132 de 313 de Usados y 2.227 respondentes de Mecánica.
- **P1 y P3 tienen menos solapamiento con venta** (P1-P3: 22 % en Nuevo, 31 % en Usados). Su evidencia es distinta, pero se apoya en la misma población.
- **P4 y C-21 (reparación mal hecha) son casi la misma gente:** de 1.735 detractores con claridad de reparación ≤3, 968 (55,8 %) tienen reparado = No. El miedo "no sé qué pasó" es, en buena parte, "no quedó bien".

### 4. Veredictos por persona

- **P1 "El que espera sin fecha": cae como persona independiente.** Pasa la regla solo contando MdV (3 DATO), pero son 2 poblaciones (venta y taller), con 93 % y 86 % de solapamiento entre FMOT y UMOT. Mantener como **hipótesis de proceso largo** (C-02, C-03, C-04).
- **P2 "El que escribe y no le responden": sobrevive con redefinición.** Tiene 3 poblaciones (leads, venta, taller). Pero el silencio directo solo se mide en leads (C-05, base 431 respondidos: 13,9 %; 40,4 % en 2026, n=47). En venta y taller lo medido es "facilidad de comunicación". Renombrar como **fricción de comunicación** y fusionar (ver 5).
- **P3 "El que no entiende cuánto pagará": cae como persona.** Solo 2 poblaciones, y C-09b es una demanda de información, no un miedo. Mantener como **hipótesis de costo** (C-10, C-11, C-12).
- **P4 "El que no sabe qué pasó con su auto": se funde** con P2 (Jaccard 63 % en Mecánica, 53 % en Nuevo) y tiene 56 % de solapamiento con C-21 (reparado = No).
- **P5 "El que llega y se siente mal recibido": se funde** con P2 y P4 (Jaccard 52-56 %). En Usados, la acogida de UMOT es casi igual a la de FMOT.

### 5. Propuesta de fusión (para comité)

Dos opciones, con la misma base:
- **Opción A (recomendada):** 3 personas: P1 (hipótesis de espera), P3 (hipótesis de costo), y **F = P2 + P4 + P5 "El que no recibe respuesta, explicación ni buen trato"**. F tiene 3 poblaciones: leads (silencio), venta (comunicación, información y atención) y taller (comunicación, información, atención). Es la única que cumple la regla con poblaciones independientes.
- **Opción B:** 4 personas: P1, P3, **P2 + P4** y P5 sola. Solo si comité quiere distinguir trato de comunicación. P5 tiene menos evidencia propia (ZMOT descartado; acogida ≈ atención) y solapa con P2 y P4 en 52-56 %.

El documento actual deja cinco, que es el máximo y no lo que sostienen los datos. `research/06` §3 ya proponía fusionar P2 y P4; los números sugieren que sumar P5 es igual de justificable.

### 6. ¿Usar la encuesta web como proxy de SMOT para P2?

**No es la encuesta web.** El proxy SMOT de P2 es C-07, de la encuesta de Mecánica ("Facilidad para comunicarse con servicio técnico", ≤3 en 64,9 % de detractores). La encuesta web aparece en P2 solo como "Funcionalidades que pide" en la bajada, y está marcada como proxy de compradores de nuevo [DATO, `zmot_funcionalidades.py`, D-N6]. Eso es correcto.

**Sobre C-07:** es legítimo como **fricción de comunicación** en taller, pero **no** como silencio. Por eso no cuenta como MdV de silencio. El conteo de P2 pasa a 3 MdV (ZMOT, FMOT, UMOT) solo si se acepta "facilidad de comunicación" como silencio. Si no se acepta, P2 tiene 1 MdV de silencio directo (ZMOT) y 2 de fricción. Decisión de comité, pero debe quedar escrita.

### 7. Denominadores de evidencia (corregidos)

`6F_recuentos_correccion.py` cuenta `\[HIPÓTESIS\]` (con corchete de cierre). El documento también usa `[HIPÓTESIS C-01: ...]` y `[HIPÓTESIS C-05b; ...]`, que no se cuentan. El denominador queda subcontado:

| Persona | DATO | WEB | HIP (6F, estricto) | HIP (todas las etiquetas) | Denominador documentado | Denominador corregido | NO VERIFICADO (fuera) |
|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | 13 | 0 | 3 | 5 | 16 | **18** (72,2 % DATO; 27,8 % HIP) | 6 |
| P2 | 17 | 0 | 2 | 3 | 19 | **20** (85,0 % DATO; 15,0 % HIP) | 6 |
| P3 | 10 | 1 | 2 | 4 | 13 | **15** (66,7 % DATO; 6,7 % WEB; 26,7 % HIP) | 1 |
| P4 | 10 | 0 | 2 | 4 | 12 | **14** (71,4 % DATO; 28,6 % HIP) | 2 |
| P5 | 11 | 0 | 2 | 3 | 13 | **14** (78,6 % DATO; 21,4 % HIP) | 1 |

Los NO VERIFICADO están fuera del denominador, como pidió F. La corrección sube la parte [HIPÓTESIS] en las cinco personas. P1, P3 y P4 cambian dos puntos cada una, porque usan etiquetas del tipo `[HIPÓTESIS C-…]`. **Corrección para `6F`:** cambiar la regex a `\[HIPÓTESIS` (sin el corchete de cierre). No edité el script, porque es de F.

### 8. Arquetipo de marca

Separado: aparece solo en §10 ("El Acompañante", [HIPÓTESIS]). No se mezcla con P1 a P5 ni se usa en el conteo. **Cumple.** Sin embargo, §10 incluye el marco legal del SERNAC (ver 10) y "garantía en usados", que es un término de la competencia y viola el lenguaje de premium (ver 9).

### 9. PII, "usado" en premium, conversión lead→venta, USO INTERNO

- **PII:** no se encontraron correos, RUT, teléfonos ni patentes en el documento ni en `research/` de esta fase. Los nombres son internos (Beto, Iván Balaguera). Las URL son públicas (clicar.cl, kavak.com/cl, derco.cl, reclamos.cl, chileautos.cl). **Cumple.** Un detalle de bajo riesgo: la cita de P1 `CR_2025-Venta-Nuevo_#3943` incluye "el 4 de septiembre" (fecha de compra). No identifica a la persona, pero conviene quitar la fecha.
- **"usado":** una ocurrencia fuera de la regla, en §10 ("garantía en usados") para describir a Pompeyo. Es término de competidor, pero el documento es de marca. Cambiar a "seminuevos" o marcar como cita de competidor. Las demás ocurrencias son nombres de archivo o categorías del CRM. **Un hallazgo menor.**
- **Conversión lead→venta:** ninguna afirmación. Aparece solo para negarla (§0, §8, §9). **Cumple.**
- **USO INTERNO:** el encabezado lo declara. Cumple.

### 10. Citas y legal

**Citas (17 verificadas contra su row_id):** 16 coinciden exactamente (sin distinguir acentos ni mayúsculas). **Una no coincide por ortografía:** la cita de leads `CR_Lead-Portillo_202#662` dice en el archivo "Ser más **trasparente** con el costo establecido en la cotización"; el documento escribe "transparente". Es una corrección de ortografía que el documento presenta como cita textual. Corregir, o marcar "[sic]" o "ortografía corregida".

**Legal:** la frase "El SERNAC exige que la garantía voluntaria esté por escrito y detallada" (§5, P4) y la restricción de §10 se apoyan en **prensa** (The Clinic, DF) y en **un análisis de estudio jurídico** (Garrigues). `research/05` dice que es "informativo; no es asesoría legal; validar con SERNAC directo". El documento lo presenta como exigencia establecida. Según la regla de "nada legal sin respaldo", debe marcarse **NO VERIFICADO (fuente primaria no leída: circular Res. Ex. N° 923)** hasta confirmarlo.

### 11. Contradicciones: presencia con ambas cifras

| ID | ¿Está en el documento? | Con ambas cifras | Observación |
|---|---|---|---|
| D-N1 | Sí | Parcial | Aparece 7.881 y 245, pero no el "127 / NPS 84,3" |
| D-N2 | **No** | No | Faltan 114 (script) y 163 (consulta directa) |
| D-N3 | **No** | No | Faltan 1.313 (bruto) y 1.312 (NPS válido) |
| D-N4 | Sí (en P1) | Sí | 132 (versión 2) y 85 (versión 1) |
| D-N5 | Sí (en P2) | Sí | 39 (versión 2) y 61 (versión 1) |
| D-N6 | Parcial | No | Dice "compradores de nuevo", pero no contrasta con "visitante" del brief |
| D-N7 | **No** | No | Faltan 142 (campaña, reproducido por `umot_03`) y 102 (concesionario) |
| D-B1 | **No** | No | Faltan 108, 145 y 114 |
| D-E1 | Parcial | No | Se menciona "Clicar" como marca bloqueada, pero no aparece el aviso con "PORTILLO \| USADOS" |
| D-A1 | Sí (en P5) | Sí | "mal trato" (script) frente a "acogida" (ítem) |
| #13 | Sí (en P2) | Sí | 60 "No" y 275 "ya en contacto" |

**Faltan cinco contradicciones completas (D-N2, D-N3, D-N7, D-B1) y una a medias (D-E1).** Deben agregarse a §8.4 del documento.

### 12. Tres formas en que cada persona podría estar equivocada, y la prueba

**P1 (espera sin fecha)**
1. **Es el mismo detractor medido dos veces.** FMOT y UMOT comparten 202 de 217 respondentes en Nuevo. *Prueba:* contar solo FMOT y ver cuántas MdV de venta quedan. Si una, P1 pierde una MdV. *Resultado:* ya cuantificado (93 %).
2. **"Fluidez general del proceso" no mide entrega.** Podría incluir crédito y trámite. *Prueba:* leer el texto exacto de la pregunta (NO VERIFICADO) y clasificar los 202 detractores con fluidez 1-2 por microcategoría. Si la mayoría es crédito o documentos, P1 se llama mal.
3. **Es una foto de la entrega de taller, no de la venta.** "Tiempo de entrega del vehículo" en Mecánica (C-03) y la fluidez de venta (C-02) son distintos procesos. *Prueba:* verificar si el ítem de taller se contestó después de la entrega; si se responde antes, el ítem mide la espera del vehículo en taller, no el proceso de compra.

**P2 (silencio, ahora fricción de comunicación)**
1. **"No" a contacto puede ser campo sin capturar.** 2023 no tiene respuestas; 2024 tiene 4,9 %, 2025 23,5 % y 2026 40,4 %. *Prueba:* pedir a CRM la fecha en que se empezó a capturar el campo y el flujo. Si el aumento viene de un cambio de captura, P2 no es un fenómeno nuevo. *Resultado parcial:* el denominador ya está corregido.
2. **"Facilidad de comunicación" no es silencio.** Un cliente puede comunicarse fácil y no recibir respuesta, y al revés. *Prueba:* cruzar "facilidad ≤2" con "No" a contacto en leads (no se puede, no hay clave). Alternativa: pedir al CRM el tiempo de primera respuesta. Sin ese dato, P2 se llama fricción.
3. **Los 275 "ya estoy en contacto" contradicen los 60 "No".** Si la mayoría de los 60 ya tenía contacto, no hay silencio. *Prueba:* para los 60 "No", pedir la fecha del primer contacto en CRM. Si tienen contacto registrado, el silencio desaparece.

**P3 (costo poco claro)**
1. **C-09b no es un miedo.** Pedir información de financiamiento no implica miedo a pagar de más. *Prueba:* bajar C-09b a [HIPÓTESIS] y ver si P3 queda con 2 MdV.
2. **El driver de "claridad de precios" es un tema de marca o de red, no de persona.** En Mecánica, PEUGEOT tiene NPS 55,6 y CITROËN 59,2 (research/03 §5a). *Prueba:* cortar "claridad de precios ≤3" por marca y por sucursal con n ≥ 200. Si se concentra en una o dos marcas, es un problema de red y no un perfil.
3. **Otro miedo es más fuerte.** Entre detractores de taller, "Cumplimiento de acuerdos" (17,5 %) pesa más que "Precios y costos" (9,2 %). *Prueba:* si "cumplimiento de acuerdos" se concentra en las mismas filas que "claridad de precios", P3 es parte de P2/P4, no persona propia. Ver la tabla de solapamiento: P2-P3 53 % en Mecánica.

**P4 (no sabe qué pasó con su auto)**
1. **Es la misma gente que P2 y que C-21 (reparación mal hecha).** P4 se solapa con P2 en 63 % (Mecánica) y con reparado = No en 56 %. *Prueba:* fusionar (ver 5) y ver si la fusión conserva la señal. Si la señal de "información" desaparece dentro de reparado = Sí, P4 es calidad, no información.
2. **En Usados no hay medición equivalente.** C-14 solo existe en Nuevo. El persona dice "compradores que reciben el vehículo", pero solo se mide en un canal. *Prueba:* pedir a CRM si el ítem "Información proporcionada por vendedor" existe en la encuesta de Usados (no aparece en el archivo). Si no, P4 es de Nuevo.
3. **ZMOT no mide el miedo.** C-13 (2,3 %) es un pedido de información, no miedo. *Prueba:* bajar a hipótesis y ver que P4 queda con 3 MdV de taller y venta, sin ZMOT. Es lo que hoy ya se muestra.

**P5 (llega y se siente mal recibido)**
1. **La etiqueta "mal trato" no corresponde al ítem.** El UMOT de taller mide "acogida en sala de espera", y el de Usados mide "acogida en sala" (D-A1). *Prueba:* renombrar a "acogida" y ver si el miedo sigue siendo "trato". Si no, P5 es un ítem de una sola dimensión.
2. **Es la misma gente que P2 y P4.** En Usados, la acogida de UMOT (76) está casi entera en FMOT (73). *Prueba:* fusión (ver 5). La señal de trato no crece al sumar P5 a F.
3. **Atención es valence, no miedo.** La atención es el motivo de 82 % de promotores en Venta y 76,9 % en Mecánica. *Prueba:* comparar la tasa de atención ≤2 entre detractores y promotores. Si los promotores también la califican bajo, es un tema neutro. Con la tasa de detractores (21-51 %) sí parece un miedo, pero el documento no mide la tasa de promotores con ≤2.

### 13. Qué debe corregir F antes de comité (en orden)

1. **C-05:** cambiar el denominador de 1.003 a 431 respondidos (13,9 %) y mostrar el corte por año (2024: 4,9 %; 2025: 23,5 %; 2026: 40,4 %). Mencionar que 2023 no tiene respuestas.
2. **Regla de independencia:** la regla "3 MdV" debe contar poblaciones de respondentes, no MdV. Con ese criterio solo P2 (y F) cumple. Presentar la regla y el resultado en la misma tabla.
3. **Fusión:** decidir entre la opción A (3 personas, F = P2+P4+P5) y la B (4 personas). Hoy el documento deja 5, que el solapamiento no sostiene.
4. **Denominadores de §9:** corregir `6F` (regex `\[HIPÓTESIS`) y reportar 18, 20, 15, 14 y 14.
5. **C-09b y C-13:** bajar a [HIPÓTESIS] y unificar la matriz §7 con el recorrido de P3.
6. **Contradicciones:** agregar D-N2, D-N3, D-N7, D-B1 con ambas cifras, y completar D-N6 y D-E1.
7. **Cita #662:** corregir "transparente" a "trasparente" o marcar [sic].
8. **SERNAC:** marcar el marco legal como NO VERIFICADO hasta leer la circular primaria.
9. **"garantía en usados" (§10):** cambiar a "seminuevos" o marcar como término de competidor.
10. **Fecha de la cita `#3943`:** quitar "el 4 de septiembre".
11. **Referencia del 76,9 %:** el valor sale de `smot_mecanica.py` (sección de promotores), no de `research/03_smot.md §6`, que no lo contiene.
12. **P2 y P4 en la matriz §7:** P4 en ZMOT está marcado ○ y en el recorrido [DATO débil]. Unificar.

### 14. Veredicto resumido

- P1: **cae** como persona independiente; pasa solo contando MdV.
- P2: **sobrevive con redefinición** (fricción de comunicación), con el silencio directo solo en leads.
- P3: **cae** como persona; hipótesis de costo.
- P4: **se funde** con P2 (y tiene 56 % de solapamiento con reparación mal hecha).
- P5: **se funde** con P2 y P4.
- **Fusión propuesta:** P1 y P3 como hipótesis, y F = P2 + P4 + P5 como persona única con respaldo en 3 poblaciones.

### 15. Cambios hechos en esta auditoría

- `entregables/GUIA_ENTREVISTA.md`: reescrita. Las preguntas pasan a Q1-Q10 para no chocar con P1-P5. Se reemplazó la pregunta de terminación (ahora C-23, hipótesis sin persona) por una sobre el plazo de respuesta a solicitudes (P2). Se actualizaron las referencias a personas (P1 espera, P3 costo) y se quitó la referencia a "MOFU de P4" (la tasación es la familia C-22, sin persona).
- `analisis/7G_solapamiento_personas.py`: nuevo, solo lectura.
- `entregables/BUYER_PERSONAS_PORTILLO.md`: sin cambios (es de F).

---

## Re-auditoría final (cierre, 2026-11-23)

**Objeto:** `entregables/BUYER_PERSONAS_PORTILLO.md` (versión 3) y `research/06_arquetipos_cliente.md`, después de las correcciones de F. **USO INTERNO.**

**Veredicto: necesita un último cambio** (de etiquetas, no de cifras). Lista de bloqueos al final.

### Verificación punto por punto

1. **Una persona y tres hipótesis.** Confirmado. §0 dice "una persona (P2, fusión F) y tres hipótesis (H1, H2, H3)". En la matriz de §5 y en las tarjetas de §6, H1-H3 aparecen con la etiqueta "H" y no como persona. research/06 §3 lo presenta igual. **Pero** la GUIA de entrevista todavía habla de "P1", "P3" y "P4" como personas (ver bloqueo 1).
2. **C-05 y cortes por año.** Reproducido con `analisis/8H_c05_por_anio.py` (nuevo, solo lectura; creado para este cierre porque ningún script existente produce el corte por año). Salida: base respondidos 431 (Sí 371, No 60), tasa **13,9 %**. Por año: 2023 sin respuestas (294 filas); 2024 13 de 265 (**4,9 %**); 2025 28 de 119 (**23,5 %**); 2026 19 de 47 (**40,4 %**). El 6,0 % sobre 1.003 queda marcado como incorrecto. research/06 (C-05-año) cita "conteo directo"; debe citar el script.
3. **Cita #662.** Verificado por fila `CR_Lead-Portillo_202#662`: la fuente dice "Ser más **trasparente** con el costo establecido en la cotización"; el documento dice lo mismo. Coincide. Sin corrección pendiente.
4. **SERNAC y "garantía en usados".** Sin afirmación sin respaldo. El marco legal está en §7 como NO VERIFICADO (circular Res. Ex. N° 923 no leída en primaria). El "garantía" de §9 se aplica como prohibición. La cita de Pompeyo ("inspeccionados, con garantía") sí está en `research/05` línea 34 como [WEB]. Kavak "7 días o 300 km" y Derco "CAE" también tienen fuente en `research/05`. "Usado" aparece en §7 como término de marco legal y en la tabla D-E1 como cita del aviso de Chileautos. Ninguna es copy de marca.
5. **Denominadores** (reproducidos con `6F_recuentos_correccion.py`, sección D): P2 30 (25 DATO / 0 WEB / 5 HIP; NO VERIFICADO fuera: 6); H1 7 (6 / 0 / 1; fuera: 2); H2 11 (6 / 0 / 5; fuera: 1); H3 5 (5 / 0 / 0; fuera: 0). Coinciden con el documento.
6. **Solapamiento 78,5 %** (2.105 de 2.681, Mecánica) en "Qué NO sabemos": coincide con `7G_solapamiento_personas.py`. Ambos documentos usan 78,5 %; sin discrepancia.
7. **PII, premium, conversión.** Sin correos, RUT, teléfonos ni patentes en el documento ni en research/06. Sin "usado" en copy de marca. Sin conversión lead→venta: solo aparecen negaciones ("no hay conversión ni tasa de cierre").

### Bloqueos (de quién dependen)

1. **Etiquetas de GUIA_ENTREVISTA** (último cambio, sin cifras): Q1, Q4, Q5, Q6, Q7, Q8 y Q9 citan "P1", "P3" y "P4" como personas. Ahora son H1, H2 o parte de P2. Cambiar etiquetas. Dependencia: nadie; lo hace F o yo en la siguiente vuelta.
2. **research/06, C-05-año:** cambiar "conteo directo" por `analisis/8H_c05_por_anio.py`. Dependencia: F.
3. **Captura del campo de contacto:** la pregunta no tiene respuestas en 2023 y la tasa sube en 2025-2026. Dependencia: Beto (fecha de inicio de captura en CRM).
4. **Clave de respondente entre archivos:** sin ella, el solapamiento solo se mide dentro de cada archivo. Dependencia: Beto.
5. **Validación legal (SERNAC):** leer la circular Res. Ex. N° 923 en primaria. Dependencia: Beto / validación legal.
6. **Plazo de respuesta a solicitudes** (base del mensaje de P2): dependencia del equipo comercial Portillo y Beto.
7. **Asignación a Portillo y marca del seminuevo** (D-N1, D-N2, D-E1): dependencia de Beto / Iván Balaguera / equipo comercial Portillo.
