"""Escena 4A: comparativa de angulos de rampa (35 vs 45 grados).

Dos conjuntos rampa+bola lado a lado, mismo estilo que la escena 3B pero con
el perfil parametrizado por angulo. La animacion cuenta la idea del guion:
la rampa suave (35) se abre antes y mas; la pronunciada (45) aguanta mas par
y se abre despues y menos.
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
from materiales_metalicos import acero_pulido, aluminio_anodizado, asignar, titanio

from generar_escena_3b import animar, prisma

BASE = "/home/user/Como-funciona/motogp-3d"
SALIDA_RENDER = os.path.join(BASE, "renders", "embrague-antirrebote",
                             "escena-4a", "preview_frame70.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "embrague-antirrebote",
                            "escena-4a-v1.blend")

RADIO_BOLA = 0.33


def perfil_inferior(angulo_grados, profundidad=0.3):
    """Perfil XZ del bloque inferior con la rampa al angulo pedido."""
    dx_rampa = profundidad / math.tan(math.radians(angulo_grados))
    x_pie = -0.52            # pie de la rampa (borde del pocket)
    x_cima = x_pie - dx_rampa
    return [
        (-1.5, 0.0), (1.5, 0.0), (1.5, 0.5), (0.15, 0.5),
        (0.10, 0.2), (x_pie, 0.2), (x_cima, 0.5), (-1.5, 0.5),
    ]


def conjunto(nombre, angulo, desfase_x, retardo, desliza, eleva):
    """Crea un conjunto rampa+bola centrado en desfase_x y anima su apertura."""
    perfil = perfil_inferior(angulo)
    perfil_sup = [(-x, 1.06 - z) for x, z in perfil]

    inferior = prisma(f"{nombre}_inferior", perfil)
    superior = prisma(f"{nombre}_superior", perfil_sup)
    inferior.location.x += desfase_x
    superior.location.x += desfase_x
    asignar(inferior, acero_pulido())
    asignar(superior, aluminio_anodizado())

    bpy.ops.mesh.primitive_uv_sphere_add(radius=RADIO_BOLA,
                                         location=(desfase_x, 0, 0.53),
                                         segments=48, ring_count=24)
    bola = bpy.context.active_object
    bola.name = f"{nombre}_bola"
    bpy.ops.object.shade_smooth()
    asignar(bola, titanio())

    inicio = 30 + retardo
    animar(superior, [
        (1, (0, 0, 0)), (inicio, (0, 0, 0)),
        (80, (desliza, 0, eleva)), (120, (0, 0, 0)),
    ])
    animar(bola, [
        (1, (0, 0, 0)), (inicio, (0, 0, 0)),
        (80, (desliza / 2, 0, eleva / 2)), (120, (0, 0, 0)),
    ])


def construir():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    # Rampa suave: se abre pronto y mucho. Rampa pronunciada: tarda y abre menos.
    conjunto("Rampa35", 35, -2.2, retardo=0, desliza=0.45, eleva=0.31)
    conjunto("Rampa45", 45, 2.2, retardo=15, desliza=0.28, eleva=0.28)

    objetivo = bpy.data.objects.new("Objetivo_camara", None)
    objetivo.location = (0.0, 0.0, 0.55)
    bpy.context.scene.collection.objects.link(objetivo)

    cam_data = bpy.data.cameras.new("Camara_4A")
    camara = bpy.data.objects.new("Camara_4A", cam_data)
    camara.location = (0.0, -7.5, 2.6)
    bpy.context.scene.collection.objects.link(camara)
    restr = camara.constraints.new("TRACK_TO")
    restr.target = objetivo
    restr.track_axis = "TRACK_NEGATIVE_Z"
    restr.up_axis = "UP_Y"

    luces_estudio(600)
    escena = bpy.context.scene
    escena.camera = camara
    escena.frame_start = 1
    escena.frame_end = 120

    os.makedirs(os.path.dirname(SALIDA_RENDER), exist_ok=True)
    configurar_render(resolucion=(640, 360), samples=24, motor="CYCLES",
                      salida=SALIDA_RENDER)
    os.makedirs(os.path.dirname(SALIDA_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=SALIDA_BLEND)
    return len(bpy.data.objects)


def renderizar(frame=70):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    print(f"Escena 4A construida ({construir()} objetos)")
    renderizar()
