"""Vista explosionada: separa objetos a lo largo de un eje.

Uso dentro de Blender:
    from vista_explosionada import explosionar
    explosionar(objetos, eje="Z", separacion=0.35)

Con animar=True, cada objeto se mueve de su posición original a la
explosionada entre frame_inicio y frame_fin (útil para secuencias de
montaje/desmontaje).
"""

import bpy

_EJES = {"X": 0, "Y": 1, "Z": 2}


def explosionar(objetos, eje="Z", separacion=0.5, animar=False,
                frame_inicio=1, frame_fin=60):
    """Separa `objetos` a lo largo de `eje` manteniendo su orden actual.

    El objeto central apenas se mueve; los extremos se desplazan más, de
    forma simétrica respecto al centro del grupo.
    """
    idx = _EJES[eje.upper()]
    ordenados = sorted(objetos, key=lambda o: o.location[idx])
    centro = (len(ordenados) - 1) / 2.0

    for i, obj in enumerate(ordenados):
        desplazamiento = (i - centro) * separacion
        destino = obj.location.copy()
        destino[idx] += desplazamiento

        if animar:
            obj.keyframe_insert("location", frame=frame_inicio)
            obj.location = destino
            obj.keyframe_insert("location", frame=frame_fin)
        else:
            obj.location = destino
    return ordenados
