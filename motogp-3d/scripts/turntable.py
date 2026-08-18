"""Cámara turntable: órbita 360 grados alrededor de un punto.

Uso dentro de Blender:
    from turntable import crear_turntable
    crear_turntable(radio=4.0, altura=1.5, frames=120)

Crea un empty en el objetivo, una cámara emparentada a él mirando al centro,
y anima la rotación Z del empty de 0 a 360 grados con interpolación lineal.
Deja la cámara como activa y ajusta el rango de frames de la escena.
"""

import math

import bpy


def crear_turntable(objetivo=(0.0, 0.0, 0.0), radio=4.0, altura=1.5,
                    frames=120, nombre="Turntable"):
    escena = bpy.context.scene

    pivote = bpy.data.objects.new(f"{nombre}_pivote", None)
    pivote.location = objetivo
    escena.collection.objects.link(pivote)

    cam_data = bpy.data.cameras.new(f"{nombre}_camara")
    camara = bpy.data.objects.new(f"{nombre}_camara", cam_data)
    escena.collection.objects.link(camara)
    camara.parent = pivote
    camara.location = (radio, 0.0, altura)

    # La cámara apunta siempre al pivote (el centro de la escena)
    restriccion = camara.constraints.new("TRACK_TO")
    restriccion.target = pivote
    restriccion.track_axis = "TRACK_NEGATIVE_Z"
    restriccion.up_axis = "UP_Y"

    pivote.rotation_euler = (0.0, 0.0, 0.0)
    pivote.keyframe_insert("rotation_euler", frame=1)
    pivote.rotation_euler = (0.0, 0.0, math.tau)
    pivote.keyframe_insert("rotation_euler", frame=frames + 1)

    # Interpolación lineal para velocidad de giro constante
    for fcurve in pivote.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = "LINEAR"

    escena.frame_start = 1
    escena.frame_end = frames
    escena.camera = camara
    return camara, pivote
