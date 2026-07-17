# Kit de arranque: un vault de conocimiento consultable por IA

Este es el andamiaje de un vault en [Obsidian](https://obsidian.md) diseñado para que una IA
pueda ayudarte a capturarlo y consultarlo, con reglas lo bastante estrictas como para poder
confiar en lo que capturó.

No es un producto. Es la metodología detrás de un proyecto personal (un mapa de crimen y poder
en México) despojada de todos los datos reales. Lo comparto para que apliques la misma lógica a
tu propio material: investigación de campo, entrevistas, un archivo periodístico, lo que sea.

## La idea de fondo

Todo lo demás cuelga de una sola distinción: **separar los sustantivos de los verbos.**

- Una **entidad** es un sustantivo (una persona, una organización). Existe. Es fija,
  monolítica, y el tiempo no le hace nada.
- Un **evento** es un verbo (un hecho, una fecha, algo que pasó y ya). Es efímero, y no vive
  solo: orbita a las entidades que aparecen en él.

El día que dejas de guardar "notas" y empiezas a guardar sustantivos con sus verbos alrededor,
la pregunta "¿qué hay de esta persona/organización?" por fin tiene dónde caer: son todos los
verbos que la rodean.

## La filosofía híbrida

Dos ideas que llegan al mismo lugar por caminos distintos:

- **Kepano** (el desarrollador de Obsidian) y su "file over app": tus archivos tienen que
  sobrevivir al programa que los abre. Texto plano, nada propietario, portable para siempre.
- El **Open Knowledge Format (OKF)** de Google: un estándar abierto para que un modelo de
  lenguaje lea tu conocimiento sin depender de un proveedor. Exige poco — que cada archivo
  markdown tenga un encabezado YAML parseable con un campo `type` no vacío.

Este vault cumple ambas cosas a la vez, con las mismas ocho líneas de encabezado: un humano las
lee y las corrige en cualquier editor; una máquina las entiende sin tener que interpretar prosa.

## Los superpoderes que esto le da a un LLM

Un LLM sin esta estructura contesta desde texto suelto: adivina de dónde sacó el dato, no
distingue una mención de una relación real, y no tiene forma de saber si algo es corroborado o
si lo dijo un solo medio. Con esta arquitectura encima, un LLM gana capacidades concretas, no
genéricas:

- **Resuelve identidad, no solo texto.** No busca la cadena "Fulano" — busca un nodo. El apodo,
  el nombre completo y la variante mal escrita son la misma entidad, sin que el modelo tenga que
  adivinarlo cada vez que se lo preguntas.
- **La procedencia viene incluida, no inventada.** Cada afirmación ya carga quién la dijo
  (`source`) y cuándo (`timestamp`/`published`). El LLM no tiene que recordar de dónde sacó el
  dato para citarlo — el dato mismo trae la cita puesta.
- **La corroboración es estructural, no una opinión del modelo.** No hay campo de "confianza"
  porque no hace falta: cuántos hechos distintos enlazan a la misma entidad ya ES la
  corroboración. El LLM cuenta respaldo real en vez de generar una sensación de qué tan creíble
  suena algo.
- **Las relaciones están tipadas y son navegables, no inferidas por cercanía.** El modelo no
  adivina "seguro se conocen porque aparecen juntos" — la relación ya está declarada, con
  dirección y con reciprocidad garantizada por el portero. "¿Quién conoce a quién?" deja de ser
  una conjetura y se vuelve una consulta.
- **El rol vive en el hecho, no en la persona.** La misma entidad puede jugar un papel distinto
  en cada evento que la menciona. El LLM puede contestar "¿qué papel jugó en cada cosa que le
  pasó?" en vez de encasillarla con una etiqueta fija para siempre.
- **La alucinación tiene techo.** Donde el dominio es cerrado (una fecha, un estado, un tipo), el
  LLM acierta o el portero lo rechaza — no hay término medio donde el modelo invente una
  categoría plausible que no existe en tu vocabulario.
- **La capa de consulta no está atada a un proveedor.** Como el vault es conforme a OKF (ver
  abajo), cualquier agente que hable el estándar lo puede leer sin que le enseñes tu formato
  desde cero. La asistencia investigativa no depende de que sigas usando el mismo modelo para
  siempre.

## Por qué las reglas no son gustos, son una correa

Dejar que una IA capture tu material suena imprudente, y lo es si no le pones límites. Un
modelo suelto se inventa categorías, cambia de criterio a media tarea y te deja un archivo bien
bonito que no sirve para nada.

Por eso el vocabulario está cerrado y hay un portero que no es el modelo (ver `.claude/`
abajo): un programa que revisa cada ficha contra el contrato y la rechaza si se salió. Con eso
no se negocia.

## Antes, no después

Definir los campos del esquema cuesta una tarde. No definirlos, y dejar que el LLM improvise
sobre la marcha, cuesta meses: notas con campos que no coinciden entre sí, una categoría que
cambió de nombre a medio proyecto, una migración dolorosa para enderezar lo ya escrito. La
diferencia no es de esfuerzo total, es de **cuándo lo pagas**.

Ayuda pensarlo con un concepto de arquitectura de bases de datos. Una base de datos relacional
(la que usa tablas y SQL) impone su estructura *al escribir*: antes de guardar una fila, un motor
la revisa contra las columnas y los tipos que ya existen, y la rechaza si no calza. Una carpeta de
archivos de texto no trae ningún motor así de fábrica — nada revisa nada, puedes escribir lo que
sea como sea, y el orden, si llega a existir, te lo impones tú, cuando puedas (o nunca).

Este vault es justamente eso: markdown suelto, sin ningún motor de base de datos detrás. La
diferencia es que no lo dejamos así. El esquema se define **antes**, con calma
(`Admin/esquema.yaml`), y el portero (sección de arriba) hace de aproximación al motor que aquí no
existe. Con una salvedad honesta, no una promesa exagerada: es una aproximación parcial — revisa
valor y tipo, no todo lo que revisaría un motor de verdad — y solo actúa en los caminos que pasan
por ella (una edición hecha directo en Obsidian, fuera de este flujo, no la activa). Aun
imperfecta, es lo único que se interpone entre un LLM sin supervisión y la misma cicatriz que
originó este proyecto: definiciones que divergen porque nunca vivieron en un solo lugar.

## Estructura

```
├── AGENTS.md                     ← manual completo, para cualquier agente (Claude Code, Codex…)
├── CLAUDE.md                     ← gemelo de AGENTS.md, resumen para Claude Code
├── Admin/
│   ├── esquema.yaml              ← el contrato: fuente única de verdad
│   ├── Reglas del Vault.md       ← la filosofía y la ética de captura
│   ├── Catálogo de Metadatos.md  ← el vocabulario, campo por campo
│   ├── Guía de Estilo.md         ← formato, nombres de archivo, estructura de carpetas
│   ├── Open Knowledge Format — cómo funciona.md   ← el estándar y dónde diverge este vault
│   └── Templates/
│       ├── _plantilla-okf-genérica.md   ← el punto de partida real (ver arriba)
│       └── (una plantilla por tipo de este ejemplo, ya adaptadas)
├── Bases/                        ← vistas .base: el clasificador (no las carpetas)
├── Notes/                        ← los eventos (los verbos)
├── Entities/                     ← las personas y organizaciones (los sustantivos)
├── Inbox/                        ← material sin clasificar, a la espera de procesarse
└── .claude/
    ├── settings.json             ← conecta los hooks de abajo a Claude Code
    ├── hooks/
    │   ├── check_frontmatter.py  ← valida al escribir (fail-open, feedback inmediato)
    │   └── gate_vault.sh         ← valida al cerrar el turno (fail-closed, el candado real)
    └── skills/
        └── obsidian-cli/         ← adaptación de la skill de Kepano (ejemplo, ver abajo)
```

`AGENTS.md`/`CLAUDE.md` son el punto de entrada: lo primero que lee cualquier agente antes de
tocar una nota. Son gemelos a propósito — mismas reglas, dos formatos, para que el mismo vault
sirva tanto a Claude Code como a cualquier otro agente que hable el
[estándar Agent Skills](https://agentskills.io/specification).

**Las carpetas son planas a propósito.** `Notes/` y `Entities/` no tienen subcarpetas.
Clasificar con carpetas es apostar a que hoy adivinaste la única forma en que vas a querer ver
tu material en diez años. Clasificar se hace con las vistas en `Bases/`, que se arman con
preguntas y se pueden tener veinte distintas del mismo material.

## Sobre el portero: lo que sí trae este kit y lo que no

Los dos hooks (`check_frontmatter.py`, `gate_vault.sh`) son el código real de mi proyecto, sin
editar. Hacen dos cosas complementarias, a propósito con políticas de falla opuestas:

- **Al escribir** (`check_frontmatter.py`): revisa el valor que se va a guardar contra
  `esquema.yaml`. Si falla, no bloquea — es fail-open, porque un enlace `[[X]]` puede apuntar a
  una ficha que se va a crear en el siguiente paso.
- **Al cerrar el turno** (`gate_vault.sh`): corre el validador completo sobre el estado final del
  vault. Si el contrato no se cumple, bloquea el cierre. Es fail-closed: el candado real.

**Lo que falta:** `check_frontmatter.py` llama a un módulo Python (`obsidiana.vault`) que hace la
validación real leyendo `esquema.yaml` — ese módulo es parte de un motor más grande y no viene en
este kit. Para replicar el patrón necesitas escribir tu propio validador (no es complicado: leer
el YAML, revisar que cada campo tenga un valor dentro de su enum, fallar si no) y ajustar la ruta
de carpeta que trae hardcodeada (`Vault-NotasRojas`) al nombre de la tuya.

## Las skills que lo redactan

Tres de las herramientas que uso para escribir y consultar el vault **no son mías** — son el
[plugin oficial de Kepano](https://github.com/kepano/obsidian-skills) para Claude Code, Codex y
OpenCode, con licencia MIT:

- `obsidian-markdown` — wikilinks, callouts, propiedades y el resto de Obsidian Flavored
  Markdown.
- `obsidian-bases` — crear y editar las vistas `.base` (filtros, fórmulas, resúmenes).
- `json-canvas` — crear y editar archivos `.canvas` (como el que arma el diagrama de este kit).

No las copié a este repo: se instalan directo de la fuente, así nunca quedan desactualizadas.

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

La cuarta, `obsidian-cli` (en `.claude/skills/obsidian-cli/` de este kit), **sí la adapté** al
vocabulario de mi esquema — es el ejemplo que dejo de cómo se personaliza una skill genérica de
Kepano para un dominio propio. Cámbiala por la tuya.

Sobre la lógica exacta del estándar de Google que hace posible que un LLM lea todo esto sin que
le enseñes tu formato desde cero, y de dónde este vault decide **no** seguirlo al pie de la
letra: [`Admin/Open Knowledge Format — cómo funciona.md`](Admin/Open%20Knowledge%20Format%20%E2%80%94%20c%C3%B3mo%20funciona.md).

**El punto de partida real, antes de las cinco plantillas de este proyecto, está en
`Admin/Templates/_plantilla-okf-genérica.md`**: el archivo mínimo que el estándar exige, sin
nada de nota roja encima. Las cinco plantillas de este kit son esa plantilla genérica después de
cinco decisiones de adaptación (documentadas en el doc de arriba); para tu propio dominio, el
punto de partida es el genérico, no las cinco mías.

## Cómo adaptarlo a lo tuyo

1. Parte de `Admin/Templates/_plantilla-okf-genérica.md`, no de mis cinco plantillas —
   repite ahí las decisiones de adaptación que documento en el doc de OKF, con tu propio
   dominio.
2. Cambia el `type` por los de tu dominio (no tienen que ser cinco; sí te conviene que la
   lista quede **cerrada**, en `Admin/esquema.yaml`).
3. Agrega los campos y enums propios en `Admin/esquema.yaml` para lo que tú necesitas capturar.
   `Admin/Catálogo de Metadatos.md` es la vista humana de lo mismo — regenérala a mano.
4. Repite el paso 1 por cada `type` que hayas definido — puedes terminar con más o menos de
   cinco plantillas, según tu dominio.
5. Escribe tu propio validador (o adapta uno existente) y conéctalo en `.claude/hooks/`.
6. Empieza a capturar. La red se teje sola: cada vez que enlazas una entidad en una nota, ya
   quedó conectada con todo lo demás que la menciona.

## Qué no es esto

No es una base de datos. No es un producto terminado. Es un experimento personal, todavía en
construcción, que decidí compartir como metodología abierta porque el estándar que lo hace
posible (OKF) apenas se publicó y creo que vale la pena que más gente lo use, no solo yo.

¿Es perfecto? No. Pero qué cosa lo es.
