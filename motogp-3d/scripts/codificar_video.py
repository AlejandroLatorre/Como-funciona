"""Codifica una secuencia de PNGs a MP4 (H.264) usando el FFMPEG de Blender.

No requiere ffmpeg instalado en el sistema: Blender trae el codificador.

Uso headless:
    blender --background --python scripts/codificar_video.py -- \
        <dir_secuencia> <salida.mp4> [fps]
"""

import os
import sys

import bpy


def codificar(dir_secuencia, salida, fps=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene

    frames = sorted(f for f in os.listdir(dir_secuencia)
                    if f.lower().endswith(".png"))
    if not frames:
        raise RuntimeError(f"No hay PNGs en {dir_secuencia}")

    # Tomar la resolución del primer frame
    primera = bpy.data.images.load(os.path.join(dir_secuencia, frames[0]))
    ancho, alto = primera.size
    bpy.data.images.remove(primera)

    escena.sequence_editor_create()
    tira = escena.sequence_editor.sequences.new_image(
        "secuencia", os.path.join(dir_secuencia, frames[0]),
        channel=1, frame_start=1)
    for nombre in frames[1:]:
        tira.elements.append(nombre)

    escena.frame_start = 1
    escena.frame_end = len(frames)
    escena.render.fps = fps
    escena.render.resolution_x = ancho
    escena.render.resolution_y = alto
    escena.render.resolution_percentage = 100
    escena.render.image_settings.file_format = "FFMPEG"
    escena.render.ffmpeg.format = "MPEG4"
    escena.render.ffmpeg.codec = "H264"
    escena.render.ffmpeg.constant_rate_factor = "MEDIUM"
    escena.render.ffmpeg.gopsize = fps
    escena.render.filepath = salida

    bpy.ops.render.render(animation=True)
    print(f"Video codificado: {salida} ({len(frames)} frames a {fps} fps, "
          f"{ancho}x{alto})")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) < 2:
        print("Uso: blender --background --python codificar_video.py -- "
              "<dir_secuencia> <salida.mp4> [fps]")
        sys.exit(1)
    codificar(argv[0], argv[1], int(argv[2]) if len(argv) > 2 else 24)
