"""Materiales PBR reutilizables para componentes mecánicos de MotoGP.

Uso dentro de Blender:
    from materiales_metalicos import acero_pulido, carbono_oscuro
    obj.data.materials.append(acero_pulido())

Cada función devuelve el material ya existente si se creó antes (idempotente).
"""

import bpy


def _material_principled(nombre, base_color, metallic, roughness, anisotropic=0.0):
    mat = bpy.data.materials.get(nombre)
    if mat is not None:
        return mat
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if "Anisotropic" in bsdf.inputs:
        bsdf.inputs["Anisotropic"].default_value = anisotropic
    return mat


def acero_pulido():
    """Acero gris claro, muy reflectante. Para ejes, muelles, discos metálicos."""
    return _material_principled("MGP_AceroPulido", (0.75, 0.76, 0.78), 1.0, 0.18, 0.4)


def aluminio_anodizado():
    """Aluminio gris medio, semi-mate. Para carcasas y tapas mecanizadas."""
    return _material_principled("MGP_AluminioAnodizado", (0.60, 0.61, 0.63), 1.0, 0.35)


def carbono_oscuro():
    """Material oscuro casi negro, poco reflectante. Para discos de fricción
    de carbono y piezas de composite (sin trama de tejido, versión simple)."""
    return _material_principled("MGP_CarbonoOscuro", (0.03, 0.03, 0.035), 0.3, 0.55)


def titanio():
    """Titanio con tinte cálido. Para tornillería y escapes."""
    return _material_principled("MGP_Titanio", (0.62, 0.58, 0.54), 1.0, 0.28, 0.3)


def asignar(obj, material):
    """Asigna un material a un objeto reemplazando los que tuviera."""
    obj.data.materials.clear()
    obj.data.materials.append(material)
