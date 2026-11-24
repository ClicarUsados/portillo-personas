# ZMOT — Mapa de empatía (Subagente A)

Fecha de extracción: 2026-11-23. Fuentes: `inputs_clean/CR_Lead-Portillo_*` (1.003 filas, 2023-06-08 a 2026-01-23) y `inputs_clean/CR_Encuesta-funcionalidades-Web_*` (324 filas, 2025-07-18 a 2025-08-23).
Scripts: `python3 analisis/zmot_leads.py` y `python3 analisis/zmot_funcionalidades.py` (imprimen conteos, nunca filas ni texto libre).
Punto de partida: `research/v1_pre_MdV/02_leads_cotizacion.md` y `research/v1_pre_MdV/04_intencion_funcionalidades_demografia.md`. Recalculado desde los parquets; donde difiere de v1, se muestran ambas cifras.

## Advertencias que leer primero

1. **El lead ya cotizó.** Estos leads no representan al visitante general. Ninguna cifra describe el ZMOT completo.
2. **Leads no son compradores [DATO].** No se calcula tasa lead→venta. No hay clave verificada entre `CR_Lead-Portillo` y Venta-Nuevo / Venta-Usados.
3. **La encuesta web no es de visitantes.** Las 324 filas tienen `nombre_categoria_venta` = NUEVO y `fec_factura` poblada (324 de 324). La factura va de 2024-01 a 2025-05; la mediana entre factura y respuesta es de 262 días. Son compradores de vehículo nuevo que responden una lista de deseos post-venta. Las funcionalidades pedidas se usan aquí como **proxy**, no como necesidad de ZMOT. [DATO]
4. **Sesgo de campaña en la encuesta web [DATO]:** Salazar Israel 205 (63,3%), Portillo 72 (22,2%), Coseche 28 (8,6%), Servimaq 19 (5,9%).
5. **Escala de evaluación NO VERIFICADA.** Se asume 5 = mejor en "proceso de cotización" y "calidad del contacto". La escala de acuerdo de la encuesta tampoco tiene diccionario.
6. **Fecha de corte NO VERIFICADA.** La última respuesta del lead es 2026-01-23, casi 10 meses antes de la extracción. No se sabe si es corte de exportación o falta de datos posteriores.

## Universos usados

- **GRUPO_COMPLETO:** 1.003 leads; 324 encuestados web. Es la base principal de este mapa.
- **PORTILLO_HIPOTESIS [HIPÓTESIS, BLOQUEADA]:** leads con PORT/PORTILLO en `nombre_sucursal` = 140 (14,0%). Para encuesta web: PORT/PORTILLO en `nombre_concesionario` = 30 (9,3%). La asignación a Portillo depende de **Beto / Iván Balaguera**. Se usa solo como descriptivo; n < 30 en subgrupos de marca o sucursal no se concluye.

---

## 1. Evaluación de la cotización y del contacto (leads)

**1a. Evaluación del proceso** (base 1.003) [DATO] `¿Cómo evaluaría el proceso de cotización?`

| Valor | n | % |
|---|---:|---:|
| 1 | 119 | 11,9% |
| 2 | 53 | 5,3% |
| 3 | 64 | 6,4% |
| 4 | 113 | 11,3% |
| 5 | 654 | 65,2% |

Top-2 (4-5): 767 (76,5%). Bottom-2 (1-2): 172 (17,1%). Dirección de escala NO VERIFICADA.

**1b. ¿Fue contactado por ventas?** (base 1.003) [DATO] `¿Ha sido contactado por nuestro equipo de ventas…?`

| Valor | n | % sobre 1.003 | % sobre respondidos (431) |
|---|---:|---:|---:|
| Sí | 371 | 37,0% | 86,1% |
| No | 60 | 6,0% | 13,9% |
| Sin respuesta | 572 | 57,0% | — |

**1c. Calidad del contacto** (base 371, solo "Sí") [DATO] `¿Cómo evaluaría la calidad del contacto?`
1: 1 (0,3%) · 2: 9 (2,4%) · 3: 7 (1,9%) · 4: 27 (7,3%) · 5: 327 (88,1%). Respondidos: 371 de 371.

**1d. Cruce proceso × contacto** [DATO] (base 172 con proceso 1-2): No = 36; Sí = 12; sin respuesta = 124. La mayoría de la evaluación baja viene de leads sin respuesta de contacto o que no respondieron ese bloque. Coincide con v1 (36 / 12 / 124).

## 2. Barreras: "¿Qué necesita para seguir con su proceso de cotización?"

Base: 431 respondidos (43,0%). [DATO]

