# Guion v1 — "El truco genial dentro de tu VHS"

- Duración objetivo: 6-7 minutos
- Público: general/joven; nostalgia para quien lo vivió, arqueología curiosa
  para quien no
- Estado: v1 (borrador). Cifras marcadas ⚠ pendientes de la verificación
  técnica (ver notas) antes del render final.

Convención: **[ESCENA]** = plano 3D Blender · **[ARCHIVO]** = metraje/foto ·
*(locución)* en cursiva.

---

## 1. Gancho (0:00 – 0:40)

**[ESCENA gancho]** Un cassette VHS girando en turntable; la trampilla se
abre y asoma la cinta.

*(locución)* "Esto es una película entera. Dos horas de imagen y sonido en
un plástico que costaba tres euros en la gasolinera. Y lo increíble no es la
cinta... es el truco que hay dentro del aparato. Un truco tan bueno que
durante treinta años nadie lo pudo superar. Hoy abrimos un VHS."

## 2. El problema (0:40 – 2:00)

**[ESCENA 2A]** Comparación visual: un cassette de audio reproduciéndose
(cinta lenta ante un cabezal fijo) junto a un contador de "datos por
segundo" — y al lado la misma idea con video, con el contador disparado.

*(locución)* "El video necesita mover muchísima más información que el
audio — cientos de veces más. Y en una cinta magnética, más información
significa más velocidad entre la cinta y el cabezal que la lee. Si el VHS
funcionara como un cassette de música, la cinta tendría que pasar a varios
metros por segundo: una película serían kilómetros de cinta. Imposible.
Salvo que le des la vuelta al problema."

**[ESCENA 2B]** La cinta acelerándose hasta lo absurdo y saliéndose
volando del carrete (momento de humor visual).

## 3. Cómo funciona (2:00 – 4:30) — bloque central

**[ESCENA 3A — la idea]** El tambor plateado inclinado, girando. La cinta
se acerca lenta y lo abraza en diagonal.

*(locución)* "La solución: si la cinta no puede correr, que corra el
cabezal. Dentro de todo VHS hay un tambor inclinado que gira a 1500
revoluciones por minuto ⚠ con dos cabezales diminutos en el borde. La cinta
avanza a paso de tortuga — dos centímetros por segundo — pero como el tambor
gira tan rápido, cada cabezal la barre a casi cinco metros por segundo ⚠.
Doscientas veces más rápido que la propia cinta."

**[ESCENA 3B — PLANO CLAVE: las franjas diagonales]** Vista cenital de la
cinta semitransparente pasando ante el tambor inclinado: cada pasada del
cabezal pinta una franja diagonal luminosa sobre la cinta. Acumulación de
cientos de franjas paralelas.

*(locución)* "Y aquí está el truco completo: como el tambor está inclinado,
cada barrido no escribe una línea recta, sino una franja en diagonal. Cada
franja diagonal es medio fotograma de tu película. La cinta corta y lenta
guarda horas de video porque su pista de verdad no es su longitud... es la
suma de miles de diagonales apretadas."

**[ESCENA 3C — la carga en M]** El VHS por dentro al pulsar play: los dos
brazos sacan la cinta del cassette y la enhebran alrededor del tambor
dibujando una M. Sonido mecánico real de archivo.

*(locución)* "¿Y ese clac-clac al meter la cinta? Son dos brazos robóticos
sacando la cinta de su carcasa y abrazándola al tambor con forma de letra M.
Cada vez que dabas al play, ocurría esta coreografía."

## 4. El detalle fino (4:30 – 5:45)

**[ESCENA 4A — azimut]** Zoom a dos franjas diagonales vecinas, pegadas sin
hueco. Los dos cabezales con sus entrehierros girados en ángulos opuestos ⚠.

*(locución)* "Las franjas van pegadas, sin separación, para no desperdiciar
ni un milímetro. ¿Y cómo evita un cabezal leer la franja de al lado? Los dos
cabezales están torcidos unos grados en sentidos opuestos. Cada uno solo ve
'su' inclinación; la vecina se le vuelve borrosa. Un filtro sin electrónica:
pura geometría."

**[ESCENA 4B — tracking]** La pista de control en el borde de la cinta y el
efecto de imagen nevada corrigiéndose (composición con archivo).

*(locución)* "¿Y el botón de tracking que tocabas cuando la imagen nevaba?
Estabas alineando los cabezales con las diagonales, guiado por una pista de
pulsos en el borde de la cinta. Ahora ya sabes qué estabas ajustando."

## 5. Cierre (5:45 – 6:30)

**[ESCENA 5A]** El VHS recomponiéndose (despiece inverso) hasta quedar
cerrado; la trampilla se cierra.

*(locución)* "Cabezales que vuelan sobre cintas lentas: el mismo truco que
usó después tu videocámara, y hasta las cintas de backup de los servidores.
Todo por no poder hacer correr una cinta. La próxima vez: su hermano
pequeño — el walkman — y el misterio del autoreverse. Suscríbete si quieres
verlo por dentro."

---

## Lista de escenas Blender

| ID | Descripción | Dificultad |
|----|-------------|------------|
| gancho | Cassette VHS en turntable, trampilla abriéndose | baja (CAD de GrabCAD probable) |
| 2A | Comparativa audio vs video con contadores | baja |
| 2B | Cinta acelerándose (humor) | media (sim de cinta) |
| 3A | Tambor inclinado girando, cinta abrazándolo | media |
| 3B | PLANO CLAVE: franjas diagonales pintándose | media |
| 3C | Carga en M animada | alta (la joya mecánica) |
| 4A | Azimut: dos cabezales torcidos, franjas vecinas | media |
| 4B | Pista de control + tracking | baja |
| 5A | Recomposición (despiece inverso) | gratis (reverse en DaVinci) |

## Pendientes para v2

- Resolver las 4 dudas de verificación de las notas técnicas (azimut, writing
  speed, inclinación del tambor, velocidades exactas PAL/NTSC) — bloquean
  las cifras marcadas ⚠ de la locución.
- Decidir PAL vs NTSC como referencia (audiencia hispanohablante: PAL en
  España, NTSC en Latinoamérica — quizá dar ambas o redondear).
- Buscar CAD del cassette VHS y del tambor en GrabCAD.
- Conseguir el sonido real de la carga en M (grabarlo de un VHS real o
  archivo libre).
