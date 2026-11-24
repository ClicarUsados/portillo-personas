# Contradicciones y brechas: plan vs datos — v3 cliente ideal

Fecha de consulta: 2026-11-23. Cada discrepancia muestra ambas cifras. No se corrige en silencio.

| # | Tema | Cifra A | Cifra B | Fuente | Estado |
|---|---|---|---|---|---|
| P1 | Número de sucursales de usados | Plan p.02: "cinco sucursales de usados entre Av. Luis Carrera y La Dehesa" | Plan p.05–06: "7 sucursales Portillo"; tabla de p.06 lista 7 | [PLAN] p.02, p.06 | Contradicción dentro del plan. Confirmar con Beto |
| P2 | Nombres de sucursal | Plan p.06: Chacabuco 255, JM Carrera 6197, Las Condes Bilbao 5593, Los Cobres Vitacura 6875, Vitacura 5555, Vitacura Padre Hurtado 1246, José Alcalde Délano 11021 | Base Venta-Usados: sucursales `PORT USADOS` LUIS CARRERA, LA DEHESA, CERRILLOS, PADRE HURTADO, SAN FELIPE, LAS CONDES, VICUÑA MACKENNA, GRAN AVENIDA, PORTILLO USADOS BILBAO | [PLAN] p.06 vs `inputs_clean/CR_2025-Venta-Usados*` (`nombre_concesionario`) | Mapeo NO VERIFICADO. Bloqueado: Beto / Iván Balaguera |
| P3 | Universo Portillo Usados | Campaña "2025 - Venta Usados Portillo": 114 filas | Sucursal `PORT` / `PORTILLO` en `nombre_concesionario`: 145 filas | `inputs_clean/CR_2025-Venta-Usados*` | Regla de filtro distinta (ver D-B1 y #15 en research/00_contradicciones.md). El prompt pide ambas condiciones: se reporta cada una |
| P4 | Ventas 982 | Plan p.02: 982 ventas ene–oct 2026 | Base de Venta-Usados: encuesta de satisfacción, no de ventas; ~1.100 filas PORT en 2025-2026 no son ventas | [PLAN] p.02 vs base | Imposible verificar con la base. Queda [PLAN]. No recalcular |
| P5 | Ticket del stock | Plan p.06: "$15–17 MM+ en las 7 sucursales" | Sin stock en la carpeta (tabla vacía) | [PLAN] p.06 | Bloqueado: responsable de stock |
| P6 | Garantía de la competencia | Plan p.05: Kavak 12 meses, Bruno Fritsch 24 meses | Web pública: ver research/05_contexto_web.md (Kavak "7 días o 300 km"; Bruno Fritsch sin acceso 403) | [PLAN] p.05 vs [WEB] | Garantías de competidores: solo [PLAN]; no verificadas en web |

## Bloqueos vigentes

- Export de ventas de usados ene–oct 2026 (ventas_usados_oriente.xlsx): **Beto**. Sin él, ticket, marca, modelo, año y forma de pago por persona quedan como [HIPÓTESIS].
- Tabla de stock por sucursal (p.06): **responsable de stock**.
- Mapeo de sucursales del plan a las de la base: **Beto / Iván Balaguera**.
- Marca que firma el seminuevo premium (Portillo o Clicar): **Beto / Iván Balaguera / equipo comercial Portillo**.

## Actualización P3 (v3)

- La regla por subcadena "PORT" da 145 y captura "PORTALES" (37 filas de Salazar Israel). La regla por token PORT/PORTILLO da **108**. Usar 108 o la campaña (114). Ver research/00_contradicciones.md.

## Contradicciones de comunas (web, v3 C)

| # | Tema | Cifra A | Cifra B | Fuente | Estado |
|---|---|---|---|---|---|
| P7 | Población Censo 2017 por comuna (misma fuente BCN/INE) | Las Condes 294.838 (tabla 1.1); Vitacura 85.384; Lo Barnechea 105.833; Providencia 142.079 | Las Condes 288.298 (tabla 1.5); Vitacura 83.759; Lo Barnechea 103.512; Providencia 139.025 | [WEB] https://www.bcn.cl/siit/reportescomunales/reporpdf.html?anno=2017 (idcom 13114, 13123, 13132, 13115) | Dos tablas de la misma fuente no calzan. Se muestran ambas. Usar tabla 1.1 hasta confirmar |
