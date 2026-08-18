# Notas técnicas — Embrague antirrebote (slipper clutch / back-torque limiter)

## El problema que resuelve

Al frenar fuerte y reducir varias marchas seguidas (entrada a curva en
MotoGP), el freno motor aplica un par inverso ("back torque") enorme sobre la
rueda trasera a través de la transmisión. Consecuencias sin mitigar:

1. **Rebote de la rueda trasera** (wheel hop / chatter): la rueda pierde y
   recupera adherencia a golpes; la moto se vuelve inestable justo cuando el
   piloto está tumbando.
2. **Sobrerrevolucionado del motor** al soltar embrague tras una reducción
   agresiva.
3. **Bloqueo parcial de la rueda trasera** y derrapes de entrada no deseados.

## Componentes clave (para el despiece 3D)

- **Campana / cesta (clutch basket)**: recibe el par del cigüeñal vía la
  transmisión primaria. Aloja los discos conductores.
- **Discos de fricción y discos lisos** alternados (en MotoGP, paquete
  carbono/carbono; en calle, orgánicos en baño de aceite).
- **Cubo interior (inner hub)**: conectado al eje de entrada del cambio.
  En un slipper se divide en **dos piezas** enfrentadas.
- **Rampas con bolas o tetones (ball & ramp / dog & ramp)**: mecanizadas
  entre las dos mitades del cubo. Son el corazón del mecanismo.
- **Plato de presión (pressure plate)** y muelles (o muelle de diafragma).

## Funcionamiento (las dos direcciones del par)

**Tracción normal (motor → rueda):** las superficies de arrastre de las dos
mitades del cubo empujan en el sentido "plano" de las rampas; el paquete de
discos queda comprimido con toda la fuerza de los muelles y el embrague
transmite el par íntegro, como uno convencional.

**Retención (rueda → motor, frenada):** el par inverso hace que una mitad del
cubo gire ligeramente respecto a la otra; las bolas/tetones **suben por las
rampas inclinadas** y esa cuña genera una fuerza axial que **separa el plato
de presión**, descargando los discos. El embrague patina de forma controlada
hasta que las velocidades de motor y rueda se igualan, y entonces vuelve a
cerrar solo.

Idea fuerza para el video: el embrague antirrebote es una **válvula de par
unidireccional**: aprieta en un sentido, afloja proporcionalmente en el otro.

## Parámetros de diseño (nivel detalle del video)

- **Ángulo de rampa**: define cuánto par inverso hace falta para abrir.
  Referencia real: STM comercializa rampas de 35° y 45° — más ángulo, más
  freno motor llega a la rueda; menos ángulo, apertura más fácil.
- **Precarga de muelles**: umbral base de apertura; se ajusta por tarado.
- En MotoGP se combina con la **gestión electrónica del freno motor**
  (engine brake control): el slipper es la protección mecánica y la
  electrónica afina el resto.
- Embrague MotoGP: seco, multidisco **carbono/carbono**, diámetro pequeño y
  poca inercia (AP Racing/Brembo es proveedor habitual de la parrilla).

## Guion visual (ideas de animación)

1. Vista explosionada axial de todo el paquete (campana → discos → cubo
   partido con rampas → plato de presión).
2. Zoom a una rampa con su bola: animar los dos sentidos de giro relativo
   (plano = aprieta / cuña = separa). Es EL plano clave del video.
3. Sección de la campana con los discos comprimiéndose y descargándose
   (transparencia u ocultación de media campana).
4. Contexto: moto frenando fuerte de 340 km/h con reducciones — comparar
   rueda con rebote (sin slipper) vs estable (con slipper).

## Dudas a verificar antes del guion v2

- Confirmar si el paquete carbono/carbono de MotoGP usa la misma geometría de
  rampas que los STM comerciales o mecanismo propio de cada fábrica.
- Buscar despiece real (foto o CAD) de un cubo partido con rampas para
  modelar la geometría con fidelidad.