| Opción | n | % sobre 431 | % sobre 1.003 |
|---|---:|---:|---:|
| Ya estoy en contacto con mi ejecutivo | 275 | 63,8% | 27,4% |
| Opción "otros" (ver 2b) | 57 | 13,2% | 5,7% |
| No deseo continuar con el proceso | 31 | 7,2% | 3,1% |
| La cotización formal | 23 | 5,3% | 2,3% |
| Que un ejecutivo me contacte | 21 | 4,9% | 2,1% |
| Información de financiamiento | 14 | 3,2% | 1,4% |
| Mayor información del vehículo | 10 | 2,3% | 1,0% |

**Lectura:** la opción más marcada es "ya estoy en contacto", no una barrera. Las barreras explícitas (cotización formal, que me contacten, financiamiento, más información) suman **68 de 431 (15,8%)** [DATO]. Tratarlas como barrera es [HIPÓTESIS].

**2b. Texto "otros"** (57 filas) [HIPÓTESIS, palabras clave, sin validar a mano]: 40 declaran compra ya realizada (v1, codificación manual: 42). Es una autodeclaración, NO VERIFICADA contra ventas. Por eso "otros" no es una barrera del proceso.

**Contradicción de contacto (ambas cifras):** 60 leads dicen "No" al contacto de ventas, y 275 dicen "ya estoy en contacto con mi ejecutivo". El cruce da **10** casos que no calzan. Se muestra sin corregir.

## 3. Motivo "¿Por qué?" (texto libre, multietiqueta)

Base: 558 respuestas con texto (55,6%). [HIPÓTESIS] Codificación por palabras clave, **baja precisión, sin validación con muestra etiquetada**. Las cifras cambian según la regla (ver sección 7).

| Tema (palabras clave) | n sobre 558 | % | n con proceso 1-2 |
|---|---:|---:|---:|
| Sin respuesta o sin contacto | 39 | 7,0% | 36 |
| Lentitud o tiempos | 132 | 23,7% | 12 |
| Información o documentación | 71 | 12,7% | 13 |
| Precio o transparencia | 40 | 7,2% | 15 |
| Financiamiento, crédito o parte de pago | 23 | 4,1% | 14 |
| Reserva o devolución de dinero | 13 | 2,3% | 6 |
| Stock o disponibilidad | 12 | 2,2% | 5 |
| Trato o atención del ejecutivo | 5 | 0,9% | 1 |

Entre quienes evaluaron 1-2 (n=138 con texto), el tema con más peso es el silencio: 36 de 138 (26,1%) por esta regla. v1 llegó a 54 de 138 (39,1%) con otra regla. Se reporta el rango, no un número.

## 4. Canal de entrada (descripción, no atribución de venta)

[DATO] `origen`, base 1.003. Describe por dónde entró el lead; **no mide qué canal produjo ventas**.

| Origen | n | % |
|---|---:|---:|
| WEB | 609 | 60,7% |
| SALON | 284 | 28,3% |
| SITIO WEB MARCA | 48 | 4,8% |
| SITIO WEB PROPIO | 33 | 3,3% |
| TELEFONICO | 11 | 1,1% |
| Otros (CONTACT CENTER, CAMPAÑA ADS, CAMPAÑAS, DIGITAL EJECUTIVO VTA, EVENTOS, RRSS, SITIOWEBMARKETPLACE) | 15 | 1,5% |
| Vacío | 2 | 0,2% |

## 5. Universo PORTILLO_HIPOTESIS (leads) [HIPÓTESIS, descriptivo]

| Universo | n | Contacto respondido | Contacto Sí |
|---|---:|---:|---:|
| PORTILLO_HIPOTESIS | 140 | 82 | 62 (75,6% de respondidos) |
| Resto | 863 | 349 | 309 (88,5% de respondidos) |

Diferencia con n pequeño (82) y depende de una hipótesis sin confirmar. **No se interpreta como hallazgo.**

## 6. Funcionalidades pedidas (encuesta web) — proxy de compradores nuevos

Universo: GRUPO_COMPLETO, n=324. Todas son compradores de vehículo nuevo (ver advertencia 3). [DATO]

**Top-3 (cada persona marca 3 de 10; control: 972 marcas = 3 × 324):**

