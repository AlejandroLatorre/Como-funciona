# Inventario de decisiones cerradas en Zestiqa (candidatas para un modelo solo-decisión como Jev)

Alcance: repositorio `/home/user/voices-sells` en el commit `10ca5a7` ("El árbitro de la apertura va por OpenRouter", 30-09-2026). Solo lectura. Todas las citas son `ruta:línea` dentro de ese repositorio. Por "decisión cerrada" se entiende una salida tipada: una opción entre varias, una nota en una escala o un sí/no. Se distingue en cada caso si la misma llamada al modelo produce **además** texto libre que un modelo solo-decisión no podría escribir.

Leyenda de ruta: **RT-crítica** = el comercial espera ese resultado antes de oír al comprador; **RT-2º plano** = durante la llamada pero sin bloquear el turno; **Post** = al colgar o fuera de la llamada; **Offline** = scripts y bancos de prueba.

---

## 1. ¿Qué decisiones cerradas toma hoy un MODELO durante la llamada de voz?

### Takeaway
Solo hay una decisión de modelo "de juicio" dentro de la llamada: el **árbitro de la apertura** (sube/baja/igual + regla + objeción disparada), que corre con `gpt-4.1-mini` en segundo plano, una vez por turno del comercial, y además devuelve un `motivo` en texto libre que se inyecta en el prompt del comprador. Las otras dos decisiones de modelo en tiempo real son el **detector de fin de turno** de LiveKit y el **VAD Silero**, que ya son clasificadores especializados. El pinganillo (coach) también corre durante la llamada, pero su salida es sobre todo texto.

### Cited Findings

**1.1 Árbitro de la apertura (`consultar_arbitro` / `Apertura.arbitrar`)**
- Modelo: `MODELO_ARBITRO`, por defecto `gpt-4.1-mini`; se eligió "SIN razonamiento a proposito: ... hace falta que vuelva pronto y no cueste nada". — [agente-voz/agente.py:1105-1109](/home/user/voices-sells/agente-voz/agente.py)
- Proveedor: OpenRouter primero cuando hay `OPENROUTER_API_KEY` (el nombre se convierte en `openai/gpt-4.1-mini`); si no, OpenAI directo; sin ninguna de las dos claves devuelve `None`. El cambio es del 30-09-2026: con la cuenta de OpenAI sin crédito el árbitro "fallaba en TODOS los turnos" y en una llamada el comprador "paso trece turnos en el nivel 0, no solto ni una de sus cinco objeciones y colgo por estancamiento". — [agente-voz/agente.py:1112-1138](/home/user/voices-sells/agente-voz/agente.py)
- Salida exacta pedida (JSON, `response_format: json_object`, `temperature: 0`, `max_tokens: 120`, timeout 12 s): `{"movimiento":"sube|baja|igual","regla":"S1..S5 o B1..B4, o vacio si es igual","objecion":"O1..On o vacio","motivo":"en segunda persona y en una linea, que hizo el comercial"}`. — [agente-voz/agente.py:1196-1227](/home/user/voices-sells/agente-voz/agente.py)
- Por tanto son **tres decisiones cerradas en una sola llamada**: (a) movimiento, elección entre 3; (b) regla, elección entre ~4-5 S más ~4 B (o vacío); (c) objeción disparada, elección entre N objeciones pendientes del escenario más "ninguna". Y un campo de **texto libre** (`motivo`). — [agente-voz/agente.py:1167-1200](/home/user/voices-sells/agente-voz/agente.py)
- Entradas: la frase del comercial, la última frase del comprador (`pregunta`), las listas `sube`/`baja` de la ficha y los disparadores de las objeciones pendientes. Pasar también la frase del comprador fue una corrección: sin ella "tres de los cinco disparadores son imposibles de juzgar" y en una llamada real "el nivel no se movio ni una vez en seis turnos" mientras el banco decía 11 de 12. — [agente-voz/agente.py:1145-1165](/home/user/voices-sells/agente-voz/agente.py); la frase del comprador se saca del contexto del turno en [agente-voz/agente.py:1964-1972](/home/user/voices-sells/agente-voz/agente.py)
- Las listas S/B dependen del **foco** del personaje (resultado / relación / detalle): 4 reglas "sube" y 4 "baja" por foco, más un juego genérico de 5 "sube" para escenarios antiguos. — [src/voz/focos.ts:40-115](/home/user/voices-sells/src/voz/focos.ts); se meten en la ficha en [src/app/api/sesiones/[id]/ficha/route.ts:70-79](/home/user/voices-sells/src/app/api/sesiones/[id]/ficha/route.ts)
- Incoherencia detectada en el prompt: dice "Comprueba LAS CINCO" y "S1..S5", pero con foco las listas tienen 4 reglas. — [agente-voz/agente.py:1170-1177](/home/user/voices-sells/agente-voz/agente.py) frente a [src/voz/focos.ts:48-58](/home/user/voices-sells/src/voz/focos.ts)
- Ruta: **RT-2º plano**. Se lanza con `asyncio.create_task` desde `on_user_turn_completed` y **no se espera**: su veredicto mueve el nivel para el turno *siguiente*. El hook está en la ruta crítica y "el framework le mide el retraso". — [agente-voz/agente.py:1974-1978](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1653-1661](/home/user/voices-sells/agente-voz/agente.py)
- Frecuencia: una vez por turno del comercial que no sea despedida (en los turnos de despedida no se arbitra). — [agente-voz/agente.py:1944-1962](/home/user/voices-sells/agente-voz/agente.py)
- Lógica de código alrededor del veredicto: la misma regla no puede subir dos turnos seguidos (`sube_repetida`); si a la vez sube y se dispara una objeción "larga", gana la subida y la larga se aplaza; durante el cierre se ignora la objeción; si falla la llamada, el nivel no se mueve y el contador de estancamiento suma 1. — [agente-voz/agente.py:1664-1765](/home/user/voices-sells/agente-voz/agente.py)
- Uso del texto libre `motivo`: se guarda en `self._recien` y al turno siguiente se inyecta al comprador como "Acaba de ganarselo: {motivo} Que se NOTE en este turno". También va a los eventos de traza `sube` y `baja`. — [agente-voz/agente.py:1742-1753](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1566-1574](/home/user/voices-sells/agente-voz/agente.py)
- Niveles de apertura: 0 a 3 (el diagnóstico habla de "apertura X de 3"); el avance del estancamiento es AVISO=3 y LIMITE=5 turnos quieto. — [agente-voz/agente.py:1385-1386](/home/user/voices-sells/agente-voz/agente.py), [src/diagnostico/escenarios.ts:143](/home/user/voices-sells/src/diagnostico/escenarios.ts)

