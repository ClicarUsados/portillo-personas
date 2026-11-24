# 02 — Mapa de empatía FMOT (sala de ventas) — Subagente B

**USO INTERNO.** Encuesta post-venta del CRM de Grupo Americar. Fecha de extracción de los datos: 2026-11-23.
Script reproducible: `python3 analisis/fmot_mapa_empatia.py` (imprime conteos; citas filtradas por anti-PII).
Arquetipo de cliente: **no asignado aquí** (se obtiene después, con miedos repetidos en ≥3 de 4 MdV). Sin arquetipo de marca.

## Fuentes y universos

- **Venta-Nuevo**: `inputs_clean/CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f6b8ef__sin_segmento.parquet` (6.458 filas).
- **Venta-Usados (seminuevo)**: `inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet` (4.103 filas). Columna de sucursal: `nombre_concesionario` (`nombre_sucursal` vacío al 100%).
- **Clicar**: `inputs_clean/CR_Clicar_2023-03-01_2026-11-23_56ee57c8__sin_segmento.parquet` (223 filas, fechas 2023-06-30 a 2024-04-08, **desactualizado**).
- **Universo declarado**: `GRUPO_COMPLETO` por defecto. `PORTILLO_HIPOTESIS` = `nombre_concesionario` empieza por "PORT" (regla de `research/00_mapeo_portillo.md`). **Asignación bloqueada: depende de Beto / Iván Balaguera.**
- **Segmentos NPS** (pregunta `En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa#…`): promotor 9-10, pasivo 7-8, detractor 0-6. Una fila sin dato en cada archivo, excluida.
- Escala de etapas 1-5. "No aplica" en parte de pago excluido.

## Limitaciones de cobertura (leer antes del mapa)

- **Clicar no tiene puntaje de parte de pago.** El brief lo pedía. En el archivo no existe ninguna columna de puntaje de parte de pago; `fecha_pa` (222 no nulos) tiene formato no interpretable. [DATO] columnas de Clicar. **NO VERIFICADO** qué representa `fecha_pa`. Solo se usa la oferta final.
- **Clicar no tiene macrocategorías.** Sus verbatims (`¿Por qué?`, 189 con texto) no están codificados en el archivo.
- **Macrocategorías de bloques por etapa son pocas.** Parte de pago: 67 codificadas en Nuevo y 26 en Usados. Esas cifras son demasiado pequeñas para leer tendencias; solo se usan como indicio.
- **El NPS mide la compra completa, no la sala por sí sola.** Se atribuye a FMOT por ser el tramo de venta, pero es [HIPÓTESIS] de atribución.
- **Proceso de Entrega (solo Usados)** es un tramo SMOT (entrega). Se reporta como contexto y no cuenta como etapa FMOT.
- **Relación con ventas cerradas o conversión:** no se afirma ninguna. Son clientes que completaron compra y respondieron.

---

## 1. Tamaños

[DATO] Venta-Nuevo, GRUPO_COMPLETO (n=6.458; sin NPS=1). Promotor 5.732 (88,8 %), pasivo 377 (5,8 %), detractor 348 (5,4 %). Fecha 2026-11-23.
[DATO] Venta-Usados, GRUPO_COMPLETO (n=4.103; sin NPS=1). Promotor 3.544 (86,4 %), pasivo 245 (6,0 %), detractor 313 (7,6 %).
[DATO] Venta-Nuevo, PORTILLO_HIPOTESIS (n=1.311; prefijo PORT). Promotor 1.149, pasivo 81, detractor 81.
[DATO] Venta-Usados, PORTILLO_HIPOTESIS (n=108; prefijo PORT). Promotor 90, pasivo 8, detractor 10. **Base demasiado pequeña para leer tendencias de detractores (n=10).**
[DATO] CR_Clicar, GRUPO_COMPLETO (n=223). NPS 0-10: promotor 145 (65,0 %), pasivo 25 (11,2 %), detractor 53 (23,8 %).

**Sensibilidad de universo PORTILLO (contradicción C-A, sin corregir):**
- Venta-Nuevo: prefijo PORT = 1.311; `\bPORT` en cualquier posición = 1.311; campaña "2025 - Venta Nuevo Portillo" = 1.313.
- Venta-Usados: prefijo PORT = 108 (detractores 10); `\bPORT` = 145 (detractores 11); campaña "2025 - Venta Usados Portillo" = 114 (detractores 10).

## 2. Mapa de empatía

Cada patrón: n, %, etiqueta. Base de % indicada. Citas ≤15 palabras, con row_id, anonimizadas.

### 2.1 Piensa y siente

