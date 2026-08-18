"""Plano 4: leer rapido moviendo solo la cinta es imposible (sale disparada)."""

import math
import sys

RUTA = "/home/user/Como-funciona/retro-tec/escenas/vhs"
if RUTA not in sys.path:
    sys.path.append(RUTA)

import comun_blockout as cb


def construir():
    cb.limpiar()

    mat_cinta = cb.mat("P4_Cinta", (0.25, 0.12, 0.06), metallic=0.3,
                       roughness=0.35)
    mat_lector = cb.mat("P4_Lector", (0.7, 0.7, 0.75), metallic=0.8,
                        roughness=0.3)
    mat_carrete = cb.mat("P4_Carrete", (0.85, 0.85, 0.88), roughness=0.5)

    rot_carrete = (math.pi / 2, 0, 0)
    rollo = cb.cilindro("Rollo", 0.9, 0.3, (-3.2, 0, 0.9), mat_cinta,
                        rot_carrete)
    cb.cilindro("Nucleo", 0.25, 0.34, (-3.2, 0, 0.9), mat_carrete,
                rot_carrete)

    # El carrete gira cada vez mas rapido
    rollo.rotation_euler = rot_carrete
    rollo.keyframe_insert("rotation_euler", frame=1)
    for frame, vueltas in ((40, 1.0), (65, 3.5), (85, 9.0)):
        rollo.rotation_euler = (rot_carrete[0], vueltas * math.tau, 0)
        rollo.keyframe_insert("rotation_euler", frame=frame)

    # El lector fijo (una lupa esquematica: bloque con aro)
    cb.caja("Lector", (0.5, 0.4, 0.8), (1.5, 0, 1.6), mat_lector)

    # La cinta pasa cada vez mas rapido bajo el lector
    cinta = cb.caja("Cinta", (10.0, 0.03, 0.42), (0.5, 0, 0.9), mat_cinta)
    cinta.keyframe_insert("location", frame=1)
    for frame, avance in ((40, 1.2), (65, 4.0), (84, 10.0)):
        cinta.location = (0.5 + avance, 0, 0.9)
        cinta.keyframe_insert("location", frame=frame)
    for attr in ("hide_render", "hide_viewport"):
        setattr(cinta, attr, False)
        cinta.keyframe_insert(attr, frame=1)
        setattr(cinta, attr, True)
        cinta.keyframe_insert(attr, frame=85)

    # Frame 85: la cinta revienta en trozos que salen volando
    destinos = [(3.5, 1.2, 2.6, 0.9), (5.2, -1.0, 1.8, 2.2),
                (2.2, 0.8, 3.4, -1.4), (6.0, 1.5, 0.6, 1.1),
                (4.0, -1.6, 2.9, -2.0), (1.2, 0.4, 3.8, 2.7)]
    for k, (dx, dy, dz, giro) in enumerate(destinos):
        trozo = cb.caja(f"Trozo_{k}", (1.6, 0.03, 0.42), (1.5, 0, 0.9),
                        mat_cinta)
        cb.visibilidad_desde(trozo, 85)
        trozo.keyframe_insert("location", frame=85)
        trozo.keyframe_insert("rotation_euler", frame=85)
        trozo.location = (dx, dy, dz)
        trozo.rotation_euler = (giro, giro * 0.7, giro * 1.3)
        trozo.keyframe_insert("location", frame=115)
        trozo.keyframe_insert("rotation_euler", frame=115)

    cb.camara_fija((1.0, -7.5, 2.8), (0.8, 0, 1.2), "Camara_P4")
    return cb.finalizar("plano4")


def renderizar():
    salida = "/home/user/Como-funciona/retro-tec/renders/vhs/plano4/preview.png"
    cb.render_frame(100, salida)
    return salida


if __name__ == "__main__":
    construir()
    renderizar()