**1.2 Sonda del árbitro (`sonda_arbitro`)**
- Una vez por proceso, al precalentar, se ejecuta el árbitro con una frase fija ("Serian veintiocho euros al mes por doscientos mil de capital.") y se exige `movimiento == "sube"`. Si falla, lo registra como error pero no tumba el worker. — [agente-voz/agente.py:1140-1266](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1077](/home/user/voices-sells/agente-voz/agente.py)

**1.3 Detector de fin de turno y VAD**
- `turn_detection=TurnDetector()` (de `livekit.agents.inference`): "este modelo mira lo que has dicho y decide si has terminado la frase o solo has hecho una pausa". Es un sí/no en la **ruta RT-crítica**, en cada pausa del comercial. Endpointing: mínimo 0,2 s y máximo 1,2 s (`ENDPOINTING_MIN/MAX`). Además `preemptive_generation=True`. — [agente-voz/agente.py:36](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:2072-2081](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:348-349](/home/user/voices-sells/agente-voz/agente.py)
- VAD Silero cargado una vez por proceso. — [agente-voz/agente.py:1079](/home/user/voices-sells/agente-voz/agente.py)
- En modo s2s (`MOTOR_COMPRADOR=s2s`) ni el VAD ni el detector de turno propios se usan: el modelo realtime lo hace todo. — [agente-voz/agente.py:2054-2061](/home/user/voices-sells/agente-voz/agente.py)

**1.4 Pinganillo / coach (modo entrenamiento)**
- Modelo `MODELO_COACH`, por defecto `gemini-3.1-flash-lite` (~1 s; "El flash normal tarda 15-30 s y mata el tiempo real (medido 24-08-2026)"). Sin respaldo: sin `GEMINI_API_KEY` lanza un error. — [src/entrenamiento/coach.ts:32-34](/home/user/voices-sells/src/entrenamiento/coach.ts), [src/entrenamiento/coach.ts:79-98](/home/user/voices-sells/src/entrenamiento/coach.ts)
- Salida: `lectura` (texto), `jugadas` (1-3 textos), `alerta` (texto o null) y `bien` (texto o null). Las dos últimas llevan dentro un **sí/no implícito** ("¿la última intervención tiene un error claro?" / "¿hizo algo claramente bueno?"), pero el valor es la frase. — [src/entrenamiento/coach.ts:14-28](/home/user/voices-sells/src/entrenamiento/coach.ts)
- Frecuencia: se dispara con cada fragmento de transcripción, con un rebote de 1,2 s y un mínimo de 6 s entre consultas; solo si el escenario tiene la asistencia activada. — [src/app/sesion/[id]/conversacion.tsx:354-376](/home/user/voices-sells/src/app/sesion/[id]/conversacion.tsx)

