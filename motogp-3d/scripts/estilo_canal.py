"""Pasada de look del canal (estilo limpio tipo Lagon/Lesics).

Funciones que se aplican a una escena ya construida:
  - biseles():        Bevel en todas las mallas (nada tiene aristas perfectas)
  - fondo_estudio():  fondo degradado suave en vez de gris plano
  - dof():            profundidad de campo ligera en la camara activa
  - calidad_final():  resolucion y samples de render final

Uso tipico (via MCP o headless, tras abrir/construir la escena):
    from estilo_canal import aplicar_look
    aplicar_look(samples=256, resolucion=(1920, 1080))
"""

import bpy


def biseles(ancho=0.015, segmentos=2):
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if any(m.type == "BEVEL" for m in obj.modifiers):
            continue
        mod = obj.modifiers.new("look_bevel", "BEVEL")
        mod.width = ancho
        mod.segments = segmentos
        mod.limit_method = "ANGLE"
        mod.angle_limit = 1.0472  # 60 grados


def fondo_estudio(color_bajo=(0.02, 0.02, 0.025), color_alto=(0.10, 0.11, 0.13),
                  fuerza=1.0):
    """Degradado vertical suave en el mundo (abajo oscuro, arriba claro)."""
    mundo = bpy.context.scene.world or bpy.data.worlds.new("Mundo")
    bpy.context.scene.world = mundo
    mundo.use_nodes = True
    nodos = mundo.node_tree.nodes
    enlaces = mundo.node_tree.links
    nodos.clear()

    coords = nodos.new("ShaderNodeTexCoord")
    mapeo = nodos.new("ShaderNodeMapping")
    mapeo.inputs["Rotation"].default_value = (0.0, 1.5708, 0.0)
    degradado = nodos.new("ShaderNodeTexGradient")
    rampa = nodos.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].color = (*color_bajo, 1.0)
    rampa.color_ramp.elements[1].color = (*color_alto, 1.0)
    fondo = nodos.new("ShaderNodeBackground")
    fondo.inputs["Strength"].default_value = fuerza
    salida = nodos.new("ShaderNodeOutputWorld")

    enlaces.new(coords.outputs["Generated"], mapeo.inputs["Vector"])
    enlaces.new(mapeo.outputs["Vector"], degradado.inputs["Vector"])
    enlaces.new(degradado.outputs["Fac"], rampa.inputs["Fac"])
    enlaces.new(rampa.outputs["Color"], fondo.inputs["Color"])
    enlaces.new(fondo.outputs["Background"], salida.inputs["Surface"])


def dof(distancia=None, apertura=2.8):
    """Profundidad de campo ligera en la camara activa de la escena."""
    camara = bpy.context.scene.camera
    if camara is None:
        return
    camara.data.dof.use_dof = True
    camara.data.dof.aperture_fstop = apertura
    objetivo = None
    for restr in camara.constraints:
        if restr.type == "TRACK_TO" and restr.target:
            objetivo = restr.target
            break
    if objetivo is not None:
        camara.data.dof.focus_object = objetivo
    elif distancia is not None:
        camara.data.dof.focus_distance = distancia


def calidad_final(samples=256, resolucion=(1920, 1080)):
    escena = bpy.context.scene
    escena.render.resolution_x, escena.render.resolution_y = resolucion
    escena.cycles.samples = samples
    # El denoise sigue condicionado a las capacidades del build (ver
    # configuracion_camara.configurar_render); con 256 samples la escena
    # tipo estudio queda limpia incluso sin denoiser.


def aplicar_look(samples=256, resolucion=(1920, 1080)):
    biseles()
    fondo_estudio()
    dof()
    calidad_final(samples, resolucion)
