"""Iluminación de estudio y ajustes de render.

Uso dentro de Blender:
    from configuracion_camara import luces_estudio, configurar_render
    luces_estudio()
    configurar_render(resolucion=(640, 360), samples=32)
"""

import math

import bpy


def luces_estudio(energia=800.0):
    """Esquema de 3 puntos: key, fill y rim, con luces de área."""
    escena = bpy.context.scene
    luces = [
        # (nombre, ubicación, rotación, energía relativa, tamaño)
        ("Luz_Key", (4.0, -4.0, 5.0), (math.radians(50), 0, math.radians(45)), 1.0, 3.0),
        ("Luz_Fill", (-5.0, -2.0, 3.0), (math.radians(65), 0, math.radians(-65)), 0.35, 4.0),
        ("Luz_Rim", (0.0, 6.0, 4.0), (math.radians(-55), 0, 0), 0.6, 2.0),
    ]
    creadas = []
    for nombre, ubicacion, rotacion, factor, tamano in luces:
        data = bpy.data.lights.new(nombre, "AREA")
        data.energy = energia * factor
        data.size = tamano
        obj = bpy.data.objects.new(nombre, data)
        obj.location = ubicacion
        obj.rotation_euler = rotacion
        escena.collection.objects.link(obj)
        creadas.append(obj)

    # Fondo gris neutro suave para que los metales tengan algo que reflejar
    mundo = escena.world or bpy.data.worlds.new("Mundo")
    escena.world = mundo
    mundo.use_nodes = True
    fondo = mundo.node_tree.nodes.get("Background")
    if fondo:
        fondo.inputs["Color"].default_value = (0.05, 0.05, 0.06, 1.0)
        fondo.inputs["Strength"].default_value = 1.0
    return creadas


def configurar_render(resolucion=(1920, 1080), samples=128, motor="CYCLES",
                      salida=None, formato="PNG"):
    """Ajustes de render. Con motor CYCLES activa denoise y usa CPU si no hay GPU."""
    escena = bpy.context.scene
    escena.render.engine = motor
    escena.render.resolution_x, escena.render.resolution_y = resolucion
    escena.render.image_settings.file_format = formato
    if salida:
        escena.render.filepath = salida
    if motor == "CYCLES":
        escena.cycles.samples = samples
        # El Blender de los repositorios de Ubuntu viene compilado sin
        # OpenImageDenoiser; activar el denoise ahí aborta el render.
        try:
            import _cycles
            escena.cycles.use_denoising = bool(
                getattr(_cycles, "with_openimagedenoise", False))
        except ImportError:
            escena.cycles.use_denoising = False
    return escena
