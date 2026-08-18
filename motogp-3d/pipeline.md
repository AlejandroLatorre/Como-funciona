# Pipeline de producción de un video

Checklist paso a paso. Copiar esta lista en un issue o nota por cada video y
marcar sobre la marcha.

## 1. Guion e investigación
- [ ] Elegir componente (ej. embrague antirrebote) y crear `investigacion/<tema>/`
- [ ] Recopilar referencias: patentes, artículos técnicos, despieces, videos existentes
- [ ] Anotar fuentes con URL y fecha en `investigacion/<tema>/referencias.md`
- [ ] Redactar guion en `guiones/<tema>-v1.md` (estructura: gancho → problema → cómo funciona → detalle clave → cierre)
- [ ] **Verificación técnica del guion**: contrastar cada afirmación mecánica
      con al menos dos fuentes independientes (idealmente una primaria:
      patente, manual de taller, documentación de fabricante). Las dudas van
      a la lista "dudas a verificar" de las notas; ninguna llega al render
      final sin resolver. Lo que no se pueda confirmar se reformula como
      principio general o se elimina — el canal se llama "Cómo funciona":
      la exactitud es el producto.
- [ ] Revisar el guion y versionar los cambios (-v2, -v3...)

## 2. Modelos CAD
- [ ] Buscar el componente en GrabCAD (o modelarlo desde cero si no existe)
- [ ] Verificar la licencia del modelo y anotarla en `modelos/<componente>/fuente.md`
- [ ] Descargar STEP (preferido) o STL/OBJ a `modelos/<componente>/`
- [ ] Convertir STEP a malla (addon STEPper o FreeCAD) si hace falta
- [ ] Importar en Blender y comprobar escala, normales y nombres de piezas

## 3. Escena en Blender (con Claude vía MCP)
- [ ] Abrir Blender, conectar el addon BlenderMCP (panel N > BlenderMCP > Connect)
- [ ] Crear `escenas/<video>/` y guardar el .blend con nombre versionado
- [ ] Aplicar materiales (`scripts/materiales_metalicos.py`)
- [ ] Organizar piezas en colecciones con nombres claros
- [ ] Montar vista explosionada donde el guion lo pida (`scripts/vista_explosionada.py`)
- [ ] Animar el mecanismo (rotaciones, acoples, secuencias de montaje)
- [ ] Cámaras: turntable para presentación (`scripts/turntable.py`) + cámaras fijas para detalles
- [ ] Iluminación de estudio (`scripts/configuracion_camara.py`)
- [ ] Preview en baja resolución para validar tiempos con el guion

## 4. Render
- [ ] Ajustar resolución/samples finales (1080p o 4K, Cycles con denoise)
- [ ] Renderizar por secuencias a `renders/<video>/<secuencia>/` (frames PNG, no video, para poder reanudar)
- [ ] Comprobar frames corruptos o saltos

## 5. Montaje (DaVinci Resolve)
- [ ] Importar secuencias de frames como clips
- [ ] Montar según el guion, grabar/añadir locución
- [ ] Rótulos y grafismos en capas propias — NUNCA quemados en el render 3D
      (regla de internacionalización, ver canal/formatos-y-distribucion.md)
- [ ] Subtítulos: SRT en español desde el guion + traducciones (EN mínimo)
- [ ] Corrección de color y exportación final
- [ ] Shorts: 2-3 renders verticales (9:16) de los planos clave con subtítulos
      incrustados por idioma
- [ ] Archivar el proyecto de Resolve junto al video

## 6. Cierre
- [ ] Commit y push de guion, escena, scripts nuevos y notas
- [ ] Anotar en el README los cambios de configuración si los hubo
