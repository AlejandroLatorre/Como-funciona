"""Escena gancho: el embrague completo montado girando en turntable 360.

Reutiliza los constructores de piezas de generar_escena_3a pero sin
explosion: conjunto compacto, orbita completa en 120 frames.
"""

import math
import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
ESCENAS = "/home/user/Como-funciona/motogp-3d/escenas/embrague-antirrebote"
for ruta in (SCRIPTS, ESCENAS):
    if ruta not in sys.path:
        sys.path.append(ruta)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import acero_pulido, aluminio_anodizado, asignar, carbono_oscuro, titanio
from turntable import crear_turntable

import generar_escena_3a as e3a

BASE = "/home/user/Como-funciona/motogp-3d"
SALIDA_RENDER = os.path.join(BASE, "renders", "embrague-antirrebote",
                             "gancho", "preview_frame1.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "embrague-antirrebote",
                            "escena-gancho-v1.blend")


def construir():
    e3a.limpiar_escena()

    e3a.campana("Campana", 0.0)
    z = 0.05
    for i in range(8):
        if i % 2 == 0:
            e3a.cilindro(f"Disco_friccion_{i//2 + 1}", 1.15, 0.06, z, carbono_oscuro())
        else:
            e3a.cilindro(f"Disco_acero_{i//2 + 1}", 1.10, 0.04, z, acero_pulido())
        z += 0.075

    e3a.cilindro("Cubo_inferior", 0.62, 0.22, z + 0.06, acero_pulido())
    for k in range(3):
        ang = k * math.tau / 3
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.07,
            location=(0.42 * math.cos(ang), 0.42 * math.sin(ang), z + 0.22),
            segments=24, ring_count=12)
        bola = bpy.context.active_object
        bola.name = f"Bola_{k + 1}"
        bpy.ops.object.shade_smooth()
        asignar(bola, titanio())
    e3a.cilindro("Cubo_superior", 0.62, 0.22, z + 0.38, acero_pulido())
    e3a.cilindro("Plato_presion", 1.15, 0.08, z + 0.60, aluminio_anodizado())
    for k in range(4):
        ang = k * math.tau / 4 + math.tau / 8
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.09, depth=0.28,
            location=(0.85 * math.cos(ang), 0.85 * math.sin(ang), z + 0.82),
            vertices=24)
        muelle = bpy.context.active_object
        muelle.name = f"Muelle_{k + 1}"
        asignar(muelle, titanio())

    crear_turntable(objetivo=(0.0, 0.0, 0.8), radio=5.0, altura=1.9,
                    frames=120, nombre="OrbitaGancho")
    luces_estudio(700)

    os.makedirs(os.path.dirname(SALIDA_RENDER), exist_ok=True)
    configurar_render(resolucion=(640, 360), samples=24, motor="CYCLES",
                      salida=SALIDA_RENDER)
    os.makedirs(os.path.dirname(SALIDA_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=SALIDA_BLEND)
    return len(bpy.data.objects)


def renderizar(frame=1):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    print(f"Gancho construido ({construir()} objetos)")
    renderizar()
