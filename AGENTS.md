# AGENTS.md — Manual de este vault

> Manual operativo **universal**, para cualquier agente compatible con la
> [Agent Skills specification](https://agentskills.io/specification) (Claude Code, Codex,
> OpenCode…) — el mismo estándar detrás del [plugin de Kepano](https://github.com/kepano/obsidian-skills)
> que este kit usa. **Gemelo de `CLAUDE.md`** (mismas reglas; si editas uno, actualiza el otro).
> Filosofía: **"file-over-app"** (Kepano) + estándar **OKF** (Google). La constitución vive en
> **`Admin/`**.

## `Admin/` es la constitución — léela SIEMPRE antes de crear, editar o clasificar
- **Reglas del vault:** `Admin/Reglas del Vault.md` — formato híbrido OKF+Kepano + ética (caso
  de estudio de nota roja mexicana).
- **Vocabulario permitido:** `Admin/Catálogo de Metadatos.md` — campos, enums y su porqué. Elige
  **solo** de aquí; nunca inventes campos ni valores.
- **Formato, nombres y mapa de carpetas:** `Admin/Guía de Estilo.md`.
- **Plantillas:** `Admin/Templates/` — cinco de ejemplo (`event`, `context`, `investigation`,
  `organization`, `person`) más la plantilla mínima del estándar
  (`_plantilla-okf-genérica.md`), que es tu verdadero punto de partida si estás adaptando esto.
- **El estándar y sus límites:** `Admin/Open Knowledge Format — cómo funciona.md` — qué exige
  OKF de verdad, y dónde este vault decide no seguirlo al pie de la letra (y por qué).
- **Bitácora:** `Admin/Log/` — una nota por día (`log-AAAA-MM-DD.md`), orden cronológico
  inverso (lo más reciente arriba).

## 0. Protocolo
1. Abre `Guía de Estilo.md` y `Catálogo de Metadatos.md` para el vocabulario cerrado y el mapa
   del vault.
2. Antes de crear una entidad, busca si ya existe (por título y `aliases`) para no duplicar
   nodos.
3. Parte de una plantilla de `Admin/Templates/`; **no** armes el frontmatter a mano.

## 1. Qué es este vault
Un andamiaje de base de conocimiento por entidad: cada nota es un **evento** (hecho localizable
y efímero, `type: event`/`context` en el ejemplo) o describe una **entidad** (sustantivo fijo,
`type: person`/`organization`), conectados por enlaces tipados. Es un **híbrido**: frontmatter
conforme a OKF + el vocabulario de tu propio dominio → exportable a DB relacional o de grafo el
día que haga falta (ver README, "Antes, no después").

Este kit viene poblado con un ejemplo de dominio (nota roja mexicana, cinco `type`), pero
**el dominio no es lo que se comparte — la arquitectura sí.** Cámbialo por el tuyo.

## 2. Estructura (dónde va cada cosa)
- **`Notes/`** (plano) → tus tipos de "evento": lo que pasó, con fecha y lugar.
- **`Entities/`** (plano) → tus tipos de "sustantivo": lo que existe, fijo en el tiempo.
- **`Bases/`** → vistas `.base` = **el clasificador**: filtran por `type` y los campos que tú
  definas (no se clasifica con carpetas).
- **`Admin/`** → la constitución (no se escribe aquí en el día a día, salvo el Log).
- **`Inbox/`** → material sin clasificar todavía, a la espera de procesarse.
- **Raíz** → `AGENTS.md`, `CLAUDE.md`, `.claude/` (skills + hooks). Se mantiene limpia.

## 3. Reglas sagradas
1. **Frontmatter en inglés, limpio y desglosado.** Claves y enums en inglés (portables,
   exportables); título y texto libre en el idioma que prefieras. Significado y mapeo →
   `Catálogo de Metadatos.md`.
2. **Vocabulario cerrado.** `type` es un enum fijo. No inventes campos ni valores — proponlos y
   espera confirmación. Un **gate determinista** (hooks en `.claude/`) corre el portero al
   escribir y al cerrar el turno: un valor fuera de enum se **bloquea** — corrige el valor, no
   sortees el hook (qué trae este kit y qué falta de esa pieza: README, "Sobre el portero").
3. **Sin `tags`, sin `categories`, sin campo de confianza.** El filtrado lo hacen `type` y tus
   propios campos; la corroboración se ve por los **backlinks**, no se declara a mano.
4. **Relaciones = enlaces `[[ ]]` en el frontmatter**, nunca sueltas en el cuerpo. Las
   relaciones simétricas entre entidades deben ser **recíprocas** — que su ausencia sea un error
   del portero, no un aviso que nadie lee.
5. **Registra todo cambio** en la nota del día en `Admin/Log/` (`## HH:MM — Título`); lo más
   reciente **ARRIBA** (orden cronológico inverso, no se anexa al final).

## 4. Ética, si tu dominio la necesita
- Este vault de ejemplo (nota roja mexicana) exige una política ética explícita: nombres reales
  de la fuente en captura, presunción de inocencia por encuadre (`alleged: true` + atribución,
  nunca afirmar culpabilidad), y la anonimización reservada para el momento de publicar, nunca
  para el vault de trabajo. Detalle real en `Admin/Reglas del Vault.md` §5 — como caso de
  estudio, no receta universal.
- Si tu dominio toca personas, menores, salud o cualquier dato sensible: define tu propia
  política **antes** de capturar la primera nota. Improvisarla a medio proyecto es exactamente
  el tipo de deuda que este kit existe para evitar (README, "Antes, no después").

## 5. Skills de Obsidian — úsalas siempre, no inventes sintaxis
Las cuatro primeras son el plugin oficial de Kepano (`kepano/obsidian-skills`, MIT); instálalas
desde la fuente (ver README). La sintaxis la dan ellas; el *contenido* permitido lo da tu
`Catálogo de Metadatos.md`.

| Cuando toques… | Skill | Para |
|---|---|---|
| Cualquier `.md` | **obsidian-markdown** | wikilinks, embeds, callouts, propiedades. |
| Un `.base` | **obsidian-bases** | vistas, filtros, fórmulas. |
| El vault por CLI | **obsidian-cli** | abrir/buscar/crear notas, backlinks, automatización — la versión de este kit ya está adaptada al esquema propio (`.claude/skills/obsidian-cli/`), como ejemplo. |
| Un `.canvas` | **json-canvas** | nodos, aristas, mapas de relaciones. |

Además de estas, mi propio vault usa skills **propias** que no vienen en este kit (son
específicas de mi dominio) — las nombro como ejemplo del tipo de herramienta que vale la pena
construirte encima de este andamiaje:
- Una skill de **clasificación** — decide el `type` y la plantilla al capturar una nota nueva,
  aplicando tu esquema y tu ética.
- Una skill de **drenado por lotes** — procesa todo tu `Inbox/` de una sentada, nota por nota.
- Una skill de **búsqueda por entidad** — resuelve alias→canónico y arma el expediente de una
  entidad con sus relaciones y procedencia (el objetivo estrella de este tipo de vault).
- Una skill de **salud del grafo** — detecta entidades duplicadas bajo nombres distintos y las
  fusiona guiado, offline.
- Una skill de **briefing** — sintetiza lo ya capturado sobre un tema, citando fuente y fecha de
  cada afirmación.

Ninguna de las cinco viene en el kit porque su lógica depende enteramente de tu dominio; el
patrón sí es reusable.
