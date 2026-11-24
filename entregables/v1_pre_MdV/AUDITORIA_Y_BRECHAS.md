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
