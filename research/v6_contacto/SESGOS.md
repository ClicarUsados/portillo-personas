# SESGOS · v6 universo de contacto [HIPÓTESIS-ML]
Fecha de corte: 2026-11-24. Uso INTERNO. Generado por `analisis/v6_contacto/01_afinidad.py` y `03_sensibilidad_lexica.py`.

## 1. Contrafactual de género y comuna (Fase 4)
Método: para cada persona se agregó una semilla extra (peso 0,3) con el atributo, solo emb+PPR (sin NLI, para no correrlo 4 veces).
- Género: directo (Antonia "mujer", Tomás "hombre") y cruzado (Antonia "hombre", Tomás "mujer").
- Comuna: directa (Antonia "La Dehesa", Tomás "Providencia") y cruzada (Antonia "Providencia", Tomás "La Dehesa").
- Criterio: |Δ puesto| > 20 respecto a la base = eliminar del top y listar aquí.

Resultado:
- Antonia: máximo |Δ| = 6 puestos. Ningún candidato supera 20.
- Tomás: máximo |Δ| = 7 puestos. Ningún candidato supera 20.
- Candidatos eliminados por sesgo: **ninguno**. Detalle: `sesgos_detalle_antonia.csv`, `sesgos_detalle_tomas.csv`.

Límite de la prueba: un solo token con peso 0,3 sobre ~30 semillas es un estímulo débil. Que no se mueva nada no prueba ausencia de sesgo; solo dice que el modelo casi no reacciona a esa palabra. Una prueba más dura (peso 1,0 y reemplazo completo de semillas) queda pendiente.

## 2. Fuga léxica: el ranking base es eco del vocabulario de compra (hallazgo principal)
- Los 5 primeros de Antonia y los 4 primeros de Tomás son intereses automotrices (Car Culture, Auto Buying and Selling, Auto Shows, Auto Safety). Las semillas contienen "auto", "auto usado", "vehículo", "compra" y "seminuevo", y los nombres de candidatos comparten esas palabras. Es coincidencia léxica, no afinidad de estilo de vida.
- Prueba de sensibilidad (`03_sensibilidad_lexica.py`): con solo las 3 semillas de estilo de vida de Antonia (HIPÓTESIS), el top 10 pasa a Family Travel, Landscaping, Gardening, Home Entertaining, Honeymoons and Getaways, Smart Home, Outdoor Activities, Interior Decorating, Excursiones naturales, Parenting. Solapamiento con el top 10 base: 3 de 10. Advertencia: son solo 3 semillas.
- Conclusión: el ranking base mide cercanía a vocabulario de compra. Para decidir contenido de estilo de vida hay que separar los dos ejes.

## 3. Riesgo de estereotipo (requiere decisión de Beto)
- Las semillas `r_antonia_00` ("colegio de los hijos") y `r_antonia_01` tomaron rasgos de la ficha de Antonia. En el perfil, "Casada, dos hijos" y el detalle de la familia están marcados **ILUSTRATIVO** (inventados para humanizar), no DATO.
- Efecto medido: Parenting, Family Travel, Home Entertaining y Smart Home entran al top 15 de Antonia y no aparecen en el de Tomás. Son los candidatos que más dependen de esa ficha.
- Acción recomendada antes de usar el ranking: retirar esas semillas (o marcarlas) y volver a correr `01_afinidad.py`. No se cambió en esta corrida para no alterar los entregables sin tu visto bueno.
- Tomás no tiene semillas de estilo de vida en el perfil. Su ranking es, en la práctica, de proceso de compra. Eso sesga la comparación entre personas: las diferencias "propias de Antonia" reflejan más el perfil ILUSTRATIVO que datos.

## 4. Otras revisiones (criterios de detector-de-ruido y abogado-del-diablo)
Las skills no se invocaron en esta corrida; se aplicaron sus criterios a mano. Lo digo para que sepas qué vino de quién.
- **NLI poco fiable.** mDeBERTa satura: 10 de 70 candidatos quedan por encima de 0,9 para ambas personas, y el Kendall contra emb/PPR es 0,12 a 0,24. Está en el ensamble, pero su peso es dudoso. Si se quita, el robusto pasa a ser "top 14 en emb y PPR".
- **Estabilidad sobreestimada.** El bootstrap solo remuestrea semillas y recalcula emb+PPR. Por eso 63 a 65 de 70 aparecen como "estables". El rango de bootstrap llega a 43 y 48 puestos. Tomar "estable" como garantía sería un error.
- **Robusto con criterio adaptado.** Sin M4 (filtro colaborativo), robusto = top 14 en los tres métodos disponibles, no "3 de 4". Antonia: 5 robustos; Tomás: 6.
- **Falsos positivos semánticos.** Tomás tiene "Inicio de clases y vuelta a clases (marzo)" en el puesto 5. Probablemente se engancha con "respuesta rápida al aviso" y "agendada", no con un estilo de vida. Hay que validarlo antes de usarlo en un calendario.
- **Comparación sin control de tamaño.** El universo tiene 70 candidatos, con 49 de taxonomía IAB (intereses genéricos) y 21 locales o de calendario. Los locales están subrepresentados en el ranking porque su texto es más corto.
- **Género sin evidencia propia.** El contrafactual muestra que el modelo casi no responde a "mujer" u "hombre", pero eso no implica que los intereses estén libres de estereotipo: la ficha ya los define.

## 5. Lo que no se pudo medir
- Comunas reales de residencia: ninguna encuesta las registra (dato de perfil ILUSTRATIVO). La prueba de comuna compara La Dehesa y Providencia como contexto, no como variable real.
- Filtro colaborativo (M4): sin dataset público de co-ocurrencia. No se fabricaron datos.