**1.5 Cerebro del comprador (NO es una decisión cerrada, se anota como contexto)**
- `MODELO_COMPRADOR_TEXTO`, por defecto `gpt-4.1` (OpenAI directo si el nombre empieza por `gpt-`; si no, OpenRouter). Genera el habla del personaje y puede llamar a la herramienta `colgar(motivo)`, que es una decisión binaria implícita dentro de la generación. — [agente-voz/agente.py:118-133](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:369-407](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1984-1995](/home/user/voices-sells/agente-voz/agente.py)
- Latencia medida que justifica que el cerebro no razone: gpt-5 en razonamiento low daba "4 s de mediana y 9,4 de cola hasta la primera palabra, el 70-85% de la espera de cada turno (el oido pone 578 ms y la voz 91 ms)". — [agente-voz/agente.py:118-123](/home/user/voices-sells/agente-voz/agente.py)

### Inferences
- El árbitro es el candidato más claro para Jev: sus tres salidas son exactamente una Choice (3 opciones), otra Choice (≈9 reglas) y otra Choice (N objeciones + ninguna). Pero el `motivo` en texto libre se usa en el prompt del comprador; con Jev habría que sustituirlo por una plantilla derivada de la regla elegida (por ejemplo, el propio texto de la regla S*i* de `focos.ts`) o quedarse sin él.
- Como el árbitro ya corre en segundo plano, la velocidad de Jev no reduce la espera que percibe el comercial. Lo que sí ganaría es el desfase de un turno (si respondiera antes de que el cerebro empiece a generar, podría llegar a aplicarse en el *mismo* turno) y coste. La ventaja principal sería el coste por turno y la **probabilidad calibrada**, que permitiría umbrales ("solo sube si P(sube) > x") en lugar del voto duro actual.
- La decisión de objeción (O1..On) es una Choice con opciones que **cambian por escenario** (disparadores en texto libre escritos por el generador), en castellano coloquial y con fragmentos de transcripción. Es justo el terreno donde "más flojo en español" pesa más.
- El detector de turno ya es un clasificador especializado y rápido en la ruta crítica; sustituirlo por una llamada de red a un servicio externo probablemente empeoraría la latencia. No es un buen candidato.

### Gaps
- No hay latencia ni coste del árbitro registrados en el repositorio: `agente-voz/agente.log` y `latencia.log` están vacíos (0 líneas) y la tabla de precios `src/lib/precios.ts` no tiene partida para el árbitro (solo voz, oído, cerebro, evaluador y sala). El banco `npm run arbitro` imprime la mediana y el peor caso en ms, pero no hay ninguna ejecución guardada.
- No he comprobado qué modelo exacto hay detrás de `livekit.agents.inference.TurnDetector` ni si está afinado para español.

---

## 2. ¿Qué decisiones cerradas toma el CÓDIGO (heurísticas) durante la llamada, que un modelo podría complementar?

### Takeaway
Hay cinco heurísticas deterministas en la ruta crítica del turno (insulto, paso concreto, despedida, cierre de cortesía y "larga"), más una de extracción de pregunta y un contador de estancamiento. Existen justamente porque el árbitro llega un turno tarde. Todas son listas de palabras o regex en español, con fallos documentados de cobertura. Serían sí/no ideales para un modelo rápido si su latencia cabe en el hook síncrono.

### Cited Findings
- **`parece_falta_de_respeto(texto) -> bool`**: lista cerrada de insultos. Deja fuera a propósito "joder", "coño", "hostia" y "mierda", porque en España son muletillas. Se ejecuta de forma **síncrona en la ruta crítica** en cada turno ("el arbitro contesta un turno tarde, y para esto un turno tarde es tardisimo"). Si da positivo, fuerza a colgar. — [agente-voz/agente.py:1771-1808](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1487-1499](/home/user/voices-sells/agente-voz/agente.py)
- **`parece_paso_concreto(texto) -> bool`**: exige canal (WhatsApp, correo, "te llamo"...) Y momento (regex "a las", "mañana", día de la semana...). Dicho dos veces, se activa el modo cierre (`cierre_acordado`). Ruta crítica, en cada turno. — [agente-voz/agente.py:1837-1858](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1505-1514](/home/user/voices-sells/agente-voz/agente.py)
- **`parece_despedida(texto) -> bool`** (+ `cierre_de_cortesia`): marcadores en los últimos 90 caracteres y sin pregunta detrás, o un turno de al menos 60 caracteres que acaba en una fórmula de cortesía. Tiene historia de fallos: una despedida real de 113 caracteres no se detectaba con el tope antiguo de 90. Ruta crítica. Si da positivo, se salta el árbitro y se ordena colgar. — [agente-voz/agente.py:1861-1899](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1812-1834](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1944-1962](/home/user/voices-sells/agente-voz/agente.py)
- **`es_una_larga(objecion) -> bool`**: ¿la pega "cierra la puerta" ("ahora no", "mándamelo", "no me interesa"...)? Lista ampliada tras fallos ("no estoy con ese tema" faltaba el 03-09-2026). Se aplica a textos de objeción del escenario, no a la voz. — [agente-voz/agente.py:1268-1321](/home/user/voices-sells/agente-voz/agente.py). La misma lista se mide en transcripciones en [src/diagnostico/tells.ts](/home/user/voices-sells/src/diagnostico/tells.ts) ("Mismas marcas que es_una_larga()").
- **`acusar_pregunta(texto) -> str`**: saca la última pregunta del comercial con regex (`?`) y obliga al comprador a acusarla. La decisión implícita ("¿hizo el comercial una pregunta directa?") es un sí/no basado en el signo `?`, que depende de la puntuación del STT. — [agente-voz/agente.py:1324-1356](/home/user/voices-sells/agente-voz/agente.py)
- **Estancamiento**: contador de turnos sin subir; a los 3 avisa y a los 5 ordena colgar. Es código puro alimentado por el árbitro. — [agente-voz/agente.py:1581-1606](/home/user/voices-sells/agente-voz/agente.py)
- **Los dos primeros turnos van sin directriz de nivel**. — [agente-voz/agente.py:1529-1556](/home/user/voices-sells/agente-voz/agente.py)