- **P1. Frustración con la demora del proceso.** Fluidez general del proceso, detractores con 1-2 (Nuevo): **58,0 % (202 de 348)**. Distribución en detractores: 1=119, 2=83, 3=67, 4=54, 5=25.
  [DATO] Venta-Nuevo, `Fluidez general del proceso`, NPS 0-6, n=348, 2026-11-23.
  - Usados: **50,8 % (159 de 313)**. [DATO] Venta-Usados, misma columna, n=313.
  - Cita: "Mucha demora en entrega de factura y entrega de vehiculo" — `CR_2025-Venta-Nuevo_#143` (10 palabras).
- **P2. Sentir que no reciben lo que pagaron (lectura de detractores).** [HIPÓTESIS] Cita: "Pague y aún no recibí información del vehículo solo que está retrasado" — `CR_2025-Venta-Nuevo_#34` (15 palabras). Sin conteo propio: se apoya en P1.
- **Contraste con promotores.** Fluidez promotores 1-2 = 0,3 % (Nuevo) y 0,5 % (Usados). [DATO]. La media total de fluidez (4,69 Nuevo; 4,61 Usados) **oculta** esta polarización: el 3,7 % de 1-2 está casi todo en detractores (202 de 238 = 85 %).

### 2.2 Oye

- **O1. Lo que dice el vendedor sobre el auto.** Información proporcionada por vendedor, detractores con 1-2 (Nuevo): **31,0 % (108 de 348)**. [DATO] Venta-Nuevo, columna `Información proporcionada por vendedor` (solo Nuevo).
  - Cita: "Vehículo con muchos detalles que no se informo por parte del vendedor" — `CR_2025-Venta-Usados#314` (12 palabras).
- **O2. Lo que oyen de precio y financiamiento.** Claridad de precios y financiamiento, detractores con 1-2: Nuevo **20,1 % (70 de 348)**; Usados **25,2 % (79 de 313)**. [DATO].
  - Cita: "Lento muy ambiguo nada claro solo por disponibilidad y precio" — `CR_2025-Venta-Nuevo_#774` (10 palabras).
- **O3. Lo que oyen del precio tras la negociación (miedo a cambio de condiciones).** [DATO] Nuevo, Macrocategoría "Precios y financiamiento" en detractores: 20 de 261 codificadas (7,7 %). Usados: 13 de 214 (6,1 %).
  - Cita: "Vendedora me dio un precio y despues lo subio" — `CR_2025-Venta-Nuevo_#476` (9 palabras).

### 2.3 Ve

- **V1. Acogida en sala.** Acogida, detractores con 1-2: Nuevo **12,4 % (43 de 348)**; Usados **23,3 % (73 de 313)**. [DATO]. Total de 1-2 en acogida: 0,9 % y 2,1 %.
- **V2. Trato del vendedor visible.** Atención del vendedor, detractores con 1-2: Nuevo **21,3 % (74 de 348)**; Usados **26,8 % (84 de 313)**. [DATO].
  - Cita: "Vendedor inoperante, poco profesional, cero compromiso de venta, comunicación deficiente, mala experiencia" — `CR_2025-Venta-Usados#159` (12 palabras).
- **V3. Parte de pago visible.** Vehículo en parte de pago, detractores con 1-2: Nuevo **21,8 % (27 de 124)**; Usados **39,6 % (42 de 106)**. [DATO]. En promotores 1-2 = 2,7 % (Nuevo) y 3,0 % (Usados): **más alto que en otras etapas de promotores**.
  - Cita: "Dificultades para toma de crédito, unidad no la entregaron lavada" — `CR_2025-Venta-Usados#400` (10 palabras). Es de financiamiento y entrega, no de parte de pago. Cita de parte de pago pura **no encontrada con filtro**.

### 2.4 Dice y hace

- **D1. Motivo declarado de la nota (Nuevo, codificado).** Promotores: Atención 82,0 % (3.209 de 3.915). Detractores: Atención 29,5 % (77 de 261), Rapidez del proceso 24,5 % (64), Documentación 14,9 % (39), Condición del vehículo 12,3 % (32), Comunicación 11,1 % (29), Precios y financiamiento 7,7 % (20). [DATO] Venta-Nuevo, `Macrocategoría 1`.
- **D2. Motivo declarado (Usados, codificado).** Promotores: Atención 82,3 % (1.953 de 2.372). Detractores: Atención 37,4 % (80 de 214), Condición del vehículo 24,3 % (52), Rapidez 11,7 % (25), Documentación 11,2 % (24), Comunicación 8,9 % (19), Precios y financiamiento 6,1 % (13). [DATO] Venta-Usados.
- **D3. Lo que piden al cerrar la fluidez (Nuevo, codificado).** Detractores: Rapidez 58 de 157 (36,9 %), Documentación 24 (15,3 %), Comunicación 23 (14,6 %), Precios y financiamiento 19 (12,1 %), Atención 19 (12,1 %). [DATO] Venta-Nuevo `Macrocategoría 1.1`, base de detractores codificados.
- **Lectura de D1:** Atención es el tema dominante también entre promotores (82 %). Es un tema, no una valencia. El dolor se lee con la tasa de 1-2 dentro de cada etapa (sección 2.3), no con el conteo bruto.

