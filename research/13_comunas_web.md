# 13 · Zona oriente y Providencia: perfil comunal desde fuentes web públicas

Subagente C de la v3 "Cliente ideal de Seminuevos Portillo Zona Oriente". Fecha de consulta de todas las fuentes: **2026-11-23**.
Uso: INTERNO. Etiquetas: [WEB] = fuente pública con URL; NO VERIFICADO = no encontrado en fuente primaria abierta. No se estimaron ni rellenaron cifras. No se calculó nada: no hay scripts en `analisis/` para este entregable.

## 1. Lo que sí se verificó (fuente primaria abierta)

### 1.1 Población por comuna, Censo 2017 (INE, vía reporte comunal BCN)

Fuente: BCN, Reporte comunal Censo 2017 (`https://www.bcn.cl/siit/reportescomunales/reporpdf.html?anno=2017&idcom=<código>`), que cita "Censos de Población y Vivienda 2002 y 2017, INE", tabla 1.1. Consultado 2026-11-23.

| Comuna | Población Censo 2017 (tabla 1.1) | Población Censo 2017 (tabla 1.5, mismo reporte) | Superficie (km²) |
|---|---|---|---|
| Las Condes | 294.838 | 288.298 | 99,0 |
| Vitacura | 85.384 | 83.759 | 28,3 |
| Lo Barnechea | 105.833 | 103.512 | 1.024,0 |
| Providencia | 142.079 | 139.025 | 14,3 |

- **Contradicción interna de la fuente:** cada reporte BCN trae dos cifras de población 2017 distintas (tabla 1.1 vs 1.5). Se muestran ambas. No se corrige.
- Dato 2002 del mismo reporte (Las Condes 249.893): solo como referencia, no se usa para tendencia.
- **Lo que el reporte NO trae** para ninguna de las cuatro comunas: número de hogares, hogares unipersonales, viviendas, densidad, ingresos de hogares, parque automotriz. Lo que sí trae: ingresos municipales (SINIM), no ingresos de personas ni hogares. Vitacura: propios permanentes 55,06 % del ingreso municipal 2017. Lo Barnechea: 59,31 % en 2017. Esto es finanzas municipales, no perfil del cliente; no se usa para el perfil.

### 1.2 Censo 2024 (INE): cifras nacionales y de la RM (la única base disponible por ahora)

- Nota INE, 27-03-2025: `https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/03/27/primeros-resultados-del-censo-2024-18.480.432-personas-fueron-censadas-en-chile-manteni%C3%A9ndose-la-tendencia-de-envejecimiento-de-la-poblaci%C3%B3n`. Consultado 2026-11-23.
  - Personas censadas: 18.480.432. Hogares: 6.596.527. Promedio de personas por hogar: 2,8.
  - RM: 7.400.741 personas (40 % del total nacional).
  - La nota **no trae cifras por comuna**; remite a censo2024.cl.
- Portal Censo 2024 (`https://censo2024.ine.gob.cl/`), consultado 2026-11-23: solo totales nacionales (viviendas censadas 7.642.716; hogares censados 6.596.527). Sin tablas comunales descargables en la página de inicio. Las tablas por comuna quedan **NO VERIFICADO**.

### 1.3 Movilidad al trabajo, Censo 2024 (vía nota de prensa que cita el INE)

Fuente: The Clinic, 22-12-2025, "La fuerte brecha que revela el Censo 2024…", `https://www.theclinic.cl/2025/12/22/la-fuerte-brecha-que-revela-el-censo-2024-solo-en-cinco-comunas-del-gran-santiago-predomina-ir-a-trabajar-en-auto-mientras-la-mayoria-usa-el-transporte-publico/`. Análisis de Territorio Sig sobre Censo 2024 (INE). Consultado 2026-11-23. **Es fuente secundaria** (medio que procesa el dato del INE); el dato de INE original no se abrió directamente.

| Comuna | Medio de traslado al trabajo, Gran Santiago (según el artículo) |
|---|---|
| Vitacura | Auto particular: más de 60 %. Bicicleta: más de 6 % |
| Lo Barnechea | Auto particular: más de 60 % |
| Las Condes | Auto particular: poco más de 50 % |
| Providencia | Sin cifra exacta de auto. Bicicleta: más de 6 %. Caminar: 10 % a 15 % |

- Contexto del mismo artículo: Gran Santiago auto 29 %, transporte público 54 %, caminar 8 %, bici 3 %. Región Metropolitana auto 51,3 %. Nacional auto 35,3 %, transporte público 42,1 %.
- Esto dice algo sobre la **zona** (la comuna se mueve en auto): es el dato más útil del lote para el perfil de movilidad. Es de la comuna, no del cliente de Portillo.

### 1.4 Pobreza por ingresos, estimación comunal CASEN 2024 (SAE)

- Documento: Ministerio de Desarrollo Social y Familia, División Observatorio Social, "Estimaciones comunales de pobreza por ingresos y multidimensional en base a Casen 2024" (SAE): `https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/pobreza-comunal/2024/Estimaciones_SAE_2024.pdf`. Consultado 2026-11-23.
- Advertencia del propio documento: "las comunas no son un dominio de estudio por lo que las estimaciones a ese nivel pueden tener una baja precisión y no se recomienda realizarlas". Las estimaciones SAE "no son comparables entre distintos años".
- Los **valores numéricos por comuna están en Anexos 1 y 2, que son mapas coloreados** (sin tabla de texto). Leí las páginas de anexos: no permiten leer la tasa de Las Condes, Vitacura, Lo Barnechea ni Providencia con precisión. **Cifra por comuna: NO VERIFICADO.** La tabla numérica está en `https://bidat.gob.cl/directorio/Pobreza%20comunal/`, que devolvió HTTP 500 al consultar 2026-11-23. Pendiente.
- Lo único legible en el mapa es la escala de la RM centro (no se pudo asignar a comuna sin tabla).

