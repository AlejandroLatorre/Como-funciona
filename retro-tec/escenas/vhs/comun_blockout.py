"""Utilidades comunes de los blockouts del video del VHS."""

import math
import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import asignar

BASE = "/home/user/Como-funciona/retro-tec"


def limpiar():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def mat(nombre, color, alpha=1.0, metallic=0.0, roughness=0.5, emision=0.0):
    m = bpy.data.materials.get(nombre)
    if m is None:
        m = bpy.data.materials.new(nombre)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            m.blend_method = "BLEND"
        if emision > 0 and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emision
        elif emision > 0:
            bsdf.inputs["Emission"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emision
    return m


def caja(nombre, escala, ubicacion, material, rotacion=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=ubicacion)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.scale = escala
    obj.rotation_euler = rotacion
    asignar(obj, material)
    return obj


def cilindro(nombre, radio, alto, ubicacion, material, rotacion=(0, 0, 0),
             vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=alto,
                                        location=ubicacion, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.rotation_euler = rotacion
    asignar(obj, material)
    return obj


def camara_fija(ubicacion, objetivo_loc, nombre="Camara"):
    objetivo = bpy.data.objects.new(f"{nombre}_objetivo", None)
    objetivo.location = objetivo_loc
    bpy.context.scene.collection.objects.link(objetivo)
    cam_data = bpy.data.cameras.new(nombre)
    camara = bpy.data.objects.new(nombre, cam_data)
    camara.location = ubicacion
    bpy.context.scene.collection.objects.link(camara)
    restr = camara.constraints.new("TRACK_TO")
    restr.target = objetivo
    restr.track_axis = "TRACK_NEGATIVE_Z"
    restr.up_axis = "UP_Y"
    bpy.context.scene.camera = camara
    return camara, objetivo


def lineal(obj):
    """Pone interpolacion lineal en todas las curvas del objeto."""
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kf in fc.keyframe_points:
                kf.interpolation = "LINEAR"


def keyframe_segmento(obj, punto_a, punto_b, frame, grosor=0.06):
    """Coloca una caja unitaria como segmento 2D (plano XY) entre A y B."""
    ax, ay = punto_a
    bx, by = punto_b
    largo = max(1e-4, math.hypot(bx - ax, by - ay))
    obj.location = ((ax + bx) / 2, (ay + by) / 2, obj.location.z)
    obj.rotation_euler = (0, 0, math.atan2(by - ay, bx - ax))
    obj.scale = (largo, grosor, grosor)
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)
    obj.keyframe_insert("scale", frame=frame)


def visibilidad_desde(obj, frame):
    for attr in ("hide_render", "hide_viewport"):
        setattr(obj, attr, True)
        obj.keyframe_insert(attr, frame=1)
        setattr(obj, attr, False)
        obj.keyframe_insert(attr, frame=frame)


def finalizar(nombre_plano, frames=120, luz=600):
    luces_estudio(luz)
    escena = bpy.context.scene
    escena.frame_start = 1
    escena.frame_end = frames
    salida_render = os.path.join(BASE, "renders", "vhs", nombre_plano,
                                 "preview.png")
    salida_blend = os.path.join(BASE, "escenas", "vhs",
                                f"{nombre_plano}-v1.blend")
    os.makedirs(os.path.dirname(salida_render), exist_ok=True)
    configurar_render(resolucion=(640, 360), samples=24, motor="CYCLES",
                      salida=salida_render)
    os.makedirs(os.path.dirname(salida_blend), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=salida_blend)
    return salida_render


def render_frame(frame, salida):
    escena = bpy.context.scene
    escena.frame_set(frame)
    escena.render.filepath = salida
    bpy.ops.render.render(write_still=True)
