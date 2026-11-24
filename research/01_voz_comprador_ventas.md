# 01 — Voz del comprador (ventas) — Subagente A

**USO INTERNO.** Datos de encuesta post-venta (CRM de Grupo Americar). No compartir fuera del equipo.

Fecha de extracción de los archivos: 2026-11-23.
Script reproducible: `analisis/1A_voz_ventas.py` (desde la raíz: `python3 analisis/1A_voz_ventas.py`). Solo imprime conteos y porcentajes.
Fuentes: `inputs_clean/CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f6b8ef__sin_segmento.parquet` y `inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet`.

## Universos y definiciones

- **GRUPO_COMPLETO**: todas las filas de cada archivo.
- **PORTILLO_HIPOTESIS** [HIPÓTESIS, bloqueado]: `nombre_concesionario` contiene la palabra `PORT` o `PORTILLO`. La asignación a Portillo depende de Beto / Iván Balaguera.
- **Segmento NPS** (columna `En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa#...`): promotor 9-10, pasivo 7-8, detractor 0-6. Una fila sin dato en cada archivo, excluida.
- **Detractor de etapa** (criterio de este análisis, no estándar): puntuación 1-2 en escala 1-5.
- **Motivo** = macrocategoría codificada en la columna `Macrocategoría 1` del bloque NPS (pregunta `¿Qué te motiva a dar esa puntuación?`). Los códigos vienen ya asignados en el archivo; no los recodifiqué.

## 1. Tamaños de muestra

[DATO] Nuevo (`CR_2025-Venta-Nuevo`, 6.458 filas), GRUPO_COMPLETO:
- Promotor 5.732 (88,8 %), pasivo 377 (5,8 %), detractor 348 (5,4 %).

[DATO] Usados (`CR_2025-Venta-Usados`, 4.103 filas), GRUPO_COMPLETO:
- Promotor 3.544 (86,4 %), pasivo 245 (6,0 %), detractor 313 (7,6 %).

[DATO] Nuevo, PORTILLO_HIPOTESIS (n = 1.311): promotor 1.149 (87,6 %), pasivo 81 (6,2 %), detractor 81 (6,2 %). [HIPÓTESIS] en la asignación.

[DATO] Usados, PORTILLO_HIPOTESIS (n = 145 con `\bPORT`): promotor 123, pasivo 11, detractor 11. **El subconjunto de detractores (n = 11) es demasiado pequeño para leer tendencias.** Ver contradicción C1.

## 2. Motivos NPS: ranking por segmento

Base: filas del segmento con motivo codificado (`Macrocategoría 1`). Porcentaje sobre codificadas del segmento.

[DATO] Nuevo, GRUPO_COMPLETO (`Macrocategoría 1`, filtro por segmento NPS):

| Segmento | Macrocategoría | n | % de codificadas |
|---|---|---:|---:|
| Promotor (n codificadas 3.915) | Atención | 3.209 | 82,0 % |
| | Condición del vehículo | 356 | 9,1 % |
| | Rapidez del proceso | 127 | 3,2 % |
| | Comunicación con cliente | 115 | 2,9 % |
| Pasivo (n codificadas 186) | Atención | 103 | 55,4 % |
| | Rapidez del proceso | 33 | 17,7 % |
| | Condición del vehículo | 17 | 9,1 % |
| Detractor (n codificadas 261) | Atención | 77 | 29,5 % |
| | Rapidez del proceso | 64 | 24,5 % |
| | Documentación | 39 | 14,9 % |
| | Condición del vehículo | 32 | 12,3 % |
| | Comunicación con cliente | 29 | 11,1 % |
| | Precios y financiamiento | 20 | 7,7 % |

[DATO] Usados, GRUPO_COMPLETO (`Macrocategoría 1`, filtro por segmento NPS):

| Segmento | Macrocategoría | n | % de codificadas |
|---|---|---:|---:|
| Promotor (n codificadas 2.372) | Atención | 1.953 | 82,3 % |
| | Condición del vehículo | 231 | 9,7 % |
| Pasivo (n codificadas 139) | Atención | 74 | 53,2 % |
| | Condición del vehículo | 19 | 13,7 % |
| | Rapidez del proceso | 17 | 12,2 % |
| Detractor (n codificadas 214) | Atención | 80 | 37,4 % |
| | Condición del vehículo | 52 | 24,3 % |
| | Rapidez del proceso | 25 | 11,7 % |
| | Documentación | 24 | 11,2 % |
| | Comunicación con cliente | 19 | 8,9 % |
| | Precios y financiamiento | 13 | 6,1 % |

