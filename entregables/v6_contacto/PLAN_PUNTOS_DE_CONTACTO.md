# PLAN DE PUNTOS DE CONTACTO · Antonia y Tomás · v6 [HIPÓTESIS-ML]
Corte 2026-11-24. Uso INTERNO, no publicar. Las ideas son hipótesis de contenido, no evidencia. Ver `research/v6_contacto/SESGOS.md` antes de usar cualquier ranking.

## Qué se construyó
- Universo de 76 candidatos: 70 con URL verificada y 6 NO VERIFICADO (no entran al ranking).
- Cuatro métodos planeados. Corrieron tres (similitud de embeddings, NLI zero-shot y PageRank personalizado sobre grafo). El filtro colaborativo no corrió: no hay dataset público de co-ocurrencia.
- Detalle de métodos en `research/v6_contacto/METODO.md`.

## Lo que dice el modelo (resumen honesto)
- Los primeros puestos de ambas personas son intereses automotrices (Car Culture, Auto Buying and Selling, Auto Shows, Auto Safety). Se explican por vocabulario de compra en las semillas, no por estilo de vida.
- Las diferencias entre personas son pequeñas. Coinciden 16 de los 20 primeros puestos.
- Solo aparecen en el top 20 de Antonia: Certified Pre-Owned Cars, Family Travel, Home Entertaining y Parenting. Vienen de rasgos de perfil ILUSTRATIVOS o HIPÓTESIS y hay que validarlos antes de usarlos.
- Solo aparecen en el top 20 de Tomás: Inicio de clases (marzo), Outdoor Activities, Travel Insurance y Trekking El Morado. Inicio de clases tiene una explicación semántica débil.

## Territorios
Ver `research/v6_contacto/territorios.csv` y `UNIVERSO_CONTACTO.html` (uso interno, no publicar).
- Auto y seminuevos (compartido): Car Culture, Auto Buying and Selling, Auto Shows, Auto Safety, Luxury Cars, Green Vehicles, Certified Pre-Owned Cars, SUV.
- Viajes y naturaleza cerca de Santiago (mixto): Cajón del Maipo, El Morado, playas del litoral central, escapadas de Semana Santa, Parks & Nature.
- Hogar (mixto, poco detalle): Smart Home, Home Entertaining, Home Improvement.
- Deportes y entretención (mixto): esquí, pádel, running en Parque Bicentenario, ciclismo urbano.
- Los territorios "propios" no tienen dominio claro con 70 candidatos. No se afirma que un territorio sea exclusivo de una persona.

## Calendario por punto de contacto
Ver `CALENDARIO_PUNTOS_DE_CONTACTO.csv` (diciembre 2026 a noviembre 2027). Reglas:
- Cada idea tiene persona, territorio, etapa del funnel, formato, canal y la hipótesis que la sostiene.
- El auto acompaña la vida de la persona; el seminuevo resuelve. La marca usa "seminuevo", nunca "usado".
- Sin promesas de garantía ni plazos que no estén respaldados. Sin cifras internas en piezas públicas. Sin afirmar conversión lead→venta.
- Las fechas de 2027 (vacaciones de invierno, Semana Santa, Fiestas Patrias) no están verificadas. Se marcan como NO VERIFICADO.

## Qué puede ir como prueba chica A/B y qué espera validación
- Prueba chica posible (contexto de calendario con fuente WEB): Fiestas Patrias, vacaciones de invierno y temporada de esquí. Requieren confirmar fechas 2027 antes.
- Espera validación (hipótesis de interés): Family Travel, Home Entertaining, Parenting, Certified Pre-Owned Cars (Antonia) y Trekking El Morado, Travel Insurance (Tomás). No lanzar hasta pasar `PLAN_VALIDACION.md`.

## Bloqueos con responsable
- Decisión sobre semillas ILUSTRATIVAS de Antonia (hijos, colegio): Beto.
- Acceso de lectura a GA4 y a la cuenta de Meta: Beto.
- Autorización y muestra para la encuesta de compradores: Beto y equipo comercial.
- Export de ventas con ticket, modelo y comuna (sin él no se puede cruzar el ranking con compras): Beto.
- Artifact de UNIVERSO_CONTACTO.html: no publicado. Requiere autorización de Beto (contiene el método interno y nombres derivados).
- Filtro colaborativo: sin dataset público confiable. Responsable: Beto, si decide buscar uno.
