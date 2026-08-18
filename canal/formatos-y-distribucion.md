# Formatos y distribución — Canal "Cómo funciona"

## Principio: un render, todos los idiomas

**Regla de oro: ningún texto quemado en los renders 3D.** Ni etiquetas, ni
cifras, ni títulos dentro de la imagen renderizada. Todo texto se añade en
DaVinci en capas propias (o como subtítulo). Así el mismo render sirve para
español, inglés o cualquier idioma sin volver a renderizar, que es la parte
cara.

Consecuencia para las locuciones del guion: donde el guion diga "cada pieza
se etiqueta al separarse", la etiqueta es un rótulo de montaje, no parte de
la escena 3D.

## Subtítulos (internacionalización sin doblaje)

1. La locución se graba en español a partir del guion versionado.
2. Del guion (que ya es el texto exacto) se genera el `.srt` en español —
   los tiempos se ajustan una vez en DaVinci.
3. Claude traduce el `.srt` a inglés (y los idiomas que se decidan)
   manteniendo los tiempos: `guiones/<tema>-subs-es.srt`, `-subs-en.srt`...
4. En YouTube se suben todas las pistas de subtítulos; el video es uno solo.
5. Los shorts llevan subtítulos incrustados grandes (es la convención del
   formato y se ven sin audio), en versión por idioma — regenerarlos es
   barato porque el short reutiliza render existente.

Ventaja extra: el guion versionado en markdown ES la fuente de los
subtítulos — no hay transcripción manual.

## Shorts / píldoras (vertical 9:16, 30-60 s)

Cada video largo debe generar **2-3 shorts** con su plano clave:

- El short no es un recorte del video: es el mecanismo central contado en
  una frase. Ejemplo VHS: "La cinta va lentísima. El truco es que el cabezal
  vuela." + escena 3B vertical.
- Render vertical nativo (1080×1920): NO reencuadrar el 16:9 — se rehace el
  encuadre de cámara para vertical (los generadores de escena lo permiten
  cambiando resolución y cámara; coste de render similar por plano corto).
- Estructura: gancho visual inmediato (0-2 s) → mecanismo (hasta ~40 s) →
  remate + "el video completo en el canal".
- Los shorts se planifican en el guion (columna "short candidato" en la
  lista de escenas) para renderizar la variante vertical en la misma tanda
  que la horizontal.

## Checklist de distribución por video (se suma al pipeline)

- [ ] Render horizontal final (video largo)
- [ ] 2-3 renders verticales de planos clave (shorts)
- [ ] SRT español desde el guion + ajuste de tiempos en DaVinci
- [ ] SRT inglés (+ otros idiomas decididos) traducidos del español
- [ ] Miniatura (sin texto o con texto en capa editable, por idioma si aplica)
- [ ] Título y descripción en ES + EN