**Lectura importante.** `Atención` es el motivo dominante también entre promotores (82 %). Es un tema, no una valencia: explica la nota alta y la baja. Por eso el dolor se lee con la **tasa de detractores dentro de cada tema** (sección 4), no con el conteo bruto.

[DATO] Menciones en cualquier macro 1-5 (Nuevo, detractores, GRUPO_COMPLETO; base = 261 filas codificadas): Rapidez del proceso 150 (57,5 %), Atención 115 (44,1 %), Comunicación con cliente 80 (30,7 %), Precios y financiamiento 62 (23,8 %), Documentación 42 (16,1 %), Condición del vehículo 33 (12,6 %).

[DATO] Menciones en cualquier macro 1-5 (Usados, detractores, GRUPO_COMPLETO; base = 214): Atención 121 (56,5 %), Rapidez del proceso 83 (38,8 %), Comunicación con cliente 59 (27,6 %), Precios y financiamiento 58 (27,1 %), Condición del vehículo 52 (24,3 %), Documentación 35 (16,4 %).

[DATO] Top microcategoría 1 entre detractores, Nuevo, GRUPO_COMPLETO (`Microcategoría 1`): Plazos de entrega 64 (18,4 % de los 348 detractores); Atención general 32 (9,2 %); Atención post venta 30 (8,6 %); Calidad del producto 23 (6,6 %); Factura 22 (6,3 %); Permiso de circulación 17 (4,9 %).

[DATO] Top microcategoría 1 entre detractores, Usados, GRUPO_COMPLETO (`Microcategoría 1`): Sin categoría 57 (18,2 % de 313); Atención post venta 47 (15,0 %); Detalles del vehículo 26 (8,3 %); Plazos de entrega 24 (7,7 %); Atención general 23 (7,3 %); Calidad del producto 22 (7,0 %); Permiso de circulación 18 (5,8 %).

## 3. Qué etapa castiga la nota

Escala 1-5. Media, % de 1-2 y media por segmento. Bandera de polarización = media ≥ 4,0 y % de 1-2 ≥ 10 % (criterio de este script). **Ninguna etapa cumple la bandera.** Pero la media total oculta una separación fuerte por segmento, que se ve abajo.

[DATO] Nuevo, GRUPO_COMPLETO (`CR_2025-Venta-Nuevo`, columnas de etapa):

| Etapa (columna) | n | Media total | % 1-2 total | Media detractores | % detractores con 1-2 (n) |
|---|---:|---:|---:|---:|---:|
| Acogida en sala de ventas | 6.458 | 4,80 | 0,9 % | 3,76 | 12,4 % (43 de 348) |
| Atención del vendedor | 6.458 | 4,87 | 1,2 % | 3,59 | 21,3 % (74 de 348) |
| Claridad de precios y opciones de financiamiento | 6.458 | 4,74 | 1,4 % | 3,47 | 20,1 % (70 de 348) |
| Facilidad de comunicación con vendedor | 6.458 | 4,84 | 1,7 % | 3,36 | 28,2 % |
| **Fluidez general del proceso** | 6.458 | 4,69 | 3,7 % | **2,38** | **58,0 % (202 de 348)** |
| Información proporcionada por vendedor (solo Nuevo) | 6.458 | 4,81 | 1,8 % | 3,19 | 31,0 % |
| Vehículo en parte de pago | 2.984 | 4,58 | 3,7 % | 3,37 | 21,8 % (27 de 124) |

[DATO] Usados, GRUPO_COMPLETO (`CR_2025-Venta-Usados`):

| Etapa (columna) | n | Media total | % 1-2 total | Media detractores | % detractores con 1-2 (n) |
|---|---:|---:|---:|---:|---:|
| Acogida en sala de ventas | 4.103 | 4,73 | 2,1 % | 3,42 | 23,3 % (73 de 313) |
| Atención del vendedor | 4.102 | 4,83 | 2,2 % | 3,41 | 26,8 % (84 de 313) |
| Claridad de precios y opciones de financiamiento | 4.103 | 4,64 | 2,5 % | 3,26 | 25,2 % (79 de 313) |
| Facilidad de comunicación con vendedor | 4.103 | 4,81 | 2,2 % | 3,37 | 26,8 % |
| **Fluidez general del proceso** | 4.103 | 4,61 | 4,9 % | 2,56 | **50,8 % (159 de 313)** |
| Vehículo en parte de pago | 1.525 | 4,45 | 6,3 % | 2,81 | 39,6 % (42 de 106) |
| **Proceso de Entrega** (solo Usados) | 4.103 | 4,58 | 6,4 % | **2,24** | **61,7 % (193 de 313)** |

