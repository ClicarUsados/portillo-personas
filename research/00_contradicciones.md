# Contradicciones y discrepancias — Fase 0

Fecha de extracción de los archivos: 2026-11-23. Cada discrepancia se muestra con ambas cifras; no se corrige en silencio.

| # | Tema | Cifra / afirmación A | Cifra / afirmación B | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | Ventana de Lead-Portillo | Brief: 2023-06 a 2026-01 | Datos: 2023-06-08 a 2026-01-23 (1.003 filas, `fecha respuesta`) | `research/00_diccionario_datos.md` | Coincide |
| 2 | Ventana de Clicar | Brief: 2023-06 a 2024-04 | Datos: 2023-06-30 a 2024-04-08 (223 filas) | ídem | Coincide. Nota: una primera corrida mostró 88 fechas válidas por un error de parseo de formato ISO; corregido en `analisis/01_diccionario.py` |
| 3 | Etiqueta Portillo en archivos | Brief: "Ningún archivo está etiquetado como Portillo" (`empresa` = Grupo Americar) | El archivo se llama `CR_Lead-Portillo_*` y `nombre_sucursal` contiene "PORTILLO" en 140 de 1.003 filas (p. ej. "BILBAO USADOS PORTILLO", "PRE VENTA PORTILLO") | `research/00_mapeo_portillo.md` | **Contradicción real.** `empresa` no lo etiqueta, pero sucursales y nombre de archivo sí. Se usa como [HIPÓTESIS] |
| 4 | Sucursal en Venta-Usados | Brief: `nombre_sucursal` vacío | Confirmado: `nombre_sucursal` y `marca_sucursal` 100% vacíos; `nombre_concesionario` sí poblado (149 valores) | `research/00_diccionario_datos.md` | Coincide. Se usa `nombre_concesionario` |
| 5 | Hoja1 de CASOS_PBI | Brief: 42 MB, Hoja1 con empresa/area_negocio/motivo_reclamo en 0.0 | Archivo **no presente** en `inputs_raw/` (solo 7 de 8 xlsx copiados) | Verificación de carpeta | **BLOQUEADO.** Depende de Beto |
| 6 | Número de archivos en inputs_raw | Brief: 8 .xlsx | 7 .xlsx en `inputs_raw/` | `ls` | Ver #5 |
| 7 | Prefijos de sucursal en Mecánica | Brief no los menciona | Sucursales "GAP ...", "ACSA ...", "DENALI ...", "PORTILLOLA FLORIDA", "PORTILLOTALCA" conviven con "PORTILLO" en el mismo archivo | `research/00_mapeo_portillo.md` | [HIPÓTESIS]. "PORTILLOLA"/"PORTILLOTALCA" pueden ser falsos positivos de la regex; confirmar |
| 8 | Marca en Mecánica | Columna `des_marca` (77 valores) vs `marca` (78) vs `marca_sucursal` (62) | Códigos de `marca` abreviados ("TO", "CV"...) no coinciden 1:1 con `des_marca` ("TOYOTA", "CHEVROLET") | `research/00_diccionario_datos.md` | Se usa `des_marca` como fuente de marca |

## Agregadas por Subagente D (Fase 1)

| # | Tema | Cifra A | Cifra B | Fuente | Estado |
|---|---|---|---|---|---|
| 9 | Portillo en encuesta web | 72 filas por campaña "Portillo" [DATO] (`campaña o sensor`) | 30 filas por PORT/PORTILLO en `nombre_concesionario` [HIPÓTESIS] | research/04_intencion_funcionalidades_demografia.md | Contradicción abierta. Dos criterios distintos de "Portillo" |
| 10 | Portillo en seguridad vial | 142 filas por campaña [DATO] | 102 filas por PORT/PORTILLO en `nombre_concesionario` [HIPÓTESIS] | ídem | El 102 coincide con el mapeo; el 142 no aparece en él |

## Agregadas por Subagente E (Fase 1)

| # | Tema | Cifra / afirmación A | Cifra / afirmación B | Fuente | Estado |
|---|---|---|---|---|---|
| 11 | Usados de Portillo | Mapeo: "PORT USADOS" asumido Portillo [HIPÓTESIS] | portillo.cl comunica el usado como CLICAR [WEB] | research/05_mercado_externo_web.md; research/00_mapeo_portillo.md | Contradicción abierta. Validar universo con Beto / Iván Balaguera |
| 12 | Plantilla Portillo 2025 | Nota secundaria: 3.389 a 2.973 empleados, 24 locales cerrados [WEB, NO VERIFICADO en fuente oficial] | Sin cifra en datos internos | research/05_mercado_externo_web.md | No verificada en fuente primaria |

