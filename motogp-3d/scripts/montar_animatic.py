"""Ensambla un animatic: varias secuencias PNG en orden + subtítulos SRT,
codificado a MP4 con el FFMPEG interno de Blender.

Uso headless:
    blender --background --python scripts/montar_animatic.py -- \
        <salida.mp4> <archivo.srt> <dir_seq_1> <dir_seq_2> ... [--fps N]
"""

import os
import sys

import bpy

RUTA_SCRIPTS = os.path.dirname(os.path.abspath(__file__))
if RUTA_SCRIPTS not in sys.path:
    sys.path.append(RUTA_SCRIPTS)

from montaje_borrador import parsear_srt


def montar(salida, ruta_srt, dirs_secuencias, fps=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene
    escena.sequence_editor_create()
    editor = escena.sequence_editor

    ancho = alto = None
    frame_actual = 1
    for d in dirs_secuencias:
        frames = sorted(f for f in os.listdir(d) if f.lower().endswith(".png"))
        if not frames:
            raise RuntimeError(f"No hay PNGs en {d}")
        if ancho is None:
            img = bpy.data.images.load(os.path.join(d, frames[0]))
            ancho, alto = img.size
            bpy.data.images.remove(img)
        tira = editor.sequences.new_image(
            os.path.basename(d.rstrip("/")) or "seq",
            os.path.join(d, frames[0]), channel=1, frame_start=frame_actual)
        for nombre in frames[1:]:
            tira.elements.append(nombre)
        frame_actual += len(frames)

    total = frame_actual - 1

    for i, (inicio, fin, texto) in enumerate(parsear_srt(ruta_srt)):
        f_ini = max(1, int(round(inicio * fps)) + 1)
        f_fin = min(total, int(round(fin * fps)) + 1)
        if f_ini >= f_fin:
            continue
        tira = editor.sequences.new_effect(
            f"sub_{i + 1:02d}", "TEXT", channel=2,
            frame_start=f_ini, frame_end=f_fin)
        tira.text = texto
        tira.font_size = max(18, alto // 14)
        tira.location = (0.5, 0.10)
        if hasattr(tira, "anchor_x"):
            tira.anchor_x, tira.anchor_y = "CENTER", "BOTTOM"
        else:
            tira.align_x, tira.align_y = "CENTER", "BOTTOM"
        tira.use_shadow = True
        tira.wrap_width = 0.85

    escena.frame_start = 1
    escena.frame_end = total
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
    print(f"Animatic montado: {salida} ({total} frames, "
          f"{len(dirs_secuencias)} planos)")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    fps = 24
    if "--fps" in argv:
        idx = argv.index("--fps")
        fps = int(argv[idx + 1])
        argv = argv[:idx] + argv[idx + 2:]
    if len(argv) < 3:
        print("Uso: ... -- <salida.mp4> <archivo.srt> <dir_seq...> [--fps N]")
        sys.exit(1)
    montar(argv[0], argv[1], argv[2:], fps)
