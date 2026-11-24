# Dolores que el cliente ideal trae del mercado (seminuevo premium)

**USO INTERNO.** Subagente B de la v3 "Cliente ideal de Seminuevos Portillo Zona Oriente".
Fecha de corte: 2026-11-23. Fuente de conteos: `inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet` (4.103 filas, encuesta "2025 Venta Usados"). Script: `analisis/v3B_dolores_seminuevo.py` (solo conteos). No se leyó `inputs_raw/`.

## 0. Advertencias antes de leer

1. **Los dolores vienen de detractores (NPS 0-6).** El cliente ideal es el comprador satisfecho que recomienda. Este documento no describe a esa persona; describe lo que teme y lo que Portillo debe resolverle para ganarla.
2. **En el universo Portillo hay solo 10 detractores.** Con ese n no hay orden de frecuencia confiable. El ranking se hace sobre el grupo completo de Venta-Usados (313 detractores) y se usa como referencia de mercado, no como cifra de Portillo.
3. **Los porcentajes son de la encuesta, no de conversión.** Ninguna cifra aquí es tasa de cierre ni conversión lead -> venta.
4. Cada dolor se mide con uno o dos indicadores (ítem de encuesta ≤2 o código de microcategoría). Las palabras clave sobre texto libre se reportan aparte porque son conteos por regex, no codificación manual.

## 1. Universo: qué regla se usa y por qué

| Universo | Regla | n total | Detractores (NPS 0-6) | Uso en este documento |
|---|---|---:|---:|---|
| **PORT_CAMP** (principal Portillo) | campaña "2025 - Venta Usados Portillo" | 114 | 10 | Verbatims Portillo y conteos. [DATO] |
| PORT_SUC (control) | `nombre_concesionario` empieza con "PORT" | 108 | 10 | Control. Es subconjunto de PORT_CAMP (108 de 114). [HIPÓTESIS de mapeo, BLOQUEADO] |
| PORT_BPORT (descartado) | `nombre_concesionario` contiene "\bPORT" | 145 | 11 | **No usar.** Incluye 37 filas "USADOS SAN BDO AV PORTALES 3698" que no son Portillo. |
| GRUPO (referencia de mercado) | todas las filas de Venta-Usados | 4.103 | 313 | Ranking de dolores. No es universo Portillo. |

Las 6 filas de PORT_CAMP fuera de PORT_SUC tienen nombres de sucursal que coinciden con números de calle del plan (1246, 5555, 11021, 5593, 255). Es una pista de mapeo, no una confirmación. [HIPÓTESIS] · Mapeo de sucursales: NO VERIFICADO (Beto / Iván Balaguera).

## 2. Ranking de dolores en el grupo de detractores (base n = 313)

Un dolor cuenta si el detractor tiene el ítem ≤2 **o** un código de microcategoría asociado (unión). Base: 313 detractores de Venta-Usados [DATO].

| # | Dolor | Tipo | n | % (base) | Indicador |
|---:|---|---|---:|---:|---|
| 1 | Entrega: plazos, información de entrega | **Postventa** [HIPÓTESIS de clasificación] | 242 | 77,3 % (313) | Ítem "Proceso de Entrega" ≤2 (193; 61,7 %) o micro "Plazos de entrega" / "Entrega de información" |
| 2 | Proceso y tiempos de la compra | **Compra** | 161 | 51,4 % (313) | Ítem "Fluidez general del proceso" ≤2 (159; 50,8 %) o micro "Rapidez proceso en general" |
| 3 | Respuesta y trato en la venta | **Compra** | 147 | 47,0 % (313) | Ítems "Acogida", "Atención del vendedor", "Comunicación con vendedor" ≤2, o micro "Atención del vendedor" / "Respuesta de consultas" / "Disponibilidad de contacto" |
| 4 | Claridad de precio y financiamiento | **Compra** | 125 | 39,9 % (313) | Ítem "Claridad de precios y financiamiento" ≤2 (79; 25,2 %) o micro "Diferencia de precios en relación a la cotización", "Claridad de cobros", "Financiamiento", "Percepción de precios" |
| 5 | Tasación / vehículo en parte de pago | **Compra** | 42 | 39,6 % (106 que aplican) | Ítem "Vehículo en parte de pago" 1-2. Base: 106 detractores para quienes aplica (207 respondieron "No aplica"). Sobre 313: 13,4 % |
| 6 | Atención post venta | **Postventa** | 101 | 32,3 % (313) | Micro "Atención post una venta de vehículo" o "Cumplimiento de acuerdos" |
| 7 | Estado del auto (al recibirlo) | **Compra** | 69 | 22,0 % (313) | Micro "Detalles del vehículo", "Calidad del producto", "Limpieza del vehículo" |
| 8 | Documentación: permiso y factura | **Postventa** | 50 | 16,0 % (313) | Micro "Permiso de circulación" o "Factura" |
| 9 | Garantía | **Compra/postventa** | 7 | 2,2 % (313) | Solo palabra clave "garant" en texto libre. **No hay código de encuesta para garantía.** Es un hueco de la encuesta. |

