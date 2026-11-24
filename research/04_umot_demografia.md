# 04 · UMOT (recomendación, retorno, salida) + demografía — Subagente D

Fecha de extracción: 2026-11-23. Fuente: `inputs_clean/*.parquet` únicamente.
Estado general: **[DATO] para conteos; [HIPÓTESIS] para interpretación de miedos; NO VERIFICADO donde se indica.**
No hay conversión lead → venta en este informe. "Volvería" es **intención declarada**, no retorno observado.

## Universos

| Universo | Regla | Estado |
|---|---|---|
| GRUPO_COMPLETO | todas las filas de cada encuesta | Usado como principal |
| PORTILLO_HIPOTESIS | `\bPORT` en `nombre_sucursal` (Mecánica, Clicar) o `nombre_concesionario` (Venta-Nuevo, Venta-Usados, Web, Seguridad) | **BLOQUEADO**: asignación pendiente de Beto / Iván Balaguera. [HIPÓTESIS] |
| PORT_CAMPAÑA (control) | `campaña o sensor` contiene "Portillo" | [DATO] etiqueta en el archivo; **contradice** el universo anterior (ver Contradicciones) |

Encuestas usadas: Mecánica, Venta-Nuevo, Venta-Usados, Clicar (NPS + "¿Volverías?"); Web (solo columna `nps`, ver abajo); Seguridad vial (solo demografía, §5). **Lead-Portillo: no aplica** (no tiene pregunta NPS ni "¿Volverías?"; tiene "¿Ha sido contactado…?").

Definiciones: Promotor 9–10, Pasivo 7–8, Detractor 0–6; NPS = %Prom − %Det. Pool UMOT = Detractor **o** volver = "No" / "No sé". Ítem de escala 1–5 con valor ≤2 = frustración (lectura [HIPÓTESIS]).

## 1. Recomendación y retorno declarado por encuesta

Archivo / columna / filtro: ver `analisis/umot_01_recomendacion_retorno.py`. Fecha 2026-11-23.

| Encuesta | Universo | n NPS | Prom | Pas | Det | NPS | Volvería Sí | No sé | No |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mecánica | GRUPO | 27.516 | 82,5% | 8,4% | 9,1% | +73,5 | 88,6% (n=27.515) | 7,5% | 3,9% (n=1.079) |
| Mecánica | PORT_HIP [HIPÓTESIS] | 245 | 79,6% | 9,0% | 11,4% | +68,2 | 86,5% | 6,9% | 6,5% |
| Mecánica | PORT_CAMPAÑA [DATO] | 7.881 | 81,2% | 9,1% | 9,7% | +71,6 | 88,2% | 7,5% | 4,3% |
| Venta-Nuevo | GRUPO | 6.457 | 88,8% | 5,8% | 5,4% | +83,4 | 91,2% (n=6.457) | 6,6% | 2,2% (n=142) |
| Venta-Nuevo | PORT_HIP [HIPÓTESIS] | 1.311 | 87,6% | 6,2% | 6,2% | +81,5 | 90,8% | 6,7% | 2,4% |
| Venta-Usados | GRUPO | 4.102 | 86,4% | 6,0% | 7,6% | +78,8 | 90,7% (n=4.102) | 5,8% | 3,5% (n=144) |
| Venta-Usados | PORT_HIP [HIPÓTESIS] | 145 | 84,8% | 7,6% | 7,6% | +77,2 | 90,3% | 6,2% | 3,4% |
| Clicar | GRUPO | 223 | 65,0% | 11,2% | 23,8% | +41,3 | 68,6% (n=223) | 11,2% | 20,2% (n=45) |

Control de la discrepancia #15 (Venta-Usados): con `\bPORT` n=145; con prefijo `^PORT` n=108. Se reportan ambas; no se unifica.

**Web (`nps`)**: solo valores 9 (n=53) y 10 (n=271) de 324. [NO VERIFICADO como NPS] — no hay detractores observables; no se calcula NPS.

**Clicar** no tiene filas PORT_HIP (0).

## 2. Qué separa a quien recomienda de quien no (GRUPO_COMPLETO)

Ítem ≤2 (escala 1–5), Promotores vs Detractores. Asociación descriptiva, no causal.