### Inferences
- Estas heurísticas son sí/no en la ruta crítica. Jev podría complementarlas como segunda opinión (por ejemplo, "¿es despedida?" con probabilidad) solo si su latencia de red + inferencia es claramente menor que el presupuesto del hook. El framework suma ese retraso a la espera del comercial, y hoy la espera ya incluye ~578 ms de oído. Una opción razonable: la heurística decide en síncrono y Jev solo corrige en segundo plano, o se usa Jev offline para auditar los falsos negativos de las listas.
- `parece_falta_de_respeto` y `parece_despedida` son los casos con más valor: los comentarios del código documentan varios falsos negativos en llamadas reales, y el coste de un error es alto (seguir vendiendo tras un insulto, reabrir tras una despedida).

### Gaps
- No hay banco de pruebas con casos etiquetados para estas heurísticas (sí lo hay para el árbitro). La verificación de `hoy/reglas.ts` en `npm run pruebas` es de otra cosa.

---

## 3. ¿Qué decisiones cerradas se toman DESPUÉS de la llamada o fuera de ella?

### Takeaway
Al colgar, el evaluador (el modelo caro, `gpt-6-astra`) mezcla muchas decisiones cerradas (superado sí/no, 5 notas de 1 a 5, enums de objeciones y reglas, recuentos) con mucho texto libre. El crítico decide "apta sí/no" por cada recomendación, pero también reescribe. Hay otras decisiones cerradas más limpias: el diagnóstico de escenarios (`hay_problema` + `campo`), el juez de carácter (foco × dificultad, solo offline) y umbrales de embeddings. Casi todo tiene la decisión pegada a texto.

### Cited Findings