**Respuesta a la pregunta:** en ambos archivos, la etapa que más castiga la nota es **fluidez general del proceso**, y en usados además la **entrega**. Son las etapas con mayor % de detractores con 1-2. En usados, la parte de pago también pesa (39,6 % en detractores; 17,3 % en pasivos con 1-2).

**Polarización:** ninguna etapa activa la bandera total. El patrón es de segmento: la nota alta del total viene de promotores (media de 4,8 a 5,0 en todas las etapas de Nuevo), y los detractores concentran la cola baja.

## 4. Dolores: frecuencia real

Tasa de detractores dentro del tema = detractores codificados con ese motivo / todas las filas codificadas con ese motivo (en todos los segmentos). Base pequeña en algunos temas.

[DATO] Nuevo, GRUPO_COMPLETO, bloque NPS (`Macrocategoría 1`, `¿Qué te motiva a dar esa puntuación?`):

| Dolor (macro) | n detractores | % de 348 detractores | Tasa de detractores dentro del tema (n total) |
|---|---:|---:|---:|
| Documentación | 39 | 11,2 % | 47,0 % (83) |
| Precios y financiamiento | 20 | 5,7 % | 40,0 % (50) |
| Rapidez del proceso | 64 | 18,4 % | 28,6 % (224) |
| Comunicación con cliente | 29 | 8,3 % | 18,7 % (155) |
| Atención | 77 | 22,1 % | 2,3 % (3.389) |
| Condición del vehículo | 32 | 9,2 % | 7,9 % (405) |

[DATO] Usados, GRUPO_COMPLETO, bloque NPS (`Macrocategoría 1`):

| Dolor (macro) | n detractores | % de 313 detractores | Tasa de detractores dentro del tema (n total) |
|---|---:|---:|---:|
| Precios y financiamiento | 13 | 4,2 % | 46,4 % (28) |
| Documentación | 24 | 7,7 % | 35,3 % (68) |
| Comunicación con cliente | 19 | 6,1 % | 25,0 % (76) |
| Rapidez del proceso | 25 | 8,0 % | 19,2 % (130) |
| Condición del vehículo | 52 | 16,6 % | 17,2 % (302) |
| Atención | 80 | 25,6 % | 3,8 % (2.107) |

[DATO] Bloque de entrega, Usados (`Macrocategoría 1.2`, columna `¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor?`, filtro: NPS 0-6): 149 detractores codificados de 234 con texto. Rapidez del proceso 48 (32,2 % de codificados); Atención 34 (22,8 %); Condición del vehículo 24 (16,1 %); Comunicación 21 (14,1 %); Documentación 18 (12,1 %).

[DATO] Bloque de etapas, Nuevo (`Macrocategoría 1.1`, columna `¿Nos contarías por qué?`, filtro: NPS 0-6): 157 detractores codificados de 219 con texto. Rapidez del proceso 58 (36,9 %); Documentación 24 (15,3 %); Comunicación 23 (14,6 %); Precios y financiamiento 19 (12,1 %); Atención 19 (12,1 %).

**Deseos (lectura de promotores, [HIPÓTESIS] de interpretación):** entre promotores, lo que se valora es la atención (82 % de codificadas en Nuevo y Usados) y la rapidez en el bloque de entrega de usados (51,1 % de los promotores codificados en `¿Qué faltó…?`, lo que sugiere que pedían algo más rápido aun estando satisfechos). Esto requiere validación cualitativa.

## 5. Citas textuales (≤ 15 palabras, sin nombres ni datos de contacto)

Filas identificadas por `row_id` tal como aparecen en el archivo.

