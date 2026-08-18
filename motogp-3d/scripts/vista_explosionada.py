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
                frame_inicio=1, frame_fin=60, tolerancia=0.02):
    """Separa `objetos` a lo largo de `eje` manteniendo su orden actual.

    Los objetos cuya coordenada en el eje difiere menos de `tolerancia` se
    tratan como un grupo (p. ej. varios muelles o bolas a la misma altura) y
    se desplazan juntos. El grupo central apenas se mueve; los extremos se
    desplazan más, de forma simétrica respecto al centro del conjunto.
    """
    idx = _EJES[eje.upper()]
    ordenados = sorted(objetos, key=lambda o: o.location[idx])

    grupos = []
    for obj in ordenados:
        if grupos and abs(obj.location[idx] - grupos[-1][0].location[idx]) <= tolerancia:
            grupos[-1].append(obj)
        else:
            grupos.append([obj])

    centro = (len(grupos) - 1) / 2.0
    for i, grupo in enumerate(grupos):
        desplazamiento = (i - centro) * separacion
        for obj in grupo:
            destino = obj.location.copy()
            destino[idx] += desplazamiento
            if animar:
                obj.keyframe_insert("location", frame=frame_inicio)
                obj.location = destino
                obj.keyframe_insert("location", frame=frame_fin)
            else:
                obj.location = destino
    return grupos