**3.1 Evaluador de la llamada (una vez por llamada, Post, el comercial espera en la pantalla de resultado)**
- Cadena con respaldo: OpenAI (`MODELO_EVALUADOR_OPENAI`, defecto `gpt-6-astra`) > Claude (`MODELO_EVALUADOR_CLAUDE`, defecto `claude-opus-5`) > OpenRouter (`MODELO_OPENROUTER`, defecto `anthropic/claude-opus-5`) > Gemini (`MODELO_EVALUADOR_GEMINI`, defecto `gemini-3.6-flash`). — [src/evaluacion/index.ts:10-18](/home/user/voices-sells/src/evaluacion/index.ts), [src/lib/openai-texto.ts:24-40](/home/user/voices-sells/src/lib/openai-texto.ts), [src/evaluacion/claude.ts:8](/home/user/voices-sells/src/evaluacion/claude.ts), [src/evaluacion/gemini.ts:10](/home/user/voices-sells/src/evaluacion/gemini.ts), [src/lib/openrouter.ts:11-12](/home/user/voices-sells/src/lib/openrouter.ts)
- `gpt-6-astra` es "el UNICO sitio del producto con el modelo caro (10 $/M de entrada, 50 $/M de salida)". — [src/lib/openai-texto.ts:24-38](/home/user/voices-sells/src/lib/openai-texto.ts)
- Decisiones cerradas dentro del JSON: `superado: boolean`; `dimensiones[].puntuacion` de 1 a 5 (5 dimensiones por defecto: apertura, descubrimiento, propuesta, objeciones, cierre); `preguntas_abiertas` / `preguntas_cerradas` (enteros ≥0); `objeciones[].manejo` ∈ {resuelta, parcial, esquivada, no_salio}; `reglas_empresa[].cumplimiento` ∈ {cumplida, incumplida, no_aplico}; `preguntas_sin_responder[].veces` ≥1. — [src/evaluacion/tipos.ts:11-157](/home/user/voices-sells/src/evaluacion/tipos.ts), [src/evaluacion/forma-json.ts:1-24](/home/user/voices-sells/src/evaluacion/forma-json.ts), [src/lib/rubrica-defecto.ts:8-49](/home/user/voices-sells/src/lib/rubrica-defecto.ts)
- Texto libre en la misma llamada: `veredicto`, cada `justificacion`, `momentos_clave` (cita + alternativa), `aciertos`, `contradicciones`, `para_la_proxima`, `sobre_la_anterior` y comentarios. — [src/evaluacion/forma-json.ts:5-18](/home/user/voices-sells/src/evaluacion/forma-json.ts)
- `superado` no tiene un criterio explícito en el prompt más allá de "Decide si supero el objetivo del escenario y explica el veredicto en una o dos frases". — [src/evaluacion/prompt.ts:190](/home/user/voices-sells/src/evaluacion/prompt.ts)
- Entradas: escenario, rúbrica, transcripción con minutos, métricas objetivas, traza del motor, historial del comercial, calibración de la empresa (correcciones del manager), argumentario, paso de la ruta y sector. — [src/evaluacion/ejecutar.ts:94-113](/home/user/voices-sells/src/evaluacion/ejecutar.ts)
- Coste registrado: tokens del evaluador sumados a la sesión; "el critico gasta tokens aparte y todavia no los devuelve, asi que el coste del analisis sale corto". — [src/evaluacion/ejecutar.ts:114-122](/home/user/voices-sells/src/evaluacion/ejecutar.ts)
- Métricas objetivas (no LLM): calculadas por código y mostradas como "medido, sin interpretacion". — [src/evaluacion/metricas.ts:1-15](/home/user/voices-sells/src/evaluacion/metricas.ts)

**3.2 Crítico de recomendaciones (Post, N llamadas en paralelo por evaluación: una por momento clave, 2-5, + "para la próxima")**
- Modelo `MODELO_CRITICO`, defecto `gpt-4.1`, **solo por OpenAI** (`llamarOpenAI`), sin cadena de respaldo; si una revisión falla, la recomendación pasa sin revisar. — [src/evaluacion/critico.ts:19-25](/home/user/voices-sells/src/evaluacion/critico.ts), [src/evaluacion/critico.ts:188-204](/home/user/voices-sells/src/evaluacion/critico.ts)
- Salida: `{apta: boolean, motivo: string, corregida: string|null}`. La decisión real tiene tres valores: ok / corregida / eliminada. Comprueba una **lista cerrada de 7 criterios** (cabe en el momento, se dice en voz alta, no inventa, encaja con el estado, no abre con la muerte, respeta el argumentario, avanza). — [src/evaluacion/critico.ts:27-32](/home/user/voices-sells/src/evaluacion/critico.ts), [src/evaluacion/critico.ts:72-107](/home/user/voices-sells/src/evaluacion/critico.ts), [src/evaluacion/critico.ts:206-215](/home/user/voices-sells/src/evaluacion/critico.ts)
- Recibe ejemplos de decisiones anteriores del manager en situaciones parecidas (recuperadas por embeddings). — [src/evaluacion/critico.ts:49-69](/home/user/voices-sells/src/evaluacion/critico.ts)

**3.3 Huellas / herencia de recomendaciones (embeddings + umbrales: decisiones sí/no por código)**
- `text-embedding-3-small` (`MODELO_HUELLA`), OpenAI. Similitud coseno calculada en JS. — [src/lib/huellas.ts:1-60](/home/user/voices-sells/src/lib/huellas.ts)
- Dos umbrales: `UMBRAL = 0.78` ("dos situaciones no son la misma" por debajo) para recuperar ejemplos para el crítico; `UMBRAL_HERENCIA = 0.9` (variable de entorno) para **heredar la decisión del manager sin preguntarle**. Una recomendación descartada no se hereda. — [src/evaluacion/recomendaciones.ts:31-40](/home/user/voices-sells/src/evaluacion/recomendaciones.ts), [src/evaluacion/recomendaciones.ts:275-298](/home/user/voices-sells/src/evaluacion/recomendaciones.ts)

