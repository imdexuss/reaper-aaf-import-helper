from pathlib import Path
import sys
import tempfile
from lupa.lua54 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'scripts'

MOCK = r'''
calls = {messages={}, commands={}, opens={}, logs={}, sets={}, repos={}, browses={}}
cfg = {engine=true, selected=true, modern=true, newtab=true, tracks=2, items=3,
       repository=false, repository_ok=true, repository_enabled=true,
       auto_install=2, missing_api='', confirmation=1, play_state=0}
active = 'original'
reaper = {
  ShowMessageBox=function(text, title, kind)
    table.insert(calls.messages, text)
    if kind==1 then return cfg.confirmation end
    return 1
  end,
  GetAllProjectPlayStates=function(ignore) assert(ignore==nil); return cfg.play_state end,
  GetPlayState=function() return cfg.play_state end,
  GetResourcePath=function() return '/mock' end,
  EnumerateFiles=function(folder, index)
    assert(folder=='/mock/UserPlugins')
    if index==0 then return 'reaper_sws-arm64.dylib' end
    if index==1 and cfg.engine then return 'reaper_reAAF-arm64.dylib' end
    return nil
  end,
  APIExists=function(name)
    if name==cfg.missing_api then return false end
    if name=='GetUserFileName' then return cfg.modern end
    return true
  end,
  GetExtState=function() return '' end,
  GetUserFileName=function(mode, title, initial, extensions)
    assert(mode==1); return cfg.selected, cfg.path
  end,
  GetUserFileNameForRead=function(initial, title, ext)
    assert(ext=='aaf'); return cfg.selected, cfg.path
  end,
  EnumProjects=function(index, buf) assert(index==-1); return active, '' end,
  Main_OnCommand=function(command, flag)
    assert(command==40859 and flag==0)
    table.insert(calls.commands, command)
    if cfg.newtab then active='destination' end
  end,
  Main_openProject=function(path)
    assert(active=='destination', 'Opening into original project!')
    if cfg.open_error then error('simulated import exception') end
    table.insert(calls.opens, path)
    if cfg.replace_on_open then active='loaded-destination' end
  end,
  SetExtState=function(section, key, value, persist)
    assert(persist==false); table.insert(calls.sets, value)
  end,
  defer=function(callback)
    if cfg.switch_before_report then active='original' end
    callback()
  end,
  CountTracks=function(proj)
    assert(proj==active)
    if cfg.report_error then error('simulated report error') end
    return cfg.tracks
  end,
  CountMediaItems=function(proj) assert(proj==active); return cfg.items end,
  ShowConsoleMsg=function(text) table.insert(calls.logs, text) end,
  ReaPack_GetRepositoryInfo=function(name)
    assert(name=='reAAF'); return cfg.repository, cfg.repository_url, cfg.repository_enabled, cfg.auto_install
  end,
  ReaPack_AddSetRepository=function(name, url, enabled, auto)
    table.insert(calls.repos, {name=name,url=url,enabled=enabled,auto=auto})
    return cfg.repository_ok, 'simulated repository error'
  end,
  ReaPack_ProcessQueue=function(refresh) assert(refresh==true); calls.processed=true end,
  ReaPack_BrowsePackages=function(filter) table.insert(calls.browses, filter) end
}
'''

count = 0
def run(name, script, setup, assertion):
    global count
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(MOCK)
    for k, v in setup.items():
        lua.globals().cfg[k] = v
    lua.execute((PACKAGE / script).read_text())
    lua.execute(assertion)
    count += 1
    print('PASS', name)