- **Fluidez / plazo de entrega (Nuevo, detractor):** "Es demasiado el tiempo de entrega" — `CR_2025-Venta-Nuevo_#414`
- **Entrega ya pagada (Nuevo, detractor, tema Atención):** "No es posible que se demoran tanto en entregar un auto nuevo ya pagado" — `CR_2025-Venta-Nuevo_#612`
- **Espera del vehículo (Nuevo, detractor, tema Rapidez):** "ya va un mes y aun no me lo entregan" — `CR_2025-Venta-Nuevo_#445`
- **Experiencia general (Nuevo, detractor):** "la experiencia en la compra no es para nada positiva" — `CR_2025-Venta-Nuevo_#518`
- **Calidad y gestión (Usados, detractor, tema Condición del vehículo):** "no se preocupan de entregar un producto de calidad" — `CR_2025-Venta-Usados#41`
- **Terminación del vehículo (Usados, detractor, tema Condición del vehículo):** "Pintaron los parachoques de otro color no igual al del vehículo" — `CR_2025-Venta-Usados#86`
- **Entrega (Usados, bloque `¿Qué faltó…?`):** "Agilizar un poco más los tiempos de entrega" — `CR_2025-Venta-Usados#26`

## 6. Trazabilidad: verbatim no vacío y codificación

Verbatim no vacío = texto distinto de vacío en la columna de verbatim del bloque. Codificadas = `Macrocategoría 1` del mismo bloque no nula. Sin codificar = con texto y sin macro.

[DATO] Nuevo (`CR_2025-Venta-Nuevo`, 6.458 filas):

| Bloque | Columna de verbatim | Con texto | Codificadas | Con texto sin codificar | Codificadas sin texto |
|---|---|---:|---:|---:|---:|
| NPS (sufijo "") | ¿Qué te motiva a dar esa puntuación? | 5.193 | 4.362 | **831** | 0 |
| Etapas (".1", tras Fluidez) | ¿Nos contarías por qué? | 330 | 238 | 92 | 0 |
| Parte de pago (".2") | ¿Nos contarías por qué?.1 | 202 | 67 | 135 | 0 |

[DATO] Usados (`CR_2025-Venta-Usados`, 4.103 filas):

| Bloque | Columna de verbatim | Con texto | Codificadas | Con texto sin codificar | Codificadas sin texto |
|---|---|---:|---:|---:|---:|
| NPS (sufijo "") | ¿Qué te motiva a dar esa puntuación? | 3.332 | 2.725 | **607** | 0 |
| Etapas (".1", tras Vehículo en parte de pago) | ¿Qué te motivó a otorgar esta calificación? | 57 | 26 | 31 | 0 |
| Entrega (".2", tras Proceso de Entrega) | ¿Qué faltó para que la entrega de tu nueva compra hubiera sido mejor? | 645 | 417 | **228** | 0 |

**Alerta de trazabilidad:** el bloque NPS de Usados tiene 2.725 codificadas, todas con texto. Pero el verbatim del bloque etapas de Usados casi no tiene texto (57 de 4.103). Los nombres de bloque (".1", ".2") son por **posición** en el archivo; la asignación semántica de cada bloque es [HIPÓTESIS] y debe confirmarse con quien hizo la codificación.

## Qué no sabemos (NO VERIFICADO)

- **Quién codificó las macrocategorías y con qué libro de códigos.** No hay documentación en el repo. Tampoco sé si la codificación es manual, automática o mixta. Depende de Beto.
- **Si `sentimiento` y las macros se aplicaron al mismo texto** que la columna de verbatim. Hay 831 filas con texto sin macro en Nuevo y 607 en Usados.
- **Equivalencia Portillo.** Toda cifra PORTILLO_HIPOTESIS depende de la asignación bloqueada (Beto / Iván Balaguera).
- **Muestra de promotores vs. detractores en Portillo:** en usados, n = 11 detractores; no hay base para inferencias.
- **Si la nota de satisfacción corresponde a la compra o a la entrega** en usados: la pregunta de entrega está en una columna distinta y no sé si el encuestado la respondió después de recibir el auto.
- **Relación con ventas cerradas o tasas de cierre:** no se afirma ninguna. Estos son solo clientes que completaron una compra y respondieron la encuesta.

## Contradicciones (sin corregir)

- **C1. Universo PORTILLO en Usados.** `research/00_mapeo_portillo.md` da **108** filas (conteo por prefijo "PORT" al inicio del `nombre_concesionario`). Este análisis da **145** (palabra `PORT` en cualquier posición, `\bPORT`). La diferencia son 37 filas donde la palabra aparece después de "USADOS" u otro prefijo. Usé 145 en el script; el resultado de Portillo en usados debe leerse con 108 también. Pendiente de decisión.
- **C2. Universo PORTILLO en Nuevo.** Coincide: 1.311 (mapeo) y 1.311 (este análisis).