### 2.5 Esfuerzos (miedos, frustraciones, objeciones)

- **E1. Esperar el auto.** Rapidez del proceso es la macro con más detractores en Nuevo, en el bloque NPS (64 de 348 detractores; 24,5 % de 261 codificadas). [DATO] Venta-Nuevo `Macrocategoría 1`. En el bloque de fluidez, Rapidez suma 58 de 157 detractores codificados (36,9 %) [DATO] `Macrocategoría 1.1`. Cita: "Aún no recibo el auto y lo compre el 4 de septiembre" — `CR_2025-Venta-Nuevo_#3943` (12 palabras).
- **E2. Trámites y documentación.** Documentación detractores Nuevo 39 de 261 codificadas (14,9 %); Usados 24 de 214 (11,2 %). [DATO] Pesa más en Nuevo. Cita: "Demora en la entrega del vehículo" — `CR_2025-Venta-Usados#435` (6 palabras). *(Entrega: SMOT.)*
- **E3. Objeción de precio y crédito.** Precio y financiamiento en Usados: detractores 13 de 214 codificados (6,1 %). Cita: "Los precios de los autos están muy altos" — `CR_2025-Venta-Usados#3394` (8 palabras).
- **E4. Oferta final en Clicar (desactualizado).** Claridad de la oferta final, detractores con 1-2: **84,9 % (45 de 53)**; promotores 4-5 = 97,9 %. [DATO] CR_Clicar, `Claridad en la oferta final del vehículo`, n=223, fechas 2023-06-30 a 2024-04-08. Es el equivalente más cercano a parte de pago en Clicar. [HIPÓTESIS] de equivalencia.

### 2.6 Resultados

- **R1. Deseo: que la atención sea buena.** Promotores codifican Atención en 82 % (Nuevo y Usados). [DATO]. Medida de éxito implícita: nota alta.
- **R2. Deseo: entrega más rápida, incluso en promotores.** Entrega (Usados, `¿Qué faltó…?`): promotores codificados 190, de ellos Rapidez 97 (51,1 %). [DATO] Venta-Usados `Macrocategoría 1.2`. [HIPÓTESIS] de interpretación: quieren rapidez aunque estén satisfechos. Requiere validación cualitativa.
- **R3. Medida de éxito:** la nota de recomendación (NPS) y la fluidez en 4-5. Fluidez 4-5 Nuevo 93,6 %; Usados 91,3 %. [DATO].
- **Lo que no se mide:** si el cliente volvería a comprar (`Dada tu reciente experiencia… ¿Volverías a comprar…?`). No se analizó en este mapa. [NO VERIFICADO] para FMOT.

---

## 3. Cuadro por etapa (distribución, GRUPO_COMPLETO)

| Etapa | Nuevo: media / 1-2 total / 1-2 detractores (n) | Usados: media / 1-2 total / 1-2 detractores (n) |
|---|---|---|
| Acogida en sala de ventas | 4,80 / 0,9 % / 12,4 % (43 de 348) | 4,73 / 2,1 % / 23,3 % (73 de 313) |
| Atención del vendedor | 4,87 / 1,2 % / 21,3 % (74) | 4,83 / 2,2 % / 26,8 % (84) |
| Información del vendedor (solo Nuevo) | 4,81 / 1,8 % / 31,0 % (108) | — |
| Claridad de precios y financiamiento | 4,74 / 1,4 % / 20,1 % (70) | 4,64 / 2,5 % / 25,2 % (79) |
| Facilidad de comunicación con vendedor | 4,84 / 1,7 % / 28,2 % (98) | 4,81 / 2,2 % / 26,8 % (84) |
| **Fluidez general del proceso** | 4,69 / 3,7 % / **58,0 % (202)** | 4,61 / 4,9 % / **50,8 % (159)** |
| Vehículo en parte de pago | 4,58 (n=2.984) / 3,7 % / 21,8 % (27) | 4,45 (n=1.525) / 6,3 % / 39,6 % (42) |
| Proceso de Entrega (SMOT, contexto) | — | 4,58 / 6,4 % / 61,7 % (193) |

[DATO] Fuente: columnas de etapa de cada archivo, fecha 2026-11-23. Ver script para distribuciones 1..5 completas.

**Etapa que más castiga:** en ambos archivos, **fluidez general del proceso** (mayor tasa de 1-2 entre detractores, 58,0 % y 50,8 %). En Usados, la entrega le gana, pero es SMOT. Parte de pago es la tercera en Usados (39,6 %) con n bajo (106 detractores evaluables). Ninguna etapa activa la bandera de polarización (media ≥ 4 y 1-2 ≥ 10 % en total).