## 2. Lo que se buscó y NO se verificó

| Dato pedido | Resultado | Estado |
|---|---|---|
| Hogares por comuna (Las Condes, Vitacura, Lo Barnechea, Providencia), Censo 2017 o 2024 | No aparece en el reporte BCN 2017 ni en las notas INE 2024 | NO VERIFICADO. Pendiente: tabulados INE por comuna (censo2024.ine.gob.cl, sección Resultados) |
| Ingreso de hogares por comuna | No hay en BCN; CASEN 2024 publica ingreso nacional y por decil; por comuna solo vía SAE (mapa) | NO VERIFICADO |
| Ingreso autónomo promedio CASEN 2024 nacional | Aparece en resultados de búsqueda ($1.456.694 mensual, nacional). No abrí el PDF; es solo referencia nacional, **no es dato de la zona** | [WEB] snippet, no usar en perfil sin abrir la fuente |
| Composición de hogares (unipersonales, familias) por comuna | No encontrado. Existe "Hogares unipersonales Casen 2024" del MDS, sin cifra comunal abierta | NO VERIFICADO |
| Parque automotriz o permisos de circulación por comuna | Página INE "Permiso de circulación" (`https://www.ine.gob.cl/estadisticas/economia/transporte-y-comunicaciones/permiso-de-circulacion`, consultada 2026-11-23): año más reciente 2024, total nacional 6.727.472, **sin cuadros por comuna enlazados**. Un resumen de búsqueda da cifras 2023 por comuna (Las Condes 133.726 INE; otra fuente 129.491), pero no abrí el archivo INE y las dos cifras no cuadran | NO VERIFICADO por comuna |
| Transferencias, SII por comuna (renta, bienes raíces) | Búsqueda en sii.cl sin cifras comunales de renta 2024. No abrí las páginas de estadísticas del SII | NO VERIFICADO |
| Providencia: densidad, viviendas | No está en el reporte BCN | NO VERIFICADO |
| Pobreza SAE 2024 por comuna | Ver 1.4 | NO VERIFICADO |
| Contraloría 2022-2025 sobre permisos irregulares (Providencia 5.727; Lo Barnechea 16) | Solo prensa (Meganoticias, CNN Chile, junio 2026). No abrí el informe de Contraloría. No es perfil del cliente | No usado |

**Bloqueos de fuente:** bidat.gob.cl (HTTP 500 al consultar); el PDF SAE 2024 tiene tablas solo como imagen; censo2024.cl solo muestra totales nacionales. Ningún sitio bloqueó el acceso por política anti-bot.

## 3. Por comuna: las cifras más útiles (resumen)

- **Las Condes:** población 2017 294.838 (tabla 1.1) / 288.298 (tabla 1.5), [WEB] BCN; auto para ir al trabajo "poco más de 50 %", [WEB] The Clinic sobre Censo 2024. Tasa de pobreza 2024: NO VERIFICADO.
- **Vitacura:** población 2017 85.384 / 83.759, [WEB] BCN; auto al trabajo "más de 60 %" y bici "más de 6 %", [WEB] The Clinic. Hogares y ingreso: NO VERIFICADO.
- **Lo Barnechea:** población 2017 105.833 / 103.512, [WEB] BCN; auto al trabajo "más de 60 %", [WEB] The Clinic. Superficie 1.024 km², la comuna más extensa de las cuatro (no es densidad). Hogares e ingreso: NO VERIFICADO.
- **Providencia:** población 2017 142.079 / 139.025, [WEB] BCN; caminar 10-15 % y bici más de 6 %, [WEB] The Clinic (la comuna es de movilidad no motorizada, no de auto). Superficie 14,3 km². Hogares e ingreso: NO VERIFICADO.

Lectura para el perfil (solo como dato de zona, no del cliente): Las Condes, Vitacura y Lo Barnechea tienen el mayor uso de auto al trabajo; Providencia tiene más caminata y bici. Esto ayuda a diferenciar la comuna de referencia de Tomás (Providencia) frente a Javiera (zona oriente).

## 4. Qué dice la fuente sobre la comuna y qué sobre la zona

- **Sobre la comuna:** BCN (población, superficie), INE (si hubiera tabulado por comuna).
- **Sobre la zona:** The Clinic/Censo 2024 habla de "Gran Santiago" y de la comuna, pero el dato de auto es por comuna; el de Gran Santiago (29 %) y RM (51,3 %) es zona. SAE habla de comunas en general, no de la zona oriente.

## 5. Pendientes para cerrar (con responsable)

1. Hogares y composición de hogares por comuna, Censo 2017/2024: tabulados INE (Beto para revisar; sin responsable de datos, es web).
2. Tasa de pobreza SAE 2024 por comuna: abrir tabla de bidat.gob.cl cuando responda; si no, leer la tabla en Excel (Beto).
3. Parque por comuna: archivo INE de permisos de circulación 2024 (Beto).
4. Renta por comuna: SII estadísticas de personas naturales (no abierto).

## Rutas

- Este archivo: `/Users/betosanchez/portillo-personas/research/13_comunas_web.md`
- Texto extraído del PDF SAE (intermedio, no entregable): `/private/tmp/claude-501/-Users-betosanchez/24be6daf-63e5-47fe-9340-aa059ab3e68f/scratchpad/v3C/sae2024.txt`
- No se creó script en `analisis/` (no hubo cálculo). Sin git commit. No se modificó ningún archivo existente.
