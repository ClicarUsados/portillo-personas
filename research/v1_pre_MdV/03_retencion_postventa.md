# 03 Retención y fricciones de postventa (Subagente C)

Fecha de extracción de los archivos: 2026-11-23. Script: `python3 analisis/3C_retencion_mecanica.py`.
Fuente: `inputs_clean/CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet` (27.516 filas, 58 columnas).
Clasificación: cifras de base CRM de encuesta = **USO INTERNO**.

Etiquetas usadas: [DATO] (archivo + columna + filtro + extracción 2026-11-23), [HIPÓTESIS], NO VERIFICADO, BLOQUEADO.

## Universos

- **GRUPO_COMPLETO**: 27.516 filas, todas las del archivo. Universo principal.
- **PORTILLO_HIPOTESIS** [HIPÓTESIS BLOQUEADA]: `nombre_sucursal` con PORT/PORTILLO al inicio de palabra, regla de `research/00_mapeo_portillo.md`. n = 245 (0,9%) [DATO]. Coincide con el conteo del mapeo (245). Depende de: Beto / Iván Balaguera. Incluye "GAP PORTILLO SERVICIO" (127), "PORTILLOLA FLORIDA SERVICIOS" (60) y "PORTILLOTALCA SERVICIOS" (58); estas dos últimas solo coinciden por prefijo y no están confirmadas como Portillo.

## Contraste con diccionario

Seis cifras de control (filas, nulos de sucursal, sentimiento y macrocategoría, TOYOTA, CHEVROLET) **calzan** con `research/00_diccionario_datos.md`. No hay contradicciones que reportar.

## 1. Distribución NPS

Columna: "En base a tu última experiencia en servicio técnico, ¿qué tan probable es que recomiendes #empresa# a un familiar o amigo?" [DATO]

| Segmento (GRUPO_COMPLETO) | n | % |
|---|---:|---:|
| Detractor (0-6) | 2.497 | 9,1 |
| Pasivo (7-8) | 2.306 | 8,4 |
| Promotor (9-10) | 22.713 | 82,5 |

- NPS (%prom − %det) = **73,5**. Media 9,03; desviación 2,20; mediana 10.
- Distribución: 0 = 2,4%; 1-3 = 2,7%; 4-6 = 4,0%; 7 = 2,9%; 8 = 5,4%; 9 = 12,4%; 10 = 70,2%.
- **Polarización:** no es bimodal en el sentido de dos masas medias. Hay un efecto techo: 72,6% de las notas son 0 o 10, pero el lado bajo (0-6) pesa solo 9,1%. La cola de detractores es pequeña y se concentra en 0-3 (5,3%).
- PORTILLO_HIPOTESIS (n=245) [HIPÓTESIS]: NPS 68,2; detractores 11,4% (n=28); promotores 79,6%. Con n=28 detractores, la diferencia contra grupo no es concluyente.

## 2. Drivers por etapa (escala 1-5; "nota baja" = ≤3; GRUPO_COMPLETO) [DATO]

Base: promotores n=22.712 y detractores n=2.497 (2 NaN por driver, excluidos).

| Driver | % promotores ≤3 | % detractores ≤3 | % detractores ≤2 | Δ pp |
|---|---:|---:|---:|---:|
| Calidad del servicio realizado | 0,6 | 78,2 | 52,3 | 77,6 |
| Fluidez general del proceso | 0,9 | 69,6 | 45,5 | 68,7 |
| Claridad sobre la reparación/mantenimiento | 0,9 | 69,5 | 46,9 | 68,6 |
| Claridad de precios y costos | 8,2 | 70,4 | 44,0 | 62,2 |
| Facilidad para comunicarse | 3,4 | 64,9 | 43,9 | 61,5 |
| Tiempo de entrega del vehículo | 1,8 | 60,9 | 44,6 | 59,1 |
| Acogida en la sala de espera | 2,3 | 51,4 | 23,5 | 49,1 |
| Atención de personal | 0,1 | 46,5 | 25,2 | 46,4 |

Lectura: el detractor califica mal casi todas las etapas. "Atención de personal" es la etapa con menor brecha relativa para detractores (46,5%), mientras que la calidad técnica y la claridad de la reparación separan más a promotores de detractores.

## 3. Macro y microcategorías de motivo por segmento

