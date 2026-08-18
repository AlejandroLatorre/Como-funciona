"""Montaje borrador: secuencia PNG (repetida N veces) + subtítulos de un SRT,
codificado a MP4 con el FFMPEG interno de Blender.

Sirve para previsualizar "producto final" (imagen + subtítulos) sin DaVinci.
El montaje real del canal se hace en DaVinci; esto es la maqueta rápida.

Uso headless:
    blender --background --python scripts/montaje_borrador.py -- \
        <dir_secuencia> <archivo.srt> <salida.mp4> [repeticiones] [fps]
"""

import os
import re
import sys

import bpy


def parsear_srt(ruta):
    """Devuelve [(inicio_s, fin_s, texto), ...]."""
    contenido = open(ruta, encoding="utf-8").read()
    patron = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*"
        r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)",
        re.DOTALL)
    subtitulos = []
    for m in patron.finditer(contenido):
        h1, m1, s1, ms1, h2, m2, s2, ms2, texto = m.groups()
        inicio = int(h1) * 3600 + int(m1) * 60 + int(s1) + int(ms1) / 1000
        fin = int(h2) * 3600 + int(m2) * 60 + int(s2) + int(ms2) / 1000
        texto = " ".join(linea.strip() for linea in texto.strip().splitlines())
        subtitulos.append((inicio, fin, texto))
    return subtitulos


def montar(dir_secuencia, ruta_srt, salida, repeticiones=1, fps=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene

    frames = sorted(f for f in os.listdir(dir_secuencia)
                    if f.lower().endswith(".png"))
    if not frames:
        raise RuntimeError(f"No hay PNGs en {dir_secuencia}")

    primera = bpy.data.images.load(os.path.join(dir_secuencia, frames[0]))
    ancho, alto = primera.size
    bpy.data.images.remove(primera)

    escena.sequence_editor_create()
    editor = escena.sequence_editor

    # Video: la secuencia repetida N veces, una tira tras otra
    for r in range(repeticiones):
        tira = editor.sequences.new_image(
            f"secuencia_{r + 1}", os.path.join(dir_secuencia, frames[0]),
            channel=1, frame_start=1 + r * len(frames))
        for nombre in frames[1:]:
            tira.elements.append(nombre)

    total_frames = len(frames) * repeticiones

    # Subtítulos como tiras de texto
    for i, (inicio, fin, texto) in enumerate(parsear_srt(ruta_srt)):
        f_ini = max(1, int(round(inicio * fps)) + 1)
        f_fin = min(total_frames, int(round(fin * fps)) + 1)
        if f_ini >= f_fin:
            continue
        tira = editor.sequences.new_effect(
            f"sub_{i + 1:02d}", "TEXT", channel=2,
            frame_start=f_ini, frame_end=f_fin)
        tira.text = texto
        tira.font_size = max(18, alto // 14)
        tira.location = (0.5, 0.10)
        tira.anchor_x = "CENTER"
        tira.anchor_y = "BOTTOM"
        tira.use_shadow = True
        tira.wrap_width = 0.85

    escena.frame_start = 1
    escena.frame_end = total_frames
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
    print(f"Piloto montado: {salida} ({total_frames} frames, "
          f"{len(parsear_srt(ruta_srt))} subtítulos)")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) < 3:
        print("Uso: blender --background --python montaje_borrador.py -- "
              "<dir_secuencia> <archivo.srt> <salida.mp4> [repeticiones] [fps]")
        sys.exit(1)
    montar(argv[0], argv[1], argv[2],
           int(argv[3]) if len(argv) > 3 else 1,
           int(argv[4]) if len(argv) > 4 else 24)
