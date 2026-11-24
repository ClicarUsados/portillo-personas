# Leads y proceso de cotización — Subagente B

Fuente: `inputs_clean/CR_Lead-Portillo_2023-03-01_2026-11-23_216d73e0__sin_segmento.parquet` (1.003 filas, 26 columnas).
Fecha de extracción de los archivos: 2026-11-23.
Script: `analisis/2B_leads_cotizacion.py` — reproducir con `python3 analisis/2B_leads_cotizacion.py`.

## Advertencias antes de leer las cifras

- **Cobertura [DATO]:** las encuestas las responde quien ya cotizó y dejó sus datos. No es el universo de visitantes ni de todos los interesados. Ninguna cifra de este reporte describe a todo el público de Portillo.
- **Leads no son compradores [DATO]:** este reporte describe leads que respondieron una encuesta. No se calcula ni se afirma tasa de cierre ni conversión lead→venta. Los compradores se analizan en otro subagente, y no hay una clave verificada que cruce este archivo con Venta-Nuevo o Venta-Usados.
- **Universos:**
  - GRUPO_COMPLETO = las 1.003 filas del archivo.
  - PORTILLO_HIPOTESIS = filas con PORT o PORTILLO en `nombre_sucursal` (140 filas, 14,0%). **[HIPÓTESIS] bloqueada**: la asignación a Portillo depende de Beto / Iván Balaguera (ver `research/00_mapeo_portillo.md`).
- **Umbral de conclusión:** n < 30 se marca como NO CONCLUYENTE.
- **Fecha de corte [NO VERIFICADO]:** la última respuesta es 2026-01-23, casi 10 meses antes de la fecha de extracción (2026-11-23). No sabemos si el corte es de exportación o si no hubo leads después.

## 1. Evaluación del proceso de cotización y del contacto

**1a. Evaluación del proceso de cotización** (base: 1.003) — [DATO] `¿Cómo evaluaría el proceso de cotización?`

| Valor | n | % sobre 1.003 |
|---|---:|---:|
| 1 | 119 | 11,9% |
| 2 | 53 | 5,3% |
| 3 | 64 | 6,4% |
| 4 | 113 | 11,3% |
| 5 | 654 | 65,2% |

Top-2 (4-5): 76,5%. Bottom-2 (1-2): 17,1%.
*Dirección de la escala (5 = mejor) — NO VERIFICADO.* El diccionario no la documenta; la lectura de arriba depende de ese supuesto.

**1b. ¿Fue contactado por ventas?** (base: 1.003) — [DATO] `¿Ha sido contactado por nuestro equipo de ventas…?`

| Valor | n | % sobre 1.003 | % sobre respondidos (431) |
|---|---:|---:|---:|
| Sí | 371 | 37,0% | 86,1% |
| No | 60 | 6,0% | 13,9% |
| Sin respuesta (no aplica al flujo) | 572 | 57,0% | — |

**1c. Calidad del contacto** (base: 371, solo quienes dijeron Sí) — [DATO] `¿Cómo evaluaría la calidad del contacto?`

| Valor | n | % sobre 371 |
|---|---:|---:|
| 1 | 1 | 0,3% |
| 2 | 9 | 2,4% |
| 3 | 7 | 1,9% |
| 4 | 27 | 7,3% |
| 5 | 327 | 88,1% |

**1d. Cruce proceso × contacto** — [DATO]. Entre quienes evaluaron el proceso con 1 o 2 (n=172): 36 dicen No al contacto, 12 dicen Sí y 124 no respondieron la pregunta de contacto. La mayoría de la evaluación baja viene de leads que no fueron contactados o que no respondieron ese bloque.

## 2. Qué necesita el lead para seguir

Base: 431 respondidos (43,0% del total). — [DATO] `¿Qué necesita para seguir con su proceso de cotización?`

| Opción | n | % sobre 431 | % sobre 1.003 |
|---|---:|---:|---:|
| Ya estoy en contacto con mi ejecutivo | 275 | 63,8% | 27,4% |
| Opción otros (ver codificación) | 57 | 13,2% | 5,7% |
| No deseo continuar con el proceso | 31 | 7,2% | 3,1% |
| La cotización formal | 23 | 5,3% | 2,3% |
| Que un ejecutivo me contacte | 21 | 4,9% | 2,1% |
| Información de financiamiento | 14 | 3,2% | 1,4% |
| Mayor información del vehículo | 10 | 2,3% | 1,0% |

**Lectura:** la opción más marcada es "ya estoy en contacto", no una barrera. Las barreras explícitas (cotización formal, contacto, financiamiento, más información) suman 68 de 431 (15,8%). Esto es [DATO] sobre las opciones; su interpretación como barrera es [HIPÓTESIS].