| Encuesta | Ítem | Prom ≤2 | Det ≤2 |
|---|---|---:|---:|
| Mecánica (Prom n=22.712; Det n=2.497) | Acogida en sala de espera | 0,5% | 23,5% |
| Mecánica | Claridad de precios y costos | 2,0% | 44,0% |
| Mecánica | Claridad sobre reparación/mantenimiento | 0,1% | 46,9% |
| Mecánica | Facilidad para comunicarse | 1,0% | 43,9% |
| Mecánica | Fluidez general | 0,1% | 45,5% |
| Mecánica | Calidad del servicio realizado | 0,1% | 52,3% |
| Venta-Nuevo (Prom n=5.732; Det n=348) | Fluidez | 0,3% | 58,0% |
| Venta-Nuevo | Facilidad de comunicación con vendedor | 0,1% | 28,2% |
| Venta-Nuevo | Claridad precios/financiamiento | 0,2% | 20,1% |
| Venta-Usados (Prom n=3.544; Det n=313) | Fluidez | 0,5% | 50,8% |
| Venta-Usados | Comunicación con vendedor | 0,1% | 26,8% |
| Clicar (Prom n=145; Det n=53) | Facilidad para vender | 0,0% | 79,2% |
| Clicar | Claridad de oferta final | 0,0% | 84,9% |
| Clicar | Rapidez del proceso | 0,7% | 79,2% |

Motivo abierto (sentimiento): Detractores con sentimiento Negative — Mecánica 83,9% (n=1.811); Venta-Nuevo 83,2% (n=242); Venta-Usados 83,6% (n=229). Promotores Positive — 90,7% / 91,8% / 91,9%.

Tema principal del motivo (Macrocategoría 1), Detractores vs Promotores:
- Mecánica: Atención 48,1% (n=882) vs 76,9%; Calidad del servicio 28,1% (n=515) vs 15,7%; Precios y costos 9,2% (n=169) vs 1,2%.
- Venta-Nuevo: Rapidez del proceso 24,5% (n=64) vs 3,2%; Documentación 14,9% (n=39); Atención 29,5% (n=77) vs 82,0%.
- Venta-Usados: Condición del vehículo 24,3% (n=52) vs 9,7%; Atención 37,4% (n=80) vs 82,3%.

## 3. Qué separa a quien volvería de quien no

Mecánica (Sí n=24.384; No n=1.079) — ítem ≤2 en Sí vs No: Claridad de precios 2,4% vs **59,1%**; Claridad de reparación 0,3% vs **66,4%**; Calidad 0,3% vs **72,8%**; Fluidez 0,3% vs **63,5%**; Comunicación 1,4% vs **60,2%**.
Venta-Nuevo (Sí n=5.889; No n=142): Fluidez 0,5% vs **76,8%**; Comunicación vendedor 0,1% vs **47,9%**; Acogida 0,3% vs 24,6%.
Venta-Usados (Sí n=3.722; No n=144): Fluidez 0,9% vs **63,9%**; Acogida 0,4% vs 36,1%; Comunicación 0,1% vs 38,9%.
Clicar (Sí n=153; No n=45): Facilidad de venta 0,0% vs **86,7%**; Claridad de oferta 0,0% vs **88,9%**; Rapidez 0,7% vs 84,4%.

## 4. Mapa de empatía UMOT

Cada patrón: n, %, etiqueta, cita (≤15 palabras, anonimizada, row_id). Citas obtenidas con `analisis/umot_04_citas.py`.

**Piensa y siente**
- Malestar tras la experiencia de servicio: Mecánica Detractores con sentimiento Negative, n=1.811 (83,9%). [DATO]
- Satisfacción sostenida en promotores: Mecánica Positive, n=14.996 (90,7%). [DATO]
- Cita: "Mala gestión por parte del ejecutivo, no aporta la información para hacer más fluido el" — Venta-Nuevo, row_id `CR_2025-Venta-Nuevo_#1454`. [DATO]

**Oye** — NO VERIFICADO. Las encuestas no preguntan qué escucharon antes de decidir ni de terceros. No se analizó la pregunta "¿Cómo llegaste…?" (Venta-Nuevo / Usados) en esta fase.

**Ve**
- Recepción/sala percibida como fría o lenta: Acogida ≤2 en Detractores — Mecánica 23,5% (n=2.497); Venta-Usados 23,3% (n=313); Venta-Nuevo 12,4% (n=348). [DATO]
- Lo que ve en el papel: claridad de reparación ≤2 en Detractores Mecánica 46,9% (n=2.497). [DATO]
- Cita: "Mucho tiempo de espera, respecto a la hora reservada" — Mecánica, row_id `CR_2025-Mecánica_202#25654`. [DATO]

