"""Escena 3B del VHS (plano clave): el tambor inclinado pinta franjas
diagonales sobre la cinta.

Composicion didactica: la cinta (semitransparente) avanza despacio ante el
tambor inclinado que gira rapido con sus dos cabezales; cada media vuelta
"pinta" una franja diagonal luminosa que viaja con la cinta. Al acumularse
las franjas se entiende el barrido helicoidal.

Escala visual exagerada donde ayuda (inclinacion del tambor ~8 grados para
que la diagonal se lea en pantalla; la real es menor). Sin texto quemado:
cifras y rotulos van en capas de montaje.

Ejecutable via MCP o headless:
    blender --background --python generar_escena_3b_vhs.py
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
SALIDA_RENDER = os.path.join(BASE, "renders", "vhs", "escena-3b",
                             "preview_frame90.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "vhs", "escena-3b-v1.blend")

FRAMES = 120
NUM_FRANJAS = 14
VUELTAS_TAMBOR = 7            # 2 cabezales -> 2 franjas por vuelta
INCLINACION = math.radians(8) # exagerada para legibilidad (real ~6)
AVANCE_CINTA = 6.0            # unidades que recorre la cinta en 120 frames


def limpiar_escena():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def material_cinta():
    mat = bpy.data.materials.get("VHS_Cinta")
    if mat is None:
        mat = bpy.data.materials.new("VHS_Cinta")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.05, 0.04, 0.06, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.4
        bsdf.inputs["Roughness"].default_value = 0.35
        bsdf.inputs["Alpha"].default_value = 0.75
        mat.blend_method = "BLEND"
    return mat


def material_franja():
    mat = bpy.data.materials.get("VHS_Franja")
    if mat is None:
        mat = bpy.data.materials.new("VHS_Franja")
        mat.use_nodes = True
        nodos = mat.node_tree.nodes
        nodos.clear()
        emision = nodos.new("ShaderNodeEmission")
        emision.inputs["Color"].default_value = (0.15, 0.85, 1.0, 1.0)
        emision.inputs["Strength"].default_value = 4.0
        salida = nodos.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(emision.outputs["Emission"],
                                salida.inputs["Surface"])
    return mat


def construir():
    limpiar_escena()

    # --- Tambor inclinado con dos cabezales ---
    pivote_tambor = bpy.data.objects.new("Tambor_inclinacion", None)
    pivote_tambor.location = (0.0, 0.6, 0.0)
    pivote_tambor.rotation_euler = (INCLINACION, 0.0, 0.0)
    bpy.context.scene.collection.objects.link(pivote_tambor)

    bpy.ops.mesh.primitive_cylinder_add(radius=1.03, depth=0.9,
                                        location=(0, 0, 0), vertices=96)
    tambor = bpy.context.active_object
    tambor.name = "Tambor"
    if hasattr(tambor.data, "use_auto_smooth"):
        bpy.ops.object.shade_smooth()
        tambor.data.use_auto_smooth = True
    else:
        bpy.ops.object.shade_auto_smooth()
    asignar(tambor, acero_pulido())
    tambor.parent = pivote_tambor

    mat_franja = material_franja()
    for k in range(2):
        ang = k * math.pi
        bpy.ops.mesh.primitive_cube_add(
            size=0.12, location=(1.03 * math.cos(ang), 1.03 * math.sin(ang), -0.1))
        cabezal = bpy.context.active_object
        cabezal.name = f"Cabezal_{k + 1}"
        cabezal.scale = (0.6, 0.6, 1.4)
        asignar(cabezal, mat_franja)
        cabezal.parent = tambor

    # Giro rapido del tambor (interpolacion lineal)
    tambor.rotation_euler = (0.0, 0.0, 0.0)
    tambor.keyframe_insert("rotation_euler", frame=1)
    tambor.rotation_euler = (0.0, 0.0, VUELTAS_TAMBOR * math.tau)
    tambor.keyframe_insert("rotation_euler", frame=FRAMES)
    for fc in tambor.animation_data.action.fcurves:
        for kf in fc.keyframe_points:
            kf.interpolation = "LINEAR"

    # --- Cinta con sus franjas, todo colgado de un empty que avanza ---
    cinta_movil = bpy.data.objects.new("Cinta_movil", None)
    bpy.context.scene.collection.objects.link(cinta_movil)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.75, 0.0))
    cinta = bpy.context.active_object
    cinta.name = "Cinta"
    cinta.scale = (26.0, 0.02, 0.42)
    asignar(cinta, material_cinta())
    cinta.parent = cinta_movil

    for i in range(NUM_FRANJAS):
        bpy.ops.mesh.primitive_plane_add(size=1.0)
        franja = bpy.context.active_object
        franja.name = f"Franja_{i + 1:02d}"
        # Plano vertical sobre la cara frontal de la cinta, inclinado
        franja.rotation_euler = (math.radians(90), math.radians(-14), 0.0)
        franja.scale = (0.07, 0.40, 1.0)
        franja.location = (-0.5 * i, -0.772, 0.0)
        asignar(franja, mat_franja)
        franja.parent = cinta_movil

        # Aparece cuando "su" media vuelta del tambor la pinta
        frame_aparicion = max(1, round(i * FRAMES / NUM_FRANJAS))
        for attr in ("hide_render", "hide_viewport"):
            setattr(franja, attr, True)
            franja.keyframe_insert(attr, frame=1)
            setattr(franja, attr, False)
            franja.keyframe_insert(attr, frame=frame_aparicion + 1)

    # La cinta avanza despacio hacia +X
    cinta_movil.location = (0.0, 0.0, 0.0)
    cinta_movil.keyframe_insert("location", frame=1)
    cinta_movil.location = (AVANCE_CINTA, 0.0, 0.0)
    cinta_movil.keyframe_insert("location", frame=FRAMES)
    for fc in cinta_movil.animation_data.action.fcurves:
        for kf in fc.keyframe_points:
            kf.interpolation = "LINEAR"

    # --- Camara y luces ---
    objetivo = bpy.data.objects.new("Objetivo_camara", None)
    objetivo.location = (1.2, -0.4, 0.1)
    bpy.context.scene.collection.objects.link(objetivo)

    cam_data = bpy.data.cameras.new("Camara_3B_VHS")
    camara = bpy.data.objects.new("Camara_3B_VHS", cam_data)
    camara.location = (3.6, -5.2, 2.4)
    bpy.context.scene.collection.objects.link(camara)
    restr = camara.constraints.new("TRACK_TO")
    restr.target = objetivo
    restr.track_axis = "TRACK_NEGATIVE_Z"
    restr.up_axis = "UP_Y"

    luces_estudio(500)

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


def renderizar(frame=90):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    print(f"Escena 3B VHS construida ({construir()} objetos)")
    renderizar()
