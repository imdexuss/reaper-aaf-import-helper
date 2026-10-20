# Seguridad y privacidad

## Alcance

Este repositorio mantiene dos acciones Lua. El análisis de AAF y la resolución de medios se realizan en la extensión nativa reAAF y su dependencia LibAAF. **No se ha realizado una auditoría completa de esas dependencias ni un análisis de seguridad de memoria.** La revisión del helper no convierte un AAF desconocido en un archivo seguro.

Los scripts y los plugins de REAPER se ejecutan con los permisos de REAPER, sin un aislamiento adicional aportado por este proyecto. Utiliza software de procedencia verificable y archivos de intercambio de fuentes conocidas. El filtro de cabecera CFB solo evita enviar algunos archivos evidentemente incompatibles al lector; un contenedor válido puede contener datos dañados o maliciosos.

## Comportamiento de las acciones

- No contienen comandos de shell, ejecución de procesos, descarga directa, subida de archivos ni telemetría.
- La preparación exige poder inspeccionar los repositorios antes de modificarlos. Solo reconoce la URL HTTPS oficial de reAAF y su variante equivalente sin `refs/heads`.
- No sustituye una URL distinta con el mismo nombre ni cambia un repositorio ya existente. Si está habilitado, abre el buscador; si está deshabilitado, pide revisarlo manualmente.
- Los repositorios nuevos se agregan con instalación automática desactivada. ReaPack puede procesar otras operaciones que ya estuvieran en su cola: el asistente lo explica y permite cancelar antes de cambiar la configuración.
- La importación lee una cabecera de ocho bytes y consulta el tamaño del archivo sin escribirlo. No repara ni modifica el AAF.
- Rechaza rutas relativas, prefijos de comandos de REAPER y caracteres de control; evita iniciar la importación durante una grabación y abre una pestaña nueva.
- Conserva la última ruta solo en memoria durante la sesión del helper. El resumen habitual utiliza el nombre del archivo. Los errores y las aplicaciones subyacentes pueden mostrar o registrar rutas completas por su cuenta.
- Detectar un archivo llamado reAAF no verifica su firma, integridad, arquitectura ni carga efectiva en REAPER.

ReaPack administra descargas y actualizaciones del motor. Este helper no fija ni verifica criptográficamente el binario que ReaPack instala. Los medios referenciados por un AAF pueden estar en otros discos o rutas de red; su acceso depende de REAPER/reAAF y de tus permisos. No se promete ausencia de actividad de red en las aplicaciones externas.

## Antes de compartir un informe

Revisa y elimina nombres de usuario, rutas de discos, nombres de clientes, URL privadas y cualquier dato de autenticación. No subas audio, vídeo, AAF o proyectos de terceros sin autorización. Usa una reproducción sintética o un fragmento que puedas compartir.

## Reportar un problema de seguridad

Si GitHub ofrece **Security → Report a vulnerability** en este repositorio, usa ese canal privado. Si no está disponible, abre un issue mínimo solicitando un canal de contacto, sin incluir el archivo malicioso, secretos ni instrucciones de explotación. El mantenedor podrá coordinar la comunicación. Los defectos de lectura nativa deben comunicarse también al proyecto upstream correspondiente de forma responsable.

## Versiones

La versión pública inicial es 1.0.0. Los cambios se describen en [CHANGELOG.md](CHANGELOG.md). No hay compromiso de soporte indefinido ni garantía de ausencia de vulnerabilidades. El alcance y los resultados concretos de la revisión están en [docs/SECURITY_REVIEW.md](docs/SECURITY_REVIEW.md).
