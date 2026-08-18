"""Plano 2 del guion v2: que hay dentro de la cajita.

Blockout en dos partes dentro de la misma escena:
  - frames 1-60:  el cassette de frente; la carcasa se vuelve transparente y
                  se ven los dos carretes girando y la cinta entre ellos
  - frames 61-120: corte a la cinta estirada perdiendose en el horizonte
                  sobre un campo de futbol (comparacion de longitud)

Ejecutable via MCP o headless.
"""

import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import asignar

BASE = "/home/user/Como-funciona/retro-tec"
SALIDA_RENDER = os.path.join(BASE, "renders", "vhs", "plano2",
                             "preview_frame50.png")
SALIDA_RENDER_B = os.path.join(BASE, "renders", "vhs", "plano2",
                               "preview_frame95.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "vhs", "plano2-cajita-v1.blend")

FRAMES = 120
CORTE = 60  # frame del cambio de parte


def _mat(nombre, color, alpha=1.0, metallic=0.0, roughness=0.5, emision=None):
    mat = bpy.data.materials.get(nombre)
    if mat is None:
        mat = bpy.data.materials.new(nombre)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            mat.blend_method = "BLEND"
    return mat


def _caja(nombre, escala, ubicacion, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=ubicacion)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.scale = escala
    asignar(obj, material)
    return obj


def _cilindro(nombre, radio, alto, ubicacion, material):
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=alto,
                                        location=ubicacion, vertices=48)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.rotation_euler = (1.5707963, 0.0, 0.0)  # eje del carrete hacia camara
    asignar(obj, material)
    return obj


def _visibilidad(obj, visible_hasta=None, visible_desde=None):
    """Muestra el objeto solo en una de las dos partes del plano."""
    for attr in ("hide_render", "hide_viewport"):
        if visible_hasta is not None:  # parte A
            setattr(obj, attr, False)
            obj.keyframe_insert(attr, frame=1)
            setattr(obj, attr, True)
            obj.keyframe_insert(attr, frame=visible_hasta + 1)
        else:                          # parte B
            setattr(obj, attr, True)
            obj.keyframe_insert(attr, frame=1)
            setattr(obj, attr, False)
            obj.keyframe_insert(attr, frame=visible_desde)


def construir():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    mat_carcasa = _mat("P2_Carcasa", (0.06, 0.06, 0.07), alpha=1.0,
                       roughness=0.4)
    mat_cinta = _mat("P2_Cinta", (0.25, 0.12, 0.06), roughness=0.3,
                     metallic=0.3)
    mat_carrete = _mat("P2_Carrete", (0.85, 0.85, 0.88), roughness=0.5)
    mat_cesped = _mat("P2_Cesped", (0.05, 0.35, 0.10), roughness=0.9)
    mat_linea = _mat("P2_Linea", (0.9, 0.9, 0.9), roughness=0.8)

    # ---- Parte A: el cassette ----
    parte_a = []
    carcasa = _caja("Carcasa", (3.7, 0.5, 2.05), (0, 0, 0), mat_carcasa)
    parte_a.append(carcasa)
    # La carcasa se vuelve transparente entre los frames 20 y 45
    bsdf = mat_carcasa.node_tree.nodes["Principled BSDF"]
    mat_carcasa.blend_method = "BLEND"
    bsdf.inputs["Alpha"].default_value = 1.0
    bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=20)
    bsdf.inputs["Alpha"].default_value = 0.10
    bsdf.inputs["Alpha"].keyframe_insert("default_value", frame=45)

    for lado, radio_cinta in ((-1, 0.78), (1, 0.45)):
        rollo = _cilindro(f"Rollo_{'izq' if lado < 0 else 'der'}",
                          radio_cinta, 0.30, (0.95 * lado, 0.0, 0.1),
                          mat_cinta)
        nucleo = _cilindro(f"Nucleo_{'izq' if lado < 0 else 'der'}",
                           0.22, 0.34, (0.95 * lado, 0.0, 0.1), mat_carrete)
        # Giro lento de los carretes
        for obj in (rollo, nucleo):
            obj.keyframe_insert("rotation_euler", frame=1)
            obj.rotation_euler.y += 3.0 * lado
            obj.keyframe_insert("rotation_euler", frame=CORTE)
            parte_a.append(obj)

    tramo = _caja("Cinta_frontal", (2.1, 0.02, 0.42), (0, 0, -0.95),
                  mat_cinta)
    parte_a.append(tramo)

    for obj in parte_a:
        _visibilidad(obj, visible_hasta=CORTE)

    # ---- Parte B: la cinta estirada sobre el campo ----
    parte_b = []
    campo = _caja("Campo", (60.0, 40.0, 0.05), (25.0, 0.0, -1.3), mat_cesped)
    parte_b.append(campo)
    for i in range(7):
        linea = _caja(f"Linea_{i}", (0.12, 40.0, 0.052),
                      (i * 9.0, 0.0, -1.295), mat_linea)
        parte_b.append(linea)
    cinta_larga = _caja("Cinta_larga", (120.0, 0.42, 0.02),
                        (55.0, 0.0, -0.9), mat_cinta)
    parte_b.append(cinta_larga)

    for obj in parte_b:
        _visibilidad(obj, visible_desde=CORTE + 1)

    # ---- Camara con salto en el corte (interpolacion constante) ----
    objetivo = bpy.data.objects.new("Objetivo", None)
    bpy.context.scene.collection.objects.link(objetivo)
    cam_data = bpy.data.cameras.new("Camara_P2")
    camara = bpy.data.objects.new("Camara_P2", cam_data)
    bpy.context.scene.collection.objects.link(camara)
    restr = camara.constraints.new("TRACK_TO")
    restr.target = objetivo
    restr.track_axis = "TRACK_NEGATIVE_Z"
    restr.up_axis = "UP_Y"

    # Parte A: acercamiento suave al cassette
    objetivo.location = (0, 0, 0)
    objetivo.keyframe_insert("location", frame=1)
    objetivo.keyframe_insert("location", frame=CORTE)
    camara.location = (0.0, -7.5, 1.6)
    camara.keyframe_insert("location", frame=1)
    camara.location = (0.0, -5.2, 1.1)
    camara.keyframe_insert("location", frame=CORTE)
    # Parte B: vista baja siguiendo la cinta hacia el horizonte
    objetivo.location = (30.0, 0.0, -0.9)
    objetivo.keyframe_insert("location", frame=CORTE + 1)
    camara.location = (-3.0, -2.2, 0.3)
    camara.keyframe_insert("location", frame=CORTE + 1)
    camara.location = (0.5, -2.2, 0.5)
    camara.keyframe_insert("location", frame=FRAMES)
    # El salto de la parte A a la B debe ser un corte seco, no un viaje:
    # interpolacion constante en el keyframe del corte para camara Y objetivo
    for obj in (camara, objetivo):
        for fc in obj.animation_data.action.fcurves:
            for kf in fc.keyframe_points:
                if abs(kf.co[0] - CORTE) < 0.5:
                    kf.interpolation = "CONSTANT"

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


def renderizar():
    escena = bpy.context.scene
    escena.frame_set(50)
    escena.render.filepath = os.path.abspath(SALIDA_RENDER)
    bpy.ops.render.render(write_still=True)
    escena.frame_set(95)
    escena.render.filepath = os.path.abspath(SALIDA_RENDER_B)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER, SALIDA_RENDER_B


if __name__ == "__main__":
    print(f"Plano 2 construido ({construir()} objetos)")
    renderizar()