Dolores sobre los que la encuesta no mide el tema, y que el brief pide: **confianza en el estado del auto** (fila 7, micro-códigos, 22 %), **garantía** (fila 9, palabra clave, 2,2 %). La garantía casi no aparece en la encuesta. Eso no prueba que no importe: el plan muestra que la garantía de Portillo es de 3 meses frente a 12 de Kavak y 24 de Bruno Fritsch [PLAN p.05]. Es un tema que la encuesta no captura. [HIPÓTESIS]

**Lectura de la tabla:** las filas 2, 3, 4 y 5 son dolores de compra con base sólida (n ≥ 39). La fila 1 domina en postventa. La fila 1 también incluye el ítem de entrega, que mide algo que pasa después de firmar.

**Cruce de control con research/06_arquetipos_cliente.md** (misma base de 313 detractores Usados): Claridad ≤2 = 25,2 % (C-10 Usados 25,2 %), Acogida ≤2 = 23,3 % (C-18 Usados 23,3 %), Atención ≤2 = 26,8 % (C-18 Usados 26,8 %), Fluidez ≤2 = 50,8 % (C-02 Usados 50,8 %), parte de pago 42/106 = 39,6 % (C-22 Usados 42/106). Los conteos coinciden. [DATO]

## 3. Universo Portillo (PORT_CAMP, n = 10 detractores): conteos, sin ranking

| Dolor | n / 10 detractores | Nota |
|---|---:|---|
| Claridad de precio y financiamiento | 5 | |
| Entrega: plazos, información | 5 | |
| Atención post venta | 6 | |
| Proceso y tiempos de compra | 4 | |
| Respuesta y trato en la venta | 4 | |
| Estado del auto | 3 | |
| Documentación | 2 | |
| Garantía (palabra clave) | 1 | Sin código de encuesta |
| Tasación (parte de pago) | 1 de 2 que aplican | Base de 2: no interpretable |

Con n = 10, un cambio de 1 fila mueve el porcentaje 10 puntos. **No se ordenan estos dolores por frecuencia.** Solo sirven para ver que los mismos temas aparecen en Portillo: postventa, precio/ficha, trato y estado del auto. Sentimiento negativo en 7 de 10 textos de detractores [DATO]. Dato de contexto: en PORT_CAMP hay 95 promotores (83 %), que es la base de la persona de la tarea A, no de esta.

## 4. Dolores con verbatims

Cada verbatim es literal, ≤15 palabras, sin nombres ni datos de contacto. Fuente: Venta-Usados. "PORT" = PORT_CAMP; "GRUPO" = los 313 detractores.

**Compra**

