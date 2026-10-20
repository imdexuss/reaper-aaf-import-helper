# REAPER AAF Import Helper

Two Spanish-language Lua actions that help install **[reAAF](https://github.com/smandrap/reAAF)** and open an audio AAF in a new REAPER project tab. The AAF reader is reAAF, by Federico Manuppella, using [LibAAF](https://github.com/agfline/LibAAF). This independent helper does not include their source or binaries.

## Requirements

- REAPER with built-in Lua. Tested inside REAPER 7.79 on macOS Apple Silicon.
- [ReaPack](https://reapack.com/) with the repository inspection API, for the setup helper.
- A compatible, installed reAAF extension; tested engine version: 0.3.7.
- Your AAF and the audio files it references. Keep external drives connected.
- Internet access for installation through ReaPack.

Python, pip, SWS and ReaImGui are not required to use the actions. Upstream provides other platform binaries, but this helper has not been tested inside REAPER on Windows, Linux or Intel Macs.

## Installation

1. Install ReaPack from its official website. Use **Options → Show REAPER resource path in explorer/finder**, place its compatible extension file in **UserPlugins**, and restart REAPER.
2. Download this repository with **Code → Download ZIP** and unzip it. Copy both files from `scripts/` into a permanent folder under REAPER's **Scripts** resource folder.
3. In **Actions → Show action list**, select **Main** and use **New action → Load ReaScript** to load both Lua files.
4. Run **01_Preparar_importacion_AAF.lua**. Before adding a new repository, it explains that processing ReaPack's queue can execute other pending operations. Review or cancel those operations first. It adds the official repository with automatic installation disabled.
5. Select **reAAF** in the package browser, choose **Actions → Install**, then **Apply**. Review the result and restart REAPER.

To set up manually, use **Extensions → ReaPack → Import repositories** with:

```text
https://raw.githubusercontent.com/smandrap/reAAF/refs/heads/main/index.xml
```

Then browse and install reAAF as above. Once the engine is installed, action 02 works without running action 01.

## Usage

Stop recording, then run **02_Importar_AAF.lua** and choose the AAF. It checks the extension and a superficial CFB container header before opening a new tab. This does not validate the complete AAF or make an unknown file safe.

Wait for import and peak building. Review reAAF's logs, media availability, channel layout, cuts, levels and fades against an editing reference. Save a separate `.rpp`. To make it portable, use **Save project as → Copy all media into project directory**.

With reAAF loaded, **File → Open** and drag-and-drop also work without this helper. The scripts do not export AAF, convert media, repair missing paths or transfer plugins/routing. Stereo or multichannel material may appear as separate tracks.

## Troubleshooting and removal

If the engine is missing, install it and restart REAPER. A matching plugin filename is only an installation hint; it does not prove the binary is loaded, compatible or authentic. If repository inspection functions are missing, update ReaPack or follow manual setup. A repository with a different URL or a disabled repository is left unchanged.

Keep exported audio alongside its AAF and reconnect external drives if files are offline. Do not disable operating-system protections globally to install an extension.

Remove the actions and Lua files to uninstall the helper. Remove reAAF separately through ReaPack and restart REAPER if you also want to uninstall the engine. Imported projects and media are not deleted.

## Security, testing and license

See [SECURITY.md](../SECURITY.md) and [the review](SECURITY_REVIEW.md). The wrapper has no shell execution, uploads or telemetry. ReaPack and the native engine have their own behavior and permissions. Ordinary summaries show only the basename; the last selected path is kept for the helper's current session only. External logs may still contain private paths.

The development tests use Python and a simulated REAPER API. Install `requirements-dev.txt` in a virtual environment, then run `python tests/test_scripts.py` and `python tests/check_release.py` from the repository root. They do not audit the native parser. Earlier functional imports succeeded on the tested macOS setup; the later hardening changes are covered by simulated tests.

Original helper files are [MIT licensed](../LICENSE). reAAF/LibAAF remain separate projects with their own licenses. Maintained by [Martin Aguirre](https://github.com/imdexuss).