**Dice y hace**
- Recomienda: Mecánica 82,5% (n=22.713); Venta-Nuevo 88,8%; Venta-Usados 86,4%; Clicar 65,0%. [DATO]
- Declara que volvería: Mecánica 88,6%; Venta-Nuevo 91,2%; Venta-Usados 90,7%; Clicar 68,6%. [DATO] — **intención, no observado**.
- Clicar, motivo principal "Por lo seguro": n=94 de 223 (42,2%). [DATO]
- Cita: "castigan demasiado el valor del vehiculo sin valorar los extras que tenga" — Venta-Usados, row_id `CR_2025-Venta-Usados#1385`. [DATO]
- Cita: "Arreglen el tasador de la página ya que el precio es muy diferente al entregado" — Clicar, row_id `CR_Clicar_2023-03-01#145`. [DATO]

**Esfuerzos (miedos, frustraciones, objeciones)** — pool UMOT (Detractor o No/No sé), conteo de ítems ≤2. Ver `analisis/umot_02_miedos_umot.py`.

| Pool | n pool | Miedo candidato | n (≤2) | % pool |
|---|---:|---|---:|---:|
| Mecánica | 3.399 | Trabajo mal hecho (Calidad del servicio) | 1.355 | 39,9% |
| Mecánica | 3.399 | Costos poco claros | 1.311 | 38,6% |
| Mecánica | 3.399 | Reparación no explicada | 1.210 | 35,6% |
| Mecánica | 3.399 | Sin respuesta (comunicación) | 1.189 | 35,0% |
| Mecánica | 3.399 | Proceso largo o desordenado | 1.191 | 35,0% |
| Mecánica | 3.399 | Mal trato en recepción | 621 | 18,3% |
| Venta-Nuevo | 614 | Proceso de entrega largo | 217 | 35,3% |
| Venta-Nuevo | 614 | Vendedor inaccesible | 103 | 16,8% |
| Venta-Nuevo | 614 | Precio o financiamiento poco claro | 76 | 12,4% |
| Venta-Usados | 413 | Proceso de entrega largo | 170 | 41,2% |
| Venta-Usados | 413 | Vendedor inaccesible | 87 | 21,1% |
| Venta-Usados | 413 | Precio o financiamiento poco claro | 86 | 20,8% |
| Clicar | 70 | Oferta baja o poco clara | 46 | 65,7% |
| Clicar | 70 | Demora en la venta | 44 | 62,9% |

Motivo con sentimiento Negative dentro del pool: Mecánica 2.115 (62,2%); Venta-Nuevo 300 (48,9%); Venta-Usados 268 (64,9%). [DATO]

Cita: "Mala respuesta para la fecha de entrega y cero comunicación" — Venta-Nuevo, row_id `CR_2025-Venta-Nuevo_#6271`. [DATO]
Cita: "Mucho tiempo de espera, respecto a la hora reservada" — Mecánica, row_id `CR_2025-Mecánica_202#25654`. [DATO]

**Resultados (deseos, medida de éxito)**
- Promotores: atención como motivo (Mecánica 76,9% de los promotores con código, n=11.219; Venta-Nuevo 82,0%; Venta-Usados 82,3%). [DATO]
- Calificación máxima en Calidad del servicio (Mecánica): 5 en 77,3% (n=21.274 de 27.514). [DATO]
- Cita: "mala experiencia solicite hora el día lunes [X] de noviembre me dieron hora para el" — Mecánica, row_id `CR_2025-Mecánica_202#14465`. [DATO] (cita de contraste; expresa la experiencia de no cumplimiento de hora)

## 5. Demografía — encuesta de seguridad vial (n=709)

**SESGO DECLARADO**: solo clientes de autos **nuevos**; un mes (2025-10-22 a 2025-10-29); **no representa a seminuevos** (Venta-Usados). Archivo `CR_Encuesta-de-seguridad-vial-en-Chile_*`, columnas `Rango de edad` y `Género`.

| Variable | Categoría | n | % del total (709) | % de válidos |
|---|---|---:|---:|---:|
| Edad (faltan 26) | 60 o más | 186 | 26,2% | 27,2% |
| | 50–59 | 183 | 25,8% | 26,8% |
| | 40–49 | 175 | 24,7% | 25,6% |
| | 30–39 | 103 | 14,5% | 15,1% |
| | 18–29 | 36 | 5,1% | 5,3% |
| Género (faltan 36) | Masculino | 434 | 61,2% | 64,5% |
| | Femenino | 230 | 32,4% | 34,2% |
| | Prefiero no decirlo | 9 | 1,3% | 1,3% |

