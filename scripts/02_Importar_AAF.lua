-- @description Importar AAF en una pestana nueva (requiere reAAF)
-- @version 1.0.0
-- @author Martin Aguirre
-- SPDX-License-Identifier: MIT
-- Accion Lua de acceso al importador nativo reAAF. No es un lector AAF independiente.
-- Motor: https://github.com/smandrap/reAAF (Federico Manuppella; GPLv3+).

local r = reaper
local title = "Importar AAF"
local state = "REAPER_AAF_Import_Helper"

local function message(text)
  r.ShowMessageBox(text, title, 0)
end

local function engine_on_disk()
  local folder = r.GetResourcePath() .. "/UserPlugins"
  local i = 0
  while true do
    local name = r.EnumerateFiles(folder, i)
    if not name then return false end
    name = name:lower()
    if name:match("^reaper_reaaf.*%.dylib$") or
       name:match("^reaper_reaaf.*%.dll$") or
       name:match("^reaper_reaaf.*%.so$") then return true end
    i = i + 1
  end
end

local function main()
  local play_state = r.APIExists("GetAllProjectPlayStates") and r.GetAllProjectPlayStates(nil) or r.GetPlayState()
  if play_state & 4 ~= 0 then
    message("Detén la grabación antes de importar un AAF.")
    return
  end
  if not engine_on_disk() then
    message("No encontré reAAF en UserPlugins.\n\n" ..
      "Ejecuta primero 01_Preparar_importacion_AAF.lua, instala reAAF y reinicia REAPER.\n\n" ..
      "Este script necesita ese motor para leer archivos AAF.")
    return
  end

  local initial = r.GetExtState(state, "ultimo_aaf")
  local selected, path
  if r.APIExists("GetUserFileName") then
    selected, path = r.GetUserFileName(1, "Selecciona el AAF para importar", initial,
      "AAF|*.aaf;*.AAF|Todos los archivos|*.*")
  else
    selected, path = r.GetUserFileNameForRead(initial, "Selecciona el AAF para importar", "aaf")
  end
  if not selected or not path or path == "" then return end
  local absolute = path:sub(1, 1) == "/" or path:match("^%a:[/\\]") or path:sub(1, 2) == "\\\\"
  if not absolute or path:find("[%z\1-\31\127]") then
    message("Selecciona una ruta absoluta de archivo sin caracteres de control.")
    return
  end
  if not path:lower():match("%.aaf$") then
    message("Selecciona un archivo con extensión .aaf.")
    return
  end

  local file, err = io.open(path, "rb")
  if not file then
    message("No puedo leer el AAF:\n" .. path .. "\n\n" .. tostring(err))
    return
  end
  local header = file:read(8)
  local size = file:seek("end")
  file:close()
  -- Comprobación superficial CFB; no valida el contenido AAF ni lo aísla.
  if header ~= "\208\207\17\224\161\177\26\225" or not size or size < 512 then
    message("El archivo no tiene una cabecera CFB válida o está truncado.\n\n" ..
      "No se abrirá con el lector nativo. Exporta otra vez un AAF compatible.")
    return
  end

  -- 40859: New project tab. No se cierra ni guarda el proyecto original.
  local original = r.EnumProjects(-1, "")
  r.Main_OnCommand(40859, 0)
  local destination = r.EnumProjects(-1, "")
  if not destination or destination == original then
    message("REAPER no abrió una pestaña nueva. La importación se ha detenido.")
    return
  end

  -- reAAF registra el formato mediante projectimport; REAPER elige el lector.
  -- No usar noprompt: ni envolver la carga de proyectos en un bloque Undo.
  r.Main_openProject(path)
  -- La carga puede sustituir el identificador de la pestaña vacía.
  local imported = r.EnumProjects(-1, "")
  -- Solo memoria de esta sesión; no se escribe la ruta en reaper-extstate.ini.
  r.SetExtState(state, "ultimo_aaf", path, false)

  local function report()
    if not imported or r.EnumProjects(-1, "") ~= imported then return end
    local tracks = r.CountTracks(imported)
    local items = r.CountMediaItems(imported)
    r.ShowConsoleMsg(("\n[Importar AAF] %s\nPistas en la pestaña: %d. Ítems: %d.\n" ..
      "Revisa el registro de reAAF y comprueba la sincronía y los medios antes de guardar.\n")
      :format(path:match("[^/\\]+$") or "AAF", tracks, items))
    if tracks == 0 and items == 0 then
      message("La pestaña sigue sin pistas ni ítems. No se puede confirmar la importación.\n\n" ..
        "Revisa el registro de reAAF. Si acabas de instalarlo, reinicia REAPER.\n" ..
        "Detectar el archivo de la extensión en disco no garantiza que REAPER la haya cargado.")
    end
  end
  r.defer(function()
    local ok, err = xpcall(report, debug.traceback)
    if not ok then message("No se pudo generar el informe:\n" .. tostring(err)) end
  end)
end

local ok, err = xpcall(main, debug.traceback)
if not ok then
  message("La importación se ha detenido:\n" .. tostring(err) ..
    "\n\nSi quedó una pestaña nueva, revísala antes de cerrarla.")
end