- **D1 · Proceso y tiempos de la compra** (GRUPO n = 161 · 51,4 %). Lo que teme: un proceso largo sin fecha. Qué debe resolver Portillo: un calendario de compra visible. [HIPÓTESIS, research/06 H1]
  - "Tramite muy engorroso" (CR_2025-Venta-Usados#1478, GRUPO)
- **D2 · Respuesta y trato en la venta** (GRUPO n = 147 · 47,0 %; PORT n = 4 de 10). Lo que teme: no recibir respuesta. Qué debe resolver: un contacto con respuesta en tiempo acordado. Coincide con la persona P2 del research/06 (silencio y trato). [DATO]
  - "Pésima atención del vendedor" (CR_2025-Venta-Usados#3434, PORT)
  - "Uno debe estar llamando" (CR_2025-Venta-Usados#112, GRUPO)
- **D3 · Claridad de precio y financiamiento** (GRUPO n = 125 · 39,9 %; PORT n = 5 de 10). Lo que teme: que el precio o la información de la ficha no coincidan con lo que se firma. Qué debe resolver: precio y financiamiento explicados por escrito antes de firmar. [DATO]
  - "Publicaron el auto que compré como 2024, pero era 2023." (CR_2025-Venta-Usados#3915, PORT)
  - "Me dijeron que el auto tenía todos los servicios de agencia y no era cierto" (CR_2025-Venta-Usados#977, GRUPO)
  - "dificultades para toma de crédito con financiera que estaba aprobada" (CR_2025-Venta-Usados#400, GRUPO)
- **D4 · Tasación / parte de pago** (GRUPO 42 de 106 que aplican · 39,6 %; PORT 1 de 2). Lo que teme: que el valor de su auto en parte de pago no sea justo o no coincida con lo publicado. Qué debe resolver: tasación clara y coherente con la web. Es el dolor que la v3 pide tratar por C-22; el significado de la pregunta de parte de pago sigue en bloqueo (Beto). [DATO con base reducida; C-22 NO VERIFICADO en su significado]
  - "Los valores ofrecidos en la página web por vehículos en parte de pago no son" (CR_2025-Venta-Usados#2256, GRUPO)
  - "Mejor tasación de mi vehículo" (CR_2025-Venta-Usados#1708, GRUPO)
- **D5 · Estado del auto al recibirlo** (GRUPO n = 69 · 22,0 %; PORT n = 3 de 10). Lo que teme: un seminuevo que llega con fallas o sin revisar. Qué debe resolver: inspección y estado del auto visibles antes de firmar. Es la confianza que el plan pide en el estándar de sucursal (p.05). [DATO]
  - "Nunca me dejaron probar el auto." (CR_2025-Venta-Usados#3361, PORT)
  - "al entregarme no enciende porque se descargo la batería" (CR_2025-Venta-Usados#3477, PORT)
  - "unidad se entrego sin limpieza" (CR_2025-Venta-Usados#400, GRUPO)
- **D6 · Garantía** (GRUPO 7 filas por palabra clave · 2,2 %; PORT 1 fila). Lo que teme: no saber qué cubre la garantía ni cómo se hace valer. Qué debe resolver: garantía explicada con su proceso. La garantía de 3 meses del plan es dato [PLAN p.05]. Sin código de encuesta: NO VERIFICADO como frecuencia.
  - "Que me entreguen un auto en optimas condiciones y que pueda hacer valer la garantía" (CR_2025-Venta-Usados#2540, GRUPO)
  - "para dar cualquier solución hay que enviar a la garantía" (CR_2025-Venta-Usados#3870, PORT; es postventa)

**Postventa**

- **P1 · Entrega: plazos e información de entrega** (GRUPO n = 242 · 77,3 %; PORT n = 5 de 10). Lo que teme: que el auto no llegue cuando se prometió o llegue con cosas que faltan. Qué debe resolver: fecha de entrega cumplida y kit de entrega completo. Es la fila más frecuente del grupo. Clasificarla como postventa es una decisión [HIPÓTESIS].
  - "No cumplen con fechas de entregas" (CR_2025-Venta-Usados#112, GRUPO)
  - "Sinceridad de que el vehículo venía trasladado de otra sucursal" (CR_2025-Venta-Usados#3870, PORT)
  - "Haber recibido el vehículo con todos los documentos y sin fallas de mecanica" (CR_2025-Venta-Usados#3477, PORT; respuesta a "¿qué faltó?")
- **P2 · Atención post venta y cumplimiento de acuerdos** (GRUPO n = 101 · 32,3 %; PORT n = 6 de 10). Lo que teme: que después de firmar nadie responda ni cumpla lo prometido. Qué debe resolver: seguimiento posterior a la venta con un responsable. [DATO]
  - "no me entregaron ningún tipo de información" (CR_2025-Venta-Usados#3451, PORT)
  - "No cumplen con lo acordado pre compra" (CR_2025-Venta-Usados#3801, PORT)
  - "los vendedores despues se olvidan del comprador" (CR_2025-Venta-Usados#1667, GRUPO)
- **P3 · Documentación: permiso y factura** (GRUPO n = 50 · 16,0 %; PORT n = 2 de 10). Sin verbatim seleccionado en la muestra revisada. Qué debe resolver: papeles completos en la entrega. [DATO]

## 5. Compra frente a postventa (resumen)

- **Compra (dolores que se viven antes de firmar):** proceso y tiempos (51,4 %), respuesta y trato (47,0 %), claridad de precio y financiamiento (39,9 %), tasación (39,6 % de los que aplican), estado del auto (22,0 %), garantía (2,2 %, palabra clave).
- **Postventa (dolores que se viven después de firmar):** entrega (77,3 %), atención post venta (32,3 %), documentación (16,0 %).
- **Frontera:** "Proceso de Entrega" y "Plazos de entrega" se cuentan como postventa. Si Beto prefiere contarlos como compra, la fila 1 pasa a compra. [HIPÓTESIS de clasificación]

## 6. Contradicciones (ambas cifras, sin corregir en silencio)

| # | Tema | Cifra A | Cifra B | Estado |
|---|---|---|---|---|
| B-1 | Universo Portillo en Venta-Usados | Campaña "Venta Usados Portillo": **114** [DATO] | Sucursal "PORT" al inicio: **108**; contiene "PORT" en cualquier posición: **145** (incluye 37 PORTALES) | Usar 114 o 108. No usar 145. Ver P3 en research/10_contradicciones_plan.md. |
| B-2 | Detractores Portillo vs grupo | Portillo (campaña): **10** detractores de 114 | Grupo Venta-Usados: **313** de 4.103 | No es contradicción; es escala. Sin n en Portillo, no hay ranking propio. |
| B-3 | Mapeo de sucursales de la base vs plan | Plan p.06: "Vitacura Padre Hurtado 1246", "Vitacura 5555", "Las Condes Fco. Bilbao 5593", "José Alcalde Délano 11021", "Usados Chacabuco 255" | Base: 6 filas de PORT_CAMP con nombre "USADOS VITACURA PADRE HURTADO 1246" (2), "...SAN FELIPE CHACABUCO 255" (1), "...VITACURA 5555" (1), "...LA DEHESA J A DELANO 11021" (1), "...LAS CONDES FCO BILBAO 5593" (1) | Coincidencia por número de calle. [HIPÓTESIS] Confirmar con Beto / Iván Balaguera. |
| B-4 | Tasación: ítem y "parte de pago" | Ítem "Vehículo en parte de pago" 1-2 en GRUPO detractores: 42 de 106 (39,6 %) | research/06 C-22: Usados 42 de 106 (39,6 %) | **Coinciden.** Su significado sigue NO VERIFICADO (Beto). |
| B-5 | Garantía | Plan p.05: Portillo 3 meses; Kavak 12; Bruno Fritsch 24 [PLAN] | Encuesta: 7 de 313 detractores (2,2 %) la nombran, y no existe código de garantía | El plan y la encuesta no se contradicen; la encuesta no mide garantía. |

## 7. Rutas

- Script (solo conteos): `/Users/betosanchez/portillo-personas/analisis/v3B_dolores_seminuevo.py`. Reproducir: `python3 analisis/v3B_dolores_seminuevo.py`.
- Fuente: `/Users/betosanchez/portillo-personas/inputs_clean/CR_2025-Venta-Usados_2023-03-01_2026-11-23_eda66aaf__sin_segmento.parquet`.
- Contraste: `/Users/betosanchez/portillo-personas/research/06_arquetipos_cliente.md` (C-02, C-10, C-18, C-22).

## 8. Bloqueos

- Mapeo de sucursales del plan a la base (B-3): **Beto / Iván Balaguera**.
- Significado de la pregunta de parte de pago (C-22): **Beto**.
- Tabla de stock y ticket del stock (no afectan este documento): **responsable de stock**.
- Encuesta sin código de garantía: decisión de **Beto** si se agrega a la encuesta.
- Clasificación de "Proceso de Entrega" como postventa: confirmar con **Beto**.
