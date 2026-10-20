-- @description Preparar importacion AAF mediante reAAF y ReaPack
-- @version 1.0.0
-- @author Martin Aguirre
-- SPDX-License-Identifier: MIT
-- Helper independiente. Motor: https://github.com/smandrap/reAAF (GPLv3+).

local r = reaper
local title = "Preparar importación AAF"
local url = "https://raw.githubusercontent.com/smandrap/reAAF/refs/heads/main/index.xml"

local function message(text, kind)
  return r.ShowMessageBox(text, title, kind or 0)
end

local function instructions()
  message("En el buscador de ReaPack:\n\n" ..
    "1. Busca reAAF.\n2. Selecciona el paquete y abre Actions → Install.\n" ..
    "3. Pulsa Apply y revisa el resultado.\n4. Reinicia REAPER.\n\n" ..
    "Después ejecuta 02_Importar_AAF.lua.\n" ..
    "Si el paquete no aparece, sincroniza su repositorio desde Manage repositories.\n\n" ..
    "Abrir el buscador no confirma que el motor esté instalado ni cargado.")
  r.ReaPack_BrowsePackages("reAAF")
end

local function main()
  for _, name in ipairs({"ReaPack_GetRepositoryInfo", "ReaPack_AddSetRepository",
                         "ReaPack_ProcessQueue", "ReaPack_BrowsePackages"}) do
    if not r.APIExists(name) then
      message("Necesitas una versión de ReaPack con su API de repositorios.\n\n" ..
        "Instálala o actualízala desde https://reapack.com y reinicia REAPER.\n\n" ..
        "También puedes instalar reAAF manualmente desde https://github.com/smandrap/reAAF")
      return
    end
  end

  local exists, existing_url, enabled = r.ReaPack_GetRepositoryInfo("reAAF")
  if exists then
    if existing_url ~= url and existing_url ~= "https://raw.githubusercontent.com/smandrap/reAAF/main/index.xml" then
      message("Ya existe un repositorio llamado reAAF con otra dirección. No se modificó.\n\n" ..
        "Revisa Extensions → ReaPack → Manage repositories.\nDirección oficial:\n" .. url)
      return
    end
    if not enabled then
      message("El repositorio oficial reAAF está deshabilitado. No se cambió su configuración.\n\n" ..
        "Habilítalo desde Extensions → ReaPack → Manage repositories y ejecuta esta acción otra vez.")
      return
    end
    instructions()
    return
  end

  if message("Se agregará únicamente el repositorio oficial reAAF con instalación automática desactivada.\n\n" ..
    "ReaPack necesita procesar su cola para guardar el cambio. Eso también puede ejecutar otras " ..
    "operaciones que tengas pendientes en ReaPack. Revísalas o cancélalas antes de continuar.\n\n" ..
    "Pulsa OK para agregar el repositorio o Cancel para salir sin cambios.", 1) ~= 1 then return end

  local ok, err = r.ReaPack_AddSetRepository("reAAF", url, true, 0)
  if not ok then
    message("ReaPack no pudo agregar el repositorio:\n" .. tostring(err))
    return
  end
  r.ReaPack_ProcessQueue(true)
  instructions()
end

local ok, err = xpcall(main, debug.traceback)
if not ok then message("No se pudo completar la preparación:\n" .. tostring(err)) end