**3.4 Diagnóstico automático de escenarios (Post; a demanda del manager o disparado por el vigilante)**
- Modelo `MODELO_OPENAI_TEXTO` (defecto `gpt-5`), solo OpenAI. Mínimo `LLAMADAS_MINIMAS = 3`. — [src/diagnostico/escenarios.ts:13](/home/user/voices-sells/src/diagnostico/escenarios.ts), [src/diagnostico/escenarios.ts:24](/home/user/voices-sells/src/diagnostico/escenarios.ts), [src/diagnostico/escenarios.ts:166](/home/user/voices-sells/src/diagnostico/escenarios.ts)
- Salida: `{"hay_problema": bool, "diagnostico": texto, "campo": "reglasComportamiento"|"personalidad"|"objecion"|"dificultad"|null, "indice": int|null, "valor_propuesto": texto|null, "motivo": texto}`. Sí/no + Choice(4+null) + índice, más texto que reescribe la ficha. — [src/diagnostico/escenarios.ts:134-170](/home/user/voices-sells/src/diagnostico/escenarios.ts)
- Entradas: medidas agregadas (superadas, nota media, apertura máxima, tells en %, notas de realismo 1-5 del cuestionario, comparación con hermanos de grupo). — [src/diagnostico/escenarios.ts:54-128](/home/user/voices-sells/src/diagnostico/escenarios.ts)
- El vigilante decide por código cuándo disparar el diagnóstico (≥3 llamadas, ≥3 cuestionarios, alguna nota por debajo del umbral, sin propuesta pendiente). — [src/diagnostico/vigilante.ts:1-60](/home/user/voices-sells/src/diagnostico/vigilante.ts)

**3.5 Informe de llamadas reales (aprendizaje-real, Post, a demanda)**
- `gpt-5` vía `llamarOpenAI`. Extrae objeciones, disparadores y reacciones (texto) con un solo campo cerrado por respuesta: `efecto` ∈ {remonta, no_remonta, cuelga}, y recuentos `veces` que se recortan por código. — [src/aprendizaje-real/informe.ts:150-215](/home/user/voices-sells/src/aprendizaje-real/informe.ts)

**3.6 Llamadas reales subidas: quién es el comercial**
- Heurística que elige entre los hablantes del diarizado (Deepgram nova-3): el que habla primero si coincide con el que más habla; si no, el que más habla. La persona lo confirma antes de evaluar. — [src/llamadas-reales/transcribir.ts:88-99](/home/user/voices-sells/src/llamadas-reales/transcribir.ts)

**3.7 Asignación de temas y "Hoy": sin modelo**
- El tema de un escenario nuevo es el pedido o uno al azar entre los menos cubiertos (`situacionMenosCubierta`); no hay clasificación por LLM. — [src/generacion/asignar.ts:18-35](/home/user/voices-sells/src/generacion/asignar.ts), [scripts/asignar-temas.ts](/home/user/voices-sells/scripts/asignar-temas.ts)
- La pantalla "Hoy" es una lista ordenada de reglas deterministas ("La primera regla que dispara gana"), sin pesos ni modelo. — [src/hoy/reglas.ts:1-12](/home/user/voices-sells/src/hoy/reglas.ts), [src/hoy/reglas.ts:83-260](/home/user/voices-sells/src/hoy/reglas.ts)
- Validador de escenarios generados: reglas deterministas (solape de palabras, etc.) que rechazan la propuesta del LLM. — [src/generacion/validador.ts:1-30](/home/user/voices-sells/src/generacion/validador.ts)
- La generación de escenarios (cadena OpenAI `gpt-5` > Claude > OpenRouter > Gemini) elige algunos enums (`foco` ∈ {resultado, relacion, detalle}, género) dentro de un texto largo. — [src/generacion/index.ts:11-17](/home/user/voices-sells/src/generacion/index.ts), [src/generacion/tipos.ts:14-28](/home/user/voices-sells/src/generacion/tipos.ts)

**3.8 Juez de carácter (Offline, `npm run caracter`)**
- Clasificación pura sin texto útil: `{"foco":"resultado|relacion|detalle","dificultad":"receptivo|esceptico|resistente","motivo":...}` con `MODELO_ARBITRO` (`gpt-4.1-mini`), `temperature 0`, `max_tokens 150`, OpenAI directo. Objetivo: 80 % de acierto en foco. — [scripts/caracter.ts:1-32](/home/user/voices-sells/scripts/caracter.ts), [scripts/caracter.ts:107-135](/home/user/voices-sells/scripts/caracter.ts), [scripts/caracter.ts:153-177](/home/user/voices-sells/scripts/caracter.ts)

