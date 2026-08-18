# motogp-3d — Videos educativos de mecánica de MotoGP (v1)

Proyecto para producir videos educativos con animaciones 3D de componentes
mecánicos de MotoGP: embrague antirrebote (slipper clutch), cambio seamless,
dispositivos de altura (holeshot / ride height device), etc.

## Pipeline de producción

```
Guion e investigación (Claude)
        │
        ▼
Modelos CAD (GrabCAD, formato STEP/STL)
        │
        ▼
Animación en Blender (controlada por Claude vía MCP)
        │
        ▼
Render (Cycles/EEVEE) → renders/<video>/
        │
        ▼
Montaje final en DaVinci Resolve
```

## Estructura del proyecto

```
motogp-3d/
  guiones/          Guiones de video en markdown, versionados (-v1, -v2, ...)
  investigacion/    Notas técnicas, patentes y referencias, un archivo o carpeta por tema
  modelos/          Archivos CAD/STEP/STL descargados, un subdirectorio por componente
  escenas/          Archivos .blend, un subdirectorio por video
  renders/          Salidas de render, un subdirectorio por video
  scripts/          Scripts Python de Blender reutilizables (ver abajo)
  pipeline.md       Checklist paso a paso para producir un video
```

### Scripts reutilizables (`scripts/`)

| Script | Qué hace |
|---|---|
| `materiales_metalicos.py` | Crea materiales PBR reutilizables: acero pulido, aluminio anodizado, carbono oscuro, titanio |
| `vista_explosionada.py` | Separa los objetos seleccionados a lo largo de un eje para vista explosionada, con animación opcional de montaje/desmontaje |
| `turntable.py` | Añade una cámara orbitando 360° alrededor del origen (o de un objeto) en N frames |
| `configuracion_camara.py` | Configuración de cámara y luces de estudio (key/fill/rim) + ajustes de render |
| `prueba_humo.py` | Escena de prueba completa (discos de embrague) para validar el pipeline de punta a punta |

Todos se pueden ejecutar de dos formas:
- **Vía MCP**: Claude los envía a Blender a través del servidor blender-mcp.
- **Headless**: `blender --background --python scripts/<script>.py`

## Decisiones de configuración (registro para reproducibilidad)

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-08-18 | Blender **4.0.2** instalado vía `apt` (Ubuntu 24.04) | Cumple el requisito 4.x; es la versión empaquetada en Noble. En tu máquina local puedes usar cualquier 4.x (recomendado ≥4.0) |
| 2026-08-18 | **uv/uvx 0.8.17** ya presente en el entorno | Requisito del servidor MCP `blender-mcp`; no hizo falta instalarlo |
| 2026-08-18 | Servidor MCP: **ahujasid/blender-mcp** vía `uvx blender-mcp` | Proyecto open source de referencia para controlar Blender desde Claude. Configurado en `.mcp.json` en la raíz del repositorio (ámbito de proyecto) |
| 2026-08-18 | Renderizador de pruebas: **Cycles por CPU** | El entorno remoto no tiene GPU ni display; EEVEE requiere OpenGL. En tu máquina local con GPU puedes usar EEVEE para previews rápidas y Cycles para el render final |
| 2026-08-18 | Entorno de trabajo de Claude: **contenedor remoto sin GUI** | Las fases con interfaz (instalar el addon, conectar el panel, DaVinci Resolve) se hacen en tu máquina local siguiendo la guía de abajo |
| 2026-08-18 | Módulo `requests` instalado en ámbito de usuario para el Python de Blender (`/usr/bin/python3.12 -m pip install --user --break-system-packages requests`) | El Blender de apt usa el Python del sistema y el addon lo necesita; no venía instalado |
| 2026-08-18 | Blender headless se ejecuta con **`xvfb-run -a blender --python scripts/arrancar_servidor_headless.py`** (Xvfb ya estaba en el sistema) | El addon rehúsa arrancar con `blender --background` porque sin bucle de eventos los comandos nunca se ejecutarían; el display virtual es la vía que recomienda el propio addon |
| 2026-08-18 | El `register()` del addon (versión actual, 1.5) **autoarranca el servidor** en el puerto 9876 | No hay que arrancarlo dos veces: el primer intento con arranque manual falló con "Address already in use" |
| 2026-08-18 | Denoise de Cycles **condicional** a las capacidades del build (`_cycles.with_openimagedenoise`) | El Blender de apt está compilado sin OpenImageDenoiser y activar el denoise aborta el render. En tu Blender local (blender.org) el denoise se activará solo |
| 2026-08-18 | Cilindros con `shade_smooth` + `use_auto_smooth` | Sin auto-smooth, el suavizado infla los discos como almohadas; con él, la pared queda suave y las caras planas nítidas (API de Blender 4.0; en 4.1+ cambia) |