Campaña "Seguridad vial en Chile - Portillo" [DATO]: n=142 (la cifra 142 de la contradicción #10 **sí se reproduce** desde la columna `campaña o sensor`). Dentro de esa campaña: 60 o más 32,6% de válidos (n=44); masculino 63,4% (n=85). PORTILLO_HIPOTESIS (`\bPORT`): n=102 [HIPÓTESIS].

Lectura: la muestra de seguridad vial es mayor de 40 años (79,6% de válidos ≥40), con predominio masculino. Es una muestra de clientes de autos nuevos de un mes; no sirve como retrato del comprador de seminuevos.

## Candidatos a miedo dominante (UMOT)

Conteo = ítems-respondentes ≤2 en pool UMOT, sumados por etiqueta entre encuestas. **Un mismo respondente puede contar en varios ítems; las sumas no son personas únicas.** Dominado por Mecánica por volumen. [HIPÓTESIS] en la etiqueta.

1. **Miedo a proceso lento o desordenado** — n=1.578 (Mecánica 1.191; Venta-Nuevo 217; Venta-Usados 170). [DATO]
2. **Miedo a costos o financiamiento poco claros** — n=1.473 (Mecánica 1.311; Venta-Nuevo 76; Venta-Usados 86). [DATO]
3. **Miedo a no recibir respuesta** — n=1.414 (Mecánica 1.189; vendedor inaccesible Venta-Nuevo 103 y Venta-Usados 87; Clicar 35). [DATO]
4. **Miedo a trabajo mal hecho** — n=1.355 (Mecánica). [DATO]
5. **Miedo a reparación no explicada** — n=1.210 (Mecánica). [DATO] Se solapa con el 2 y el 4.

Nota: el candidato 2 depende de la etiqueta común entre Mecánica y ventas; el 5 es de una sola encuesta.

## Contradicciones (ambas cifras, sin corregir)

| # | Tema | Cifra A | Cifra B |
|---|---|---|---|
| 9 | Portillo en encuesta web | 72 por campaña [DATO] | 30 por `\bPORT` (mapeo) [HIPÓTESIS] |
| 10 | Portillo en seguridad vial | 142 por campaña [DATO] (reproducido) | 102 por `\bPORT` [HIPÓTESIS] |
| 15 | Venta-Usados Portillo | 108 por `^PORT` | 145 por `\bPORT` |
| N1 (nueva) | Mecánica Portillo | 7.881 por campaña "Mecánica Portillo" [DATO] | 245 por `\bPORT` en sucursal [HIPÓTESIS] |
| N2 (nueva) | Usados por campaña | 114 campaña "Venta Usados Portillo" [DATO] | 163 campaña "Venta Usados Clicar" [DATO] |
| N3 (nueva) | Venta-Nuevo Portillo | 1.313 por campaña [DATO] | 1.311 por `\bPORT` [HIPÓTESIS] |

N1 es la más relevante: el archivo marca a Portillo por campaña en ~29% de Mecánica, pero el mapeo por sucursal da <1%. La definición de Portillo cambia el tamaño del universo de servicio.

## Bloqueos

- Definir universo PORTILLO (sucursales/concesionarios y campaña "Portillo" vs "Clicar" en Usados). Depende de: **Beto / Iván Balaguera**.
- Confirmar si `nps` de la encuesta web es la pregunta NPS completa. Depende de: **Beto** (dueño de la encuesta).
- Pregunta "¿Cómo llegaste…?" y lo que la gente oye: sin datos en esta fase (NO VERIFICADO).
- Lectura de miedo como ítem ≤2: validar con Beto antes de pasar al arquetipo de cliente.

## Scripts

- `analisis/umot_01_recomendacion_retorno.py` — NPS, retorno declarado, qué separa. Cómo reproducirlo: `python3 analisis/umot_01_recomendacion_retorno.py`
- `analisis/umot_02_miedos_umot.py` — miedos en pool UMOT. Cómo reproducirlo: `python3 analisis/umot_02_miedos_umot.py`
- `analisis/umot_03_demografia_seguridad_vial.py` — edad y género. Cómo reproducirlo: `python3 analisis/umot_03_demografia_seguridad_vial.py`
- `analisis/umot_04_citas.py` — citas candidatas anonimizadas. Cómo reproducirlo: `python3 analisis/umot_04_citas.py`

Nota de procedimiento: `research/v1_pre_MdV/04_intencion_funcionalidades_demografia.md` se citó en el brief como previo, pero no está en la lista de lectura permitida; **no se leyó**.
