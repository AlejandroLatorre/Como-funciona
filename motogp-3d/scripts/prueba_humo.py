"""Prueba de humo del pipeline: discos de embrague en vista explosionada.

Crea 6 cilindros finos apilados (discos de embrague) alternando acero pulido
y carbono oscuro, los separa en vista explosionada sobre el eje Z, añade una
cámara turntable de 360 grados en 120 frames y luces de estudio, y renderiza
un frame de prueba en baja resolución.

Ejecución headless:
    blender --background --python scripts/prueba_humo.py

También puede enviarse por trozos vía MCP (blender-mcp, execute_blender_code).
"""

import os
import sys

import bpy

# Permitir importar los scripts hermanos tanto en headless como vía MCP
_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() \
    else os.path.join(os.getcwd(), "motogp-3d", "scripts")
if _DIR not in sys.path:
    sys.path.append(_DIR)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import acero_pulido, asignar, carbono_oscuro
from turntable import crear_turntable
from vista_explosionada import explosionar

NUM_DISCOS = 6
RADIO_DISCO = 1.0
GROSOR_DISCO = 0.06
SALIDA = os.path.join(_DIR, "..", "renders", "test", "prueba_humo_frame60.png")


def crear_discos():
    discos = []
    materiales = [acero_pulido(), carbono_oscuro()]
    for i in range(NUM_DISCOS):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=RADIO_DISCO,
            depth=GROSOR_DISCO,
            location=(0.0, 0.0, i * GROSOR_DISCO * 1.5),
        )
        disco = bpy.context.active_object
        disco.name = f"Disco_{i + 1:02d}_{'acero' if i % 2 == 0 else 'carbono'}"
        # Suavizar solo la pared lateral, manteniendo aristas nítidas en las
        # caras planas (sin esto, el disco entero se ve inflado como almohada).
        # La API cambió en 4.1: use_auto_smooth desapareció en favor de
        # shade_auto_smooth(); soportamos ambas para cualquier Blender 4.x.
        if hasattr(disco.data, "use_auto_smooth"):
            bpy.ops.object.shade_smooth()
            disco.data.use_auto_smooth = True
        else:
            bpy.ops.object.shade_auto_smooth()
        asignar(disco, materiales[i % 2])
        discos.append(disco)
    return discos


def limpiar_escena():
    """Borra todos los objetos de la escena actual.

    No usamos read_factory_settings porque ejecutado vía MCP reiniciaría
    Blender y tumbaría el servidor del addon.
    """
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def construir_escena():
    limpiar_escena()
    discos = crear_discos()
    explosionar(discos, eje="Z", separacion=0.35)
    # La pila explosionada va de z=-0.9 a z=+1.3 (centro ~0.2): radio 6 y
    # cámara ligeramente elevada encuadran todo sin cortar los extremos
    crear_turntable(objetivo=(0.0, 0.0, 0.2), radio=6.0, altura=1.8, frames=120)
    luces_estudio()
    configurar_render(resolucion=(640, 360), samples=32, motor="CYCLES",
                      salida=os.path.abspath(SALIDA))
    return discos


def renderizar(frame=60):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    print(f"Render de prueba escrito en: {os.path.abspath(SALIDA)}")


def main():
    construir_escena()
    renderizar()


if __name__ == "__main__":
    main()