## Configuración del servidor MCP de Blender

### Qué hay configurado en el repositorio

El archivo `.mcp.json` en la raíz del repositorio registra el servidor para
Claude Code con ámbito de proyecto:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

Claude Code lo detecta al abrir una sesión en este repositorio (te pedirá
aprobar el servidor la primera vez). `uvx` descarga y ejecuta el paquete
`blender-mcp` automáticamente; no hay que instalar nada más por pip.

### Arquitectura de la conexión

```
Claude Code ──(stdio/MCP)── uvx blender-mcp ──(socket TCP localhost:9876)── addon.py dentro de Blender
```

El servidor MCP **no** abre Blender: se conecta a un addon que corre *dentro*
de Blender y que escucha en el puerto 9876. Por eso hay dos piezas.

### Pasos manuales en tu máquina (interfaz de Blender)

Esto lo tienes que hacer tú una sola vez en tu Blender local:

1. **Descargar el addon**: baja `addon.py` del repositorio
   <https://github.com/ahujasid/blender-mcp> (está en la raíz del repo).
   En este proyecto hay una copia en `scripts/addon.py` para no depender de la red.
2. **Instalarlo en Blender**:
   - Abre Blender.
   - `Edit > Preferences > Add-ons`.
   - Botón `Install...` (arriba a la derecha), navega hasta `addon.py` y acéptalo.
   - Busca "BlenderMCP" en la lista y **marca la casilla** para activarlo.
3. **Arrancar la conexión**:
   - En la vista 3D, pulsa `N` para abrir el panel lateral (sidebar).
   - Verás una pestaña **BlenderMCP**.
   - Pulsa **Connect to Claude** (botón "Start MCP Server" según versión).
     Esto pone a Blender a escuchar en `localhost:9876`.
4. **Verificar**: abre Claude Code en este repositorio y pídele algo simple
   ("crea un cubo"). Si el addon no está conectado, el servidor MCP dará error
   de conexión al puerto 9876; vuelve al paso 3.

> Nota: el addon solo escucha mientras esa sesión de Blender está abierta.
> Si cierras Blender, repite el paso 3 (el addon queda instalado, solo hay
> que reconectar).

### Modo headless (sin interfaz, como en este entorno remoto)

Para entornos sin GUI, el addon se puede arrancar por script:

```bash
blender --background --python scripts/arrancar_servidor_headless.py
```

Ese script registra el addon y arranca el servidor en el puerto 9876, dejando
Blender vivo escuchando. Es lo que se usó aquí para la prueba de humo.

## Prueba de humo (FASE 4)

Validación de punta a punta realizada en este entorno:
6 discos de embrague (cilindros finos) alternando material metálico y carbono,
vista explosionada en el eje Z, cámara orbitando 360° en 120 frames, luz de
estudio de 3 puntos, y un frame renderizado en baja resolución con Cycles CPU
a `renders/test/`. El resultado y los detalles están en `pipeline.md` y en el
propio render de `renders/test/`.

## Notas sobre modelos CAD (GrabCAD)

- Formatos: preferir **STEP** (geometría exacta) y convertir a malla al
  importar. Blender no importa STEP de serie: usar el addon gratuito
  **STEPper** o convertir antes con FreeCAD (`File > Export > STL/OBJ`).
- STL/OBJ se importan directamente (`File > Import`).
- Guardar cada componente en `modelos/<componente>/` junto con un `fuente.md`
  con la URL de origen, autor y licencia (GrabCAD exige atribución en algunos
  casos; verificar la licencia de cada modelo antes de publicar el video).
