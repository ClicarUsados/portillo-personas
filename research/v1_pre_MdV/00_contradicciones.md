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
