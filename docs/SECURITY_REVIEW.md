# Revisión previa a publicación — 2026-10-20

## Alcance y método

Revisión de los dos scripts Lua, de la documentación pública y del contenido autorizado para distribución. Se revisaron las llamadas con efectos secundarios, la lectura de archivos, la configuración de repositorios, el manejo de errores y la privacidad de las rutas. Se añadieron casos de regresión para las correcciones y una comprobación automatizada del contenido de publicación.

Esto es una revisión de código y de empaquetado, no una certificación ni una auditoría del parser C/C++ de reAAF/LibAAF. No incluye fuzzing, sandboxing, análisis exhaustivo de dependencias o binarios ni pruebas adversarias de todos los exportadores AAF.

## Hallazgos y cambios

| Hallazgo en el prototipo | Corrección o tratamiento |
| --- | --- |
| La API para inspeccionar repositorios era opcional. | Ahora es obligatoria. Si no está disponible, no se cambia ninguna configuración. |
| Procesar la cola de ReaPack puede ejecutar operaciones ajenas pendientes. | No se procesa al utilizar un repositorio existente. Para agregar uno nuevo se explica el efecto y se permite cancelar antes de agregarlo; el nuevo repositorio tiene instalación automática desactivada. |
| El prototipo solo verificaba que el archivo tuviera contenido. | Se exige extensión AAF, una cabecera CFB reconocible y al menos 512 bytes antes de crear una pestaña. No se afirma que esto valide el AAF completo. |
| La última ruta se guardaba de forma persistente y aparecía completa en el resumen. | Se usa un estado de sesión separado y el nombre del archivo en el resumen. Los mensajes de error externos siguen necesitando revisión antes de compartirse. |
| La función diferida de informe quedaba fuera del manejador de excepciones. | Se protege también la función diferida y se abandona el informe si cambia la pestaña. |
| No había comprobación de grabación ni restricción explícita de prefijos de apertura. | Se bloquea la importación durante grabación; se exigen rutas absolutas sin caracteres de control. |
| La carpeta de desarrollo contenía material de pruebas privado. | Se creó una carpeta de distribución independiente con una lista explícita de archivos permitidos. No se distribuyen AAF, audio, proyectos, logs privados ni dependencias instaladas. |

No se encontraron comandos de shell, envío de medios a servicios ni descargadores propios en los scripts revisados. Esa observación solo se refiere a estas acciones Lua.

## Verificación

- Las pruebas simuladas cubren cancelación, conservación del proyecto activo, disponibilidad de APIs, URL distinta con nombre coincidente, repositorio deshabilitado, errores de repositorio, colas pendientes, archivos ilegibles, cabeceras inválidas o truncadas, rutas y prefijos no permitidos, grabación y errores diferidos.
- El control de publicación compara el contenido con una lista explícita y busca formatos comunes de secretos, rutas personales y medios o binarios no autorizados. Es una defensa adicional, no un detector universal de secretos.
- La implementación anterior al endurecimiento se probó dentro de REAPER 7.79/macOS Apple Silicon con reAAF 0.3.7: un AAF sintético de dos pistas/tres clips y un AAF real de 107 clips. La prueba real recuperó los 107 clips, incluidos 13 silenciados, con referencias de medios disponibles. Se compararon pista de origen, posición, duración, recorte, estado silenciado y nombre del medio, normalizando la separación de canales.
- Los nuevos controles del wrapper se verifican con la API simulada. No se ha repetido la prueba nativa completa sobre la versión pública endurecida. No se han realizado pruebas nativas de Windows, Linux, Intel o Rosetta.

No se publican los AAF, identificadores, rutas, nombres de proyecto ni registros privados de la prueba real.

## Riesgos residuales y dependencias

reAAF realiza el análisis nativo dentro de REAPER y puede leer los medios que el AAF referencia. Los scripts no aíslan ese código ni controlan la extracción de medios o el consumo de memoria. Un archivo corrupto podría fallar aunque pase la comprobación superficial.

ReaPack y el repositorio oficial del motor son dependencias de confianza para la instalación. El helper no incorpora el motor ni verifica el binario instalado. Mantener actualizados esos componentes y verificar su procedencia sigue siendo responsabilidad de quien instala.

La página pública de [seguridad de reAAF](https://github.com/smandrap/reAAF/security) consultada durante esta revisión no mostraba avisos publicados. La ausencia de avisos no demuestra ausencia de vulnerabilidades. También se consultaron [el código de la API de ReaPack](https://github.com/cfillion/reapack/blob/master/src/api_repo.cpp) y [la API oficial de REAPER](https://www.reaper.fm/sdk/reascript/reascripthelp.html).
