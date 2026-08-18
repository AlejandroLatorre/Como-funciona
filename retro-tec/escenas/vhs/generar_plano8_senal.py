"""Plano 8: la senal viaja del tambor a la tele y la pantalla se pinta
linea a linea."""

import math
import sys

RUTA = "/home/user/Como-funciona/retro-tec/escenas/vhs"
if RUTA not in sys.path:
    sys.path.append(RUTA)

import comun_blockout as cb

LINEAS = 10


def construir():
    cb.limpiar()

    mat_metal = cb.mat("P8_Metal", (0.75, 0.76, 0.78), metallic=1.0,
                       roughness=0.25)
    mat_cable = cb.mat("P8_Cable", (0.08, 0.08, 0.09), roughness=0.6)
    mat_tv = cb.mat("P8_TV", (0.12, 0.12, 0.13), roughness=0.5)
    mat_pulso = cb.mat("P8_Pulso", (0.15, 0.85, 1.0), emision=8.0)
    mat_linea = cb.mat("P8_Linea", (0.55, 0.75, 1.0), emision=3.0)

    cb.cilindro("Tambor", 0.9, 0.7, (-4.2, 0, 1.0), mat_metal,
                rotacion=(math.radians(8), 0, 0), vertices=64)

    # Cable en L: del tambor a la tele
    cb.caja("Cable_h", (5.4, 0.08, 0.08), (-1.2, 0, 0.35), mat_cable)
    cb.caja("Cable_v", (0.08, 0.08, 0.9), (1.5, 0, 0.8), mat_cable)

    cb.caja("TV", (3.2, 0.5, 2.4), (3.6, 0.6, 1.6), mat_tv)

    # El pulso de senal recorre el cable (frames 10-55)
    import bpy
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(-4.0, 0, 0.35),
                                         segments=24, ring_count=12)
    pulso = bpy.context.active_object
    pulso.name = "Pulso"
    from materiales_metalicos import asignar
    asignar(pulso, mat_pulso)
    recorrido = [(10, (-4.0, 0, 0.35)), (40, (1.5, 0, 0.35)),
                 (50, (1.5, 0, 1.25)), (55, (2.2, 0.3, 1.6))]
    for frame, pos in recorrido:
        pulso.location = pos
        pulso.keyframe_insert("location", frame=frame)
    cb.lineal(pulso)
    for attr in ("hide_render", "hide_viewport"):
        setattr(pulso, attr, False)
        pulso.keyframe_insert(attr, frame=1)
        setattr(pulso, attr, True)
        pulso.keyframe_insert(attr, frame=56)

    # La pantalla se pinta linea a linea (frames 58-110)
    alto_linea = 1.9 / LINEAS
    for i in range(LINEAS):
        z = 2.5 - (i + 0.5) * alto_linea
        linea = cb.caja(f"Linea_{i:02d}", (2.7, 0.06, alto_linea * 0.92),
                        (3.6, 0.32, z), mat_linea)
        cb.visibilidad_desde(linea, 58 + round(i * 52 / LINEAS))

    cb.camara_fija((-0.3, -9.5, 2.6), (-0.3, 0, 1.2), "Camara_P8")
    return cb.finalizar("plano8")


def renderizar():
    salida = "/home/user/Como-funciona/retro-tec/renders/vhs/plano8/preview.png"
    cb.render_frame(90, salida)
    return salida


if __name__ == "__main__":
    construir()
    renderizar()
