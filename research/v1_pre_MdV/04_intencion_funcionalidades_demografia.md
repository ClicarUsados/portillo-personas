# Intención, funcionalidades web y demografía — Subagente D

Fecha de extracción de los archivos: **2026-11-23**. Script reproducible: `python3 analisis/4D_intencion_funcionalidades.py` (imprime solo conteos y porcentajes).

**Fuentes (solo `inputs_clean/*.parquet`):**
- `CR_Encuesta-funcionalidades-Web_*` — n=324, fecha respuesta 2025-07-18 a 2025-08-23, canal Email.
- `CR_Encuesta-de-seguridad-vial-en-Chile_*` — n=709, fecha respuesta 2025-10-22 a 2025-10-29, solo clientes de autos nuevos.

**Universos declarados:**
- **GRUPO_COMPLETO**: todas las filas de cada archivo (todas las cifras de las secciones 1 a 4 y 6).
- **PORTILLO_HIPOTESIS**: PORT/PORTILLO en `nombre_concesionario` (ver `research/00_mapeo_portillo.md`). **[HIPÓTESIS] — bloqueado: depende de Beto / Iván Balaguera.** No se usa para conclusiones.

**Umbral de n mínimo:** n ≥ 30 para reportar cortes. Por debajo se muestra el conteo, sin conclusión.

---

## Sesgos y limitaciones (leer primero)

1. **Encuesta web de un solo período y de un solo canal.** 324 respuestas en ~5 semanas, todas por email.
2. **Sesgo de campaña.** 63.3% de las respuestas web vienen de la campaña "Salazar Israel" (`campaña o sensor`). La muestra representa sobre todo a clientes de esa campaña, no al total de Portillo ni al mercado.
3. **Seguridad vial: no representa al comprador de seminuevos.** Son clientes de autos nuevos, un solo mes (2025-10-22 a 2025-10-29), y es una encuesta de un solo mes. No sirve para inferir perfil de comprador de usados.
4. **Escala de los niveles de acuerdo no verificada.** Los campos son enteros 1 a 5 sin diccionario de escala. Se asume que 5 = muy de acuerdo. Las etiquetas de extremos son **NO VERIFICADO**.
5. **Escala de estrés no verificada.** Se asume 1 = poco estrés y 5 = mucho estrés. **NO VERIFICADO**.
6. **No se hicieron pruebas estadísticas** (ni intervalos de confianza ni tests de diferencia). Las diferencias pequeñas no deben leerse como efectos.

---

## 1. Top-3 funcionalidades (web, n=324) [DATO]

Fuente: columnas `Por favor, selecciona entre las siguientes funcionalidades… las tres más importantes…` de `CR_Encuesta-funcionalidades-Web_*`. Filtro: valor no vacío = opción marcada. Cada persona elige 3.

Control: 10 columnas, suma de selecciones = 972 = 3 × 324. Cuadra. 324 de 324 respondieron el top-3 completo.

| # | Funcionalidad | n | % de 324 |
|---|---|---:|---:|
| 1 | Herramientas para comparar formas de pago / calcular qué auto puedo comprar | 141 | 43.5% |
| 2 | Contenido educativo sobre compra, financiamiento y mantenimiento | 136 | 42.0% |
| 3 | Opiniones de otros clientes y expertos antes de decidir | 131 | 40.4% |
| 4 | Recomendación de modelos según preferencias y presupuesto | 130 | 40.1% |
| 5 | Alertas sobre el mejor momento para vender mi auto | 115 | 35.5% |
| 6 | Videos, blogs y ranking de modelos | 91 | 28.1% |
| 7 | Personalizar mi auto online (colores, accesorios) | 83 | 25.6% |
| 8 | Agendar test drive en el sitio web | 62 | 19.1% |
| 9 | Sección dedicada a vehículos eléctricos | 43 | 13.3% |
| 10 | Asistente virtual que oriente mientras navego | 40 | 12.3% |

**Lectura:** el top 3 lo ocupan herramientas de decisión de compra (pago, educación, opiniones). La sección EV y el asistente virtual quedan al final.

## 2. Niveles de acuerdo (web, n=324 por ítem) [DATO] — escala 1-5, extremos NO VERIFICADOS

"De acuerdo" = 4-5. "Neutro" = 3. "En desacuerdo" = 1-2. Columnas de `CR_Encuesta-funcionalidades-Web_*`, valores enteros, sin vacíos.

