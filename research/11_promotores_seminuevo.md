# A · Quién compra y por qué recomienda (promotores de Venta-Usados Portillo)

USO INTERNO. Fecha de corte: 2026-11-23. Cliente ideal = promotor (NPS 9-10). Sin conversión lead→venta.

Cómo reproducirlo: `python3 analisis/v3A_promotores_seminuevo.py` (solo conteos; `--verbatims` imprime razones libres para revisión, no publicar).

## 1. Universo: dos reglas, una declarada

Fuente: `inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet` (4.103 filas). Columnas: `campaña o sensor`, `nombre_concesionario`, NPS `En base a tu última experiencia de compra, ¿qué tan probable es que recomiendes #empresa#…`.

| Regla | Filtro | n | Promotores 9-10 | Estado |
|---|---|---:|---:|---|
| **A (usada en este informe)** | `campaña o sensor` == "2025 - Venta Usados Portillo" | 114 | **95** | [DATO] |
| B (comparación) | `nombre_concesionario` contiene "PORT" (substring) | 145 | 123 | [DATO] pero **contaminada** (ver contradicción C-A1) |
| B corregida (ilustrativa) | `\bPORT(ILLO)?\b` en `nombre_concesionario` | 108 | — | [DATO] |

Fechas de respuesta regla A: 2025-03-03 a 2026-11-23. Regla A incluye 15 nombres distintos de sucursal: 10 con prefijo `PORT USADOS` / `PORTILLO USADOS` y 5 con nombre de calle (ver C-A2).

**Declaro la regla A.** Es la campaña propia de Portillo, sin falsos positivos y con las 6 filas de sucursales con dirección que no llevan la palabra "PORT".

### Promotores por sucursal (regla A)

Ninguna sucursal llega a n=30. **Se trabaja con el universo completo (n=95).** Por sucursal, [DATO]:

| nombre_concesionario | Promotores |
|---|---:|
| PORTILLO USADOS BILBAO | 14 |
| PORT USADOS LA DEHESA | 13 |
| PORT USADOS LUIS CARRERA | 12 |
| PORT USADOS PADRE HURTADO | 11 |
| PORT USADOS CERRILLOS | 9 |
| PORT USADOS SAN FELIPE | 7 |
| PORT USADOS VICUÑA MACKENNA (ambas grafías) | 10 |
| PORT USADOS LAS CONDES | 6 |
| PORT USADOS GRAN AVENIDA | 5 |
| PORT USADOS AUTOSHOPPING | 3 |
| Nombre con dirección (5 sucursales, 1-2 c/u) | 5 |

Nota: "PORT USADOS VICUÑA MACKENNA" y "PORT USADOS VICUA MACKENNA" son la misma sucursal con dos grafías; se suman en la fila de 10.

## 2. Por qué recomiendan (promotores, n=95)

Macrocategorías de la pregunta "¿Qué te motiva a dar esa puntuación?" (`Macrocategoría 1-5`, [DATO], n=95, presencia en al menos una columna):

| Razón | n | % de promotores |
|---|---:|---:|
| **Atención** (vendedor / ejecutivo) | 51 | **53,7 %** |
| Rapidez del proceso | 15 | 15,8 % |
| Condición del vehículo | 7 | 7,4 % |
| Comunicación con cliente | 3 | 3,2 % |
| Marcas y modelos | 1 | 1,1 % |

Filas con al menos una macrocategoría: 56 de 95 (59 %). Los 39 restantes no dejan motivo codificado. Precios y financiamiento no aparecen como macrocategoría de promotor, aunque su nota es alta (ver sección 3).

Verbatims (anonimizados, ≤15 palabras, row_id de la base). Se omitieron los que nombran vendedores:

- `CR_2025-Venta-Usados#12` (10): "La atencion del ejecutivo fue demaciado agradable,y muy cordial"
- `CR_2025-Venta-Usados#3233` (10): "La excelente atención del ejecutivo"
- `CR_2025-Venta-Usados#3512` (9 de la cita): "gran variedad de autos, la tramitación fue muy rápida"
- `CR_2025-Venta-Usados#3290` (14): "Los autos estan en buen estado, limpios, ordenados y la oficina muy bien preparada"
- `CR_2025-Venta-Usados#3509` (6): "Prestigio de marca, confianza y trayectoria."
- `CR_2025-Venta-Usados#3803` (8): "Responden el correo de consulta por el aviso"
- `CR_2025-Venta-Usados#3846` (5): "Rapidez en el proceso de compra"
- `CR_2025-Venta-Usados#3904` (13), **matiz (promesa no cumplida)**: "no se cumple en su totalidad lo que ofrece la persona que te atiende"

## 3. Notas por etapa (escala 1-5, [DATO], regla A)

