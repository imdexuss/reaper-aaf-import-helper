# Contribuir

Gracias por ayudar a mejorar el helper. Antes de proponer cambios, consulta [SECURITY.md](SECURITY.md) y distingue los fallos de estas acciones de los del lector reAAF.

## Reproducir un problema

Incluye versión y arquitectura de REAPER, sistema operativo, versión de ReaPack/reAAF, programa exportador y pasos de reproducción. Indica si el AAF utiliza medios externos o incrustados y qué esperabas obtener.

No publiques proyectos de clientes, audios privados, rutas personales, secretos ni archivos que no puedas compartir. Un ejemplo sintético es preferible. Para defectos de seguridad, utiliza el procedimiento de SECURITY.md antes de publicar detalles.

## Probar un cambio

1. Instala los requisitos de desarrollo en un entorno virtual, como explica el README.
2. Ejecuta `python tests/test_scripts.py` y `python tests/check_release.py`.
3. Para cambios de importación, verifica también un AAF sintético dentro de REAPER, en una pestaña nueva, y documenta qué plataforma has probado.
4. Mantén los scripts autocontenidos y sus mensajes en español. Actualiza la documentación en ambos idiomas si cambia el comportamiento.

No añadas binarios del motor, dependencias instaladas, medios o AAF de prueba privados al repositorio. Los cambios en las acciones no deben modificar proyectos previos, escribir en el AAF, ejecutar comandos de shell ni añadir destinos de descarga distintos del proveedor oficial sin una revisión explícita.