### Inferences
- Candidatos limpios en Post/Offline para Jev: el **juez de carácter** (dos Choices, cero texto necesario), el sí/no **`apta`** del crítico (como filtro previo: solo se llama al LLM que reescribe si Jev dice "no apta") y **`hay_problema`** del diagnóstico (filtro previo antes de gastar gpt-5).
- Las notas 1-5 y `superado` del evaluador son un Score/sí-no natural, y el repositorio ya tiene verdad de campo (las correcciones del manager, `npm run banco`). Pero el evaluador escribe en la misma pasada todo el texto que el comercial lee y las notas deben ser coherentes con sus justificaciones. Jev encajaría como **segundo juez calibrado** (detectar discrepancias o dar confianza a la nota) más que como sustituto.
- Los umbrales fijos de embeddings (0,78 / 0,9) son decisiones de "¿es la misma situación?" que un modelo de sí/no con probabilidad calibrada podría refinar, sobre todo el 0,9 de herencia, que manda recomendaciones sin revisión humana.
- Con "más flojo en español", los casos de Post con transcripciones largas en castellano coloquial (evaluador, informe real) son los de más riesgo; el juez de carácter y el crítico trabajan con fragmentos cortos.

### Gaps
- No hay mediciones registradas de latencia del evaluador ni del crítico en el repositorio (solo tokens del evaluador; el crítico no se contabiliza).
- No he verificado la precisión actual del evaluador frente al banco del manager (requiere ejecutar `npm run banco -- --si`, que gasta dinero y necesita la base de datos).

---

## 4. ¿Qué bancos de prueba existentes se podrían reutilizar para un A/B offline con otro modelo?

### Takeaway
Hay tres bancos listos, de uso directo: `npm run arbitro` (15 pares etiquetados sube/baja/igual sacados de llamadas reales, llama a `Apertura._preguntar`), `npm run bucle:disparo` (fiabilidad del disparo de una objeción en 20 intentos) y `npm run caracter` (foco/dificultad, objetivo 80 %). Para el evaluador está `npm run banco` contra las correcciones del manager. Todos están acoplados al formato chat-completions/JSON, así que Jev necesitaría un adaptador en `consultar_arbitro` o en un script paralelo.

### Cited Findings
- **`npm run arbitro`** → `scripts/arbitro.py`: 15 casos (7 sube, 4 baja, 4 igual) como pares (frase del comprador, respuesta del comercial), varios fragmentados a propósito "que es como llegan de verdad despues de pasar por la transcripcion". Imprime la regla, el motivo y la latencia (mediana y peor en ms). Sale con error si falla más de 1 de cada 4. — [package.json:42](/home/user/voices-sells/package.json), [scripts/arbitro.py:1-60](/home/user/voices-sells/scripts/arbitro.py), [scripts/arbitro.py:61-146](/home/user/voices-sells/scripts/arbitro.py)
- Detalle: el banco exige `OPENAI_API_KEY` aunque `via_arbitro` ya prefiere OpenRouter. — [scripts/arbitro.py:102-103](/home/user/voices-sells/scripts/arbitro.py)
- El modelo se puede cambiar por variable de entorno (`MODELO_ARBITRO`), pero solo dentro de proveedores compatibles con chat-completions. — [agente-voz/agente.py:1109-1138](/home/user/voices-sells/agente-voz/agente.py)
- **`npm run bucle:disparo`** → `agente-voz/probar_disparo.py`: pregunta N veces (20 por defecto) con el mismo gatillo y cuenta cuántas veces sale la objeción esperada entre las pendientes. Umbral de éxito: 2/3. "Cuesta una llamada a gpt-4.1-mini por intento. Con 20, calderilla." — [package.json:54-55](/home/user/voices-sells/package.json), [agente-voz/probar_disparo.py:1-17](/home/user/voices-sells/agente-voz/probar_disparo.py), [agente-voz/probar_disparo.py:60-100](/home/user/voices-sells/agente-voz/probar_disparo.py)
- **`npm run apertura`** → `scripts/apertura.mjs`: reconstruye desde `agente.log` cómo se movió el nivel en cada llamada (SUBE/baja/sin árbitro). — [scripts/apertura.mjs:1-50](/home/user/voices-sells/scripts/apertura.mjs)
- **`npm run caracter`**: matriz foco × dificultad con un comprador y un guion fijo; tiene modo `--seco` sin red. — [package.json:53](/home/user/voices-sells/package.json), [scripts/caracter.ts:1-32](/home/user/voices-sells/scripts/caracter.ts)
- **`npm run banco`**: vuelve a evaluar las llamadas que el manager ha corregido y compara la distancia a su nota; admite `--modelo`. — [scripts/banco.ts:1-31](/home/user/voices-sells/scripts/banco.ts), [src/evaluacion/banco.ts:1-12](/home/user/voices-sells/src/evaluacion/banco.ts)
- **Datos reales del árbitro en la base**: cada llamada envía su traza (`sesiones.traza`, jsonb) con eventos `sube`, `baja`, `sube_repetida`, `objecion`, `despedida`, `paso_concreto`, `falta_de_respeto`, `estancamiento_limite` y `colgo`, con la frase juzgada recortada a 120 caracteres. **No** se guarda un evento para los veredictos `igual` (solo se escriben en el log). — [agente-voz/agente.py:1454-1458](/home/user/voices-sells/agente-voz/agente.py), [agente-voz/agente.py:1740-1765](/home/user/voices-sells/agente-voz/agente.py), [src/app/api/sesiones/[id]/traza/route.ts](/home/user/voices-sells/src/app/api/sesiones/[id]/traza/route.ts), [src/db/schema.ts:290](/home/user/voices-sells/src/db/schema.ts)
- **Etiquetas humanas previstas**: el diseño del dataset incluye `apertura_correcta` ∈ {si, tardia, nunca, al_reves}, `objeciones_oportunas` ∈ {si, adelantadas, forzadas, faltaron} y `cierre` ∈ {natural, alargado, abrupto}, pensadas para contrastarse con la traza ("el fallo es del arbitro y se afina con npm run arbitro"). — [docs/dataset.md:25-49](/home/user/voices-sells/docs/dataset.md)

