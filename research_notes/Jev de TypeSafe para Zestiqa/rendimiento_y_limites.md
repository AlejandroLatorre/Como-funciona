# Jev (TypeSafe AI, "System One"): rendimiento real, límites y críticas (con foco en español)

> Fecha de corte: 30/09/2026. Jev se lanzó el 15/09/2026; versión evaluada en casi todas las pruebas: jev-1.13(.0).
> **Aviso metodológico importante:** WebFetch estaba bloqueado por el proxy de salida para la mayoría de dominios (typesafe.ai, typesafe-jev.com, datacamp.com, dev.to, marktechpost.com, blog.buildfastwithai.com, explainx.ai, thoughts.jock.pl, ai.plainenglish.io). Solo se pudieron leer completos repositorios de **github.com**. Todo lo citado de otros dominios procede de **fragmentos (snippets) de WebSearch**, que son resúmenes generados por el buscador y pueden sacar frases de contexto: se marcan como **[snippet]**. Los repos de GitHub son pruebas independientes de una sola persona o equipo pequeño, sin revisión por pares: se marcan como **[independiente, no revisado]**.
> Etiquetas: **[VENDOR]** = afirmación de TypeSafe; **[INDEP]** = medición independiente; **[OPINIÓN]** = valoración de analistas/desarrolladores.

## 1. Benchmarks: el benchmark de 4 workflows de TypeSafe y pruebas independientes

### Takeaway
El 67,8 % de Jev en el benchmark propio mide **acuerdo con dos LLM frontera, no exactitud frente a etiquetas humanas**, en workflows diseñados por el propio equipo que construyó Jev; por tanto es un dato de proveedor con sesgos admitidos. Las pruebas independientes (todas pequeñas y de una persona, primeras dos semanas) muestran buena precisión en tareas de clasificación "limpias" (86–94 % en benchmarks públicos de opción múltiple), calibración razonable en dominio pero sobreconfianza fuera de distribución, y fallos graves ante inyección de instrucciones o cuando falta la opción "ninguna/no se sabe".