**Codificación de "Texto opción otros"** (57 filas) — [HIPÓTESIS] codificación manual del subagente B. Cada row_id tiene un código asignado a mano en el script; el texto no se conserva en el reporte.

| Código | n |
|---|---:|
| Declara compra ya realizada (autodeclaración, no verificada contra ventas) | 42 |
| Sin contenido o ambiguo | 6 |
| En proceso de compra o con asesor | 2 |
| Espera de contacto o lentitud | 2 |
| Sigue evaluando alternativas | 2 |
| No continuará con el proceso | 1 |
| Financiamiento o parte de pago | 1 |
| Satisfacción sin barrera | 1 |

Cruce con contacto: de las 57 filas, 53 dicen Sí al contacto y 4 dicen No. **Importante:** 42 de 57 "otros" son personas que dicen haber comprado. Eso significa que la opción "otros" no es una barrera del proceso. No se calcula con ello ninguna tasa.

## 3. Desglose por marca, tipo de oportunidad y sucursal

**Reglas:** `des_marca` se normaliza a mayúsculas y sin tildes (Toyota → TOYOTA, Citroën → CITROEN). `tipo_oportunidad`: "Vehiculo Nuevos" y "NUEVOS" → nuevo; "Vehiculos Usados" y "USADOS" → usado; vacío → SIN DATO.

**3a. Por marca** ([DATO], n sobre 1.003)

| Marca | n | % | Top-2 | Contacto Sí (sobre respondidos) |
|---|---:|---:|---:|---:|
| USADOS (valor de des_marca, no es marca) | 326 | 32,5% | 81,6% | 94,9% (n=137) |
| TOYOTA | 205 | 20,4% | 72,2% | 76,5% (n=85) |
| PEUGEOT | 186 | 18,5% | 80,6% | 91,4% (n=81) |
| NISSAN | 92 | 9,2% | 72,8% | 84,6% (n=39) |
| MG | 69 | 6,9% | 81,2% | 93,1% (n=29) |
| HYUNDAI | 47 | 4,7% | 72,3% | 85,0% (n=20) |
| SIN DATO | 20 | 2,0% | 55,0% | NO CONCLUYENTE |
| OPEL (27), JAC (8), CITROEN (7), LEXUS (6), BAIC (3) y 7 marcas con n=1 | 58 | 5,8% | — | NO CONCLUYENTE (n<30 cada una) |

Las marcas con n<30 no se interpretan. JAC tiene top-2 de 25,0% con n=8, pero no es concluyente.

**3b. Por tipo de oportunidad** ([DATO])

| Tipo | n | % | Top-2 | Contacto Sí (sobre respondidos) |
|---|---:|---:|---:|---:|
| nuevo | 653 | 65,1% | 74,9% | 82,6% (n=288) |
| usado | 327 | 32,6% | 81,7% | 93,0% (n=143) |
| SIN DATO | 23 | 2,3% | 47,8% | NO CONCLUYENTE |

**3c. Por sucursal** ([DATO], `nombre_sucursal`)

- Distintas: 75 sucursales reales más la categoría vacía (SIN DATO, 231 filas = 23,0%).
- Con n≥30: 5 sucursales. Suman 181 filas (18,0%):
  - USADOS AUTOSHOPING: 50 (5,0%), top-2 96,0%
  - PLAZA OESTE PEUGEOT: 34 (3,4%), top-2 82,4%
  - USADOS MOVICENTER: 33 (3,3%), top-2 100,0%
  - PEUGEOT LAS CONDES: 32 (3,2%), top-2 75,0%
  - TOYOTA MOVICENTER: 32 (3,2%), top-2 84,4%
- Las otras 70 sucursales (591 filas, 58,9%) tienen n<30 cada una y **no son concluyentes**.
- Nota: los porcentajes de la tabla del script se calcularon sobre el subconjunto de n≥30 (412 filas). Los de este reporte están sobre 1.003.

**3d. Universos** ([DATO] salvo la hipótesis de Portillo)

| Universo | n | Top-2 | Contacto respondido | Contacto Sí |
|---|---:|---:|---:|---:|
| GRUPO_COMPLETO | 1.003 | 76,5% | 431 | 86,1% |
| PORTILLO_HIPOTESIS [HIPÓTESIS] | 140 | 72,1% | 82 | 75,6% |
| Resto (sin PORT en sucursal) | 863 | 77,2% | 349 | 88,5% |

La diferencia en contacto entre PORTILLO_HIPOTESIS y el resto (75,6% contra 88,5%) es una señal con n pequeño (82) y depende de una hipótesis no confirmada. No se interpreta como hallazgo.

