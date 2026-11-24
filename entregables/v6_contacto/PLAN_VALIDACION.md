# PLAN DE VALIDACIÓN · puntos de contacto v6 [HIPÓTESIS-ML]
Corte 2026-11-24. Uso INTERNO. Todo lo de abajo es hipótesis hasta que una prueba la pase. Nada de esto se ejecutó: no se creó ninguna campaña, audiencia, tarea ni consulta en GA4, Meta, Google ni Asana.

## Qué hay que validar primero (top 15 de cada persona)
Ver `research/v6_contacto/ranking_antonia.csv` y `ranking_tomas.csv`. Antes de validar, dos advertencias de SESGOS.md:
1. Los primeros puestos de ambas personas son intereses automotrices que se explican por vocabulario de compra. No son evidencia de estilo de vida. Conviene validar primero los candidatos que no son automotrices.
2. Las semillas de estilo de vida de Antonia tienen origen ILUSTRATIVO. Hay que decidir si se retiran antes de validar (Beto).

## Criterio común
- Lift = proporción del interés entre el grupo de interés / proporción del mismo interés en la base de referencia.
- Validado: lift > 1,2 con n ≥ 30 en el grupo. Por debajo de n = 30 se reporta como exploratorio.
- Cada prueba debe declarar su fuente y fecha. Si el dato no se obtiene, queda NO VERIFICADO.

## Método 1 · Encuesta corta a compradores de sucursales de la zona oriente
- Alcance: compradores de seminuevos de sucursales de la zona oriente (La Dehesa, Bilbao, Luis Carrera, Padre Hurtado, Las Condes, Vitacura), según el cruce de `analisis/v3_oriente_promotores.py`.
- Instrumento: 3 preguntas de selección múltiple con las 15 opciones del top de cada persona más "ninguna de las anteriores". Pregunta 1: qué hacen los fines de semana. Pregunta 2: a qué tipo de lugar o actividad van más seguido. Pregunta 3: qué medio usan para informarse.
- Análisis: FP-Growth sobre las respuestas (soporte, confianza y lift). Un conjunto de intereses es válido si lift > 1,2 y n ≥ 30.
- Lo que falta: n de compradores disponible, autorización de Beto para la encuesta, y consentimiento para usar la lista de sucursales. Responsable: Beto y el equipo comercial.
- Nota de método: con n = 30, el lift mínimo detectable es alto. Esto solo sirve para descartar, no para confirmar.

## Método 2 · GA4 (intereses de visitantes de la landing premium)
- Reporte: Google Analytics, sección de audiencias o demografía "Intereses" (categorías de afinidad y en el mercado), filtrado a la landing premium.
- Índice de afinidad = % de visitantes de la landing con el interés X / % de visitantes del sitio con el interés X. Validado si > 1,2 con n ≥ 30 visitantes.
- Lo que falta: acceso de lectura a la propiedad GA4 y que el sitio tenga landings premium con tráfico. Responsable: Beto. No se consulta nada en esta fase.

## Método 3 · Meta Ads (tamaño de audiencia por interés en comunas de la zona)
- Reporte: en el Administrador de anuncios, estimación del tamaño de audiencia por interés, filtrada a las comunas de la zona oriente. Solo lectura, sin crear audiencias.
- Índice: tamaño de audiencia del interés en la zona / tamaño del mismo interés en la RM (referencia). Validado si > 1,2.
- Lo que falta: acceso de lectura a la cuenta de Meta. La lista de intereses de Meta no tiene URL pública verificada (NO VERIFICADO), así que los nombres de interés deben tomarse del Administrador, no de la taxonomía IAB.
- Responsable: Beto y el equipo de pauta.

## Método 4 · Google Trends por región
- Términos: los nombres de los candidatos de la zona (p. ej., "trekking El Morado", "pádel Santiago", "Valle Nevado") y las palabras de búsqueda de seminuevos.
- Región: Región Metropolitana; comparar con las comunas solo si Trends lo permite a ese nivel (NO VERIFICADO).
- Estacionalidad esperada: esquí junio a agosto (chile.travel, WEB), playa enero y febrero, Fiestas Patrias septiembre, vacaciones de invierno en junio y julio (prensa citando el calendario del Mineduc, WEB), vuelta a clases en marzo.
- Criterio: que la serie de un término muestre un pico en la estacionalidad esperada. Si no hay pico, el término se descarta como contexto de calendario.

## Qué no se valida con estos métodos
- Conversión lead→venta: no se afirma en ningún método.
- Comuna real de residencia: ninguna encuesta la registra (SESGOS.md §5).
- Garantía o plazos: no son parte de la validación de intereses.

## Orden sugerido
1. Retirar o marcar semillas ILUSTRATIVAS (decisión de Beto). Re-correr `01_afinidad.py`.
2. Google Trends (sin acceso especial, bajo costo).
3. Lectura de GA4 y Meta (requiere acceso de Beto).
4. Encuesta (requiere autorización y muestra).