## Agregadas por Subagente B (Fase 1)

| # | Tema | Cifra A | Cifra B | Fuente | Estado |
|---|---|---|---|---|---|
| 13 | Contacto vs. necesidad en Lead-Portillo | 60 leads con "¿Ha sido contactado?" = No | 10 de ellos responden que "ya estoy en contacto con mi ejecutivo" | research/02_leads_cotizacion.md | Contradicción abierta. Posible error de captura o de pregunta |
| 14 | Leads usados | `des_marca` = USADOS: 326 | `tipo_oportunidad` usado normalizado: 327 | research/02_leads_cotizacion.md | Diferencia de 1 fila; revisar regla de normalización |

## Agregadas por Subagente A (Fase 1)

| # | Tema | Cifra A | Cifra B | Fuente | Estado |
|---|---|---|---|---|---|
| 15 | Universo PORTILLO en Venta-Usados | Mapeo (prefijo PORT): 108 filas | Script 1A (`\bPORT` en cualquier posición): 145 filas | research/00_mapeo_portillo.md; research/01_voz_comprador_ventas.md | Contradicción de regla de filtro. Unificar regla antes de Fase 2 |

## Notas de auditoría (Fase 3)

- **#10 (142 Portillo en seguridad vial por campaña): NO REPRODUCIBLE.** La auditoría no encontró ese 142 en `analisis/4D_intencion_funcionalidades.py`. Tratar como no confiable hasta re-derivarlo.
- **#15 (108 vs 145 en Usados):** el 108 sale solo de `analisis/02_mapeo_portillo.py`; el 145 sale de `analisis/1A_voz_ventas.py`. Son dos reglas de filtro distintas; falta unificar.
- **Incidente de procedimiento:** `analisis/00_anonimizar.py` fue ejecutado de nuevo durante la auditoría. Eso leyó `inputs_raw/`, contra la regla "no volver a abrir inputs_raw/ tras Fase 0". Regeneró `inputs_clean/`. Los conteos coinciden, pero no hay copia previa para comparar contenido.
- **Incidente:** `analisis/01_diccionario.py` y `analisis/02_mapeo_portillo.py` sobrescribieron sus reportes en `research/`. Sin git con historial no hay diff.

## Fase 1 (marco MdV)

Cifras nuevas del marco Momentos de la Verdad (ZMOT, FMOT, SMOT, UMOT). Ambas cifras se muestran sin corregir. Estado de reproducción: "script" = sale de un script de `analisis/`; "consulta directa" = verificada sobre `inputs_clean/` sin línea de script; "no reproducible" = solo aparece en `research/v1_pre_MdV/`. Fecha de extracción 2026-11-23.

