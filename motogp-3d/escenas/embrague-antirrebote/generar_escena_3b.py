"""Escena 3B del guion del embrague antirrebote: rampa + bola (plano clave).

Versión didáctica simplificada: dos bloques de cubo enfrentados con pocket y
rampa a ~35 grados, y una bola entre ambos. La animación muestra los dos
sentidos del par:

  - frames 1-30:   tracción (bloques cerrados, la bola reposa en el pocket)
  - frames 31-80:  retención (el bloque superior gira -aquí desliza- respecto
                   al inferior, la bola sube la rampa y separa los bloques)
  - frames 81-120: las velocidades se igualan y el conjunto vuelve a cerrar

Pensada para ejecutarse vía MCP (execute_blender_code) o headless:
    blender --background --python generar_escena_3b.py
"""

import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import acero_pulido, aluminio_anodizado, asignar, titanio

BASE = "/home/user/Como-funciona/motogp-3d"
SALIDA_RENDER = os.path.join(BASE, "renders", "embrague-antirrebote",
                             "escena-3b", "preview_frame60.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "embrague-antirrebote",
                            "escena-3b-v1.blend")

# Perfil del bloque inferior en el plano XZ (X = direccion tangencial de
# giro, Z = eje axial del embrague). El pocket tiene una pared casi vertical
# (lado de traccion) y una rampa a ~35 grados (lado de retencion).
PERFIL_INFERIOR = [
    (-1.5, 0.0), (1.5, 0.0), (1.5, 0.5), (0.15, 0.5),
    (0.10, 0.2),            # pared de traccion (casi vertical)
    (-0.52, 0.2),           # fondo del pocket
    (-0.95, 0.5),           # rampa a ~35 grados
    (-1.5, 0.5),
]
# El superior es el inferior reflejado en X y en Z (rampas opuestas).
PERFIL_SUPERIOR = [(-x, 1.06 - z) for x, z in PERFIL_INFERIOR]

RADIO_BOLA = 0.33
CENTRO_BOLA = (0.0, 0.0, 0.53)


def limpiar_escena():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def prisma(nombre, perfil, y0=-0.35, y1=0.35):
    """Extruye un perfil 2D (plano XZ) a lo largo de Y."""
    n = len(perfil)
    verts = [(x, y0, z) for x, z in perfil] + [(x, y1, z) for x, z in perfil]
    caras = [list(range(n)), [i + n for i in reversed(range(n))]]
    for i in range(n):
        j = (i + 1) % n
        caras.append([i, j, j + n, i + n])
    malla = bpy.data.meshes.new(nombre)
    malla.from_pydata(verts, [], caras)
    malla.validate()
    malla.update()
    obj = bpy.data.objects.new(nombre, malla)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def animar(obj, posiciones):
    """posiciones: lista de (frame, (x, y, z)) sobre la posición base."""
    base = obj.location.copy()
    for frame, delta in posiciones:
        obj.location = (base[0] + delta[0], base[1] + delta[1], base[2] + delta[2])
        obj.keyframe_insert("location", frame=frame)
    obj.location = base


def construir():
    limpiar_escena()

    inferior = prisma("Rampa_inferior", PERFIL_INFERIOR)
    superior = prisma("Rampa_superior", PERFIL_SUPERIOR)
    asignar(inferior, acero_pulido())
    asignar(superior, aluminio_anodizado())

    bpy.ops.mesh.primitive_uv_sphere_add(radius=RADIO_BOLA, location=CENTRO_BOLA,
                                         segments=48, ring_count=24)
    bola = bpy.context.active_object
    bola.name = "Bola"
    bpy.ops.object.shade_smooth()
    asignar(bola, titanio())

    # Animacion: cerrado -> abre (bola sube la rampa, bloques se separan) -> cierra
    animar(superior, [
        (1, (0, 0, 0)), (30, (0, 0, 0)),
        (80, (0.45, 0, 0.28)),
        (120, (0, 0, 0)),
    ])
    animar(bola, [
        (1, (0, 0, 0)), (30, (0, 0, 0)),
        (80, (0.22, 0, 0.14)),
        (120, (0, 0, 0)),
    ])

    # Camara fija en picado corto mirando al pocket
    objetivo = bpy.data.objects.new("Objetivo_camara", None)
    objetivo.location = (0.0, 0.0, 0.55)
    bpy.context.scene.collection.objects.link(objetivo)

    cam_data = bpy.data.cameras.new("Camara_3B")
    camara = bpy.data.objects.new("Camara_3B", cam_data)
    camara.location = (2.4, -3.0, 1.8)
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
    configurar_render(resolucion=(640, 360), samples=48, motor="CYCLES",
                      salida=SALIDA_RENDER)

    os.makedirs(os.path.dirname(SALIDA_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=SALIDA_BLEND)
    return len(bpy.data.objects)


def renderizar(frame=60):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    n = construir()
    print(f"Escena 3B construida ({n} objetos)")
    renderizar()
    print(f"Preview en {SALIDA_RENDER}")
