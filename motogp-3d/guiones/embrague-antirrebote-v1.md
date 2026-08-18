# Guion v1 — "El embrague que sabe frenar: así funciona el antirrebote de MotoGP"

- Duración objetivo: 6-8 minutos
- Público: aficionado a MotoGP con curiosidad técnica, sin formación en ingeniería
- Estado: v1 (borrador para revisión)

Convención: **[ESCENA]** = plano 3D a producir en Blender · **[ARCHIVO]** =
metraje/foto de archivo o gráfico 2D en DaVinci · *(locución)* en cursiva.

---

## 1. Gancho (0:00 – 0:40)

**[ARCHIVO]** Onboard de una frenada fuerte de MotoGP (final de recta),
sonido de reducciones rapidísimas.

*(locución)* "340 kilómetros por hora. El piloto frena, baja cuatro marchas
en menos de dos segundos... y la rueda trasera no rebota, no se bloquea, no
se cruza. Eso no lo consigue el piloto solo: dentro del motor hay una pieza
que decide, miles de veces por vuelta, cuánta fuerza puede pasar. Hoy la
abrimos por dentro."

**[ESCENA gancho]** Embrague completo girando en turntable, iluminación de
estudio, título sobreimpreso.

## 2. El problema (0:40 – 2:00)

**[ARCHIVO]** Ejemplo de rueda trasera rebotando/cruzándose en una frenada
(motos clásicas o supersport sin antirrebote).

*(locución)* "Cuando cortas gas y reduces, el motor deja de empujar y pasa a
frenar: es el freno motor. Todo ese par entra a la rueda trasera al revés de
lo normal. Si es demasiado, la rueda no puede seguirle el ritmo al motor:
salta, rebota, y la moto se vuelve inestable justo donde más estabilidad
necesitas, entrando en la curva."

**[ESCENA 2A]** Esquema 3D simplificado moto + cadena de transmisión con
flechas de par: verde (motor→rueda, aceleración) y roja (rueda→motor,
frenada). Invertir la flecha al cortar gas.

## 3. Cómo funciona (2:00 – 4:30) — bloque central

**[ESCENA 3A — despiece]** Vista explosionada axial del embrague completo:
campana, paquete de discos alternados (fricción/lisos), cubo partido en dos
mitades, plato de presión, muelles. Cada pieza se etiqueta al separarse.

*(locución)* "Un embrague normal es un sándwich de discos apretados por
muelles. Mientras están apretados, motor y rueda van solidarios. El
antirrebote añade un truco: el cubo central está partido en dos mitades, y
entre ellas hay unas rampas inclinadas con bolas."

**[ESCENA 3B — la rampa, plano clave]** Zoom extremo a una pareja de rampas
con su bola. Animar dos casos con el mismo encuadre:
1. **Acelerando**: las mitades empujan por la cara plana → no pasa nada →
   los discos siguen comprimidos (mostrar paquete apretado, tinte verde).
2. **Frenando**: el par se invierte, una mitad gira unos grados respecto a
   la otra → la bola **sube la rampa** → las mitades se separan axialmente →
   el plato de presión se levanta y los discos se descargan (tinte rojo,
   discos con holgura visible).

*(locución)* "En aceleración, las rampas empujan de plano: el embrague
aprieta con toda su fuerza. Pero cuando el par viene al revés, la bola sube
por la cuesta y hace de cuña: separa el plato y afloja el sándwich. El
embrague patina lo justo, deja pasar solo el freno motor que la rueda puede
digerir, y en cuanto las velocidades se igualan, vuelve a cerrarse solo. Es
una válvula de fuerza con un solo sentido."

**[ESCENA 3C — sección]** Corte longitudinal del embrague montado (media
campana oculta): ver los discos comprimirse y soltarse en contexto durante
una secuencia acelerar → frenar → acelerar.

## 4. El detalle fino (4:30 – 6:00)

**[ESCENA 4A]** Dos rampas lado a lado con ángulos distintos (suave vs
pronunciada), misma animación de bola.

*(locución)* "¿Y cuánto patina? Eso lo decide el ángulo de la rampa. Los
fabricantes de competición las mecanizan a la carta — 35 grados, 45 grados —
y con eso eligen cuánto freno motor llega a la rueda. Rampa suave: se abre
enseguida, entrada de curva muy dócil. Rampa pronunciada: aguanta más par,
más freno motor disponible."

**[ESCENA 4B]** Paquete de discos con material carbono (el de nuestra
prueba de humo, refinado).

*(locución)* "En MotoGP el embrague es seco y de discos de carbono: menos
diámetro, menos inercia, y aguanta temperaturas que fundirían uno de calle.
Y la mecánica no trabaja sola: la electrónica de freno motor afina lo que la
rampa hace a lo bruto."

## 5. Cierre (6:00 – 7:00)

**[ESCENA 5A]** Montaje inverso: la vista explosionada se recompone hasta el
embrague cerrado girando en turntable.

*(locución)* "La próxima vez que veas una frenada al límite, acuérdate de la
bola subiendo su rampa miles de veces por carrera. De eso van estas piezas:
problemas brutales, soluciones elegantes. Si quieres que abramos otra —el
cambio seamless, el dispositivo de salida— dilo en los comentarios."

---

## Lista de escenas Blender derivada (para `escenas/embrague-antirrebote/`)

| ID | Descripción | Scripts implicados |
|----|-------------|--------------------|
| gancho | Turntable del conjunto completo | turntable, materiales, luces |
| 2A | Moto esquemática + flechas de par | (modelado simple propio) |
| 3A | Explosionado axial etiquetado | vista_explosionada |
| 3B | Rampa + bola, dos sentidos (PLANO CLAVE) | animación específica |
| 3C | Sección con discos en contexto | booleana de corte |
| 4A | Comparativa de ángulos de rampa | variante de 3B |
| 4B | Discos carbono detalle | materiales |
| 5A | Recomposición (explosionado inverso) | vista_explosionada (animar) |

## Pendientes para v2

- Ajustar tiempos de locución leyéndola en voz alta (objetivo <7 min).
- Verificar la duda técnica anotada en `investigacion/embrague-antirrebote/notas-tecnicas.md`
  (geometría de rampas en los embragues de carbono de MotoGP).
- Decidir metraje de archivo disponible/derechos para el gancho y la escena 2.
- Conseguir modelo CAD del cubo con rampas (GrabCAD) o modelarlo desde cero.