| Etapa | Promotores (n=95): media / % 5 | No promotores (n=19): media / % 5 | Brecha |
|---|---|---|---:|
| Acogida en sala de ventas | 4,85 / 87,4 % | 4,05 / 47,4 % | 0,80 |
| **Atención del vendedor** | **4,96 / 95,8 %** | 3,74 / 52,6 % | **1,22** |
| Claridad de precios y financiamiento | 4,83 / 85,3 % | 4,05 / 42,1 % | 0,78 |
| Facilidad de comunicación con vendedor | 4,94 / 93,7 % | 4,00 / 52,6 % | 0,94 |
| **Fluidez general del proceso** | 4,80 / 83,2 % | 3,21 / 21,1 % | **1,59** |
| Vehículo en parte de pago | "No aplica" en 55 de 95 (57,9 %); entre quienes aplica n=40: media 4,75, 80 % en 5 | | |

Lectura: la etapa que más separa al promotor es la **fluidez del proceso** (mayor brecha), y la que más pesa en lo que dice el promotor es la **atención del vendedor** (95,8 % en 5 y 53,7 % de las menciones). Parte de pago aplica a poco más del 40 % de los promotores.

Cómo llegó (promotores, [DATO]): "auto que quería estaba acá" 22; publicidad en medios 18; ya era cliente 18; redes sociales 14; recomendación 11; otro 7; me queda cerca 5.

Volvería a comprar: 94 de 95 "Sí" y 1 "No sé" ([DATO]).

## 4. Qué no se puede decir

- **Ticket, marca, modelo, año, forma de pago y parte de pago por sucursal: NO VERIFICADO.** No hay export de ventas en `inputs_plan/` (el archivo `ventas_usados_oriente.xlsx` no existe). **Bloqueado: Beto** (export de ventas ene-oct 2026).
- La base de encuesta trae `des_marca` (n=114; PEUGEOT 23, TOYOTA 21, SUZUKI 7, KIA 7, MG 6, HYUNDAI 6). **No es un export de ventas**; no se usa como perfil de marca. [DATO] solo como referencia.
- Tabla de stock y ticket objetivo del plan: bloqueado con responsable de stock (ver `research/10_contradicciones_plan.md`).
- Conversión lead→venta: no se calcula.

## 5. Contradicciones (ambas cifras, lado a lado)

**C-A1. Regla de "PORT" (B).** El prompt y `research/00_contradicciones.md` (D-B1, #15) dan 145 filas para sucursal `PORT`/`PORTILLO`. Ese 145 sale de un substring `PORT`, que también captura **"PORTALES"**: `USADOS SAN BDO AV PORTALES 3698`, 37 filas, todas de la campaña "2025 - Venta Usados Salazar Israel" (33 promotores). **No son Portillo.** Con la regla de palabra completa son 108 filas. Recomiendo corregir la cifra de 145 en el registro (no se corrigió en silencio aquí: se muestra en esta línea).

**C-A2. Sucursales de la regla A.** Campaña A tiene 114 filas: 108 con nombre `PORT…`/`PORTILLO…` y 6 con nombre de calle (`USADOS VITACURA PADRE HURTADO 1246` 2; `USADOS SAN FELIPE CHACABUCO 255` 1; `USADOS VITACURA 5555` 1; `USADOS LA DEHESA J A DELANO 11021` 1; `USADOS LAS CONDES FCO BILBAO 5593` 1). Las direcciones coinciden con cinco de las siete sucursales de `[PLAN] p.06`, lo que sugiere el mapeo; **[HIPÓTESIS], NO VERIFICADO**. Bloqueado: Beto / Iván Balaguera.

**C-A3. Número de sucursales.** `[PLAN] p.02` dice "cinco sucursales de usados"; `[PLAN] p.05-06` dice "7 sucursales"; la base tiene 15 nombres distintos en la regla A (ver `research/10_contradicciones_plan.md`, P1). Sin resolver.

**C-A4. Venta-Usados no es export de ventas.** La base es encuesta de satisfacción; el `982 ventas` del plan (`[PLAN] p.02`) no se verifica con ella. Se queda como [PLAN].

## 6. Etiquetas usadas

[DATO] = `inputs_clean/CR_2025-Venta-Usados…` filtro indicado, n indicado, fecha de corte 2026-11-23. [PLAN] = `inputs_plan/Mkt_VU_Portillo___An_lisis_Premium.pdf`, página indicada. [HIPÓTESIS] = inferencia. NO VERIFICADO = sin fuente.

## 7. Bloqueos

- Export de ventas ene-oct 2026 con ticket, marca, modelo, año, forma de pago: **Beto**.
- Mapeo de sucursales del plan (p.06) a las de la base: **Beto / Iván Balaguera**.
- Tabla de stock por sucursal (p.06, vacía): **responsable de stock**.
