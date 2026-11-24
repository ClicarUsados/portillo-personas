# 03 SMOT: Mapa de empatía, después de la compra (taller / servicio técnico)

Subagente C. Fecha de extracción: 2026-11-23.
Script: `python3 analisis/smot_mecanica.py` (opcional `--citas-out RUTA_FUERA_DEL_PROYECTO`, escribe citas candidatas fuera del proyecto).
Fuente única: `inputs_clean/CR_2025-Mecánica_2025-03-01_2026-11-23_4ee29087__sin_segmento.parquet` (27.516 filas, 58 columnas). Fechas de respuesta: 2025-03-04 a 2026-11-23.
Cifras de base CRM de encuesta: **USO INTERNO**.
Etiquetas: [DATO] (archivo + columna + filtro + n + 2026-11-23), [WEB] (no usado), [HIPÓTESIS], NO VERIFICADO, BLOQUEADO.

## Alcance y límites

- Lo que mide: intención declarada y evaluación posterior a la reparación, por encuesta de NPS de taller.
- Lo que NO mide: recompra real, visitas posteriores ni conversión. "Volvería" es intención declarada. No se afirma conversión lead→venta ni recompra.
- Causalidad: las brechas por driver y motivo son asociaciones descriptivas.
- Representatividad: no hay denominador de OT cerradas en el periodo; no se conoce la tasa de respuesta (NO VERIFICADO).
- Sin arquetipo de marca. El arquetipo de cliente se obtiene después (miedos que se repiten en ≥3 de 4 MdV).

## Universos

- **GRUPO_COMPLETO** (universo principal): n = 27.516 [DATO].
- **PORTILLO_HIPOTESIS** [HIPÓTESIS, BLOQUEADO]: `nombre_sucursal` con `\bPORT` (regla de `research/00_mapeo_portillo.md`). n = 245 (0,9%) [DATO]. Depende de: Beto / Iván Balaguera.
  - Sensibilidad a la regla (importante): de los 245, 127 son "GAP PORTILLO SERVICIO" (NPS 84,3; detractores n=5; reparado=No n=1) y 118 son "PORTILLOLA FLORIDA" / "PORTILLOTALCA" (NPS 50,8; detractores n=23; reparado=No n=23). El NPS 68,2 del universo de 245 depende de esas dos sucursales dudosas. Con solo "GAP PORTILLO" el resultado cambia por completo. No usar el NPS de Portillo hasta confirmar.

## Mapa de empatía

### 1. Piensa y siente

| Patrón | n | % | Etiqueta | Base |
|---|---:|---:|---|---|
| Reparación no resuelta (reparado a la 1ª = No) en detractores | 1.097 | 43,9% de detractores (2.497) | [DATO] | Reparado=No |
| Reparación no resuelta en promotores | 374 | 1,6% de promotores (22.713) | [DATO] | Señal temprana de duda |
| Reparación no resuelta, total de la base | 1.651 | 6,0% | [DATO] | GRUPO_COMPLETO |

Citas:
- Detractor, row CR_2025-Mecánica_202#1316, NPS 0: "No solucionaron mi problema"
- Detractor, row CR_2025-Mecánica_202#446, NPS 6: "Le encuentro la misma falla"

### 2. Oye

Lo que escucha se mide por los drivers de comunicación. Son proxies de lo que escucha y no del texto de lo que se dijo [HIPÓTESIS].

| Patrón (detractores, nota ≤3 en escala 1-5) | n | % de detractores | Etiqueta |
|---|---:|---:|---|
| Claridad sobre la reparación o mantenimiento | 1.735 | 69,5% | [DATO] |
| Claridad de precios y costos | 1.757 | 70,4% | [DATO] |
| Facilidad para comunicarse con el servicio técnico | 1.620 | 64,9% | [DATO] |
| Fluidez general del proceso | n ≈ 1.738 | 69,6% | [DATO] (n calculado como % × base; exacto en script) |
| Tiempo de entrega del vehículo | 1.521 | 60,9% | [DATO] |

