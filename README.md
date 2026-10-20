# REAPER AAF Import Helper

Acciones Lua en español para preparar **reAAF** e importar un AAF de audio en una pestaña nueva de REAPER.

**El lector AAF es [reAAF, de Federico Manuppella](https://github.com/smandrap/reAAF), que utiliza [LibAAF](https://github.com/agfline/LibAAF).** Este proyecto aporta el asistente de preparación, la acción de acceso y documentación. No incluye el motor ni sus binarios y no está afiliado a esos proyectos ni a Cockos.

[English instructions](docs/README.en.md) · [Seguridad](SECURITY.md) · [Revisión de seguridad](docs/SECURITY_REVIEW.md) · [Contribuir](CONTRIBUTING.md)

## Requisitos

| Componente | Para qué sirve |
| --- | --- |
| [REAPER](https://www.reaper.fm/) con Lua | Ejecutar las dos acciones. Probado en REAPER 7.79, macOS Apple Silicon. |
| [ReaPack](https://reapack.com/) con API de repositorios | Agregar y buscar el paquete reAAF desde el asistente. |
| reAAF instalado y cargado | Leer realmente el formato AAF. ReaPack debe ofrecer un binario compatible con tu proceso de REAPER. |
| AAF y sus medios | Un AAF con audio externo necesita también sus WAV u otros medios originales. |
| Internet durante la instalación | Descargar el índice y el motor mediante ReaPack. |

**No necesitas Python, pip, SWS ni ReaImGui para utilizar estas acciones.** Python aparece solo en las pruebas de desarrollo opcionales.

El motor probado fue reAAF 0.3.7. Su índice ofrece variantes para macOS Apple Silicon/Intel, Windows x64 y Linux x64; este helper solo se ha probado dentro de REAPER en macOS Apple Silicon. Una variante disponible no implica una prueba funcional en esa plataforma. Comprueba la arquitectura del proceso de REAPER, especialmente si utilizas Rosetta.

## Instalación desde cero

### 1. Instalar ReaPack

1. Descarga ReaPack desde su [sitio oficial](https://reapack.com/), con la arquitectura que corresponda a REAPER.
2. En REAPER abre **Options → Show REAPER resource path in explorer/finder**.
3. Coloca el archivo de extensión de ReaPack en la subcarpeta **UserPlugins** de esa carpeta de recursos; créala si no existe.
4. Reinicia REAPER. Debe aparecer **Extensions → ReaPack**.

Si ya tienes ReaPack, continúa con el siguiente paso. No necesitas volver a instalarlo.

### 2. Cargar estas acciones

1. En GitHub selecciona **Code → Download ZIP** y descomprime el archivo.
2. Copia los dos archivos de `scripts/` a una carpeta permanente, por ejemplo **Scripts/AAF Import Helper** dentro de la carpeta de recursos de REAPER.
3. Abre **Actions → Show action list** y selecciona la sección **Main**.
4. Usa **New action → Load ReaScript** y carga ambos archivos:
   - `01_Preparar_importacion_AAF.lua`
   - `02_Importar_AAF.lua`

No cambies de ubicación los scripts después de registrarlos; si los mueves, vuelve a cargarlos desde su nueva ruta.

### 3. Instalar el motor reAAF

1. Ejecuta **01_Preparar_importacion_AAF.lua** desde la lista de acciones.
2. Si el repositorio es nuevo, el asistente explica el cambio antes de agregarlo, con instalación automática desactivada. **Revisa primero las operaciones pendientes de ReaPack**: su API procesa una cola global y puede ejecutar otras operaciones que ya estuvieran pendientes.
3. En el buscador selecciona **reAAF**, abre **Actions → Install** y pulsa **Apply**. También puede estar disponible mediante clic derecho sobre el paquete.
4. Revisa el resultado de instalación. Si no aparece el paquete, abre **Extensions → ReaPack → Manage repositories**, selecciona reAAF y sincronízalo.
5. Guarda tus proyectos y **reinicia REAPER**. Una extensión descargada todavía no está cargada en el proceso que sigue abierto.

El asistente conserva los repositorios existentes. Si encuentra el mismo nombre con otra URL o encuentra el repositorio deshabilitado, se detiene y explica cómo revisarlo manualmente.

### Alternativa: instalar el motor manualmente con ReaPack

En **Extensions → ReaPack → Import repositories**, importa esta dirección oficial:

```text
https://raw.githubusercontent.com/smandrap/reAAF/refs/heads/main/index.xml
```

Busca e instala reAAF como se indica arriba. También puedes seguir las instrucciones del [autor de reAAF](https://github.com/smandrap/reAAF). Una vez instalado, la acción 02 funciona sin ejecutar la acción 01.

## Importar un AAF

1. Conserva el AAF y los medios asociados en una ubicación estable. Detén cualquier grabación.
2. Ejecuta **02_Importar_AAF.lua** y selecciona el `.aaf`.
3. La acción comprueba la extensión y una cabecera básica del contenedor antes de abrir una pestaña nueva. Esa comprobación **no demuestra que un AAF sea seguro o esté completo**.
4. Espera a que REAPER cargue el proyecto y cree las formas de onda. Revisa los mensajes de reAAF, los clips y los medios.
5. Compara varios cortes con una referencia de la edición original y guarda como un nuevo proyecto `.rpp`.
6. Para trasladar el proyecto, usa **Save project as → Copy all media into project directory**. Mientras no copies los medios, REAPER seguirá necesitando sus ubicaciones originales o el disco externo.

Puedes asignar un atajo a la acción 02. Con reAAF instalado también puedes abrir el AAF mediante **File → Open** o arrastrarlo a REAPER sin estas acciones.

## Alcance y problemas habituales

- El objetivo es recuperar pistas y clips de audio con sus tiempos. No exporta AAF ni promete importar vídeo, plugins, ruteo o toda la mezcla.
- Algunos canales se separan en pistas individuales. Revisa mono/estéreo, paneos, ganancia, automatización y fundidos contra una referencia. Consulta las [notas del motor](https://github.com/smandrap/reAAF/blob/main/docs/aaf-format-support.md).
- **Motor ausente:** instala reAAF y reinicia REAPER. Detectar su archivo en UserPlugins no verifica que esté cargado ni comprueba su integridad.
- **Faltan funciones de ReaPack:** actualiza ReaPack desde su sitio oficial o utiliza la alternativa manual.
- **Error de sincronización:** comprueba qué repositorio falló. Un error de otro repositorio no significa necesariamente que reAAF haya fallado.
- **AAF rechazado:** podría estar vacío, truncado o usar un contenedor incompatible. Vuelve a exportarlo; no basta con renombrar otro archivo como `.aaf`.
- **Medios offline:** conserva la carpeta de audio exportada, conecta los discos y revisa las rutas en el registro del motor. El helper no convierte medios ni repara rutas por sí mismo.
- **macOS bloquea un binario:** verifica su procedencia y consulta las instrucciones del proveedor. Estos scripts no eliminan cuarentenas ni desactivan protecciones.

## Privacidad y seguridad

Las acciones no envían tus AAF ni tu audio a un servicio. No ejecutan comandos de shell ni incluyen descargadores o binarios. La preparación delega en ReaPack la descarga desde el repositorio oficial; el motor conserva sus propios permisos y comportamiento, incluida la resolución de medios externos.

La acción de importación recuerda la última ruta solo durante la sesión de REAPER y usa el nombre del archivo en su resumen habitual. REAPER, reAAF, el selector de archivos o los mensajes de error pueden guardar o mostrar sus propias rutas. Revísalas antes de compartir registros. Consulta [SECURITY.md](SECURITY.md) para conocer el alcance de la revisión y sus límites.

## Pruebas y desarrollo

Las acciones se probaron dentro de REAPER 7.79 en macOS Apple Silicon con un AAF sintético y un AAF de audio real. La prueba real recuperó 107 clips, incluidos 13 silenciados, y coincidió en tiempos, recortes y referencias de medios después de considerar la separación de canales. **El AAF real, sus nombres, rutas, registros y audio no se distribuyen.** Esto no certifica otros exportadores ni la fidelidad de toda la mezcla. El endurecimiento posterior a esa prueba se verifica también con pruebas simuladas; consulta [el informe](docs/SECURITY_REVIEW.md).

Para ejecutar las pruebas automatizadas de las acciones:

```sh
python3 -m venv .venv
# macOS/Linux:
. .venv/bin/activate
# Windows PowerShell, en lugar de la línea anterior:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python tests/test_scripts.py
python tests/check_release.py
```

Las pruebas utilizan una API simulada. No cargan el lector nativo ni demuestran seguridad de memoria en reAAF/LibAAF.

## Desinstalar

Retira las acciones de tu lista de REAPER y elimina los dos archivos Lua si ya no los necesitas. Para retirar el motor, desinstala reAAF desde ReaPack, aplica el cambio y reinicia REAPER. Quitar estos helpers no elimina los proyectos importados ni sus medios.

## Licencia y créditos

Los archivos originales de este repositorio se publican bajo [MIT](LICENSE). reAAF y LibAAF son proyectos externos con sus propias licencias; no se redistribuyen aquí. El trabajo de lectura AAF corresponde a sus autores. También se utiliza la [API ReaScript de Cockos](https://www.reaper.fm/sdk/reascript/reascripthelp.html).

Mantenimiento de este helper: [Martin Aguirre](https://github.com/imdexuss).