| # | Tema | Cifra A | Cifra B | Reproducción | Impacto y estado |
|---|---|---|---|---|---|
| D-N1 | Mecánica Portillo | 7.881 filas con "Portillo" en la campaña "Mecánica Portillo" [DATO] · NPS +71,6 (sobre 7.881) | 245 filas con `\bPORT` en `nombre_sucursal` [HIPÓTESIS] · NPS +68,2 (sobre 245). Sin PORTILLOLA y PORTILLOTALCA: 127 filas, NPS +84,3, detractores 3,9 % | A: `umot_01_recomendacion_retorno.py`. B: `3C` y `6F_recuentos_correccion.py` (sección A) | Define el tamaño del universo de servicio: la campaña marca ~29 % de Mecánica; el mapeo por sucursal da <1 %. **Abierta.** Depende de Beto / Iván Balaguera |
| D-N2 | Usados por campaña | 114 filas con "Portillo" en la campaña "Venta Usados Portillo" [DATO] · NPS +74,6 | 163 filas con "Clicar" en la campaña "Venta Usados Clicar" [DATO] | A: `umot_01_recomendacion_retorno.py`. B: **consulta directa** (sin línea de script) | Dos marcas para el mismo canal de usados. **Abierta.** Depende de Beto / Iván Balaguera y del equipo comercial Portillo |
| D-N3 | Venta-Nuevo Portillo | 1.313 filas con "Portillo" en la campaña "2025 - Venta Nuevo Portillo" [DATO, conteo bruto] · **1.312** filas con NPS válido en la misma campaña | 1.311 filas con prefijo PORT en `nombre_concesionario` [HIPÓTESIS] · NPS +81,5 (sobre 1.311 con NPS) | A bruto: **consulta directa**. A con NPS válido 1.312: `umot_01_recomendacion_retorno.py` (PORT_CAMPAÑA_CHECK). B: `umot_01_recomendacion_retorno.py` | Diferencia de 1-2 filas según el criterio (con o sin NPS válido). Sin efecto en personas. Dependencia: Beto |
| D-N4 | Lentitud como motivo de lead (regla de codificación) | 132 de 558 textos con "Lentitud o tiempos" (palabras clave, versión 2) [HIPÓTESIS] | 85 de 558 (versión 1, palabras clave distintas) [HIPÓTESIS] | A: `zmot_leads.py`. B: **no reproducible** (solo en `research/v1_pre_MdV/`) | No hay cifra verdadera: depende de la regla. Rango 85-132 en C-01. Prueba: dos codificadores ciegos sobre 100 textos |
| D-N5 | "Sin respuesta o sin contacto" (regla de codificación) | 39 de 558 (versión 2) [HIPÓTESIS] | 61 de 558 (versión 1) [HIPÓTESIS] | A: `zmot_leads.py`. B: **no reproducible** | Mismo caso que D-N4. C-05b usa 39 con etiqueta [HIPÓTESIS] |
| D-N6 | Marco de la encuesta web | Brief: funcionalidades pedidas por el **visitante** del sitio | Datos: 324 de 324 son compradores de **vehículo nuevo con factura** (`nombre_categoria_venta` = NUEVO; factura 2024-01 a 2025-05; mediana 262 días entre factura y respuesta) [DATO] | Script `zmot_funcionalidades.py` (salida confirmada) | Cambia cómo se lee la encuesta: es un proxy post-venta, no una necesidad de visitante. El brief y los datos no coinciden. **Abierta.** research/06 la usa solo como proxy de compradores |
| D-B1 | Universo Portillo en Venta-Usados | Prefijo `^PORT` en `nombre_concesionario`: **108** [HIPÓTESIS] | `\bPORT` en cualquier posición: **145** [HIPÓTESIS] · campaña "Venta Usados Portillo": **114** [DATO] | 108 y 145: `6F_recuentos_correccion.py` (sección B). 114: `umot_01_recomendacion_retorno.py` | Se muestran las tres. Ninguna se usa como cifra única de Portillo (ver #15). Dependencia: Beto / Iván Balaguera |
| D-E1 | Marca del usado de Portillo | Aviso de Chileautos con "Automotora PORTILLO \| USADOS VITACURA 6875" y "PORTILLO \| USADOS PADRE HURTADO NORTE 1246" [WEB, chileautos.cl, aviso consultado 2026-11-23] | Fuente de empleo: Americar unificó el usado bajo la marca Clicar [WEB, búsqueda consultada 2026-11-23]; portillo.cl comunica el usado como Clicar [WEB] (#11) | Fuente web (sin script) | Contradicción con #11. **Abierta.** Bloquea la marca que habla por el seminuevo. Dependencia: Beto / Iván Balaguera / equipo comercial Portillo |
| D-A1 | Etiqueta vs ítem en UMOT | Etiqueta del script `umot_02_miedos_umot.py`: "Miedo a mal trato en recepción" (Mecánica 621 ítems ≤2 en pool) [DATO] | El ítem medido es "Acogida en sala de espera" [DATO] | Script `umot_02_miedos_umot.py` | La etiqueta sobredice la queja. research/06 (C-20) la nombra "acogida" y deja "mal trato" entre comillas. **Abierta** en el nombre del miedo |
| D-N7 | Seguridad vial, campaña Portillo (actualiza #10) | 142 filas con "Portillo" en `campaña o sensor` [DATO] | 102 filas con `\bPORT` en `nombre_concesionario` [HIPÓTESIS] | 142: `umot_03_demografia_seguridad_vial.py` (la auditoría de Fase 3 no lo halló en 4D; sí aparece en umot_03) | **Actualización de #10:** el 142 queda reproducido por el script de UMOT. No se usa en personas. Abierta |

**Contradicciones de la Fase 1 que ya estaban en la tabla principal y se reafirman:** #13 (contacto 60 vs 275), #11 (usado de Portillo), #15 (108 vs 145).

## Corrección (v3, 2026-11-23): regla "PORT" por subcadena

- La regla `\bPORT` / `PORT` en nombre_concesionario captura "USADOS SAN BDO AV PORTALES 3698" (37 filas, campaña Salazar Israel). Eso infla el universo Portillo.
- Regla correcta (token PORT o PORTILLO): **108 filas**. La cifra de **145** queda **INFLADA** por PORTALES. Afecta a los reportes que usaron 145 (1A, 2 de C-15) y a la contradicción #15.
- Las cifras de 114 (campaña "2025 - Venta Usados Portillo") no se afectan.
- Se reportan ambas, sin corregir en silencio: 108 (token, correcta) vs 145 (subcadena, inflada).
