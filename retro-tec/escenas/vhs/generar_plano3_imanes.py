"""Plano 3 del guion v2: la pelicula esta "escrita con imanes".

Blockout: zoom a la superficie de la cinta, cubierta de imanes diminutos
(conos que apuntan izquierda o derecha). Un cabezal pasa por encima y los
va volteando: se ve "escribir" la informacion.

Ejecutable via MCP o headless.
"""

import math
import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import acero_pulido, asignar

BASE = "/home/user/Como-funciona/retro-tec"
SALIDA_RENDER = os.path.join(BASE, "renders", "vhs", "plano3",
                             "preview_frame60.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "vhs", "plano3-imanes-v1.blend")

FRAMES = 120
COLUMNAS = 16
FILAS = 5
PASO = 0.55
X0 = -(COLUMNAS - 1) * PASO / 2.0


def _mat(nombre, color, metallic=0.6, roughness=0.35):
    mat = bpy.data.materials.get(nombre)
    if mat is None:
        mat = bpy.data.materials.new(nombre)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def construir():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    mat_cinta = _mat("P3_Cinta", (0.10, 0.05, 0.03), metallic=0.2,
                     roughness=0.6)
    mat_iman = _mat("P3_Iman", (0.75, 0.30, 0.15), metallic=0.7,
                    roughness=0.3)

    # Superficie de la cinta (muy ampliada)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.15))
    cinta = bpy.context.active_object
    cinta.name = "Cinta_superficie"
    cinta.scale = (COLUMNAS * PASO + 2.0, FILAS * PASO + 1.2, 0.2)
    asignar(cinta, mat_cinta)

    # Rejilla de imanes (conos tumbados apuntando +X o -X)
    for i in range(COLUMNAS):
        for j in range(FILAS):
            x = X0 + i * PASO
            y = (j - (FILAS - 1) / 2.0) * PASO
            direccion = 1 if (i * 7 + j * 3) % 2 == 0 else -1
            bpy.ops.mesh.primitive_cone_add(radius1=0.10, depth=0.30,
                                            location=(x, y, 0.12),
                                            vertices=16)
            iman = bpy.context.active_object
            iman.name = f"Iman_{i:02d}_{j}"
            iman.rotation_euler = (0.0, direccion * math.pi / 2, 0.0)
            asignar(iman, mat_iman)

            # El cabezal pasa por su columna y lo voltea (patron nuevo)
            frame_paso = 20 + round(i * 80 / COLUMNAS)
            nueva_dir = 1 if (i * 5 + j * 11) % 2 == 0 else -1
            if nueva_dir != direccion:
                iman.keyframe_insert("rotation_euler", frame=frame_paso)
                iman.rotation_euler = (0.0, nueva_dir * math.pi / 2, 0.0)
                iman.keyframe_insert("rotation_euler", frame=frame_paso + 5)

    # El cabezal: un bloque que barre la rejilla de izquierda a derecha
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(X0 - 1.0, 0, 0.75))
    cabezal = bpy.context.active_object
    cabezal.name = "Cabezal"
    cabezal.scale = (0.5, FILAS * PASO + 0.8, 0.5)
    asignar(cabezal, acero_pulido())
    cabezal.keyframe_insert("location", frame=20)
    cabezal.location.x = X0 + (COLUMNAS - 1) * PASO + 1.0
    cabezal.keyframe_insert("location", frame=100)
    for fc in cabezal.animation_data.action.fcurves:
        for kf in fc.keyframe_points:
            kf.interpolation = "LINEAR"

    # Camara en picado suave
    objetivo = bpy.data.objects.new("Objetivo", None)
    objetivo.location = (0.0, 0.0, 0.1)
    bpy.context.scene.collection.objects.link(objetivo)
    cam_data = bpy.data.cameras.new("Camara_P3")
    camara = bpy.data.objects.new("Camara_P3", cam_data)
    camara.location = (0.0, -6.5, 5.0)
    bpy.context.scene.collection.objects.link(camara)
    restr = camara.constraints.new("TRACK_TO")
    restr.target = objetivo
    restr.track_axis = "TRACK_NEGATIVE_Z"
    restr.up_axis = "UP_Y"

    luces_estudio(600)
    escena = bpy.context.scene
    escena.camera = camara
    escena.frame_start = 1
    escena.frame_end = FRAMES

    os.makedirs(os.path.dirname(SALIDA_RENDER), exist_ok=True)
    configurar_render(resolucion=(640, 360), samples=24, motor="CYCLES",
                      salida=SALIDA_RENDER)
    os.makedirs(os.path.dirname(SALIDA_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=SALIDA_BLEND)
    return len(bpy.data.objects)


def renderizar(frame=60):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    print(f"Plano 3 construido ({construir()} objetos)")
    renderizar()
