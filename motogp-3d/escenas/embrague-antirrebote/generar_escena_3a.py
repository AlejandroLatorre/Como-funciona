"""Escena 3A del guion: vista explosionada axial del embrague completo.

Componentes (simplificados, procedurales): campana/cesta, paquete de discos
alternados (friccion carbono / acero), cubo partido en dos mitades con bolas
entre ellas, plato de presion y muelles (representados como cilindros).

Animacion:
  - frames 1-20:   conjunto montado, la camara empieza a orbitar despacio
  - frames 21-90:  explosion axial progresiva (cada pieza a su sitio)
  - frames 91-120: mantiene el explosionado mientras la camara sigue orbitando

Ejecutable via MCP o headless:
    blender --background --python generar_escena_3a.py
"""

import math
import os
import sys

import bpy

SCRIPTS = "/home/user/Como-funciona/motogp-3d/scripts"
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

from configuracion_camara import configurar_render, luces_estudio
from materiales_metalicos import (acero_pulido, aluminio_anodizado, asignar,
                                  carbono_oscuro, titanio)
from turntable import crear_turntable
from vista_explosionada import explosionar

BASE = "/home/user/Como-funciona/motogp-3d"
SALIDA_RENDER = os.path.join(BASE, "renders", "embrague-antirrebote",
                             "escena-3a", "preview_frame100.png")
SALIDA_BLEND = os.path.join(BASE, "escenas", "embrague-antirrebote",
                            "escena-3a-v1.blend")


def limpiar_escena():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def cilindro(nombre, radio, alto, z, material, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=alto,
                                        location=(0, 0, z), vertices=vertices)
    obj = bpy.context.active_object
    obj.name = nombre
    if hasattr(obj.data, "use_auto_smooth"):
        bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
    else:
        bpy.ops.object.shade_auto_smooth()
    asignar(obj, material)
    return obj


def campana(nombre, z):
    """Cesta: cilindro vaciado por boolean con otro cilindro interior."""
    exterior = cilindro(nombre, 1.45, 0.9, z, aluminio_anodizado())
    bpy.ops.mesh.primitive_cylinder_add(radius=1.28, depth=1.0,
                                        location=(0, 0, z + 0.15), vertices=64)
    interior = bpy.context.active_object
    mod = exterior.modifiers.new("hueco", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = interior
    bpy.context.view_layer.objects.active = exterior
    bpy.ops.object.modifier_apply(modifier="hueco")
    bpy.data.objects.remove(interior, do_unlink=True)
    return exterior


def construir():
    limpiar_escena()
    piezas = []

    # De abajo a arriba, en posicion montada (compacta)
    piezas.append(campana("Campana", 0.0))

    z = 0.05
    for i in range(8):
        if i % 2 == 0:
            piezas.append(cilindro(f"Disco_friccion_{i//2 + 1}", 1.15, 0.06,
                                   z, carbono_oscuro()))
        else:
            piezas.append(cilindro(f"Disco_acero_{i//2 + 1}", 1.10, 0.04,
                                   z, acero_pulido()))
        z += 0.075

    piezas.append(cilindro("Cubo_inferior", 0.62, 0.22, z + 0.06, acero_pulido()))

    # Bolas entre las dos mitades del cubo (el corazon antirrebote)
    bolas = []
    for k in range(3):
        ang = k * math.tau / 3
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.07,
            location=(0.42 * math.cos(ang), 0.42 * math.sin(ang), z + 0.22),
            segments=24, ring_count=12)
        bola = bpy.context.active_object
        bola.name = f"Bola_{k + 1}"
        bpy.ops.object.shade_smooth()
        asignar(bola, titanio())
        bolas.append(bola)

    piezas.append(cilindro("Cubo_superior", 0.62, 0.22, z + 0.38, acero_pulido()))
    piezas.append(cilindro("Plato_presion", 1.15, 0.08, z + 0.60,
                           aluminio_anodizado()))

    muelles = []
    for k in range(4):
        ang = k * math.tau / 4 + math.tau / 8
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.09, depth=0.28,
            location=(0.85 * math.cos(ang), 0.85 * math.sin(ang), z + 0.82),
            vertices=24)
        muelle = bpy.context.active_object
        muelle.name = f"Muelle_{k + 1}"
        asignar(muelle, titanio())
        muelles.append(muelle)

    # Explosion axial animada (frames 21-90). explosionar agrupa por altura,
    # asi que las 3 bolas y los 4 muelles se mueven como un solo escalon.
    todas = piezas + bolas + muelles
    explosionar(todas, eje="Z", separacion=0.18, animar=True,
                frame_inicio=21, frame_fin=90)

    # Con 13 escalones a 0.18 el conjunto explosionado abarca ~4 unidades:
    # camara lejos y centrada a media pila para encuadrarlo entero
    crear_turntable(objetivo=(0.0, 0.0, 0.95), radio=9.0, altura=2.2,
                    frames=480, nombre="Orbita3A")
    luces_estudio(700)

    escena = bpy.context.scene
    escena.frame_start = 1
    escena.frame_end = 120  # la orbita de 480 solo recorre un cuarto de vuelta

    os.makedirs(os.path.dirname(SALIDA_RENDER), exist_ok=True)
    configurar_render(resolucion=(640, 360), samples=24, motor="CYCLES",
                      salida=SALIDA_RENDER)
    os.makedirs(os.path.dirname(SALIDA_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=SALIDA_BLEND)
    return len(todas)


def renderizar(frame=100):
    bpy.context.scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    return SALIDA_RENDER


if __name__ == "__main__":
    n = construir()
    print(f"Escena 3A construida ({n} piezas)")
    renderizar()
    print(f"Preview en {SALIDA_RENDER}")