| Ítem (resumido) | De acuerdo | Neutro | En desacuerdo |
|---|---:|---:|---:|
| Herramientas para comparar pagos / calcular qué auto puedo comprar | 85.8% | 10.2% | 4.0% |
| Contenido educativo (compra, financiamiento, mantenimiento) | 84.3% | 9.3% | 6.5% |
| Recomendación de modelos según preferencias y presupuesto | 84.0% | 10.8% | 5.2% |
| Considero importante conocer opiniones de otros clientes y expertos | 83.3% | 10.5% | 6.2% |
| App: avisos de mantenimiento y notificaciones | 83.3% | 9.9% | 6.8% |
| Alertas sobre el mejor momento para vender mi auto | 81.2% | 13.0% | 5.9% |
| Valoro videos, blogs y rankings de modelos | 80.9% | 13.6% | 5.6% |
| App: historial del vehículo, documentos, mantenimientos y boletas | 89.8% | 4.6% | 5.6% |
| Test drive directamente desde el sitio web | 71.6% | 21.6% | 6.8% |
| Personalizar mi auto online | 71.3% | 21.0% | 7.7% |
| App en el celular con funcionalidades del sitio | 65.7% | 23.1% | 11.1% |
| No me molesta que el chat me derive a WhatsApp si obtengo mejor atención | 67.0% | 18.8% | 14.2% |
| Asistente virtual que me acompañe en la visita | 60.8% | 25.6% | 13.6% |
| Me interesa una sección exclusiva de autos eléctricos | 45.1% | 41.7% | 13.3% |

**Nota de lectura:** la sección EV tiene 45.1% de acuerdo en la escala, pero solo 13.3% la pone en el top 3. Son preguntas distintas (interés general vs. prioridad). No es una contradicción, pero no hay que citar una como si fuera la otra.

## 3. NPS y cobertura de respuesta

| Campo | Resultado | Fuente |
|---|---|---|
| `nps` (web) | n válido = 324 de 324 (100%). Valores: 10 → 271; 9 → 53 | [DATO] `CR_Encuesta-funcionalidades-Web_*`, columna `nps` |
| `encuesta` (web) | "Encuesta funcionalidades Web": 324 (100%) | [DATO] misma columna |
| `campaña o sensor` (web) | Salazar Israel 205 (63.3%); Portillo 72 (22.2%); Coseche 28 (8.6%); Servimaq 19 (5.9%) | [DATO] |
| `canal` (web) | Email: 324 (100%) | [DATO] |
| `fecha de inicio` (web) | 18 vacíos (5.6%) | [DATO] |
| Preguntas de top-3 (web) | Vacíos por opción: 56.5% a 87.7% (esperable en selección de 3 de 10) | [DATO] |
| Pregunta abierta "¿Hay alguna otra funcionalidad…?" | 324 vacíos (100%) | [DATO] |
| `nps` (seguridad vial) | No existe en el archivo | [DATO] columnas |
| `encuesta` (seguridad vial) | Existe, pero no se reporta en esta tarea | [DATO] |

**Lectura de NPS:** todas las respuestas valen 9 o 10. No hay detractores. Eso sugiere muestra de clientes satisfechos o sesgo de respuesta. **No se calcula NPS como indicador** porque la escala observada está truncada y no hay diccionario.

**Respuesta abierta:** 100% vacía. No hay texto que analizar.

## 4. Funcionalidades por des_marca (web) [DATO] — GRUPO_COMPLETO

Solo la marca con n ≥ 30 supera el umbral. Las demás no se concluyen.

| des_marca | n | Pide sección EV en top-3 |
|---|---:|---:|
| MG | 36 | 4 (11.1%) |
| Resto de marcas (n < 30 cada una) | 288 | sin conclusión |

- Marcas con n < 30 (no se concluye): CHEVROLET 28, TOYOTA 26, NISSAN 23, KIA MOTORS 23, VOLKSWAGEN 18, SUBARU 18, FORD 16, HONDA 16, PEUGEOT 14, CHERY 13, y 23 marcas más con n ≤ 10.
- Referencia global: EV en top-3 = 13.3% (43 de 324). MG 11.1% (4 de 36) no difiere de forma interpretable de la media. **No hay evidencia en estos datos de que alguna marca pida más la sección EV.**
- **Conclusión por marca: NO VERIFICADO** (n insuficiente para casi todas las marcas).

## 5. Universo PORTILLO_HIPOTESIS

### 5a. Web [HIPÓTESIS]

- PORT/PORTILLO en `nombre_concesionario`: **n = 30 (9.3%)** de 324. Bloqueado (Beto / Iván Balaguera).
- Bajo el umbral. Solo descriptivo, sin conclusión. Conteos de top-3 de este subgrupo: Contenido educativo 21; Opiniones 14; Recomendación de modelos 14; Videos/blogs/ranking 10; Herramientas de pago 10; Sección EV 5; Personalización 5; Alertas de venta 5; Test drive 2; Asistente virtual 4.

### 5b. Campaña o sensor (contradicción)

| Fuente | Cifra |
|---|---:|
| [DATO] `campaña o sensor` contiene "Portillo" (web) | **n = 72 (22.2%)** |
| [HIPÓTESIS] `nombre_concesionario` PORT/PORTILLO (web) | **n = 30 (9.3%)** |

**NO CALZAN: 72 vs 30.** No se corrige ninguna. Ambas cifras se reportan. Explicación posible (no verificada): la etiqueta de campaña y el concesionario de la venta son campos distintos. Hay que confirmarlo con Beto / Iván Balaguera antes de usar cualquiera de las dos para Portillo.

