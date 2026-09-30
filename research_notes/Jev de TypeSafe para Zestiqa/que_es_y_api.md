# Jev (TypeSafe AI): qué es y cómo funciona su API

> **Aviso de método (importante para quien redacte el informe):** en este entorno WebFetch estuvo bloqueado por el proxy de salida para TODOS los dominios probados: typesafe.ai, openrouter.ai, flaviocopes.com, datacamp.com, dev.to, dryhurst.io, theregister.com y truestandard.ai. Por eso **no pude leer ninguna página completa**. Todo lo que sigue sale de **fragmentos resumidos de WebSearch**, que atribuyo a la URL que el buscador asoció a cada afirmación. Esos fragmentos pueden sacar el texto de contexto o mezclar fuentes. Donde el fragmento no dejaba claro de qué URL venía un dato, lo indico. Ningún dato está verificado contra la documentación original de TypeSafe ni contra la página de OpenRouter leída directamente. Fecha de corte: 30 de septiembre de 2026.

## 1. Arquitectura: qué es Jev, qué significa "System One model" y qué versiones hay

### Takeaway
Jev es un modelo de "decisión" que no genera texto. Recibe un estado (texto o JSON) y un conjunto de preguntas tipadas, las evalúa todas en paralelo en una sola pasada y devuelve respuestas tipadas con probabilidades. Terceros lo describen como un "clasificador entrenado a escala frontier" y no autorregresivo. En OpenRouter aparecen `typesafe/jev-1.13` (alias `~typesafe/jev-latest`) y un producto aparte, `typesafe/jev-router`.