Motivo asociado: Comunicación con el cliente (macro 1) en detractores n = 144 (7,8% de 1.835 categorizados) [DATO].

Citas:
- Detractor, row CR_2025-Mecánica_202#1025, NPS 0: "cero comunicacion"
- Detractor, row CR_2025-Mecánica_202#661, NPS 0: "Abollaron mi automóvil y no me informaron a la salida del servicio técnico"

### 3. Ve

| Patrón | n | % | Etiqueta |
|---|---:|---:|---|
| Vehículo entregado con limpieza/lavado deficiente (verbatim; no cuantificado) | NO VERIFICADO | NO VERIFICADO | La columna "Lavado y limpieza del vehículo" tiene 8.366 valores no nulos; no se calculó su distribución en esta corrida |
| Vehículo entregado con daño reportado (verbatim) | NO VERIFICADO | NO VERIFICADO | Solo cita; no hay columna de daño |

Citas:
- Detractor, row CR_2025-Mecánica_202#285, NPS 4: "El vehículo no lo entregaron lavado"
- Detractor, row CR_2025-Mecánica_202#1176, NPS 1: "Llevé el vehículo a mantención y me lo devolvieron abollado."

### 4. Dice y hace

| Patrón | n | % | Etiqueta |
|---|---:|---:|---|
| Detractor: "No volvería" | ~1.016 (40,7% de 2.497) | 40,7% de detractores | [DATO] intención |
| Detractor: "No sé" | ~1.211 (48,5% de 2.497) | 48,5% de detractores | [DATO] intención |
| Detractor: "Sí volvería" | ~267 (10,7% de 2.497) | 10,7% de detractores | [DATO] intención, no conducta |
| Promotor: "Sí volvería" | 98,7% de promotores | 98,7% | [DATO] intención |
| Recompra real observada | — | — | NO VERIFICADO (no hay datos de visitas posteriores) |

