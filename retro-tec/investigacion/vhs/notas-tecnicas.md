# Notas técnicas — VHS: cómo se escribe video en una cinta

## El problema que resuelve (el corazón del video)

Una señal de video analógica necesita un ancho de banda ~300 veces mayor que
el audio. En una cinta magnética, más ancho de banda = más velocidad relativa
entre cabezal y cinta. Si el VHS lo resolviera "a lo cassette" (cabezal fijo,
cinta rápida), la cinta tendría que correr a **varios metros por segundo**:
una película de 2 horas necesitaría kilómetros de cinta.

**La solución genial: mover el cabezal, no la cinta.** La cinta avanza
lentísima (~2,3 cm/s) pero los cabezales van montados en un **tambor
inclinado que gira a 1500 rpm (PAL) / 1800 rpm (NTSC)**. La velocidad
relativa cabezal-cinta resultante es de **≈4,9 m/s** — unas 200 veces la
velocidad lineal de la cinta. (⚠ verificar cifra exacta de writing speed
en manual de servicio antes del render final.)

## Barrido helicoidal (helical scan)

- La cinta (media pulgada, 12,7 mm) abraza **algo más de 180°** del tambor
  (~62 mm de diámetro), guiada de forma oblicua por guías inclinadas.
- Como el tambor está **inclinado** respecto al recorrido de la cinta, cada
  pasada de un cabezal escribe una **franja diagonal** sobre la cinta, no una
  línea horizontal.
- Cada franja diagonal = **un campo de video** (medio fotograma). Dos
  cabezales opuestos en el tambor se alternan: uno escribe un campo, el
  siguiente el otro.
- Resultado: una cinta corta y lenta almacena horas de video porque la
  "pista" real es la suma de miles de diagonales muy juntas.

## Carga en M (M-loading)

Al pulsar play, dos brazos con postes **sacan la cinta del cassette** y la
enhebran alrededor del tambor y del resto del transporte dibujando
aproximadamente una **letra M**. (Betamax usaba carga en U; comparación
posible en el video.) Este es el "clac-clac" mecánico al meter una cinta:
oro puro para la animación 3D.

## Grabación con azimut inclinado (por qué caben tantas pistas)

- Las pistas diagonales van **pegadas unas a otras sin banda de guarda**.
- Para que un cabezal no "lea" la pista vecina, los dos cabezales están
  montados con el entrehierro girado en ángulos opuestos (**azimut ±6°**;
  ⚠ fuentes discrepan entre ±6° y ±7° — verificar con manual/patente JVC
  antes del render). La pista vecina, grabada con el azimut contrario, se
  atenúa por interferencia al leerla: filtrado mecánico, sin electrónica.

## Las otras pistas (bordes de la cinta)

- **Pista de control** (borde inferior): pulsos lineales que sincronizan el
  servo del cabrestante para que los cabezales caigan exactamente sobre las
  diagonales (el "tracking" que se ajustaba cuando la imagen nevaba).
- **Pista de audio lineal** (borde superior): mono/estéreo de baja calidad;
  el Hi-Fi posterior grabó el audio en profundidad bajo el propio video
  (depth multiplex, tema para mención breve).

## Transporte

- **Cabrestante (capstan) + rodillo de presión (pinch roller)**: el eje fino
  girando contra el rodillo de goma es lo que fija la velocidad de la cinta
  (2,34 cm/s en PAL SP; ⚠ confirmar decimales). Los platos de los carretes
  solo recogen holgura — NO tiran de la cinta. (Mismo principio que el
  cassette de audio: investigación reutilizable para ese video.)

## Piezas para el despiece 3D

Cassette (carcasa + 2 carretes + trampilla), brazos de carga con postes,
tambor inclinado con 2 cabezales, guías oblicuas, cabrestante + rodillo,
cabezal fijo de audio/control, cabezal de borrado.

## Dudas a verificar — RESUELTAS (2026-08-18, ver referencias)

- [x] **Azimut: ±6°** confirmado (la cifra de ±7° corresponde a otros
      formatos, p. ej. Betamax). Fuente: norma y literatura de azimuth
      recording.
- [x] **Velocidad lineal SP**: PAL 2,339 cm/s; NTSC 3,335 cm/s. Confirmado.
- [x] **Tambor: 62,00 mm ±0,01 de diámetro** — fijado por la norma
      EN 60774-1 (estándar internacional del VHS). Writing speed derivada:
      perímetro 194,8 mm × 25 rps (PAL) ≈ **4,87 m/s**; × 30 rps (NTSC)
      ≈ **5,84 m/s**. En locución: "casi cinco metros por segundo" (PAL) es
      correcto; ~208× la velocidad lineal PAL.
- [x] **Anchura de pista SP**: PAL 49 µm; NTSC 58 µm. Confirmado.
- [ ] (Opcional, no aparece en locución) Ángulo exacto de inclinación de
      pista respecto al borde de la cinta (~5°58' según literatura); solo
      haría falta si un rótulo lo cita.
