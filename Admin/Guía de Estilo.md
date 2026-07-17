---
type: reference
categories: [OSINT, Methodology, Administration]
title: "Guía de Estilo — Proyecto Obsidiana"
timestamp: "2026-07-16T01:14:45Z"
aliases: [Style Guide, Formato]
---

# Guía de Estilo (formato del vault de notas rojas)

> Fuente de verdad del **formato**. Vocabulario permitido en [[Catálogo de Metadatos]]; reglas y ética en [[Reglas del Vault]]. Las plantillas viven en `Admin/Templates/` — no armes el frontmatter a mano.

## 1. Estructura de carpetas
```
Vault-NotasRojas/
├── Inbox/       ← notas crudas sin clasificar (status: sin-procesar) → se procesan a Notes/ y se retiran
├── Notes/        ← type: event · context · investigation   (PLANO — estructurado)
├── Entities/     ← type: person · organization      (PLANO — nodos; los lugares son enlaces implícitos)
├── Bases/        ← vistas .base = el CLASIFICADOR (filtra por type/classification/state/role…)
├── Admin/        ← constitución: Reglas, Catálogo, Guía, Herramientas, Templates/, Log/
├── AGENTS.md · CLAUDE.md   ← manual de agentes (raíz limpia)
└── .claude/skills/         ← skills de Obsidian (Kepano)
```
**Carpetas planas a propósito:** no clasificamos con subcarpetas sino con **Obsidian Bases** (vistas `.base` en `Bases/` que filtran por `type`, `classification`, `state`, `role`…). Lo que importa es el `type` en el frontmatter y estar **bien enlazado** (`[[ ]]`), no la carpeta.

## 2. Nombres de archivo
- **event:** `AAAA-MM-DD-clasificacion-municipio-id6.md`
- **person:** `Nombre Apellido Apellido.md` (variantes en `aliases`)
- **organization:** **nombre oficial COMPLETO** (`Secretaría de Marina.md`, no `Semar.md`); los **acrónimos van SIEMPRE en `aliases`**. Nombres genéricos que existen en varios estados se desambiguan con el estado: `Agencia Estatal de Investigación (Chihuahua).md`.
- **lugar:** `Municipio, Estado.md`
- Un nombre = una nota; revisa `aliases` antes de crear para no duplicar nodos.

## 3. Las tres fechas
`event_date` = del **hecho** (vacía si no se sabe) · `timestamp` = de **captura** · `published` = del **artículo** (v5: en `event`/`context`/`investigation`; vacía si no se sabe). `author` = autoría humana (`[[nodo]]`), misma cobertura.

## 4. Relaciones en el frontmatter
`classification`, `place`, `theme` = **un** enlace `"[[…]]"`; `entities` = **lista** de actores `["[[…]]", …]` (en `event` es la **unión** de los `actors_*`, ver `Catálogo` §2.4b). Relaciones persona↔persona (`partner_of`, `ex_partner_of`, `family_of`, `associate_of`, `criminal_link`) = listas **recíprocas** en las fichas `person` (la reciprocidad es **error del portero**; auto-reparable con `obsidiana entidades reparar --apply`), respaldadas en `## Relaciones` con atribución (`Catálogo` §2.5b). **Nexos v5:** `alleged_link` (persona→organización presunta, no recíproco) y org↔org `faction_of`/`rival_of`/`allied_with` (`Catálogo` §2.5c). **Listas siempre en flujo inline** (`campo: ["[[A]]", "[[B]]"]`, nunca lista en bloque). Ver ejemplos en `Admin/Templates/`.

## 4b. Lectura ligera y footnotes citadas
- **Lectura barata** (ahorra tokens): `python3 -m obsidiana leer "<nota|ficha>" --sin-resguardo` emite frontmatter + cuerpo curado **sin** el bloque `## Texto completo (resguardo…)` (puede ser de ~90 líneas). `buscar … --limit N` acota los backlinks del expediente.
- **Footnotes de procedencia (gramática canónica, para expedientes):** cada afirmación citada usa `[^n]` y al pie **exactamente**: `[^n]: [Medio](url) — Autor, AAAA-MM-DD; vía [[nota del vault]].` — encadena origen externo + nota del vault, y es **parseable** (la evidencia por-afirmación sigue viviendo en la prosa, `Catálogo` §"disciplina de evidencia", pero así queda derivable).

## 5. Cuerpo de una nota
- **event / context:** `# {title}` (= `title` exacto) → descripción 5W → `## Texto completo (resguardo local — no publicar)` → `## Fuentes`.
- **person / organization:** `# {nombre}` → una línea de definición → `## Relaciones` (enlaces tipados **con atribución** — "según X") → `## Notas / Observaciones`. (Las fuentes = backlinks de los `event`.)
- **Enlaces inline:** los `[[…]]` se repiten en el **cuerpo curado** donde la mención exista. El **resguardo (`## Texto completo`) es copia FIEL: no se enlaza, no se edita** — un actor que solo aparece ahí va en `actors_*` sin enlace inline.

## 6. Plantillas (`Admin/Templates/`)
| Plantilla | type | Cuándo |
|---|---|---|
| `event` | event | Un hecho localizable. |
| `context` | context | Cifras/clima de un lugar o tema. |
| `person` | person | Ficha de un actor (adulto). |
| `organization` | organization | Ficha de un cártel/institución. |
| `investigation` | investigation | Análisis multi-fuente. |

## 7. Ética (resumen — detalle en [[Reglas del Vault]])
**Fiel al origen:** nombres reales de la fuente (incl. menores); presuntos con `alleged: true` + atribución. La anonimización es en la **publicación**; el vault es **local** (no difundir).

Relacionado: [[Catálogo de Metadatos]] · [[Reglas del Vault]]