## 4. Origen (canal de entrada, descriptivo, no atribución de venta)

[DATO] `origen`, base 1.003:

| Origen | n | % |
|---|---:|---:|
| WEB | 609 | 60,7% |
| SALON | 284 | 28,3% |
| SITIO WEB MARCA | 48 | 4,8% |
| SITIO WEB PROPIO | 33 | 3,3% |
| TELEFONICO | 11 | 1,1% |
| CONTACT CENTER, CAMPAÑA ADS, CAMPAÑAS, DIGITAL EJECUTIVO VTA, EVENTOS, RRSS, SITIOWEBMARKETPLACE | 15 | 1,5% |
| Vacío | 2 | 0,2% |

Esto describe por dónde entró el lead. No mide qué canal produjo ventas.

## 5. Motivo "¿Por qué?" (barreras)

Base: 558 respuestas con texto (55,6% del total). Codificación por palabras clave, **multietiqueta**: una respuesta puede contar en varios temas. **[HIPÓTESIS]**, con baja precisión. El tema "Trato" en particular fue reducido en el script para evitar falsos positivos (de 205 a 46).

| Tema | n (sobre 558) | % | n con Q1 en 1-2 (de 138) |
|---|---:|---:|---:|
| Información o documentación | 71 | 12,7% | 22 |
| Lentitud o tiempos | 85 | 15,2% | 14 |
| Sin respuesta o sin contacto | 61 | 10,9% | 54 |
| Precio o transparencia | 43 | 7,7% | 17 |
| Trato o atención del ejecutivo | 46 | 8,2% | 15 |
| Financiamiento, crédito o parte de pago | 21 | 3,8% | 14 |
| Reserva o devolución de dinero | 11 | 2,0% | 5 |
| Stock o disponibilidad | 10 | 1,8% | 8 |

Lectura: entre quienes evaluaron el proceso con 1 o 2, el tema más frecuente es **no tener respuesta o contacto** (54 de 138 textos, 39,1%). Es la señal más clara del corpus. [HIPÓTESIS] sobre la codificación, [DATO] sobre el conteo.

**Citas verbatim** (≤15 palabras, anonimizadas, con row_id; texto literal del dato):
- `CR_Lead-Portillo_202#5`: "Solicite cotización y nadie me ha contactado hasta el momento"
- `CR_Lead-Portillo_202#555`: "Nunca me enviaron nada, solo me llego un mensaje automático por WhatsApp"
- `CR_Lead-Portillo_202#61`: "No me respondieron nada sobre valores, opciones de pago y financiamiento."
- `CR_Lead-Portillo_202#662`: "Ser más trasparente con el costo establecido en la cotización"
- `CR_Lead-Portillo_202#4`: "Se suponía que me contactarían y no ha pasado nada"
- `CR_Lead-Portillo_202#32`: "No tienen el auto para verlo"

## 6. Contradicciones y chequeos de consistencia

No se corrige ninguna cifra. Se muestran ambas:

- **Contacto = No y necesidad = "Ya estoy en contacto con mi ejecutivo": n=10.** Son 60 "No" al contacto por ventas, y 275 personas dicen estar ya en contacto. Son respuestas que no calzan entre sí (10 casos).
- **Tipo usado:** `des_marca` = USADOS n=326; `tipo_oportunidad` usado tras normalizar n=327. Diferencia de 1 fila; no se resuelve.
- **Calidad del contacto (371) = contacto Sí (371).** Calza. El bloque de necesidades (431) = contacto respondido (431). Calza.
- **Sucursales con PORT:** 140, igual al mapeo (`00_mapeo_portillo.md`). Calza.
- **Marca (columna `marca`):** vacía en 992 de 1.003. `des_marca` tiene 20 vacíos. Se usa `des_marca`.

## Qué no sabemos

- Dirección de la escala de evaluación (NO VERIFICADO).
- Si la fecha de corte (2026-01-23) es un corte de exportación o falta de datos posteriores.
- Si estos leads se cruzan con ventas. No hay clave verificada con Venta-Nuevo o Venta-Usados.
- Si las 42 autodeclaraciones de compra en "otros" se corresponden con ventas registradas.
- La asignación de sucursales y marcas a Portillo ([HIPÓTESIS] bloqueada, depende de Beto / Iván Balaguera).
- La precisión real de la codificación por palabras clave del campo "¿Por qué?" (no validada con una muestra etiquetada por dos personas).
- El significado de "SIN DATO" en sucursal (231 filas): si es lead sin sucursal asignada o campo no capturado (NO VERIFICADO).
