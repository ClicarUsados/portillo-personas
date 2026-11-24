# Notas de marca · perfiles cliente ideal v2

Fecha de corte: 2026-11-23. Solo cambios visuales; ningún texto, cifra, etiqueta de evidencia ni fuente cambió, salvo "(zona definida por Beto)" en Javiera y "(comuna definida por Beto)" en Tomás, que se quitaron.

## Inconsistencias del brandbook (reportadas, no resueltas)

1. **Celeste**: brandbook dice #6bc1e9; el RGB del mismo brandbook (136, 191, 231) equivale a #88bfe7; el SVG del logo usa #69bfe8.
2. **Azul**: brandbook #0082d1; SVG del logo #0680cf.
3. **Garantía, 3 meses vs 12 meses**: el gancho "Cobertura mecánica hasta 12 meses" (p. 19) no calza con "3 meses de garantía" del plan. El propio brandbook tiene la pieza RRSS (p. 21) con "3 GARANTÍA MESES". Ambas cifras quedan sin resolver. Los perfiles no usan ninguno de los dos ganchos.
4. **Ganchos sin respaldo**: "Satisfacción garantizada", "Precio líder del mercado", "Garantía de excelencia" y "Tu auto usado como nuevo aquí" aparecen en el brandbook pero no se usaron en los perfiles.

## Licencia FF Good Pro
- Fuente comercial. En el HTML local se carga desde `assets/brand/fonts/` (@font-face). Esto requiere que la licencia cubra web. **Depende de Beto / diseño.**
- En el artifact publicado no debe incrustarse: usar "Barlow Semi Condensed" itálica (Google Fonts) como reemplazo.

## Edad de Javiera
- La ficha dice 41 años; la persona de las imágenes (02 y 03) se ve más joven. No se cambió la ficha. **Decisión de Beto**: ajustar la edad ilustrativa o regenerar la imagen.

## Confirmación de imágenes de IA
- No puedo confirmar el uso de imágenes generadas con IA. **Pendiente de Beto.** Hasta entonces, el artifact publicado no lleva imágenes; la versión local sí.

## Publicación
- Los artifacts no se han publicado. Para publicar: quitar el bloque @font-face de FF Good Pro, cambiar la fuente de títulos a Barlow Semi Condensed (ya incluida como respaldo), quitar las imágenes de Javiera hasta tener confirmación, y dejar "Imagen pendiente" en la sección de Tomás.

## Acento de color
- Por defecto solo #212c35 y blanco. Si se quiere acento de Portillo Usados (#0082d1, #6bc1e9, #fda902), es decisión de Beto. Una línea bicolor celeste/amarillo bajo la cabecera queda como opcional, no aplicada.

## Verificación
- Capturas en `capturas/`. Escritorio 1440 px y celular 390 px. El render móvil de Chrome headless puede quedar más ancho que 390 px; revisar en un celular real antes de dar por buena la responsividad.
- Contraste AA verificado para chips y texto (mínimo 5,6:1).
