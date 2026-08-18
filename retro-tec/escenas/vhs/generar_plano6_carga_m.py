"""Plano 6: los bracitos sacan la cinta y la abrazan al tambor (carga en M).

Vista cenital: el cassette abajo, el tambor arriba, dos postes que viajan
llevando la cinta. La cinta se representa como segmentos rectos entre
puntos, re-keyframeados cada pocos frames.
"""

import sys

RUTA = "/home/user/Como-funciona/retro-tec/escenas/vhs"
if RUTA not in sys.path:
    sys.path.append(RUTA)

import comun_blockout as cb

INICIO, FIN = 25, 85          # viaje de los postes
E1, E2 = (-1.3, -1.9), (1.3, -1.9)      # salidas del cassette
C1, C2 = (-0.85, 0.85), (0.85, 0.85)    # puntos de abrazo al tambor
P_INI = {(1): (-0.55, -1.5), (2): (0.55, -1.5)}   # postes dentro del cassette
P_FIN = {(1): (-1.7, 1.15), (2): (1.7, 1.15)}     # postes desplegados


def _pos_poste(k, frame):
    t = min(1.0, max(0.0, (frame - INICIO) / (FIN - INICIO)))
    x0, y0 = P_INI[k]
    x1, y1 = P_FIN[k]
    return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)


def construir():
    cb.limpiar()

    mat_cassette = cb.mat("P6_Cassette", (0.10, 0.10, 0.12), alpha=0.35,
                          roughness=0.5)
    mat_cinta = cb.mat("P6_Cinta", (0.55, 0.28, 0.12), metallic=0.3,
                       roughness=0.35)
    mat_tambor = cb.mat("P6_Tambor", (0.75, 0.76, 0.78), metallic=1.0,
                        roughness=0.2)
    mat_poste = cb.mat("P6_Poste", (0.9, 0.55, 0.15), metallic=0.6,
                       roughness=0.3)

    cb.caja("Cassette", (3.6, 1.6, 0.3), (0, -2.4, 0), mat_cassette)
    cb.cilindro("Rollo_izq", 0.6, 0.28, (-0.9, -2.4, 0), mat_cinta)
    cb.cilindro("Rollo_der", 0.6, 0.28, (0.9, -2.4, 0), mat_cinta)
    # Tambor bajo y cinta por encima de su cara superior para que el abrazo
    # se vea desde la camara cenital (si van a la misma altura, lo oculta)
    cb.cilindro("Tambor", 1.0, 0.3, (0, 1.4, 0), mat_tambor, vertices=64)

    postes = {}
    for k in (1, 2):
        postes[k] = cb.cilindro(f"Poste_{k}", 0.09, 0.7,
                                (*P_INI[k], 0.2), mat_poste, vertices=24)

    segmentos = {}
    for nombre in ("E1P1", "P1C1", "C1C2", "C2P2", "P2E2"):
        seg = cb.caja(f"Cinta_{nombre}", (1, 1, 1), (0, 0, 0.25), mat_cinta)
        segmentos[nombre] = seg

    # Keyframear postes y segmentos a lo largo del despliegue
    frames = [1] + list(range(INICIO, FIN + 1, 5)) + [120]
    for frame in frames:
        p1 = _pos_poste(1, frame)
        p2 = _pos_poste(2, frame)
        for k, pos in ((1, p1), (2, p2)):
            postes[k].location = (*pos, 0.2)
            postes[k].keyframe_insert("location", frame=frame)
        cb.keyframe_segmento(segmentos["E1P1"], E1, p1, frame)
        cb.keyframe_segmento(segmentos["P1C1"], p1, C1, frame)
        cb.keyframe_segmento(segmentos["C1C2"], C1, C2, frame)
        cb.keyframe_segmento(segmentos["C2P2"], C2, p2, frame)
        cb.keyframe_segmento(segmentos["P2E2"], p2, E2, frame)

    # Camara cenital fija (sin track: mirando recto hacia abajo)
    import bpy
    cam_data = bpy.data.cameras.new("Camara_P6")
    camara = bpy.data.objects.new("Camara_P6", cam_data)
    camara.location = (0.0, -0.5, 9.0)
    bpy.context.scene.collection.objects.link(camara)
    bpy.context.scene.camera = camara

    return cb.finalizar("plano6")


def renderizar():
    salida = "/home/user/Como-funciona/retro-tec/renders/vhs/plano6/preview.png"
    cb.render_frame(85, salida)
    return salida


if __name__ == "__main__":
    construir()
    renderizar()