Cita (verbatim, detractor): "Mi experiencia no fue de respuesta rápida y satisfactoria" (row CR_2025-Mecánica_202#1439, NPS 6).

### 5. Esfuerzos (miedos, frustraciones, objeciones)

Motivos de detractores, Macrocategoría 1 (1.835 categorizados de 2.497; 662 sin categoría = 26,5%) [DATO]:

| Macro / micro | n | % de categorizados | Etiqueta |
|---|---:|---:|---|
| Atención (macro) | 882 | 48,1% | [DATO] |
| Calidad del servicio (macro) | 515 | 28,1% | [DATO] |
| Precios y costos (macro) | 169 | 9,2% | [DATO] |
| Comunicación con el cliente (macro) | 144 | 7,8% | [DATO] |
| Tiempo de entrega del vehículo (macro) | 114 | 6,2% | [DATO] |
| Micro "Cumplimiento de acuerdos" (2.146 categorizados en micro) | 376 | 17,5% | [DATO] |
| Micro "Calidad de servicio del taller" | 305 | 14,2% | [DATO] |
| Micro "Atención del personal o asesor" | 184 | 8,6% | [DATO] |
| Micro "Percepción de precios" | 93 | 4,3% | [DATO] |

Drivers con nota ≤3 en detractores (base 2.497) [DATO]: Calidad del servicio realizado 1.953 (78,2%); Claridad de reparación 1.735 (69,5%); Fluidez 69,6%; Claridad de precios 1.757 (70,4%); Comunicarse 1.620 (64,9%); Tiempo de entrega 1.521 (60,9%); Acogida en sala de espera 51,4%; Atención de personal 1.162 (46,5%).

Lectura: el detractor califica mal casi todas las etapas, pero la brecha frente a promotores es mayor en calidad técnica (78,2% vs 0,6%), claridad de la reparación (69,5% vs 0,9%) y precios (70,4% vs 8,2%). Atención de personal tiene la brecha relativa menor (46,5% vs 0,1%).

Citas:
- Detractor, row CR_2025-Mecánica_202#492, NPS 5: "Valores muy elevados"
- Detractor, row CR_2025-Mecánica_202#477, NPS 1: "Pésimo el servicio no se hacen responsables de sus garantías"
- Detractor, row CR_2025-Mecánica_202#1445, NPS 0: "La atención al cliente es pésima"
- Detractor, row CR_2025-Mecánica_202#1346, NPS 4: "Se demoraron más de lo que me informaron al ingresar"

### 6. Resultados (deseos, medida de éxito)

| Patrón | n | % | Etiqueta |
|---|---:|---:|---|
| Reparado a la 1ª = Sí, total | 25.864 | 94,0% de 27.516 | [DATO] |
| Reparado a la 1ª = Sí, promotores | 22.339 | 98,4% de promotores | [DATO] |
| Motivo de promotor: "Atención general" (micro) | 6.416 | 38,9% de categorizados promotores (16.482) | [DATO] |
| Motivo de promotor: "Atención del personal o asesor" (micro) | 2.069 | 12,6% | [DATO] |
| Motivo de promotor: "Profesionalismo" (micro) | 1.596 | 9,7% | [DATO] |
| Motivo de promotor: "Puntualidad de la atención" (micro) | 1.096 | 6,6% | [DATO] |
| Motivo de promotor: "Resolutividad del personal" (micro) | 841 | 5,1% | [DATO] |

Medida de éxito implícita: reparación a la primera, cumplimiento de lo acordado, trato y claridad. Esto es lectura de los datos [HIPÓTESIS].

Citas (promotores):
- Promotor, row CR_2025-Mecánica_202#10, NPS 10: "La buena atención"
- Promotor, row CR_2025-Mecánica_202#16, NPS 10: "Por la información que me dieron cuando me entregaron el auto"

## NPS de taller y distribución (GRUPO_COMPLETO) [DATO]

- Detractor 0-6: 2.497 (9,1%); Pasivo 7-8: 2.306 (8,4%); Promotor 9-10: 22.713 (82,5%).
- NPS = 73,5. Media 9,03; mediana 10; sd 2,20.
- Distribución 0-10 (%): 0=2,4; 1=1,0; 2=0,8; 3=0,9; 4=1,0; 5=1,6; 6=1,3; 7=2,9; 8=5,4; 9=12,4; 10=70,2.
- Techo: 72,6% de notas son 0 o 10. La media oculta una cola baja pequeña pero concentrada.

## Tasa de detractores con reparación fallida [DATO]

- Detractores con reparado=No: 1.097 de 2.497 (43,9%).
- Su intención de volver: No 55,4%; No sé 40,1%; Sí 4,5%.
- Detractores con reparado=Sí (n=1.400): No 29,2%; No sé 55,1%; Sí 15,6%.
- Dato de control: detractores con reparado=No y sucursal vacía = 50.
- En promotores con reparación fallida (n=374), "No sé" = 6,1% frente a 1,1% cuando la reparación fue correcta.

## Drivers del NPS (escala 1-5, nota baja = ≤3) [DATO]

Ver mapa, cuadrante 2 y 5. Las distribuciones completas por driver están en la salida de `analisis/smot_mecanica.py`, sección 2.

## Casos: BLOQUEADO

- El archivo `CASOS_PBI__2_.xlsx` no está en el proyecto (no está en `inputs_raw/`). No se abrió nada fuera del proyecto.
- **Depende de: Beto** (entregar el archivo). Pendiente también la validación de Hoja1 (empresa, area_negocio, motivo_reclamo en 0,0; ciudad vacía), según `research/00_diccionario_datos.md`.
- Sin análisis de Casos: no hay reclamos, tiempos de resolución ni reincidencia en este informe.

## Candidatos a miedo dominante (SMOT)

Ranking por n. Son candidatos. Los n se solapan entre categorías y no se suman.

1. **Que la reparación no resuelva la falla (reparación fallida).** n = 1.097 detractores con reparado=No [DATO], 43,9% de detractores. Etiqueta: candidato principal por n. Interpretación del miedo [HIPÓTESIS]. Cita: "No solucionaron mi problema" (row #1316).
2. **Que no cumplan lo acordado.** n = 376 detractores (micro "Cumplimiento de acuerdos", base 2.146 categorizados) [DATO], 17,5%. Interpretación [HIPÓTESIS]. Cita: "Pésimo el servicio no se hacen responsables de sus garantías" (row #477).
3. **Ser mal atendido.** n = 882 detractores (macro "Atención", base 1.835) [DATO], 48,1%. Es el motivo más grande pero el más amplio. Cita: "La atención al cliente es pésima" (row #1445).
4. **Que el precio suba sin explicación.** n = 1.757 detractores con nota ≤3 en claridad de precios [DATO], 70,4%; motivo de precios en macro: n = 169 [DATO], 9,2%. Cita: "Valores muy elevados" (row #492).
5. **No saber qué se le hizo al vehículo.** n = 1.735 detractores con nota ≤3 en claridad de reparación [DATO], 69,5%; comunicación en macro: n = 144 [DATO], 7,8%. Cita: "Abollaron mi automóvil y no me informaron a la salida" (row #661).

Candidato dominante: (1) por n. Pendiente validarlo con los Casos (BLOQUEADO) para confirmar reincidencia.

## Universos declarados

- GRUPO_COMPLETO: universo principal de todo el informe.
- PORTILLO_HIPOTESIS: n=245, bloqueado, con la sensibilidad descrita arriba.

## Contradicciones (ambas cifras, sin corregir)

- **#7 (`research/00_contradicciones.md`)**: prefijos de sucursal en Mecánica. "PORTILLOLA FLORIDA" (n=60) y "PORTILLOTALCA" (n=58) coinciden con la regla PORT pero no están confirmados como Portillo. Con la regla y sin ellas: 245 vs 127. NPS 68,2 vs 84,3. Esto es un bloqueo de asignación, no una corrección.
- **#8 (`research/00_contradicciones.md`)**: marca. `des_marca` tiene 77 valores (TOYOTA 3.744, CHEVROLET 3.513); `marca` tiene 78 códigos abreviados (TO 3.744, CV 3.490); `marca_sucursal` tiene 62. Este informe usa `des_marca`. Las cifras de Chevrolet difieren entre columnas: 3.513 vs 3.490.
- **#3 (relacionada con universo)**: "Portillo" no está etiquetado en `empresa` (Grupo Americar), pero sí aparece en sucursales. Sin resolver.
- Control de consistencia con `research/v1_pre_MdV/03_retencion_postventa.md`: los conteos de esta corrida (27.516; NPS 73,5; 2.497 detractores; 1.097 reparado=No; PORTILLO n=245 y NPS 68,2) coinciden con el informe previo. No hay discrepancia numérica.

## Rutas

- Script: `analisis/smot_mecanica.py` (solo lectura de `inputs_clean/`).
- Informe previo de referencia: `research/v1_pre_MdV/03_retencion_postventa.md`.
- Citas candidatas (fuera del proyecto): `/private/tmp/claude-501/-Users-betosanchez/24be6daf-63e5-47fe-9340-aa059ab3e68f/scratchpad/smot_citas.tsv`.

## Qué no sabemos

- Recompra real. Solo intención declarada.
- Tasa de respuesta sobre OT cerradas (denominador no disponible).
- Causalidad entre etapa y recomendación.
- Asignación de sucursales a Portillo (BLOQUEADO: Beto / Iván Balaguera).
- Distribución de la columna de lavado (no calculada).
- Casos y reclamos (BLOQUEADO: Beto).
- Los verbatims están anonimizados y limitados a ≤15 palabras, pero el filtro no garantiza ausencia total de PII en minúscula. Revisar antes de cualquier uso externo.
