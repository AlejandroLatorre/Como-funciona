"""Arranca el addon BlenderMCP en un Blender sin interfaz visible.

El addon rehúsa arrancar con `blender --background` (los comandos nunca se
ejecutarían porque no hay bucle de eventos), así que la forma soportada en un
entorno sin pantalla es un display virtual:

    xvfb-run -a blender --python scripts/arrancar_servidor_headless.py

Blender queda vivo con su bucle de eventos bajo Xvfb, el addon escucha en
localhost:9876 y el servidor MCP (uvx blender-mcp) se conecta ahí.
"""

import importlib.util
import os
import sys

import bpy

_DIR = os.path.dirname(os.path.abspath(__file__))


def _cargar_addon():
    ruta = os.path.join(_DIR, "addon.py")
    spec = importlib.util.spec_from_file_location("blendermcp_addon", ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["blendermcp_addon"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def main():
    addon = _cargar_addon()
    # register() ya autoarranca el servidor en el puerto de la escena (9876
    # por defecto); solo hay que verificar que quedó corriendo.
    addon.register()
    servidor = getattr(bpy.types, "blendermcp_server", None)
    if servidor is None or not servidor.running:
        print("ERROR: el servidor BlenderMCP no arrancó")
        sys.exit(1)
    print(f"BlenderMCP escuchando en localhost:{servidor.port} (PID {os.getpid()})")


main()
