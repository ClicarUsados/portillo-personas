# Mapeo Portillo — Fase 0 (HIPÓTESIS)

Fuente: inputs_clean/*.parquet. Fecha de extracción de los archivos: 2026-11-23.

**Estado: [HIPÓTESIS] — BLOQUEADO.** Ninguna fuente marca explícitamente a Portillo como grupo. 
Confirmación requerida: Beto / Iván Balaguera (qué sucursales y marcas pertenecen a Portillo).

## Conteo por archivo

| Archivo | Filas | Filas PORTILLO_HIPOTESIS | % | Columna usada |
|---|---:|---:|---:|---|
| CR_2025-Mecánica_2025-03-01_2026-11-23_4ee290 | 27516 | 245 | 0.9% | nombre_sucursal |
| CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f | 6458 | 1311 | 20.3% | nombre_concesionario |
| CR_2025-Venta-Usados_2023-03-01_2026-11-23_ed | 4103 | 108 | 2.6% | nombre_concesionario |
| CR_Clicar_2023-03-01_2026-11-23_56ee57c8 | 223 | 0 | 0.0% | nombre_sucursal |
| CR_Encuesta-de-seguridad-vial-en-Chile_2023-0 | 709 | 102 | 14.4% | nombre_concesionario |
| CR_Encuesta-funcionalidades-Web_2023-03-01_20 | 324 | 30 | 9.3% | nombre_concesionario |
| CR_Lead-Portillo_2023-03-01_2026-11-23_216d73 | 1003 | 140 | 14.0% | nombre_sucursal |

## Sucursales/concesionarios que contienen PORT / PORTILLO (top 10 por archivo)

### CR_2025-Mecánica_2025-03-01_2026-11-23_4ee290
- `GAP PORTILLO SERVICIO`: 127
- `PORTILLOLA FLORIDA SERVICIOS`: 60
- `PORTILLOTALCA SERVICIOS`: 58

Primer token por prefijo en CR_2025-Mecánica_2025-03-01_2026-11-23_4ee290: {'SAIS': 0, 'DENALI': 1472, 'COSE': 0, 'GAP': 7117, 'ACSA': 11802, 'PORT': 0, 'PRE': 0, 'FLOTA': 0, 'USADOS': 0, 'SALAZAR': 0, 'ALESSANDRI': 0}

### CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f
- `PORT TOYOTA MOVICENTER`: 166
- `PORT TOYOTA VITACURA`: 136
- `PORT TOYOTA BILBAO`: 103
- `PORT TOYOTA IRARRAZAVAL`: 61
- `PORT HYUNDAI SAN FELIPE`: 57
- `PORTILLO MG CURICO`: 57
- `PORT LA FLORIDA JAC`: 44
- `PORT PEUGEOT PLAZA OESTE`: 43
- `PORT HYUNDAI CHICUREO`: 42
- `PORT HYUNDAI OSORNO`: 37

Primer token por prefijo en CR_2025-Venta-Nuevo_2025-03-01_2026-11-23_f2f: {'SAIS': 3544, 'DENALI': 503, 'COSE': 666, 'GAP': 0, 'ACSA': 0, 'PORT': 1223, 'PRE': 0, 'FLOTA': 1, 'USADOS': 0, 'SALAZAR': 0, 'ALESSANDRI': 0}

### CR_2025-Venta-Usados_2023-03-01_2026-11-23_ed
- `PORTILLO USADOS BILBAO`: 18
- `PORT USADOS LUIS CARRERA`: 17
- `PORT USADOS LA DEHESA`: 13
- `PORT USADOS CERRILLOS`: 11
- `PORT USADOS PADRE HURTADO`: 11
- `PORT USADOS SAN FELIPE`: 10
- `PORT USADOS LAS CONDES`: 7
- `PORT USADOS VICUA MACKENNA`: 7
- `PORT USADOS GRAN AVENIDA`: 6
- `PORT USADOS AUTOSHOPPING`: 5

Primer token por prefijo en CR_2025-Venta-Usados_2023-03-01_2026-11-23_ed: {'SAIS': 522, 'DENALI': 0, 'COSE': 90, 'GAP': 0, 'ACSA': 0, 'PORT': 90, 'PRE': 0, 'FLOTA': 0, 'USADOS': 3177, 'SALAZAR': 0, 'ALESSANDRI': 0}

Primer token por prefijo en CR_Clicar_2023-03-01_2026-11-23_56ee57c8: {'SAIS': 0, 'DENALI': 0, 'COSE': 0, 'GAP': 0, 'ACSA': 0, 'PORT': 0, 'PRE': 0, 'FLOTA': 0, 'USADOS': 0, 'SALAZAR': 23, 'ALESSANDRI': 8}

### CR_Encuesta-de-seguridad-vial-en-Chile_2023-0
- `PORT TOYOTA VITACURA`: 14
- `PORT TOYOTA MOVICENTER`: 10
- `PORT TOYOTA IRARRAZAVAL`: 7
- `PORT TOYOTA BILBAO`: 6
- `PORT HYUNDAI CHICUREO`: 4
- `PORTILLO MG VITACURA`: 4
- `NISSAN PLAZA EGAÑA PORTILLO`: 3
- `PORT TOYOTA PIRMIDE`: 3
- `PORT PEUGEOT PLAZA OESTE`: 3
- `PORT TOYOTA VICUA MACKENNA`: 3

Primer token por prefijo en CR_Encuesta-de-seguridad-vial-en-Chile_2023-0: {'SAIS': 381, 'DENALI': 29, 'COSE': 48, 'GAP': 1, 'ACSA': 0, 'PORT': 87, 'PRE': 0, 'FLOTA': 0, 'USADOS': 0, 'SALAZAR': 0, 'ALESSANDRI': 0}

### CR_Encuesta-funcionalidades-Web_2023-03-01_20
- `MG PLAZA EGAÑA PORTILLO`: 3
- `PORT HYUNDAI SAN FELIPE`: 3
- `PORT TOYOTA BILBAO`: 2
- `PORT TOYOTA CHICUREO`: 2
- `PORT OPEL COSTANERA`: 2
- `PORT TOYOTA VITACURA`: 2
- `MG SAN FELIPE PORTILLO`: 2
- `PORT NISSAN LA DEHESA`: 2
- `PORT MG PLAZA EGAÑA`: 2
- `PORT TOYOTA MOVICENTER`: 1

Primer token por prefijo en CR_Encuesta-funcionalidades-Web_2023-03-01_20: {'SAIS': 162, 'DENALI': 6, 'COSE': 14, 'GAP': 4, 'ACSA': 0, 'PORT': 23, 'PRE': 0, 'FLOTA': 0, 'USADOS': 0, 'SALAZAR': 0, 'ALESSANDRI': 0}

### CR_Lead-Portillo_2023-03-01_2026-11-23_216d73
- `BILBAO USADOS PORTILLO`: 27
- `MG PLAZA EGAÑA PORTILLO`: 24
- `MG SAN FELIPE PORTILLO`: 20
- `MG LA DEHESA PORTILLO`: 16
- `PRE VENTA PORTILLO`: 14
- `FLOTA PORTILLO NISSAN`: 9
- `PORT TALCA JAC`: 4
- `NISSAN PLAZA EGAÑA PORTILLO`: 3
- `PORT HYUNDAI MALL INDEPENDENCIA`: 3
- `PORT CITROEN COSTANERA CENTER`: 3

Primer token por prefijo en CR_Lead-Portillo_2023-03-01_2026-11-23_216d73: {'SAIS': 0, 'DENALI': 0, 'COSE': 0, 'GAP': 55, 'ACSA': 0, 'PORT': 19, 'PRE': 14, 'FLOTA': 9, 'USADOS': 217, 'SALAZAR': 0, 'ALESSANDRI': 0}


## Dudas abiertas (BLOQUEOS)

- **Bloqueado:** confirmar si PORT TOYOTA*, MG PLAZA EGAÑA PORTILLO, etc. son Portillo. Depende de: Beto / Iván Balaguera.
- **Bloqueado:** prefijos SAIS, DENALI, COSE, GAP, ACSA (¿otras empresas del holding? ¿marcas?). Depende de: Beto / Iván Balaguera.
- **Regla:** SAIS y Clicar son hermanas de grupo, no competencia. Competencia externa = resto del mercado.
- **Venta-Usados:** `nombre_sucursal` y `marca_sucursal` vienen vacíos; el mapeo usa `nombre_concesionario` (sí poblado).
- **Lead-Portillo:** `nombre_sucursal` contiene PORTILLO explícito en varias filas; el archivo se llama Lead-Portillo pero no todas sus filas son necesariamente Portillo (p. ej. 'GAP COSTANERA CENTER PEUGEOT'). [HIPÓTESIS]

## Universos de trabajo

- **PORTILLO_HIPOTESIS**: filas con PORT/PORTILLO en nombre de sucursal/concesionario (tabla arriba).
- **GRUPO_COMPLETO**: todo el archivo, marcado como Grupo Americar.
- Cada reporte debe declarar cuál universo usa.