IMPORT = '02_Importar_AAF.lua'
INSTALL = '01_Preparar_importacion_AAF.lua'
with tempfile.TemporaryDirectory(prefix='aaf-test-', dir=None) as directory:
    directory = Path(directory)
    sample = directory / 'Diálogo edición.AAF'
    sample.write_bytes(bytes.fromhex('d0cf11e0a1b11ae1') + bytes(504))
    empty = directory / 'empty.aaf'
    empty.touch()
    invalid = directory / 'not_a_container.aaf'
    invalid.write_bytes(b'not an AAF' + bytes(1024))
    truncated = directory / 'short.aaf'
    truncated.write_bytes(bytes.fromhex('d0cf11e0a1b11ae1'))
    base = {'path': str(sample)}
    def case(name, extras, assertion):
        run(name, IMPORT, base | extras, assertion)
    case('preserva proyecto y ruta Unicode; abre nueva pestaña', {},
         "assert(active=='destination' and #calls.commands==1 and #calls.opens==1); assert(calls.opens[1]==cfg.path); assert(#calls.logs==1)")
    case('cancelar no crea pestaña', {'selected': False},
         'assert(#calls.commands==0 and #calls.opens==0 and #calls.messages==0)')
    case('motor ausente no altera proyecto', {'engine': False},
         'assert(active==\'original\' and #calls.commands==0 and #calls.messages==1)')
    case('rechaza extensión incorrecta', {'path': str(sample.with_suffix('.rpp'))},
         'assert(#calls.commands==0 and #calls.messages==1)')
    case('ruta ausente no crea pestaña', {'path': str(directory / 'missing.aaf')},
         'assert(#calls.commands==0 and #calls.messages==1)')
    case('archivo vacío no crea pestaña', {'path': str(empty)},
         'assert(#calls.commands==0 and #calls.messages==1)')
    case('si falla nueva pestaña no reemplaza original', {'newtab': False},
         'assert(active==\'original\' and #calls.opens==0 and #calls.messages==1)')
    case('lector lanza error: lo comunica', {'open_error': True},
         "assert(#calls.opens==0 and #calls.messages==1 and calls.messages[1]:find('simulated import exception',1,true))")
    case('importación vacía no se anuncia como éxito', {'tracks': 0, 'items': 0},
         "assert(#calls.messages==1 and calls.messages[1]:find('No se puede confirmar',1,true))")
    case('REAPER con selector antiguo', {'modern': False},
         'assert(#calls.opens==1)')
    case('informe después de sustituir identificador de proyecto', {'replace_on_open': True},
         "assert(active=='loaded-destination' and #calls.logs==1 and #calls.messages==0)")
    case('rechaza un texto renombrado como AAF', {'path': str(invalid)},
         'assert(#calls.opens==0 and #calls.commands==0 and #calls.messages==1)')
    case('rechaza una cabecera truncada', {'path': str(truncated)},
         'assert(#calls.opens==0 and #calls.commands==0 and #calls.messages==1)')
    case('rechaza prefijos de comandos de REAPER', {'path': 'noprompt:/tmp/example.aaf'},
         'assert(#calls.opens==0 and #calls.commands==0)')
    case('rechaza una URL como ruta', {'path': 'https://example.com/example.aaf'},
         'assert(#calls.opens==0 and #calls.commands==0)')
    case('rechaza caracteres de control', {'path': str(directory / 'bad\nname.aaf')},
         'assert(#calls.opens==0 and #calls.commands==0)')
    case('no abre proyectos durante grabación', {'play_state': 5},
         'assert(active==\'original\' and #calls.commands==0 and #calls.messages==1)')
    case('informe diferido también maneja errores', {'report_error': True},
         "assert(#calls.messages==1 and calls.messages[1]:find('simulated report error',1,true))")
    case('no informa sobre una pestaña cambiada', {'switch_before_report': True},
         'assert(#calls.logs==0 and #calls.messages==0)')
    case('consola no revela la ruta completa', {},
         "assert(#calls.logs==1 and not calls.logs[1]:find(cfg.path,1,true))")

run('prepara repositorio sin auto instalar', INSTALL, {},
    'assert(#calls.repos==1 and calls.repos[1].auto==0 and calls.processed and calls.browses[1]==\'reAAF\')')
run('falta ReaPack: sin cambios', INSTALL, {'missing_api': 'ReaPack_AddSetRepository'},
    'assert(#calls.repos==0 and #calls.messages==1)')
run('error de repositorio: no continúa', INSTALL, {'repository_ok': False},
    "assert(not calls.processed and #calls.browses==0 and #calls.messages==2 and calls.messages[2]:find('simulated repository error',1,true))")
run('fuente diferente: no sobrescribe repositorio', INSTALL,
    {'repository': True, 'repository_url': 'https://example.com/other.xml'},
    'assert(#calls.repos==0 and not calls.processed and #calls.messages==1)')
run('repositorio existente no procesa otras operaciones pendientes', INSTALL,
    {'repository': True, 'repository_url': 'https://raw.githubusercontent.com/smandrap/reAAF/main/index.xml', 'auto_install': 2},
    'assert(#calls.repos==0 and not calls.processed and calls.browses[1]==\'reAAF\')')
run('sin API de inspección no cambia repositorios', INSTALL, {'missing_api': 'ReaPack_GetRepositoryInfo'},
    'assert(#calls.repos==0 and not calls.processed and #calls.messages==1)')
run('cancelar preparación no realiza cambios', INSTALL, {'confirmation': 2},
    'assert(#calls.repos==0 and not calls.processed and #calls.browses==0)')
run('repositorio deshabilitado conserva configuración', INSTALL,
    {'repository': True, 'repository_url': 'https://raw.githubusercontent.com/smandrap/reAAF/refs/heads/main/index.xml', 'repository_enabled': False},
    'assert(#calls.repos==0 and not calls.processed and #calls.browses==0)')
print(f'{count} comprobaciones superadas. API simulada; sin validar importación nativa.')
