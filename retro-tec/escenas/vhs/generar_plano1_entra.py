"""Plano 1: metes la cinta, clac, y la tele se enciende."""

import sys

RUTA = "/home/user/Como-funciona/retro-tec/escenas/vhs"
if RUTA not in sys.path:
    sys.path.append(RUTA)

import comun_blockout as cb


def construir():
    cb.limpiar()

    mat_vcr = cb.mat("P1_VCR", (0.08, 0.08, 0.09), roughness=0.4)
    mat_ranura = cb.mat("P1_Ranura", (0.01, 0.01, 0.01), roughness=0.9)
    mat_cinta = cb.mat("P1_Cassette", (0.10, 0.10, 0.11), roughness=0.5)
    mat_tv = cb.mat("P1_TV", (0.12, 0.12, 0.13), roughness=0.5)
    mat_pantalla = cb.mat("P1_Pantalla", (0.6, 0.75, 1.0), emision=0.0)

    cb.caja("VCR", (4.4, 1.8, 1.1), (0, 0, 0.55), mat_vcr)
    cb.caja("Ranura", (2.4, 0.1, 0.35), (0, -0.92, 0.75), mat_ranura)

    cassette = cb.caja("Cassette", (2.1, 1.2, 0.28), (0, -2.6, 0.75), mat_cinta)
    cassette.keyframe_insert("location", frame=10)
    cassette.location = (0, -0.4, 0.75)
    cassette.keyframe_insert("location", frame=45)
    cb.lineal(cassette)

    cb.caja("TV", (3.4, 0.5, 2.3), (5.4, 0.6, 1.15), mat_tv)
    cb.caja("Pantalla", (2.9, 0.06, 1.9), (5.4, 0.32, 1.15), mat_pantalla)

    # La pantalla se enciende a partir del frame 70
    bsdf = mat_pantalla.node_tree.nodes["Principled BSDF"]
    clave = ("Emission Strength" if "Emission Strength" in bsdf.inputs
             else "Emission")
    entrada = bsdf.inputs["Emission Strength"] \
        if "Emission Strength" in bsdf.inputs else None
    if entrada is None:
        entrada = bsdf.inputs[clave]
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (0.6, 0.75, 1.0, 1.0)
    entrada.default_value = 0.0
    entrada.keyframe_insert("default_value", frame=70)
    entrada.default_value = 6.0
    entrada.keyframe_insert("default_value", frame=95)

    cb.camara_fija((2.6, -9.5, 2.8), (2.6, 0, 1.0), "Camara_P1")
    return cb.finalizar("plano1")


def renderizar():
    salida = "/home/user/Como-funciona/retro-tec/renders/vhs/plano1/preview.png"
    cb.render_frame(100, salida)
    return salida


if __name__ == "__main__":
    construir()
    renderizar()