| # | Funcionalidad | n | % de 324 | De acuerdo (4-5) |
|---|---|---:|---:|---:|
| 1 | Comparar formas de pago / calcular qué auto puedo comprar (calculadora de pago) | 141 | 43,5% | 85,8% |
| 2 | Contenido educativo sobre compra, financiamiento y mantenimiento | 136 | 42,0% | 84,3% |
| 3 | Opiniones de otros clientes y expertos antes de decidir | 131 | 40,4% | 83,3% |
| 4 | Recomendación de modelos según preferencias y presupuesto | 130 | 40,1% | 84,0% |
| 5 | Alertas sobre el mejor momento para vender mi auto | 115 | 35,5% | 81,2% |
| 6 | Videos, blogs y ranking de modelos | 91 | 28,1% | 80,9% |
| 7 | Personalizar mi auto online (colores, accesorios) | 83 | 25,6% | 71,3% |
| 8 | Agendar test drive en el sitio web | 62 | 19,1% | 71,6% |
| 9 | Sección de vehículos eléctricos (EV) | 43 | 13,3% | 45,1% |
| 10 | Asistente virtual que oriente mientras navego | 40 | 12,3% | 60,8% |

**Apps y otros (acuerdo, escala 1-5 NO VERIFICADA):** historial del vehículo, documentos y boletas 89,8% de acuerdo; avisos de mantenimiento 83,3%; app en el celular 65,7%; aceptar que el chat derive a WhatsApp 67,0%.

**Lectura:** lo que más se pide tiene que ver con decidir la compra (pago, educación, opiniones). EV y asistente virtual quedan al final. Es interés en un proxy post-venta, no evidencia de lo que busca un visitante antes de llegar.

**Subgrupo PORTILLO_HIPOTESIS web (n=30, no concluyente):** contenido educativo 21; opiniones 14; recomendación 14; herramientas de pago 10. [HIPÓTESIS]

## 7. Contradicciones (ambas cifras, sin corregir)

| # | Tema | Cifra A | Cifra B | Estado |
|---|---|---|---|---|
| C1 | Portillo en encuesta web | 72 (22,2%) por `campaña o sensor` [DATO] | 30 (9,3%) por `nombre_concesionario` PORT/PORTILLO [HIPÓTESIS] | Abierta. Depende de Beto / Iván Balaguera |
| C2 | Contacto vs. necesidad (leads) | 60 dicen "No" al contacto [DATO] | 275 dicen "ya estoy en contacto" [DATO]; cruce = 10 | Abierta |
| C3 | Leads usados | `des_marca` = USADOS: 326 [DATO] | `tipo_oportunidad` usado tras normalizar: 327 [DATO] | Diferencia de 1 fila |
| C4 | Marco de la encuesta web | Brief: funcionalidades pedidas en el sitio (visitante) | Datos: 324 de 324 son NUEVO con factura, mediana 262 días antes de la encuesta [DATO] | Abierta. Cambia cómo se lee el mapa |
| C5 | Codificación del motivo (v2 vs v1) | "Sin respuesta": 39 (v2) vs 61 (v1) [HIPÓTESIS] | "Lentitud": 132 (v2) vs 85 (v1); "Precio": 40 vs 43; "Financiamiento": 23 vs 21 | Diferencia por regla de palabras clave; no hay cifra verdadera |
| C6 | Compra declarada en "otros" | 40 (v2, palabras clave) [HIPÓTESIS] | 42 (v1, codificación manual) [HIPÓTESIS] | Diferencia de regla |

## 8. Mapa de empatía ZMOT

**Piensa y siente**
- Evalúa el proceso de cotización con 4-5: **767 (76,5%)** [DATO]. Dirección de escala NO VERIFICADA.
- Calidad del contacto con 5, entre quienes fueron contactados: **327 de 371 (88,1%)** [DATO].
- Citas: sin cita positiva verificada en esta corrida.