### 5c. Seguridad vial

| Fuente | Cifra |
|---|---:|
| [DATO] `campaña o sensor` contiene "Portillo" | **n = 142 (20.0%)** de 709 |
| [HIPÓTESIS] `nombre_concesionario` PORT/PORTILLO | **n = 102 (14.4%)** de 709 |

**NO CALZAN: 142 vs 102.** Mismo tratamiento que 5b. El valor 102 coincide con el conteo de `00_mapeo_portillo.md`; el 142 no aparece en ese mapeo.

## 6. Seguridad vial: demografía (n=709) [DATO] — solo clientes de autos nuevos, 2025-10-22 a 2025-10-29

**Sesgo (repetido):** no representa al comprador de seminuevos. Encuesta de un solo mes.

### 6a. Rango de edad

| Rango | n | % de 709 |
|---|---:|---:|
| 60 o más años | 186 | 26.2% |
| 50 a 59 años | 183 | 25.8% |
| 40 a 49 años | 175 | 24.7% |
| 30 a 39 años | 103 | 14.5% |
| 18 a 29 años | 36 | 5.1% |
| Vacío | 26 | 3.7% |

### 6b. Género

| Género | n | % de 709 |
|---|---:|---:|
| Masculino | 434 | 61.2% |
| Femenino | 230 | 32.4% |
| Prefiero no decirlo | 9 | 1.3% |
| Vacío | 36 | 5.1% |

### 6c. Frecuencia de conducción

| Frecuencia | n | % de 709 |
|---|---:|---:|
| Todos los días | 502 | 70.8% |
| Varias veces por semana | 134 | 18.9% |
| Ocasionalmente | 71 | 10.0% |
| No conduzco | 2 | 0.3% |

### 6d. Estrés al conducir en ciudad (escala 1-5; dirección NO VERIFICADA)

Media global: **2.66** (n = 700 válidos; 9 vacíos).

| Corte | Grupo | n | Media |
|---|---|---:|---:|
| Frecuencia | Todos los días | 493 | 2.63 |
| Frecuencia | Varias veces por semana | 134 | 2.68 |
| Frecuencia | Ocasionalmente | 71 | 2.73 |
| Frecuencia | No conduzco | 2 | sin conclusión (n < 30) |
| Edad | 60 o más | 184 | 2.52 |
| Edad | 50 a 59 | 181 | 2.64 |
| Edad | 40 a 49 | 172 | 2.74 |
| Edad | 30 a 39 | 102 | 2.86 |
| Edad | 18 a 29 | 36 | 2.61 |

**Lectura:** con frecuencia, el estrés casi no cambia (2.63 a 2.73). Con edad hay una tendencia suave (2.52 en 60+ a 2.86 en 30-39), pero 18-29 rompe el patrón con n=36. Sin prueba estadística no se afirma relación. **No hay variable de ingreso ni de zona para explicar el estrés.**

### 6e. Cruce frecuencia x edad (n)

| Edad | Todos los días | Varias veces/sem. | Ocasionalmente | No conduzco |
|---|---:|---:|---:|---:|
| 18-29 | 22 | 10 | 4 | 0 |
| 30-39 | 73 | 16 | 14 | 0 |
| 40-49 | 131 | 33 | 11 | 0 |
| 50-59 | 131 | 32 | 18 | 2 |
| 60+ | 126 | 39 | 21 | 0 |
| Vacío | 19 | 4 | 3 | 0 |

## 7. Qué no sabemos

- **Ingreso:** no está en estos datos.
- **Pie / enganche:** no está en estos datos.
- **Financiamiento (tipo, plazo, bancos):** no está en estos datos. El ítem de comparar formas de pago no dice qué forma de pago usan hoy.
- **Zona geográfica:** no está en estos datos (solo nombre de concesionario).
- **Escala de acuerdo y de estrés:** no hay diccionario. Las etiquetas de extremos son NO VERIFICADO.
- **Significancia estadística:** no se calculó.
- **Relación entre funcionalidades y demografía de la encuesta web:** la encuesta web no tiene edad ni género. Solo tiene marca, concesionario, tipo de cuenta, modelo y campaña. No se puede cruzar funcionalidades con edad.
- **Portillo:** la asignación de sucursales/marcas a Portillo está bloqueada (Beto / Iván Balaguera). Ver contradicciones 5b y 5c.
- **Seminuevos:** ninguna de las dos encuestas representa al comprador de usados.

---

## Contradicciones (sin corregir)

| Tema | Cifra A | Cifra B |
|---|---|---|
| Portillo en encuesta web | 72 (22.2%), por `campaña o sensor` [DATO] | 30 (9.3%), por `nombre_concesionario` PORT/PORTILLO [HIPÓTESIS] |
| Portillo en seguridad vial | 142 (20.0%), por `campaña o sensor` [DATO] | 102 (14.4%), por `nombre_concesionario` PORT/PORTILLO [HIPÓTESIS] |

Pendiente de confirmar con Beto / Iván Balaguera qué campo define a Portillo.