Categorizado [DATO] (`Macrocategoría 1` / `Microcategoría 1`; 35,7% de filas sin macrocategoría).

| Macrocategoría 1 | Detractor (n=1.835 categorizados) | Pasivo (n=1.285) | Promotor (n=14.586) |
|---|---:|---:|---:|
| Atención | 48,1% | 54,6% | 76,9% |
| Calidad del servicio | 28,1% | 26,4% | 15,7% |
| Precios y costos | 9,2% | 8,2% | 1,2% |
| Comunicación con el cliente | 7,8% | 5,0% | 2,6% |
| Tiempo de entrega del vehículo | 6,2% | 5,3% | 3,5% |

Sin categoría: detractores 26,5% (662), pasivos 44,3%, promotores 35,8%.

Microcategorías top, detractor: "Cumplimiento de acuerdos" 17,5%; "Calidad de servicio del taller" 14,2%; "Atención del personal o asesor" 8,6%; "Resolutividad del personal" 5,6%; "Cumplimiento de plazos" 4,4%; "Percepción de precios" 4,3%.

## 4. Fricciones vs recompra y recomendación (advocacy)

Intención declarada, no conducta: "Volverías al servicio técnico" [DATO]. No hay en esta fuente información de recompra real, por lo que no se afirma conversión ni retención efectiva (NO VERIFICADO).

| Segmento | Sí | No sé | No | Reparado a la 1ª: No |
|---|---:|---:|---:|---:|
| Detractor (n=2.497) | 10,7% | 48,5% | 40,7% | 43,9% (1.097) |
| Pasivo (n=2.306) | 74,0% | 24,5% | 1,5% | 7,8% (180) |
| Promotor (n=22.713) | 98,7% | 1,2% | 0,1% | 1,6% (374) |

Cruce detractores (reparado a la primera × volvería):

- Reparado = Sí (n=1.400): No volvería 29,2%; No sé 55,1%; Sí 15,6%.
- Reparado = No (n=1.097): No volvería **55,4%**; No sé 40,1%; Sí 4,5%.

Es decir, cuando la reparación falla, el detractor no vuelve con más del doble de frecuencia. Entre detractores con alguna señal de fricción (reparado=No o volvería≠Sí): 2.278 (91,2%) [DATO].

Entre promotores con reparación fallida (n=374), "No sé" sube a 6,1% frente a 1,1% cuando la reparación fue correcta. Esta es la señal temprana de riesgo de recompra dentro del segmento que más recomienda.

Macrocategoría entre detractores con reparado=No (categorizados, n=832): Atención 52,5%; Calidad del servicio 26,7%; Comunicación 8,4%; Precios 7,1%.

## 5. Desgloses

### 5a. Por marca (des_marca), n ≥ 200 (54 de 77 marcas omitidas por n bajo) [DATO]

| Marca | n | NPS | % det | Volvería Sí | Reparado No |
|---|---:|---:|---:|---:|---:|
| TOYOTA | 3.744 | 78,5 | 6,6 | 91,7 | 3,9 |
| CHEVROLET | 3.513 | 72,6 | 10,0 | 88,1 | 6,8 |
| MG | 2.140 | 71,8 | 9,8 | 88,5 | 6,9 |
| NISSAN | 1.983 | 73,4 | 8,8 | 89,1 | 5,2 |
| FORD | 1.672 | 68,8 | 10,8 | 86,7 | 6,9 |
| PEUGEOT | 1.539 | 55,6 | 16,8 | 80,8 | 10,3 |
| SUBARU | 1.347 | 74,7 | 7,3 | 88,6 | 4,5 |
| HONDA | 951 | 62,8 | 13,8 | 82,4 | 6,2 |
| VOLKSWAGEN | 934 | 68,1 | 11,7 | 85,2 | 6,4 |
| KIA MOTORS / KIA | 843 / 841 | 82,9 / 82,6 | 4,9 / 5,2 | 92,9 / 93,0 | 3,7 / 5,2 |
| HYUNDAI | 671 | 82,4 | 6,1 | 92,8 | 4,5 |
| CHERY | 571 | 84,9 | 4,2 | 93,7 | 4,7 |
| CITROËN | 451 | 59,2 | 16,4 | 79,6 | 12,4 |
| OPEL | 200 | 56,0 | 18,0 | 78,0 | 11,5 |

