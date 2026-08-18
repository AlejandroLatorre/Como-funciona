"""Plano 7: el desfile de estaciones (el rodillo TIRA, el tambor LEE la
imagen, el cabezal fijo LEE el sonido). Camara viajando junto a la cinta."""

import math
import sys

RUTA = "/home/user/Como-funciona/retro-tec/escenas/vhs"
if RUTA not in sys.path:
    sys.path.append(RUTA)

import comun_blockout as cb


def _pulso(obj, frame_centro):
    """Pequeno pulso de escala cuando la camara pasa por la estacion."""
    original = tuple(obj.scale)
    obj.scale = original
    obj.keyframe_insert("scale", frame=frame_centro - 12)
    obj.scale = tuple(s * 1.18 for s in original)
    obj.keyframe_insert("scale", frame=frame_centro)
    obj.scale = original
    obj.keyframe_insert("scale", frame=frame_centro + 12)


def construir():
    cb.limpiar()

    mat_cinta = cb.mat("P7_Cinta", (0.25, 0.12, 0.06), metallic=0.3,
                       roughness=0.35)
    mat_metal = cb.mat("P7_Metal", (0.75, 0.76, 0.78), metallic=1.0,
                       roughness=0.25)
    mat_goma = cb.mat("P7_Goma", (0.05, 0.05, 0.06), roughness=0.8)
    mat_audio = cb.mat("P7_Audio", (0.9, 0.55, 0.15), metallic=0.6,
                       roughness=0.3)

    cb.caja("Cinta", (18.0, 0.03, 0.42), (0, 0, 0.8), mat_cinta)

    # Estacion 1 (x=-5): cabrestante + rodillo de goma (TIRA)
    rodillo_a = cb.cilindro("Cabrestante", 0.10, 1.6, (-5, 0.25, 0.8),
                            mat_metal)
    rodillo_b = cb.cilindro("Rodillo_goma", 0.35, 1.2, (-5, -0.42, 0.8),
                            mat_goma)
    # Estacion 2 (x=0): el tambor inclinado (LEE la imagen)
    tambor = cb.cilindro("Tambor", 1.0, 0.8, (0, 1.1, 0.9), mat_metal,
                         rotacion=(math.radians(8), 0, 0), vertices=64)
    # Estacion 3 (x=5): cabezal de audio (LEE el sonido)
    audio = cb.caja("Cabezal_audio", (0.5, 0.35, 0.7), (5, 0.35, 0.9),
                    mat_audio)

    _pulso(rodillo_b, 30)
    _pulso(rodillo_a, 30)
    _pulso(tambor, 62)
    _pulso(audio, 94)

    # Camara dolly de izquierda a derecha
    camara, objetivo = cb.camara_fija((-7.5, -4.0, 1.9), (-5.5, 0, 0.8),
                                      "Camara_P7")
    for obj, destino in ((camara, (7.0, -4.0, 1.9)), (objetivo, (5.5, 0, 0.8))):
        obj.keyframe_insert("location", frame=1)
        obj.location = destino
        obj.keyframe_insert("location", frame=120)
        cb.lineal(obj)

    return cb.finalizar("plano7")


def renderizar():
    salida = "/home/user/Como-funciona/retro-tec/renders/vhs/plano7/preview.png"
    cb.render_frame(62, salida)
    return salida


if __name__ == "__main__":
    construir()
    renderizar()