### Cited Findings
**Afirmaciones oficiales de TypeSafe, o atribuidas a TypeSafe por terceros**
- Anuncio del 15 de septiembre de 2026. Jev "no genera texto en absoluto" y abre una nueva categoría que TypeSafe llama *System One models* — [TypeSafe blog, "Introducing System One Models & Jev"](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (solo vi el fragmento de búsqueda)
- Un System One model es "una clase de IA, introducida por TypeSafe, que toma decisiones rápidas y estructuradas en lugar de generar texto". Recibe estado de programa no estructurado y devuelve decisiones tipadas y probabilísticas en una única pasada paralela, sin generar cadenas y sin nada que parsear — fragmento que agrupa [DataCamp](https://www.datacamp.com/blog/system-one-models-jev), [TrueFoundry](https://www.truefoundry.com/blog/typesafe-ai-jev) y el [blog de TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- La nota de prensa lo define como "decision model": recibe estado de la aplicación más preguntas tipadas y devuelve respuestas tipadas ("a Choice, a Score, a Boolean"), cada una con una probabilidad y evaluadas en paralelo — [AIwire/HPCwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/); [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/typesafe-ai-emerges-stealth-40m-190000776.html). **Ojo:** aquí se dice "Boolean" y no "Noul"; ver la sección 2.
- Según la descripción de OpenRouter, Jev es "the first of its System One models": devuelve una elección tipada en vez de texto libre y está pensado para enrutado, clasificación y otros puntos de decisión — [OpenRouter, página del proveedor Typesafe](https://openrouter.ai/typesafe); [OpenRouter blog "What Is Jev?"](https://openrouter.ai/blog/insights/what-is-jev/)
- Se afirma que "matemáticamente no puede alucinar ni producir errores de tipo" — fragmento asociado a DataCamp/TrueFoundry ([DataCamp](https://www.datacamp.com/blog/system-one-models-jev)). Es una afirmación de marketing sobre el formato de salida, no sobre si la decisión es correcta.

**Lectura de terceros**
- MindStudio lo llama "Non-Autoregressive System-1 Model" — [MindStudio](https://www.mindstudio.ai/blog/jev-system-one-model-launch) (solo el título)
- "El producto real es un clasificador entrenado a escala frontier para software, no un LLM mejor; todas las cifras hasta ahora las da el fabricante" — [pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim) (atribución probable dentro de un fragmento con varias fuentes)
- Es la herramienta equivocada para chat, generación de código o cualquier cosa que necesite una explicación escrita — [TrueFoundry](https://www.truefoundry.com/blog/typesafe-ai-jev) / [DataCamp](https://www.datacamp.com/blog/system-one-models-jev)

**Versiones y modelos**
- En OpenRouter hay 3 modelos Typesafe: Jev Router, Jev Latest y Jev 1.13 — [OpenRouter /typesafe](https://openrouter.ai/typesafe)
- El id del modelo es `typesafe/jev-1.13`, con alias `~typesafe/jev-latest` — [OpenRouter Decisions API reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request); también un issue de GitHub que cita "typesafe/jev-latest" ([oh-my-pi #12458](https://github.com/can1357/oh-my-pi/issues/12458))
- `typesafe/jev-router`, listado el 25 de septiembre de 2026, es un **router de LLMs sensible a la caché** que "funciona con Jev". Elige el mejor modelo y el esfuerzo de razonamiento para cada petición. Tiene precio 0 en OpenRouter y un contexto de 1.000.000 de tokens — [OpenRouter, Jev Router](https://openrouter.ai/typesafe/jev-router); [OpenRouter en X](https://x.com/OpenRouter/status/2103610898690855161). No es Jev en sí, sino un producto construido sobre él.
- También aparece una ficha de "Jev (typesafe)" en la documentación de modelos de IA de Cloudflare — [Cloudflare AI docs](https://developers.cloudflare.com/ai/models/typesafe/jev/) (solo el título; contenido no verificado)

### Inferences
- "System One" alude a la dicotomía de Kahneman entre pensamiento rápido e intuitivo (Sistema 1) y lento y deliberativo (Sistema 2). Jev haría el papel de decisor rápido que complementa a un LLM "System Two". Es una inferencia por el nombre: no encontré una cita textual de TypeSafe que lo explique.
- Como la salida es siempre una distribución sobre opciones predefinidas, el término técnico más exacto es "clasificador/regresor condicionado por instrucciones", no "generador".

### Gaps
- No hay detalles oficiales de la arquitectura interna: tamaño, base, si es un encoder o cómo se entrenó. No pude leer el blog oficial.
- No sé si existieron versiones públicas anteriores a la 1.13 ni qué cambia entre versiones.
- No confirmé si `jev-latest` existe como id en la API directa de TypeSafe o solo como alias en OpenRouter.

## 2. Los tres primitivos (Choice, Score, Noul): formas de petición y respuesta, límites y entradas

### Takeaway
Una petición lleva `state` (string, o un objeto/array JSON) y `questions`, un mapa con claves elegidas por ti a preguntas tipadas. Cada pregunta tiene un tipo (Choice/Score/Noul), `instructions` y, en Choice y Score, `criteria` o niveles.
- **Choice:** hasta 255 opciones con nombre. Devuelve `choice`, `probabilities` para cada opción y `confidence`.
- **Score:** de 2 a 10 niveles ordenados. Devuelve un valor que puede caer entre niveles, más `legend`, `probabilities` y `confidence`.
- **Noul:** una proposición de sí o no. Devuelve un único número `noul`, la probabilidad de que sea cierta, sin campo `confidence`.

Las preguntas son independientes entre sí. Los límites de contexto que se citan (64k/32k) no coinciden del todo con la ficha de OpenRouter (32k).

### Cited Findings
**Estructura de la petición**
- Cuerpo de la Decisions API de OpenRouter, con tres campos obligatorios:
  - `model`
  - `state`: string plano, u objeto/array JSON cuando el contexto tiene varias partes
  - `questions`: mapa de preguntas tipadas; tú eliges cada clave y la respuesta vuelve bajo la misma clave

  Cada pregunta tiene un tipo (Choice, Score o Noul), `instructions` y `criteria`. Algunas implementaciones mencionan además los campos `provider` y `session_id` — [OpenRouter API reference, "Submit a Decisions (questions and answers) request"](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request); [dryhurst.io](https://dryhurst.io/articles/jev-openrouter-decisions-api/) (fragmento combinado)
- Ejemplo del SDK de Python (`pip install typesafe-sdk`, Python ≥3.10; la clave se lee de `TYPESAFE_API_KEY`) — [ToolScout](https://toolscout.ai/news/how-to-use-jev) / [jevmodel.org/api](https://jevmodel.org/api/) / [abrarqasim.com](https://abrarqasim.com/blog/typesafe-ai-jev-api-tutorial-choice-score-noul-and-the-gotchas/) (el fragmento no aclara cuál de las tres):
  ```python
  from typesafe_sdk import Choice, Noul, TypeSafeClient
  client = TypeSafeClient()  # reads TYPESAFE_API_KEY
  r = client.system_one(
      state=ticket,
      questions={
          "department": Choice(
              instructions="Which team should handle this",
              criteria={"billing": "Payment issues", "technical": "Bugs"},
          ),
          "is_urgent": Noul(instructions="The message conveys urgency"),
      },
  )
  print(r.answers["department"].choice, r.answers["is_urgent"].noul)
  ```

**Cada primitivo**
- **Choice:** recibe un mapa de opciones con nombre (clave → descripción del criterio). Devuelve una probabilidad por opción más la de mayor puntuación. Admite hasta 255 opciones — fragmento combinado de [Conikee, Substack](https://conikeec.substack.com/p/a-field-guide-to-jev-primitives), [jevpatterns.com](https://jevpatterns.com/guides/choice-score-noul) y [refix.ai](https://www.refix.ai/news/jev-choice-score-noul/)
  - Respuesta: `choice`, `probabilities` sobre todas las opciones y un valor `confidence` — [ToolScout](https://toolscout.ai/news/how-to-use-jev) / [MarkTechPost](https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/)
- **Score:** recibe un array ordenado de descripciones de nivel, entre 2 y 10. Devuelve una posición a lo largo de ellos que puede caer entre niveles — mismas fuentes que Choice
  - Respuesta: `score`, `legend`, `probabilities` y `confidence` — [ToolScout](https://toolscout.ai/news/how-to-use-jev)
- **Noul:** recibe una afirmación de sí o no y devuelve un único número, la probabilidad de que sea verdadera. "Un Noul de 0,8 significa probablemente cierto, no '80% de gravedad'" — [Conikee](https://conikeec.substack.com/p/a-field-guide-to-jev-primitives) / [jevpatterns](https://jevpatterns.com/guides/choice-score-noul)
  - Las respuestas Noul no tienen campo `confidence`: el umbral se aplica directamente sobre `noul` — [ToolScout](https://toolscout.ai/news/how-to-use-jev) / [abrarqasim.com](https://abrarqasim.com/blog/typesafe-ai-jev-api-tutorial-choice-score-noul-and-the-gotchas/)
  - The Register lo describe como "a probability score of truthfulness between 0 and 1" — [The Register, 23 de septiembre de 2026](https://www.theregister.com/devops/2026/09/23/shut-up-and-calculate-jevs-new-ai-primitives-for-coders/5298431)

**Combinación de preguntas**
- Se pueden enviar los tres tipos en una misma petición. Cada pregunta es independiente: una respuesta nunca se convierte en contexto oculto de otra — [refix.ai](https://www.refix.ai/news/jev-choice-score-noul/) / [jevpatterns](https://jevpatterns.com/guides/choice-score-noul)
- Se obtienen probabilidades (y `confidence` en Choice y Score) sin pedir al modelo que "responda en JSON" — [ToolScout](https://toolscout.ai/news/how-to-use-jev)

**Límites de contexto**
- 64k tokens para estado más preguntas, y 32k para estado más la pregunta más larga. Choice limitado a 255 opciones — [Firecrawl, "What Is Jev?"](https://www.firecrawl.dev/blog/what-is-jev) (el fragmento no deja claro si viene de Firecrawl o del paper de arXiv)
- **Contradicción:** la ficha de `typesafe/jev-1.13` en OpenRouter indicaría una ventana de contexto de 32.000 tokens — [OpenRouter, Jev 1.13](https://openrouter.ai/typesafe/jev-1.13) (vía fragmento). Un paper de arXiv dice que "la ventana de contexto de Jev no está publicada" — [arXiv 2609.28940](https://arxiv.org/pdf/2609.28940)

**Nomenclatura**
- La nota de prensa de lanzamiento habla de "a Choice, a Score, a Boolean" — [AIwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/). La API y el SDK usan el nombre **Noul** (`type: noul/choice/score`) — [OpenRouter API ref](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request)

### Inferences
- **Instrucciones:** no hay un "system prompt" global documentado. Las instrucciones van por pregunta (`instructions`) y los criterios por opción o nivel. Para meter ejemplos (few-shot) o varias partes de contexto (por ejemplo, un historial), lo razonable es incluirlos en `state` como objeto o array JSON. Es una inferencia a partir del formato: no lo he visto documentado.
- **Multi-turno:** no existe como tal. Cada llamada es "un estado + preguntas". El historial de una conversación tendría que serializarse dentro de `state`.
- **JSON schema libre:** no está soportado. La "estructura" de la salida es la que imponen los tres tipos. Un esquema complejo hay que descomponerlo en varias preguntas Choice/Score/Noul con claves propias.
- **Calibración:** que las probabilidades estén "calibradas" significa, según el discurso de TypeSafe, que una p=0,8 debería acertar alrededor del 80% de las veces. Encontré la afirmación ("calibrated confidence") pero ninguna métrica publicada, como ECE o diagramas de fiabilidad. Tampoco una definición oficial exacta de cómo se calcula `confidence` frente a `probabilities`.

### Gaps
- No tengo el JSON crudo exacto de la respuesta REST: nombres de campo de nivel superior, si hay `usage`, `id` o `model`, ni los códigos de error.
- No sé cuál es el rango numérico exacto de `score` (¿índice de nivel 0..N-1, 1..N o normalizado 0..1?), ni qué contiene `legend`.
- No sé qué fórmula usa `confidence`.
- No tengo una confirmación oficial de los límites 64k/32k frente a los 32k de OpenRouter.
- No encontré documentación sobre few-shot, system prompt global, multi-turno ni `session_id`.

## 3. Disponibilidad en OpenRouter y en la API, consola y SDK de TypeSafe

### Takeaway
Sí está en OpenRouter como `typesafe/jev-1.13` (alias `~typesafe/jev-latest`), con TypeSafe como único proveedor. **No se expone por `/api/v1/chat/completions`**, sino por un endpoint propio:
- `POST https://openrouter.ai/api/alpha/decisions` (en alfa), o
- `POST https://openrouter.ai/api/v1/systemone`, compatible con la API de TypeSafe.

Por tanto no se usan `response_format` ni `logprobs`. En OpenRouter figura una latencia P50 de unos 0,26 s. La API directa de TypeSafe se ofrece mediante waitlist y el SDK `typesafe-sdk`.

### Cited Findings
**Endpoints y autenticación en OpenRouter**
- Se crea una API key de OpenRouter y se llama al endpoint alfa de Decisions (`POST https://openrouter.ai/api/alpha/decisions`) o al endpoint compatible con TypeSafe (`POST https://openrouter.ai/api/v1/systemone`), "not the chat completions API" — [OpenRouter, página del proveedor Typesafe / docs de Jev](https://openrouter.ai/docs/guides/community/jev) (vía fragmento)
- "No envíes peticiones de Jev a /api/v1/chat/completions". Jev devuelve decisiones, no texto, y por eso OpenRouter lo sirve por un endpoint de Decisions dedicado que sigue en alfa — [jevaiguide.com](https://jevaiguide.com/channels/openrouter/) (fragmento)
- Cabeceras: `Authorization: Bearer <key>` y `Content-Type: application/json` — [OpenRouter API reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request)
- Hay proyectos que migran sus clientes de Jev desde "Vercel AI Gateway" a la Decisions API de OpenRouter, lo que sugiere que Jev también está en Vercel AI Gateway — [GitHub, autoloop #257](https://github.com/Sanctum-Origo-Systems/autoloop/issues/257) (solo el título)

**Precio, proveedor, latencia y límites en OpenRouter**
- Precio de `typesafe/jev-1.13` en OpenRouter: $0,042 por millón de tokens de entrada y $0 por millón de salida — [OpenRouter, Jev 1.13](https://openrouter.ai/typesafe/jev-1.13)
- Un único proveedor, TypeSafe. OpenRouter reenvía cada petición directamente, sin decisiones de enrutado — [OpenRouter, Jev 1.13](https://openrouter.ai/typesafe/jev-1.13) (fragmento)
- Latencia P50 publicada por OpenRouter: 0,26 s. Uptime del 100,00% y disponibilidad del 99,86% en 3 días — [OpenRouter, Jev 1.13](https://openrouter.ai/typesafe/jev-1.13) (fragmento; es una cifra puntual que cambia con el tiempo)
- Límites directos publicados: 250.000 tokens por segundo y 1.200 peticiones por minuto. TypeSafe dice que "se ajustan dinámicamente" mientras añade capacidad. Los planes enterprise tienen límites mayores y zero data retention — el fragmento lo asocia a la búsqueda de OpenRouter y [jev.pro](https://jev.pro/access/jev-on-openrouter/). Probablemente son los límites de la **API directa de TypeSafe**, no de OpenRouter; no está verificado.

**API directa, SDK y acceso**
- El acceso anticipado a Jev tiene waitlist en typesafe.ai — [AIwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/)
- SDK de Python `typesafe-sdk` (Python ≥3.10), cliente `TypeSafeClient()`, método `system_one(state=..., questions=...)` y variable de entorno `TYPESAFE_API_KEY` — [ToolScout](https://toolscout.ai/news/how-to-use-jev) / [jevmodel.org/api](https://jevmodel.org/api/)
- Existe un SDK de Java hecho por la comunidad, no oficial — [DEV Community, jamilxt](https://dev.to/jamilxt/i-built-the-first-java-sdk-for-jev-typesafes-system-one-model-2m37) (solo el título)
- Existe un wrapper comunitario, "jevper", que imita el formato de Jev sobre clientes tipo OpenAI. No es Jev — [GitHub zhulinchng/jevper](https://github.com/zhulinchng/jevper)

### Inferences
- El endpoint `/api/v1/systemone` de OpenRouter replica el endpoint nativo de TypeSafe, al que el SDK llama con `system_one`. Probablemente el cuerpo `{model, state, questions}` es el mismo en ambos. Es una inferencia sin confirmar.
- Como no pasa por chat/completions, **los SDKs de OpenAI, LangChain, etc. no sirven tal cual**: hace falta una llamada HTTP propia o el SDK de TypeSafe.

### Gaps
- No pude abrir la página de OpenRouter para confirmar la URL base exacta de la API nativa de TypeSafe ni las rutas y documentación de la consola.
- No sé si hay límites de peticiones específicos de OpenRouter para este modelo.
- No sé si OpenRouter aplica algún recargo (fee) sobre el precio de TypeSafe.
- No encontré el SDK oficial para JS/TS.

## 4. Precio oficial, latencia y la afirmación "193x más rápido, 444x más barato"

### Takeaway
Precio: $0,042 por millón de tokens de entrada y salida gratis. Latencia oficial: 70–500 ms de extremo a extremo.

Las cifras "193,6x más rápido y 444,6x más barato" salen de una evaluación propia de TypeSafe sobre 4 flujos de trabajo, comparando con modelos frontier. En ese benchmark la "precisión" se mide como **acuerdo** con una referencia generada por GPT-6 Astra y Claude Fable 5.1, no contra una verdad de referencia. La propia TypeSafe advierte en nota al pie que son cifras "del extremo alto". Las pruebas independientes dan multiplicadores mucho menores.

### Cited Findings
**Afirmaciones oficiales**
- Precio: $0,042 por millón de tokens de entrada, salida gratis — [DataCamp](https://www.datacamp.com/blog/system-one-models-jev) / [TrueFoundry](https://www.truefoundry.com/blog/typesafe-ai-jev); coincide con [OpenRouter](https://openrouter.ai/typesafe/jev-1.13)
- Latencia: responde preguntas estructuradas en 70–500 ms — fragmento del grupo DataCamp/TrueFoundry
  - TypeSafe da 70–500 ms de latencia de extremo a extremo, frente a 3–329 s de los modelos frontier — [buildfastwithai](https://blog.buildfastwithai.com/jev-ai-review) / [greennode](https://greennode.ai/blog/what-is-jev) (fragmento combinado)
- Titular del lanzamiento: "193.6x faster, 444.6x cheaper" — [DEV, arifulislamat](https://dev.to/arifulislamat/typesafes-jev-model-is-it-really-193x-faster-and-444x-cheaper-56oa) / [pearpages](https://pearpages.com/blog/2026/09/16/jev-sorted-what-typesafes-system-one-model-actually-is-and-what-is-still-just-a-claim)
- Nota al pie del post de lanzamiento: "we expect that these are on the higher end of real world gains" — mismas fuentes (fragmento)

**Base de comparación (baseline) del benchmark**
- Las cifras de 193x y 444x miden **acuerdo** con GPT-6 Astra y Fable 5.1, no si la respuesta es correcta — mismas fuentes (fragmento)
- En las 4 evaluaciones de flujos de trabajo de TypeSafe, Jev saca de media alrededor de un 67,8% de acuerdo con una referencia generada con GPT-6 Astra y Claude Fable 5.1. El multiplicador depende de qué modelo frontier se use como base — [SmartScope](https://smartscope.blog/en/blog/jev-typesafe-decision-model-cost-latency/) / [layer3labs](https://www.layer3labs.io/guides/jev-benchmarks) (fragmento combinado)
- En una configuración mostrada, GPT-5.6 Terra tardó 10,1 s por caso y Jev 0,4 s, unas 25 veces más rápido — [SmartScope](https://smartscope.blog/en/blog/jev-typesafe-decision-model-cost-latency/). SmartScope titula "unas 25 veces más rápido a más o menos 1/76 del coste".
- Otra lectura: alrededor del 68% de precisión, cerca de LLMs de gama media como GPT-5.6 Terra, pero 40–400 veces más barato y 20–200 veces más rápido. También "40x–200x faster than frontier LLMs" — [DataCamp](https://www.datacamp.com/blog/system-one-models-jev) / [TrueFoundry](https://www.truefoundry.com/blog/typesafe-ai-jev)

**Mediciones independientes**
- TrueStandard midió 1,7x (velocidad) y 100x (coste) según la base elegida — [TrueStandard](https://truestandard.ai/blog/is-jev-really-193x-faster)
- En una carga real de tickets de soporte, Jev fue de 4 a 7 veces más rápido y de 31 a 65 veces más barato — fragmento de [DEV, arifulislamat](https://dev.to/arifulislamat/typesafes-jev-model-is-it-really-193x-faster-and-444x-cheaper-56oa) (atribución probable)
- En OpenRouter figura una latencia P50 de 0,26 s — [OpenRouter](https://openrouter.ai/typesafe/jev-1.13)

### Inferences
- Los multiplicadores dependen mucho del modelo base (un frontier con razonamiento largo frente a un modelo medio) y de la carga de trabajo. Para planificar, es más prudente contar con **unos 25x en latencia y entre 30x y 100x en coste** frente a LLMs de gama media, no con 193x/444x.
- Un "acuerdo del 68%" con modelos frontier significa que Jev discrepa de ellos en alrededor de un tercio de los casos en esas tareas. Antes de adoptarlo hay que validarlo con un conjunto etiquetado propio.

### Gaps
- No tengo la tabla oficial completa: los 4 flujos de trabajo, qué modelo base produce exactamente 193,6x/444,6x y si incluye tiempo de red.
- Tampoco confirmé cómo cuenta los tokens (entrada = estado + preguntas + criterios; o si las preguntas repetidas se cachean).

## 5. Datos de la empresa: fundadores, financiación y valoración

### Takeaway
TypeSafe AI se fundó en 2024. La fundaron Diogo Almeida (CEO, ex-OpenAI), Erik Gafni y Sasha Sheng. Salió del modo stealth el 15 de septiembre de 2026 con una ronda seed de $40M liderada por DCVC, que según el FT la valoraba en $200M. Alrededor de 10 días después, The Information informó de conversaciones para levantar más de $1.000M con una valoración de más de $10.000M. Esto último no está confirmado por la empresa.

### Cited Findings
- **Estructura de la ronda y fundadores:** seed de $40M liderada por DCVC. La fundaron Diogo Almeida (ex-OpenAI, "co-inventor of RLHF/ChatGPT"), Erik Gafni y Sasha Sheng — [AIwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/); [FinSMEs](https://www.finsmes.com/2026/09/typesafe-ai-raises-40m-in-seed-funding.html); [The AI Insider](https://theaiinsider.tech/2026/09/17/typesafe-ai-emerges-from-stealth-with-40m-to-build-machine-native-ai-models/)
- **Fundación y trayectoria de Almeida:** fundada en 2024. En OpenAI trabajó en aprendizaje por refuerzo, InstructGPT, ChatGPT y GPT-4 — [Hoodline](https://hoodline.com/2026/09/sf-startup-s-chat-free-ai-draws-10-billion-offers-a-week-after-launch/) / [Sovereign Magazine](https://www.sovereignmagazine.com/article/typesafe-jev-reported-10-billion-valuation) (fragmento combinado)
- **Autodescripción:** "a frontier AI lab building machine-native, composable AI" — [AIwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/)
- **Valoración de la seed:** $200M según el Financial Times. Bloomberg informó de la seed de $40M liderada por DCVC — [Sovereign Magazine](https://www.sovereignmagazine.com/article/typesafe-jev-reported-10-billion-valuation) / [GuruFocus](https://www.gurufocus.com/news/9096952/typesafe-ais-jev-model-attracts-10-billion-valuation-amidst-ai-cost-concerns) (fragmento; no pude leer Bloomberg ni el FT directamente)
- **Conversaciones posteriores:** según The Information, conversaciones para levantar más de $1.000M con una valoración superior a $10.000M. Ofertas de más de $10.000M a unos 10 días del lanzamiento — [AI Weekly, citando a The Information](https://aiweekly.co/alerts/the-information-typesafe-in-talks-to-raise-1b-at-10b-valuation-days-after-40m); [The Information en X](https://x.com/theinformation/status/2103839519019569371); [Hoodline](https://hoodline.com/2026/09/sf-startup-s-chat-free-ai-draws-10-billion-offers-a-week-after-launch/)

### Inferences
- La ronda de más de $1.000M a más de $10.000M es un informe de prensa sobre conversaciones, no un cierre anunciado. Hay que tratarla como no confirmada.

### Gaps
- No tengo una confirmación oficial de TypeSafe sobre la valoración de $200M ni sobre las conversaciones de $10.000M.
- No conozco los otros inversores de la seed.
- No pude acceder a Bloomberg, al FT ni a heise para leer el texto original.