**Oye**
- NO VERIFICADO: no hay dato de qué escucharon antes de cotizar.
- Lo que les prometieron, según texto libre: que los contactarían. Cita: "Se suponía que me contactarían y no ha pasado nada" (CR_Lead-Portillo_202#4). n no calculado.

**Ve**
- Por dónde entró: WEB 609 (60,7%), SALON 284 (28,3%) [DATO]. Es descripción, no atribución.
- Stock visible: keyword "stock o disponibilidad" 12 (2,2%) [HIPÓTESIS]. Cita: "No tienen el auto para verlo" (CR_Lead-Portillo_202#32).

**Dice y hace**
- "Ya estoy en contacto con mi ejecutivo": **275 (63,8% de 431)** [DATO].
- "No deseo continuar con el proceso": **31 (7,2% de 431)** [DATO]. Motivo no verificado.
- Declaran compra ya hecha en "otros": **40 de 57** [HIPÓTESIS, autodeclaración].
- Cita: "Solicite cotización y nadie me ha contactado hasta el momento" (CR_Lead-Portillo_202#5).

**Esfuerzos (miedos, frustraciones, objeciones)**
- Silencio después de cotizar: **60 "No" al contacto** [DATO]; keyword "sin respuesta" 39 [HIPÓTESIS]. Cita: "Nunca me enviaron nada, solo me llego un mensaje automático por WhatsApp" (CR_Lead-Portillo_202#555).
- Lentitud: keyword **132 (23,7% de 558)** [HIPÓTESIS, baja precisión; v1 = 85].
- Información insuficiente: keyword **71 (12,7%)** [HIPÓTESIS] + "mayor información del vehículo" **10** [DATO]. Cita: "No me respondieron nada sobre valores, opciones de pago y financiamiento." (CR_Lead-Portillo_202#61).
- Precio o transparencia: keyword **40 (7,2%)** [HIPÓTESIS]. Cita: "Ser más trasparente con el costo establecido en la cotización" (CR_Lead-Portillo_202#662).
- Financiamiento: keyword **23 (4,1%)** [HIPÓTESIS] + "información de financiamiento" **14 (3,2% de 431)** [DATO].
- Trato del ejecutivo: keyword 5 (0,9%). Descartado por n.

**Resultados (deseos, medida de éxito)**
- Deseo declarado: cotización formal **23 (5,3%)**; que un ejecutivo contacte **21 (4,9%)** [DATO].
- Medida de éxito observable: contacto con calidad 5 (88,1% de contactados) y proceso 4-5 (76,5% de todos) [DATO].
- Funcionalidades pedidas (proxy post-venta, sección 6): comparar pagos 43,5%; contenido educativo 42,0%; opiniones 40,4%; test drive 19,1%; EV 13,3%; asistente 12,3%.

## 9. Candidatos a miedo dominante (ZMOT)

Miedos con más evidencia en este momento. Arquetipo de cliente NO asignado aquí; se obtiene después al cruzar miedos que se repiten en al menos 3 de 4 MdV.

| # | Miedo candidato | n | Etiqueta | Evidencia |
|---|---|---:|---|---|
| C1 | Silencio tras cotizar: no ser contactado | **60** (No al contacto) | [DATO] | Sostenido por 39 "sin respuesta" [HIPÓTESIS] y 21 "que me contacte" [DATO]. Lectura más firme del corpus |
| C2 | Demora: esperar demasiado | **132** (23,7% de 558) | [HIPÓTESIS] | Baja precisión. v1 = 85. Rango 85-132 |
| C3 | Decidir sin información suficiente (vehículo, precio, pagos) | **81** (71 información + 10 "mayor información") | [HIPÓTESIS] + [DATO] | Mezcla de keyword y opción de encuesta |
| C4 | Precio y financiamiento opacos | **63** (40 precio + 23 financiamiento) | [HIPÓTESIS] | Keyword. Se solapan algunos textos (no calculado) |

Descartado: trato del ejecutivo (n=5) y stock (n=12), por tamaño.

## 10. Rutas

- **Con el archivo ya disponible:** la base de leads está lista para cruzar con MdV FMOT y SMOT. No hay clave verificada con ventas.
- **Para validar la codificación del motivo:** etiquetar a mano una muestra (p. ej. 100 textos) por dos personas. Se hace antes de usar C2-C4 en comité.
- **Para medir el ZMOT real:** encuesta o datos de visitantes que no hayan cotizado. Hoy no existen en `inputs_clean/`.

## 11. Bloqueos

- Asignación de sucursales y marcas a Portillo (PORTILLO_HIPOTESIS). Depende de **Beto / Iván Balaguera**.
- Campo que define Portillo en la encuesta web: `campaña o sensor` (72) o `nombre_concesionario` (30). Depende de **Beto / Iván Balaguera**.
- Dirección de la escala 1-5 de cotización y de calidad del contacto. Depende de **Beto** (quien diseñó o administra la encuesta y el CRM).
- Fecha de corte de leads (2026-01-23). Depende de **Beto** (fecha de exportación).
- Cruce lead→venta: no hay clave verificada. Depende de **Beto** (llave común entre leads y ventas).
- Visitantes que no cotizaron: no hay fuente en `inputs_clean/`. Depende de **Beto** (si existe analítica web).

## 12. Qué no sabemos

- Cuántos visitantes llegan al sitio y no cotizan. [NO VERIFICADO]
- Si el lead que cotizó busca lo mismo que el visitante general.
- Si el silencio post-cotización explica la baja de cierre. No se afirma: no hay dato de conversión.
- Por qué 31 leads "no deseo continuar" (no verificado).
- Si la encuesta web (compradores de nuevo) describe a quien compra usados.

[WEB] Ninguna fuente web se usó en esta corrida. [NO VERIFICADO] los datos de plantilla y cierres de locales de v1 no se repiten aquí.