**Portillo (PORTILLO_HIPOTESIS, Nuevo n=1.311):** Fluidez 1-2 total 4,6 %; detractores 60,5 % (49 de 81). Información del vendedor detractores 39,5 % (32). Claridad de precios detractores 17,3 % (14). Parte de pago total 1-2 4,8 % (n=562). [DATO] **Usados Portillo (n=108, detractores n=10):** fluidez detractores 40,0 % (4 de 10) — **no leer**.

## 4. Candidatos a miedo dominante (FMOT)

Criterio: detractores con 1-2 en la etapa (n absoluto). Cada n es independiente; **no se suman** (una persona puede estar en varios). [HIPÓTESIS] en el nombre "miedo": es interpretación de la etapa, no dato directo.

1. **Miedo a que la entrega se alargue y no llegue el auto.** Nuevo n=202 (fluidez, detractores 1-2) + Usados n=159. Total por archivo, [DATO] fecha 2026-11-23. Base de apoyo: Rapidez detractores Nuevo 64; Usados 25.
2. **Miedo a que el vendedor no informe ni responda.** Nuevo n=108 (información) / 98 (comunicación) / 74 (atención); Usados n=84 (atención). [DATO]. Cita: `CR_2025-Venta-Nuevo_#1879` "No me han entregado el auto y no responde el vendedor" (11 palabras).
3. **Miedo a que el precio cambie o no se entienda el financiamiento.** Nuevo n=70; Usados n=79. [DATO]. Cita: `CR_2025-Venta-Nuevo_#476` (9 palabras); `CR_2025-Venta-Nuevo_#530` "No se respetan los plazos de entregan cursan crédito y traspasan el auto ." (14 palabras).
4. **Miedo a una mala valoración del auto que entregan en parte de pago.** Usados n=42 (39,6 % de 106); Nuevo n=27 (21,8 % de 124). [DATO]. Base de codificación muy baja (Usados 9 codificadas en detractores). **Candidato débil en verbatim; fuerte en la tasa.** Cita: `CR_2025-Venta-Usados#31` "Compré un auto usado y no se cumplieron algunas condiciones ." (11 palabras), que no nombra la parte de pago explícitamente.
5. **Miedo a un trato de acogida frío en sala.** Usados n=73; Nuevo n=43. [DATO]. Cita: `CR_2025-Venta-Usados#154` "Llegue a casa y el vehículo no sube en reversa." (10 palabras), sin relación con la acogida. **Candidato débil**: la cita no corresponde al miedo.

**Ranking de candidatos por evidencia:** 1 > 2 > 3 > 4 > 5. La evidencia de 4 y 5 es principalmente de tasa, no de verbatim.

## 5. Clicar (desactualizado, solo oferta final)

- Oferta final: media 3,92; 1-2 total 20,6 %; 4-5 73,1 %. Por segmento: promotores 4-5 97,9 %; pasivos 4-5 68,0 %; detractores 1-2 84,9 %. [DATO] CR_Clicar, n=223.
- Clicar no tiene macro ni puntaje de parte de pago. [DATO] columnas.
- Origen de venta: PRESENCIAL 127, WEB 91, B2B 4, sin dato 1. [DATO].

## 6. Contradicciones (ambas cifras, sin corregir)

- **C-A. Universo Portillo en Usados.** Prefijo PORT (mapeo): **108**. `\bPORT` (script 1A anterior): **145**. Campaña "Venta Usados Portillo": **114**. Este mapa usa 108. La diferencia de detractores es 10 (prefijo) frente a 11 (`\bPORT`).
- **C-B. Universo Portillo en Nuevo.** Prefijo PORT: **1.311**. Campaña "Venta Nuevo Portillo": **1.313**. Diferencia de 2 filas.
- **C-C. Parte de pago en Clicar.** Brief: "solo la parte de pago y la oferta final". Datos: sin puntaje de parte de pago; solo `fecha_pa` (no interpretable). Estado: **contradicción con el brief**.
- **C-D. Atribución de codificación por bloque.** El verbatim de Venta-Usados `¿Qué te motivó…?` (bloque tras parte de pago) tiene 2.725 codificadas en NPS, pero solo 26 en su bloque. Atribución por posición, [HIPÓTESIS].

## 7. Bloqueos

- **Universo PORTILLO:** asignación de sucursales/concesionarios (prefijos PORT, PORTILLO, campaña "Portillo"). Depende de **Beto / Iván Balaguera**.
- **Codificación de macrocategorías:** quién la hizo y con qué libro de códigos. Depende de **Beto**.
- **Clicar:** qué es `fecha_pa` y si existe puntaje de parte de pago. Depende de **Beto**.
