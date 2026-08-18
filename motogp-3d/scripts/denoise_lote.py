"""Limpia el ruido de renders PNG con OpenImageDenoise (paquete pip `oidn`).

Permite renderizar con pocos samples (32-64) y limpiar despues, dividiendo
el coste de render entre 5 y 10. Pensado para el Blender de apt, que viene
compilado sin denoiser.

Uso:
    python3.12 scripts/denoise_lote.py <entrada.png|dir> [salida.png|dir]

Con un directorio, procesa todos los .png (a un dir de salida o in-place
con sufijo _dn si no se da salida).
"""

import os
import sys

import numpy as np
import oidn
from PIL import Image


def denoise_imagen(ruta_entrada, ruta_salida, device):
    img = Image.open(ruta_entrada).convert("RGB")
    ancho, alto = img.size
    # sRGB -> lineal (OIDN trabaja en lineal)
    srgb = np.asarray(img, dtype=np.float32) / 255.0
    lineal = np.where(srgb <= 0.04045, srgb / 12.92,
                      ((srgb + 0.055) / 1.055) ** 2.4).astype(np.float32)
    entrada = np.ascontiguousarray(lineal)
    salida = np.zeros_like(entrada)

    filtro = oidn.NewFilter(device, "RT")
    oidn.SetSharedFilterImage(filtro, "color", entrada, oidn.FORMAT_FLOAT3,
                              ancho, alto)
    oidn.SetSharedFilterImage(filtro, "output", salida, oidn.FORMAT_FLOAT3,
                              ancho, alto)
    oidn.CommitFilter(filtro)
    oidn.ExecuteFilter(filtro)
    oidn.ReleaseFilter(filtro)

    # lineal -> sRGB
    limpio = np.clip(salida, 0.0, 1.0)
    srgb_out = np.where(limpio <= 0.0031308, limpio * 12.92,
                        1.055 * np.power(limpio, 1 / 2.4) - 0.055)
    resultado = (np.clip(srgb_out, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(resultado).save(ruta_salida)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    entrada = sys.argv[1]
    salida = sys.argv[2] if len(sys.argv) > 2 else None

    device = oidn.NewDevice()
    oidn.CommitDevice(device)

    if os.path.isdir(entrada):
        destino = salida or entrada
        os.makedirs(destino, exist_ok=True)
        archivos = sorted(f for f in os.listdir(entrada)
                          if f.lower().endswith(".png"))
        for i, nombre in enumerate(archivos, 1):
            ruta_out = os.path.join(destino, nombre) if salida else \
                os.path.join(entrada, nombre.rsplit(".", 1)[0] + "_dn.png")
            denoise_imagen(os.path.join(entrada, nombre), ruta_out, device)
            if i % 20 == 0 or i == len(archivos):
                print(f"{i}/{len(archivos)} limpiados")
    else:
        ruta_out = salida or entrada.rsplit(".", 1)[0] + "_dn.png"
        denoise_imagen(entrada, ruta_out, device)
        print(f"Limpiado: {ruta_out}")

    oidn.ReleaseDevice(device)


if __name__ == "__main__":
    main()