Marcas con peor NPS y mayor fricción: PEUGEOT, CITROËN, OPEL, HONDA. Sus n son grandes salvo OPEL (n=200 justo en el umbral). Esto es descriptivo y no equivale a un juicio de calidad de marca, porque la marca se mezcla con la red de sucursales.

### 5b. Por sucursal (nombre_sucursal): SOLO DESCRIPTIVO, no ranking [DATO]

- Filas con `nombre_sucursal` vacío: **619 (2,2%)**; NPS de esas filas 56,4. Se reporta tal cual, no se imputa.
- 96 sucursales distintas. Con n ≥ 100 (≈75 sucursales), el NPS va de 18,0 (n=183) a 92,9 (n=831). Las diferencias son grandes, pero se observan con n de cientos y pueden reflejar la mezcla de marcas de cada sucursal.
- Sucursal de la hipótesis Portillo: "GAP PORTILLO SERVICIO" n=127, NPS 84,3, detractores 3,9%. [HIPÓTESIS]

## 6. Verbatim "¿Qué te motiva a dar esa puntuación?" (anonimizado, ≤15 palabras)

Filtro: ≤15 palabras, sin dígitos, @ ni URL, sin mayúsculas tras la primera palabra. Pasan 721 de 2.258 textos de detractores (31,9%) y 12.963 de 17.509 de promotores (74,0%). Textos de ejemplo, sin edición de contenido:

- Detractor, row_id=CR_2025-Mecánica_202#2, NPS 2: "Servicio poco prolijo, dejando mla cerrado el tapon de aceite del vehiculo, sin acerse responsable"
- Detractor, row_id=CR_2025-Mecánica_202#4, NPS 0: "bajo nivel tecnico para solucionar fallas. bajo nivel tecnico para hacer diagnostico de una falla."
- Detractor, row_id=CR_2025-Mecánica_202#15, NPS 5: "No encontré bastante limpio el aseo del auto"
- Detractor, row_id=CR_2025-Mecánica_202#145, NPS 6: "Podria ver si se cambian o no los componentes"
- Promotor, row_id=CR_2025-Mecánica_202#6, NPS 9: "facil agendamiento de hora, amabilidad de la atención, explicacion de lo realizado en vehiculo"
- Promotor, row_id=CR_2025-Mecánica_202#10, NPS 10: "La buena atención"

Nota: el filtro evita nombres propios en mayúscula, pero no garantiza ausencia total de PII en minúscula. Revisar antes de cualquier uso externo.

## 7. Notas de calidad de datos [DATO]

- "¿Qué te motiva…?" vacío en 6.085 filas (22,1%).
- Macrocategoría 1 vacía en 9.810 (35,7%); microcategoría 1 vacía en 7.318 (26,6%).
- 2 NaN por driver de etapa.
- `sentimiento` vacío en 7.248 (26,3%); no se usa en este informe.
- Fechas de respuesta: 2025-03-04 a 2026-11-23.
- Canal: 27.514 email, 2 "App offline".

## Casos: BLOQUEADO

El archivo `CASOS_PBI__2_.xlsx` no está en el proyecto (no está en `inputs_raw/`). No se buscó fuera del proyecto. No hay análisis de Casos (reclamos, tiempos de resolución, reincidencia) en este informe.
**Depende de: Beto, entregar el archivo.** Pendiente también la validación de Hoja1 (empresa, area_negocio, motivo_reclamo en 0.0; ciudad vacía), como indica el diccionario.

## Qué no sabemos

- Recompra real: no hay en esta fuente visitas ni compras posteriores. "Volverías" es intención declarada. No se afirma conversión lead→venta ni retención efectiva.
- Causalidad: las brechas por driver y motivo son asociaciones descriptivas, no efecto de una etapa sobre la recomendación.
- Representatividad: no se conoce la tasa de respuesta, porque el denominador (OT cerradas en el periodo) no está en los archivos.
- Sucursales y marcas se mezclan (la marca depende de la sucursal y viceversa); las diferencias no están desagregadas.
- Asignación a Portillo: [HIPÓTESIS] bloqueada. Cualquier cifra de PORTILLO_HIPOTESIS depende de confirmación de Beto / Iván Balaguera.
- Sentido de "Atención de personal" como driver: alta tasa de notas altas en promotores y baja brecha relativa; no se interpreta más allá de lo descriptivo.