### Inferences
- El A/B de menor esfuerzo sería un script paralelo a `scripts/arbitro.py` que reutilice `CASOS` y `FICHA`, cambie solo la función que consulta y compare acierto, latencia y (con Jev) la calibración de la probabilidad. 15 casos son pocos para medir calibración: convendría ampliarlos con turnos reales de las trazas. Ojo, que las trazas no tienen los `igual`, así que para eso hay que partir de las transcripciones completas.
- Como Jev devuelve una sola Choice por consulta, el árbitro actual (3 decisiones en una llamada) se convertiría en 2 o 3 consultas (movimiento, regla, objeción). Habría que medir si la suma de latencias sigue cabiendo en el hueco entre turnos.

### Gaps
- No hay resultados guardados de ninguna ejecución de estos bancos en el repositorio (ni aciertos ni latencias), así que no puedo dar la línea base actual de `gpt-4.1-mini` en cifras.
- No he encontrado en el repositorio ninguna mención ni integración previa de Jev o TypeSafe.

---

## Tabla resumen (para el redactor)

| # | Decisión | Opciones / escala | Hoy | Ruta | Frecuencia | ¿Texto libre en la misma salida? | Encaje con Jev |
|---|---|---|---|---|---|---|---|
| 1 | Árbitro: movimiento | sube / baja / igual | gpt-4.1-mini (OpenRouter > OpenAI) | RT-2º plano | por turno | sí, `motivo` (se inyecta al comprador) | Alto (Choice); sustituir `motivo` por plantilla |
| 2 | Árbitro: regla | S1..S4/5, B1..B4, vacío | igual que 1 | RT-2º plano | por turno | — | Alto (Choice) |
| 3 | Árbitro: objeción disparada | O1..On o ninguna | igual que 1 | RT-2º plano | por turno | — | Medio (opciones dinámicas en español) |
| 4 | Fin de turno | sí/no | LiveKit TurnDetector | RT-crítica | cada pausa | no | Bajo (ya es especializado) |
| 5 | Insulto / despedida / paso concreto / larga | sí/no | listas y regex | RT-crítica | por turno | no | Complemento o auditoría offline |
| 6 | Coach alerta/bien | sí/no implícito | gemini-3.1-flash-lite | RT-2º plano (navegador) | cada ≥6 s | sí (todo es texto) | Bajo-medio (solo como compuerta) |
| 7 | Evaluador: superado, notas 1-5, manejo, cumplimiento | bool, 1-5, enums de 4 y 3 | gpt-6-astra > claude-opus-5 > OpenRouter > gemini-3.6-flash | Post | por llamada | sí, mucho | Segundo juez / calibración |
| 8 | Crítico: apta | sí/no (+ok/corregida/eliminada) | gpt-4.1 (solo OpenAI) | Post | 2-6 por llamada | sí, `corregida` | Filtro previo |
| 9 | Herencia/recuperación por embeddings | umbrales 0,78 / 0,9 | text-embedding-3-small | Post | por llamada | no | Refinar el sí/no "misma situación" |
| 10 | Diagnóstico de escenario | hay_problema + campo (4) | gpt-5 (solo OpenAI) | Post | a demanda | sí | Filtro previo |
| 11 | Informe real: efecto | remonta / no_remonta / cuelga | gpt-5 | Post | a demanda | sí | Bajo |
| 12 | Juez de carácter | foco (3) × dificultad (3) | gpt-4.1-mini | Offline | banco | solo `motivo` (prescindible) | Alto |
| 13 | Quién es el comercial | índice de hablante | heurística | Post | por subida | no | Bajo-medio |
| 14 | Tema del escenario, tareas de Hoy | catálogo / reglas | código | — | — | no | No aplica |