### Cited Findings
**Benchmark del proveedor [VENDOR]**
- Jev 67,8 % frente a GPT-5.6 Terra 67,9 %, GPT-5.6 Sol 74,1 % y Opus 5 73,1 % en el benchmark de 4 workflows; coste ~0,0004 $ por caso frente a 0,0304–0,1761 $ de los LLM; 0,4 s frente a 10–38 s — [DataCamp, snippet](https://www.datacamp.com/blog/system-one-models-jev); [TypeSafe blog, no accesible, citado vía snippet](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- Los 4 workflows: respuesta a incidentes de seguridad, observabilidad de trazas de agentes, procesamiento de facturas y atención al cliente — [orcarouter / pearpages / otros, snippet](https://www.orcarouter.ai/blog/jev-typesafe-system-one-what-we-know)
- Por workflow (según snippet): incidentes de seguridad 61,7 % (vs 66,2 % Opus 5); observabilidad de trazas 71,6 % (vs 76,6 %); facturas 61,8 % (vs 79,1 %); atención al cliente 76,0 % (vs 78,3 %). Otro fragmento da, para facturas, Terra 74,7 %, Opus 5 78,4 % y Sol 79,1 % — **no verificado**; hay ambigüedad sobre qué modelo corresponde a cada cifra de comparación — [snippets de búsqueda: Medium de Pranay Suyash, Kingy AI, orcarouter](https://pranaysuyash.medium.com/jevs-193-6-faster-444-6-cheaper-claim-what-typesafe-s-workflow-eval-actually-measures-68b8529e822b)
- Etiquetas de referencia: promedio de respuestas de GPT-6 Astra y Claude Fable 5.1 con "high thinking"; "no hay ground truth humano en ninguna parte de la evaluación"; por eso esos dos modelos no aparecen en la tabla — [snippet, DataCamp/LargitData/pearpages](https://www.largitdata.com/en/blog/jev-system-one-model-open-source-benchmark/)
- Los LLM se evalúan a través del **adaptador System One de código abierto** de TypeSafe, que les obliga a emitir decisiones estructuradas compatibles con la API (posible desventaja para los LLM respecto a su uso nativo) — [snippet](https://www.largitdata.com/en/blog/jev-system-one-model-open-source-benchmark/)
- Los cuatro workflows los diseñó el equipo de capacidades de TypeSafe, el mismo que construyó Jev: "un conflicto de interés claro" — [snippet, DataCamp](https://www.datacamp.com/blog/system-one-models-jev)
- Lo que sigue sin conocerse según DataCamp: rendimiento en benchmarks públicos, comportamiento en tareas que no tienen forma limpia de decisión, precisión en trabajo de dominio en manos de terceros — [DataCamp, snippet](https://www.datacamp.com/blog/system-one-models-jev)
- Los titulares "193,6× más rápido, 444,6× más barato" se basan en esta misma evaluación; análisis crítico en Medium y DEV — [Medium, Pranay Suyash (título/snippet)](https://pranaysuyash.medium.com/jevs-193-6-faster-444-6-cheaper-claim-what-typesafe-s-workflow-eval-actually-measures-68b8529e822b); [DEV, arifulislamat (bloqueado)](https://dev.to/arifulislamat/typesafes-jev-model-is-it-really-193x-faster-and-444x-cheaper-56oa)

**Pruebas independientes [INDEP, no revisado]**
- scienthoon (19/09/2026, 4.621 llamadas vía Vercel AI Gateway, 0 errores, ~0,06 $): OpenBookQA 94,2 % (ECE 0,024), CommonsenseQA 88,1 % (ECE 0,032), HellaSwag 86,1 % (ECE 0,029) — probablemente en dominio. Tickets sintéticos fuera de distribución: cola (elección) 89,0 %, ECE 0,082, sobreconfiado; "cliente enfadado" (booleano) 91,7 %, ECE 0,079, **infraconfiado** (T=0,66); prioridad (score, etiqueta "incognoscible") 44,7 % con probabilidad media declarada 0,74, ECE 0,325. Conjunto 900 ítems: 75,1 %, ECE 0,107 = 4,4× el suelo de ruido (0,024). El campo "confidence" separado calibra peor que la probabilidad máxima (ECE 0,18 en sintético). Probabilidades cuantizadas a 0,01, a menudo exactamente 0 o 1. El Gateway no expone versión del modelo — [GitHub scienthoon/jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration)
- jujumilk3 (~7.000 llamadas, <1 $): ECE MMLU 0,031; coreano vs inglés 0,076 vs 0,075; phishing posterior al corte 0,154. Quitar la opción de abstención: ECE 0,023 → 0,793 y precisión en ítems sin respuesta 0,950 → 0,000; tasa de estereotipo 0,03 → 0,79 (KoBBQ). P(x)+P(no x) media 1,02 pero rango 0,71–1,42. Sin sesgo de orden de opciones (0 cambios de argmax en 400). 50 peticiones idénticas → 15 respuestas distintas. Sin "estado" (state-blind) acierta 0,38–0,46 frente a azar ~0,15 — [GitHub jujumilk3/jev-calibration-audit](https://github.com/jujumilk3/jev-calibration-audit)
- Recopilación "awesome-jev-robustness" (resúmenes de otros repos, no verificados uno a uno): repetibilidad con diferencias 0,03–0,04 entre 5 llamadas idénticas (copyleftdev); orq-ai: 12 trazas puntuadas 100 veces, veredicto repetido siempre; calibración aguanta en routing de soporte (ECE 0,075) y colapsa en 3-SAT aleatorio (willkelly); elección sobreconfiada en ítems de alto desacuerdo: 0,807 declarado vs 0,468 real (GautamTalksDev/jevbench); BBQ 97,28 % en 58.492 preguntas con abstención (simonmesmith) — [GitHub Yifan-Lan/awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- Resumen de prensa: "62,6 % preguntado una vez y 95 % dividido en cinco" (descomposición de la pregunta) — [beri.net, solo título](https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval)
- Resumen tras ocho días de pruebas independientes: "a la par de LLM de precio medio, por detrás de la frontera" — [DEV/AI in Plain English, xbill, solo título; fetch bloqueado](https://dev.to/gde/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1kln)
- La mayoría de pruebas independientes se hicieron en las dos semanas tras el lanzamiento, normalmente por una persona con presupuesto pequeño; las mediciones discrepan entre sí y el mismo modelo parece infraconfiado en un corpus y sobreconfiado en otro — [snippet, lmspedia](https://lmspedia.org/jev-limitations-calibration-confidence/)

### Inferences
- El titular "empata con GPT-5.6 Terra" es un empate en **acuerdo con dos modelos de referencia**, no en exactitud: sirve para comparar entre modelos, no para estimar la tasa de acierto real en producción.
- En tareas bien definidas y con respuesta cerrada, Jev parece bueno (86–94 %); su debilidad aparece en tareas ambiguas o "incognoscibles", donde no baja su confianza lo suficiente. Esto obliga a calibrar umbrales con datos propios (p. ej. escalado de temperatura).
- Siempre conviene incluir una opción explícita de "ninguna / no se sabe / fuera de alcance".

### Gaps
- No se pudo leer el blog ni la documentación oficial de TypeSafe (bloqueados); la descripción de los workflows y del adaptador viene de terceros.
- No hay aún ningún benchmark independiente con etiquetas humanas a gran escala comparando Jev con LLM en las mismas condiciones.
- Cifras por workflow con atribuciones de modelo inconsistentes entre fuentes; no verificadas.

## 2. Latencia real, throughput y límites de uso

### Takeaway
TypeSafe anuncia 70–500 ms extremo a extremo (servicio en la Costa Oeste de EE. UU.); las mediciones independientes van de ~170–400 ms (p50/p95 desde buena conectividad) a ~800–930 ms (p50/p95 desde otra ubicación), así que desde Europa hay que medir. Límite publicado: 1.200 peticiones/min y 250.000 tokens/s, ajustables sin aviso.

### Cited Findings
- [VENDOR] Latencia extremo a extremo 70–500 ms; la mayoría de mediciones ~100 ms desde la Costa Oeste de EE. UU., donde corre el servicio; fuera de ahí se suma latencia de red — [snippets buildfastwithai / flaviocopes](https://flaviocopes.com/jev/)
- [VENDOR] Límites de jev-1.13: 250.000 tokens/s y 1.200 peticiones/min; se ajustan dinámicamente y pueden cambiar sin aviso por la alta demanda; límites mayores en planes enterprise — [snippet, jevaiguide / docs.typesafe.ai/models](https://jevaiguide.com/jev-rate-limits/)
- [INDEP] Una pregunta: p50 280 ms, p95 397 ms — [GitHub jujumilk3/jev-calibration-audit](https://github.com/jujumilk3/jev-calibration-audit)
- [INDEP] Mediana 0,17 s con 8–10 preguntas por llamada (~1.700 tokens de entrada) — [GitHub wondertwins/jev-benchmark](https://github.com/wondertwins/jev-benchmark)
- [INDEP] Jev 1.13.0: p50 808 ms, p95 928 ms, máx 1.845 ms (24 casos); en 10 repeticiones p95 entre 847 y 1.963 ms; Qwen3 8B local ~100 ms. Incluye red; **arranque en frío no medido** — [GitHub zhengbangbo/structured-decision-bench](https://github.com/zhengbangbo/structured-decision-bench)
- [INDEP] Las preguntas agrupadas en una petición se evalúan en paralelo e interfieren poco: cambio de confianza 0,008 y 0,4 % de respuestas cambiadas — [GitHub jujumilk3](https://github.com/jujumilk3/jev-calibration-audit)
- [OPINIÓN] Las cifras de latencia y coste publicadas son "direccionalmente creíbles" pero son del proveedor — [snippet, buildfastwithai](https://blog.buildfastwithai.com/jev-ai-review)

### Inferences
- Para un servicio en España, cabe esperar ~150–250 ms extra de red transatlántica respecto a EE. UU. Oeste; el rango práctico plausible es 300–1.000 ms por llamada, a validar.
- Agrupar varias preguntas por llamada es eficiente (casi no suma latencia).

### Gaps
- No hay datos publicados de arranque en frío ni de latencia desde Europa/LatAm.
- No hay informes de throttling (errores 429) en producción; varias pruebas reportan 0 errores en miles de llamadas.

## 3. Limitaciones publicadas por TypeSafe (Jev 1.13) y fallos concretos

### Takeaway
TypeSafe documenta una página de "jaggedness" para Jev 1.13: aritmética, conteo, comparación de fechas, preguntas indirectas/doble negación/multisalto, contexto distractor y entrada adversarial; recomienda cálculos exactos en código y preguntas directas. Las pruebas independientes confirman con números: sesgo de posición en aritmética, caídas enormes ante inyección, e incoherencia entre pregunta y su negación.

### Cited Findings
- [VENDOR] Debilidades: aritmética, conteo, comparación de fechas, preguntas indirectas, contexto distractor y entrada adversarial; recomienda hacer cálculos exactos en código y formular preguntas directas — [snippet, DataCamp/Requesty](https://www.requesty.ai/blog/typesafe-jev-explained); página oficial: [docs.typesafe.ai/model-jaggedness/jev-1.13 (no accesible)](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [VENDOR] Instrucciones con doble negación o indirección compleja se responden peor; preguntas multisalto ("propiedad de una propiedad") pierden precisión; la precisión cae cuando el estado crece con contenido irrelevante. Recomendación: recuperar y filtrar en código, enviar solo los campos necesarios, nombrar las partes relevantes del estado — [snippet, jevaiguide/jevatlas](https://jevaiguide.com/jev-limitations/)
- [VENDOR] Contexto: 64.000 tokens entre estado y todas las preguntas; 32.000 para estado + la pregunta más larga; máximo 255 opciones por pregunta de elección — [snippet, DataCamp/Pydantic](https://pydantic.dev/docs/ai/models/typesafe/)
- [VENDOR/OPINIÓN] Jev decide en pasos únicos; encadenar razonamiento multi-paso es caro; no da explicación en lenguaje natural (problema de auditoría en sectores regulados) — [snippet, Kingy AI/BenchLM](https://benchlm.ai/blog/posts/what-is-jev)
- [INDEP] Aritmética: 88 % de acierto cuando la opción correcta está primera, 57 % cuando está última (11.621 peticiones) — [RINNECODER/jev-behavior-study vía awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- [INDEP] Inyección: 96,5 % → 26,5 % con una instrucción inyectada de una línea (486 debates de borrado de Wikipedia, zkousama/jagged); 312 de 508 ítems (61,4 %) cambiados con inyección de contexto fluida (xzx34/JevOut); órdenes burdas fallan pero la "inyección de autoridad" funciona en 3 de 30 casos (eugeniughelbur) — [awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- [INDEP] Fuera de alcance: 0 de 30 entradas fuera de alcance marcadas sin opción "ninguna" explícita (priorbench/jev) — [awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- [INDEP] Parafrasear la pregunta mueve las respuestas tanto como negarla (yodablocks/jev-orderby-bench); P(x)+P(no x) en rango 0,71–1,42 — [awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness); [jujumilk3](https://github.com/jujumilk3/jev-calibration-audit)
- [INDEP] En la tarea de voz, casos donde el destinatario se deduce del diálogo (no del vocativo) degradan; el estilo indirecto se vuelve ambiguo al perder comillas la transcripción — [GitHub wondertwins/jev-benchmark](https://github.com/wondertwins/jev-benchmark)

### Inferences
- Nota: la auditoría de jujumilk3 no encontró sesgo de orden de opciones en MMLU, mientras RINNECODER sí lo encuentra en aritmética: el sesgo de posición parece depender del tipo de tarea (fuerte en cálculo, débil en conocimiento).
- Para diálogos multi-turno lo razonable es resumir/filtrar en código el turno relevante antes de preguntar a Jev.

### Gaps
- No encontré documentación oficial legible sobre diálogo multi-turno propiamente dicho, ni ejemplos oficiales concretos de fallo (la página oficial estaba bloqueada).

## 4. Soporte de idiomas: español, otros idiomas y transcripciones ASR

### Takeaway
TypeSafe declara el inglés como idioma principal de entrenamiento y donde la precisión es mejor; otros idiomas están "soportados" pero pide probar cada caso con contenido propio. La única auditoría en español encontrada mide una pérdida de 3,0–6,4 puntos y ECE que se duplica en tareas difíciles; escribir las instrucciones en español no aporta nada (recomienda mantenerlas en inglés). No hay pruebas con español coloquial ni con ASR en español; la única prueba ASR (inglés) muestra degradación pequeña.

### Cited Findings
- [VENDOR] El inglés es el idioma principal de entrenamiento y donde la precisión es mejor; los demás idiomas se aceptan con menor precisión; se recomienda probar cada workload con contenido propio — [snippets, EvolupedIA / webreactiva / PotencIA](https://evolupedia.com/blog/jev-typesafe-ai-como-usar-precio/)
- [OPINIÓN, blogs en español] Recomiendan escribir instrucciones y criterios en inglés aunque el estado esté en español, y evaluar con ejemplos reales en español antes de automatizar — [snippet, webreactiva](https://www.webreactiva.com/blog/empezar-jev-typesafe); [EvolupedIA](https://evolupedia.com/blog/jev-typesafe-ai-como-usar-precio/)
- [INDEP] jev-acento (21/09/2026, jev-1.13.0, 19.200 llamadas, 0,58 $, 0 errores). Precisión inglés→español: XNLI 85,0→78,6 % (−6,4 pp); PAWS-X 83,4→77,2 % (−6,2 pp); MASSIVE intent (~60 intenciones, es-ES) 84,5→80,8 % (−3,7 pp); Belebele 98,2→95,2 % (−3,0 pp). ECE: XNLI 0,057→0,101, PAWS-X 0,033→0,078; sin diferencia en MASSIVE ni Belebele. Instrucciones en español vs inglés: sin diferencia detectable (−0,2 a +1,6 pp) → mantener en inglés. El español cuesta 17–38 % más tokens de entrada. Estabilidad: flips 0,2–2,1 %, κ ≥ 0,95 — [GitHub marcosmartinez/jev-acento](https://github.com/marcosmartinez/jev-acento)
- [INDEP] Limitaciones que el propio jev-acento declara: **no probó texto coloquial, variantes regionales ni ASR**; los datos son "traduccionés" académico limpio y corto; deben tomarse como **cota superior** para uso real; no cubrió la primitiva Score; una sola redacción por celda — [GitHub marcosmartinez/jev-acento](https://github.com/marcosmartinez/jev-acento)
- [INDEP] Ruso 77,3 % vs inglés 88,3 % en 600 pares XNLI (−11 pp) — [AHTOOOXA/jev-cyrillic-audit vía awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- [INDEP] Coreano: ECE 0,076 vs inglés 0,075 en MMLU-ProX (sin degradación de calibración) — [jujumilk3](https://github.com/jujumilk3/jev-calibration-audit); tickets con texto coreano sin fallos reportados — [scienthoon](https://github.com/scienthoon/jev-ood-calibration)
- [INDEP] ASR (inglés, detección de destinatario de NPC, 79 enunciados): F1 0,962 texto limpio, 0,944 STT (minúsculas sin puntuación), 0,927 STT con errores fonéticos; precisión 1,0 en todas; puntuaciones cerca de 0,5 en casos dudosos en lugar de errores confiados — [GitHub wondertwins/jev-benchmark](https://github.com/wondertwins/jev-benchmark)

### Inferences
- Para Zestiqa (español, habla informal y fragmentaria transcrita por ASR), la estimación honesta es: pérdida de al menos 3–6 pp respecto al inglés y calibración peor en tareas de inferencia/paráfrasis; con coloquialismo + ASR la pérdida real probablemente sea mayor, pero **no hay mediciones**. Es imprescindible un conjunto de validación propio en español real transcrito.
- La tarea MASSIVE (detección de intención, −3,7 pp, calibración intacta) es la más parecida a routing/intención por voz y es de las que menos se degrada.
- La prueba ASR sugiere robustez a minúsculas/sin puntuación/erratas fonéticas, pero es en inglés y con muestra muy pequeña.

### Gaps
- Sin pruebas en español coloquial, variantes latinoamericanas ni transcripciones ASR en español.
- No se pudo leer la página oficial de idiomas de TypeSafe (bloqueada); la postura oficial se conoce por blogs en español.
- No encontré artículos de Forbes Argentina, Fazt.dev ni agentes.ai con datos propios (no aparecieron en las búsquedas).

## 5. Críticas de analistas y desarrolladores

### Takeaway
Las críticas se centran en el marketing más que en la tecnología: llamar "frontier" a un modelo sin generación de texto, el eslogan "nunca alucina" (cierto solo en sentido estrecho: no sale del esquema, pero sí se equivoca), la demo de Doom mal contada, y un benchmark propio sin verdad humana.

### Cited Findings
- [OPINIÓN] Varios comentaristas critican el término "frontier model" para Jev, que no tiene chat, ni generación libre, ni comprensión de imágenes; su espacio de salida es un conjunto pequeño y enumerado de decisiones — crítica "justa del lenguaje de marketing, no de la utilidad de la tecnología" — [snippet, hermes-ai.net](https://hermes-ai.net/jev/guide/)
- [OPINIÓN] En redes se resume como "un LLM más rápido y barato que nunca alucina", lo cual "entiende al revés lo importante": su valor es no generar prosa — [snippet, hermes-ai.net](https://hermes-ai.net/jev/guide/)
- [VENDOR vs matiz] DataCamp titula "System One Model That Never Hallucinates" — [DataCamp](https://www.datacamp.com/blog/system-one-models-jev). La salida tipada elimina "inventar un valor inesperado o una salida malformada fuera del esquema", pero "el error de juicio semántico sigue siendo posible y debe medirse"; la calibración no garantiza que una predicción individual sea correcta — [GitHub gist pjburnhill](https://gist.github.com/pjburnhill/adf8d28efcad9df037bfdece178ef965)
- [OPINIÓN] Demo de Doom: se cuenta como "Jev ve la pantalla y juega", pero la entrada es estado estructurado en texto, ~10 decisiones/segundo; un bot con script jugaría mejor; lo que demuestra es decisión reactiva en bucle en tiempo real — [snippet, explainx.ai/hermes-ai](https://explainx.ai/blog/where-jev-actually-fails-2026)
- [OPINIÓN] Conflicto de interés en el benchmark (mismo equipo) y "accuracy" = acuerdo con otros modelos, "una afirmación bastante más débil de lo que parece" — [snippets, DataCamp/orcarouter](https://www.orcarouter.ai/blog/jev-typesafe-system-one-what-we-know)
- [OPINIÓN] Da un número sin justificación: problema para depuración y auditoría en dominios regulados — [snippet, Kingy AI](https://kingy.ai/blog/typesafe-jev-review-the-ai-model-that-doesnt-generate-text/)

### Gaps
- No pude leer hilos de Hacker News, Reddit ni X directamente (no aparecieron o estaban bloqueados); las críticas se conocen por agregadores.

## 6. Casos de uso recomendados y desaconsejados

### Takeaway
Consenso (proveedor y revisores): Jev sirve para juicios semánticos rápidos y cerrados (clasificación, routing, detección de intención, moderación, triaje, puntuación, elección de herramienta de agentes, ranking); no sirve para generar, explicar, planificar a varios pasos ni para cálculos exactos o reglas deterministas.

### Cited Findings
- [VENDOR/documentación] Recomendado: clasificación, detección, scoring, routing, búsqueda semántica, recuperación y ranking — "juicio experto de cinco segundos a escala de máquina". Desaconsejado: generación de contenido, razonamiento complejo, investigación, decisiones estratégicas nuevas — [GitHub gist pjburnhill](https://gist.github.com/pjburnhill/adf8d28efcad9df037bfdece178ef965)
- [OPINIÓN] No usar si se necesitan cadenas de razonamiento multi-paso (pruebas, planificación compleja) o si el juicio es totalmente basado en reglas (regex, SQL) — [snippet, BenchLM/Requesty](https://benchlm.ai/blog/posts/what-is-jev)
- [OPINIÓN] MarkTechPost publicó "20 Agentic Use Cases of TypeSafe AI's Jev" (27/09/2026) — [MarkTechPost (fetch bloqueado; lista no obtenida)](https://www.marktechpost.com/2026/09/27/20-agentic-use-cases-of-typesafe-ais-jev/amp/)
- [INDEP] Evidencia a favor en routing de soporte (ECE 0,075, calibración aguanta) y en contra en razonamiento combinatorio (3-SAT, calibración colapsa) — [willkelly vía awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness); en detección de intención (MASSIVE) 84,5 % inglés / 80,8 % español — [jev-acento](https://github.com/marcosmartinez/jev-acento)
- [INDEP] Como juez de trazas de agentes: repite siempre el mismo veredicto en 100 repeticiones (orq-ai/jev-judge) — [awesome-jev-robustness](https://github.com/Yifan-Lan/awesome-jev-robustness)
- [INDEP] Sin abstención explícita falla en preguntas sin respuesta (0,950 → 0,000) y dispara estereotipos (0,03 → 0,79): relevante para moderación/triaje — [jujumilk3](https://github.com/jujumilk3/jev-calibration-audit)
- [OPINIÓN] Análisis específico de uso en operaciones de seguridad — [Prophet Security (solo título)](https://www.prophetsecurity.ai/blog/jev-security-operations)

### Inferences
- Para grading/scoring, la primitiva Score es la peor calibrada fuera de distribución (prioridad: 44,7 % con confianza media 0,74), así que exige recalibración o convertirla en preguntas booleanas/elección más directas (la descomposición parece ayudar mucho, según el titular de beri.net).
- Patrón seguro: Jev como primera capa rápida con umbral de confianza calibrado localmente, opción "ninguna/no sé" siempre presente, y derivación a LLM o humano en los casos dudosos.

### Gaps
- No se obtuvo la lista de los 20 casos de MarkTechPost ni la página oficial de casos de uso de TypeSafe (dominios bloqueados).
