---
type: reference
categories: [OSINT, Methodology, Administration]
title: "Catálogo de Metadatos — Proyecto Obsidiana"
timestamp: "2026-07-16T01:14:45Z"
aliases: [Vocabulario, Metadata Index, Diccionario de Campos]
---

# Catálogo de Metadatos (vocabulario cerrado)

> **FUENTE ÚNICA DE VERDAD: `Admin/esquema.yaml`** (contrato machine-readable, `schema_version: 5`). Este catálogo es la **vista humana** del esquema; las plantillas, la skill `clasificar-nota` y el portero (`python3 -m obsidiana validar-vault`) son otras vistas. **Si algo difiere, el YAML manda** y las vistas se regeneran (gobernanza en §6). Las **preguntas** que el esquema responde —y que justifican cada campo— viven en [[Preguntas de la Base]].

> Índice maestro del vocabulario. Frontmatter **limpio y desglosado** en las notas; significado, valores y mapeo, **aquí**. **Claves en inglés** (portables/exportables); títulos y texto libre en español. Formato en [[Guía de Estilo]]; reglas/ética en [[Reglas del Vault]].

## 1. `type` — la clase de cada nota (enum cerrado)
| type | Qué es |
|---|---|
| `event` | Un **hecho localizable** (incidente). Conecta a lugar, clasificación, personas y organizaciones. |
| `context` | El **"clima"** de un lugar/tema (cifras, política, operativos), a cualquier nivel geográfico. |
| `person` | **Ficha de un actor** (perfil de una persona pública/criminal adulta). |
| `organization` | **Ficha de una organización** (cártel, célula, institución). |
| `investigation` | **Pieza analítica** multi-fuente (tipo InsightCrime). |

> Las notas del `Admin/` usan `type: reference` (documentación).

## 1b. `case` — la partición por investigación (solo en las notas)
Las **notas** (`event`/`context`/`investigation`) llevan **`case`** = a qué investigación/dataset pertenecen. Hace el vault **multi-caso** (un híbrido) sin mezclar. Las **entidades NO** llevan `case`: una persona/organización es un nodo **compartido**; su caso se deduce de sus **backlinks**.
| case | Qué |
|---|---|
| `notas-rojas` | crimen violento (dataset original; alimenta el mapa **Itztli**) |
| `corrupcion` | corrupción / escándalos de poder (**NO** va al mapa; sí al grafo) |

> **El mapa filtra `case: notas-rojas`** (+ coordenadas). Corrupción vive en el grafo y en sus Bases, no en Itztli. En notas de corrupción los campos de crimen (`sesnsp_*`, `deaths`, geo) quedan **vacíos** y `type` suele ser `investigation`/`context`/`event`.

## 2. Campos del frontmatter (todos en inglés)

### 2.1 OKF + procedencia
| campo | tipo | significado | → maestro |
|---|---|---|---|
| `type` | texto | clase (§1) | — |
| `title` | español | titular/nombre | — |
| `description` | español | resumen 5W (event) | `descripcion` |
| `url` | URI | URL (resuelta) del artículo | `url` |
| `source` | `[[nodo]]` | **medio/periódico** (nodo → conecta notas del mismo medio) | `fuente` |
| `author` | `[[nodo]]` | **autoría humana** de la nota (si la fuente la da) — v5 en event/context/investigation | — |
| `published` | AAAA-MM-DD | fecha de **publicación** del artículo (≠ `event_date`=hecho, ≠ `timestamp`=captura) — v5 en event/context/investigation | — |
| `timestamp` | AAAA-MM-DD | fecha de **captura** | `fecha_captura` |

> **Principio:** cada campo existe cuando algo lo **llena** (nada de columnas siempre-vacías). **v5 (procedencia):** `author`/`published` ya viven en `event`/`context`/`investigation` (antes solo en investigation); se llenan con la extracción de *meta* del artículo cuando la fuente la trae, vacíos si no. `street` y `country` (siempre MX) se omiten por ahora.

### 2.2 El hecho (`event`) → export a DB relacional
| campo | valores | significado | → maestro |
|---|---|---|---|
| `id` | hex(12) | llave estable (sha1 de 6 campos: url\|fecha\|municipio\|colonia\|clasificacion\|hecho) — **la MISMA columna `id` del maestro** (join) | `id` |
| `event_date` | AAAA-MM-DD | **fecha del hecho** (vacía si no se sabe) | `fecha` |
| `timestamp` | AAAA-MM-DD | fecha de **captura** — **obligatoria, jamás vacía** | `fecha_captura` |
| `deaths` | entero | **FALLECIDOS** en el hecho (heridos/desaparecidos/rescatados NO cuentan aquí). *Renombrado de `victims` 2026-07-16: el nombre viejo invitaba a contar mal.* | `victimas` |

> `tipo_fecha` se **deriva** al exportar (`event_date` llena → `incidente`; vacía → `nota`). **Desde v4** los 4 campos **SESNSP** (`bien_juridico/tipo/subtipo/modalidad`), `hora_incidente`, `rango_horario` y `hecho` viven **solo en el maestro** — ninguna pregunta del vault los usa ([[Preguntas de la Base]]); se recuperan por join con `id`.

### 2.3 Ubicación (para MAPEAR + homologar con INEGI)
| campo | valores | significado | fuente oficial / maestro |
|---|---|---|---|
| `state` | 32 entidades | estado | `estado` |
| `municipality` | texto | municipio (como lo escribe la fuente) | `municipio` |
| `locality` | texto | colonia/localidad | `colonia_localidad` |
| `cvegeo` | 5 díg. | **LA llave canónica INEGI** del municipio (los 2 primeros dígitos son la entidad) | **INEGI** |
| `lat` / `lon` | decimal | coordenadas (pueden ser aprox.) | `latitud`/`longitud` |
| `geo_precision` | street·locality·municipality·state | exactitud de la coordenada | `precision_geo` |

> **v4:** `cve_ent` se quitó (derivable: `cvegeo[:2]`) y `cp` también (ninguna pregunta lo usa; el catálogo INEGI de colonias trae 33k sentinelas "00000").

> `context` añade `scope` (nivel geográfico) y llena la ubicación **hasta ese nivel** (un dato nacional no lleva municipio).

### 2.4 Relaciones (enlaces `[[ ]]` → aristas del grafo)
| campo | forma | export a DB relacional |
|---|---|---|
| `classification` | `"[[homicidio]]"` | quita corchetes → `clasificacion` (el valor interno ∈ enum §3) |
| `place` | `"[[Municipio, Estado]]"` | derivado de state+municipality |
| `entities` | `["[[Nombre]]", "[[Cártel …]]"]` | **UNIÓN derivada de los `actors_*`** (el portero verifica la igualdad). **Regla:** toda **persona nombrada** (víctima/presunto/funcionario/civil) → algún `actors_*` **+ ficha `person`**; cárteles/instituciones → ficha `organization`. **Protocolos/programas** (Protocolo Alba…) NO son entities. |
| `theme` | `"[[…]]"` | (context/investigation) tema tratado |

### 2.4b Rol del actor EN la nota (`event` — la "tabla puente con atributo")
El rol de un actor **en ese hecho** vive en el nombre del campo (listas planas de wikilinks → el grafo y Bases funcionan; exporta 1:1 a tabla puente evento×actor con columna `rol`). El `role` de la ficha `person` es su rol **global/ocupacional** — no lo confundas con el rol-en-el-hecho.
| campo | quiénes |
|---|---|
| `actors_victim` | víctimas del hecho nombradas por la fuente |
| `actors_alleged` | **presuntos** en este hecho (ficha con `alleged: true` + atribución en el cuerpo) |
| `actors_authority` | autoridades/instituciones que investigan o responden |
| `actors_mentioned` | citados sin rol operativo (colectivos, testigos, contexto) |

> Solo `event` lleva `actors_*`; en `context`/`investigation` `entities` es directa. Una misma persona puede ser víctima en una nota y señalada en otra — por eso el rol va en la **arista**, no en el nodo.

### 2.5 Entidades (`person` / `organization`)
| campo | tipo | valores / notas |
|---|---|---|
| `aliases` | lista | variantes/alias del nombre |
| `role` | enum | (person) ver §3 — rol **global/ocupacional** (el rol-en-el-hecho va en `actors_*`, §2.4b) |
| `organizations` | lista `[[ ]]` | (person) organizaciones a las que pertenece |
| `status` | enum | ver §3 |
| `alleged` | true/false | (person) presunto (señalado sin sentencia) |
| `org_type` | enum | (organization) |
| `scope` | enum | (organization) ámbito de operación |

**Título canónico de `organization`:** nombre oficial **COMPLETO**; los acrónimos van **SIEMPRE** en `aliases` (no al revés). Nombres genéricos que existen en varios estados se **desambiguan** con el estado: `Agencia Estatal de Investigación (Chihuahua)`.

### 2.5b Relaciones persona↔persona (frontmatter de `person`)
Listas planas de wikilinks — decisión del usuario 2026-07-16 (formaliza el piloto `## Relaciones` del clúster CJNG). **Todas exigen respaldo en el cuerpo (`## Relaciones`) con atribución a la fuente** ("según X") y son **recíprocas** (si A enlaza a B, B enlaza a A — la reciprocidad es ERROR del portero, auto-reparable con `obsidiana entidades reparar --apply`).
| campo | qué |
|---|---|
| `partner_of` | relación sentimental **actual** según la fuente |
| `ex_partner_of` | relación sentimental **pasada** |
| `family_of` | parentesco (el grado se detalla en el cuerpo) |
| `associate_of` | vínculo laboral / de negocios |
| `criminal_link` | **PRESUNTA** asociación criminal persona↔persona — atribución obligatoria; **nunca** afirmación de culpabilidad |

**Nexo persona→organización (v5).** El campo `alleged_link` (frontmatter de `person`) captura el **PRESUNTO** vínculo de una persona con una **organización** (cártel/célula/institución capturada) — la arista funcionario↔cártel que antes solo cabía en prosa. Wikilinks a fichas `organization`; **cross-type y NO recíproco** (la org lo ve por *backlinks*). `alleged` implícito: **atribución obligatoria** en `## Relaciones`, **nunca** culpabilidad.

### 2.5c Relaciones organización↔organización (frontmatter de `organization`, v5)
| campo | qué | simetría |
|---|---|---|
| `faction_of` | esta org es **célula/facción** de un cártel/estructura mayor | **asimétrica** (se escribe en el hijo; el padre se recupera por *backlinks*) |
| `rival_of` | **rivalidad/disputa** con otra org | simétrica, recíproca |
| `allied_with` | **alianza/cooperación** con otra org | simétrica, recíproca |

> Wikilinks a fichas `organization`, con respaldo en el cuerpo (`## Relaciones`) + atribución. Otros tipos (absorbe a, escisión de) siguen en prosa hasta que una pregunta los pague (extensión = gobernanza §6).

## 3. Enums (valores permitidos)
- **`type`:** `event` · `context` · `person` · `organization` · `investigation`
- **`geo_precision`:** `street` · `locality` · `municipality` · `state`
- **`scope` (context):** `national` · `state` · `municipal` · `locality` · `street`
- **`role` (person):** `politician` · `journalist` · `official` · `criminal` · `military` · `business` · `civilian` · `unknown`
- **`status` (person):** `active` · `detained` · `fugitive` · `killed` · `sentenced` · `desaparecido` · `unknown`
- **`org_type`:** `cartel` · `cell` · `gang` · `institution` · `party` (partido político) · `collective` (colectivo de sociedad civil / búsqueda) · `business` (empresa privada / corporación, p. ej. proveedor de spyware)
- **`scope` (organization):** `local` · `state` · `regional` · `national` · `transnational`
- **`status` (organization):** `active` · `fragmented` · `dismantled` · `unknown`
- **`case`:** `notas-rojas` · `corrupcion` (extensible por gobernanza §6 — una investigación = un `case`; el mapa solo usa `notas-rojas`)
- **`actor_roles` (sufijos de `actors_*`, §2.4b):** `victim` · `alleged` · `authority` · `mentioned`
- **`person_relations` (§2.5b):** `partner_of` · `ex_partner_of` · `family_of` · `associate_of` · `criminal_link` (+ `alleged_link` = nexo presunto persona→organización, v5)
- **`org_relations` (§2.5c):** `faction_of` · `rival_of` · `allied_with`
- **`classification` (van como `[[nodo]]`, dominio CERRADO — extensión solo por gobernanza §6):**
  - crimen (9): homicidio · feminicidio · secuestro · desaparicion · robo con violencia · extorsion · **narcoviolencia-enfrentamiento** · hallazgo de restos · otro
  - corrupción (6): corrupcion · peculado · cohecho · conflicto de interes · abuso de autoridad · enriquecimiento ilicito
  - *Nota:* en el vault el valor va **sin barra** (`narcoviolencia-enfrentamiento`) porque `[[narcoviolencia/enfrentamiento]]` rompe el nodo (Obsidian lee la barra como carpeta). El maestro conserva su token con barra; el mapeo vive en `esquema.yaml → mappings.classification`.
- **SESNSP** (`sesnsp_*`): cadenas exactas del catálogo oficial de incidencia delictiva (fuente de verdad: `obsidiana/sesnsp.py`); inferencias con sufijo " (presunto)"; **vacío = sin dato** (prohibido copiar el tipo en subtipo/modalidad para "rellenar").

## 4. Homologación y export
El vault usa **claves en inglés**; el maestro (`datos/notas_rojas_maestro.csv`) usa español — el mapeo (columna → maestro, arriba) permite exportar a **DB relacional** (campos planos = columnas; los enlaces se exportan **sin corchetes** o como tabla de relaciones) o de **grafo** (los `[[enlaces]]` = aristas). Los **códigos oficiales** (`cve_ent`/`cvegeo` INEGI, `cp` SEPOMEX) homologan la geografía con las fuentes que el proyecto **ya usa** (el geocoder) → llenar esos campos es un pequeño ajuste al pipeline.

## 5. Ética (política — detalle en [[Reglas del Vault]])
**Vault LOCAL = FIEL AL ORIGEN:** conserva los nombres reales de la fuente (víctimas, presuntos, funcionarios, menores) — no se anonimiza en captura. Presuntos → `alleged: true` + atribución a la fuente. La **anonimización/agregación es en la PUBLICACIÓN** (`PUBLICACION.md`), no en el vault. Vault gitignored (PII/LFPDPPP, no se difunde).

## 6. Gobernanza del esquema (cómo evoluciona el vocabulario)
Los pilotos de ingesta van revelando necesidades nuevas (campos, valores, relaciones). El cambio **NUNCA** se hace "de paso" en una nota o en una vista; sigue este ciclo:
1. **Detectar** — un piloto/ingesta encuentra algo que el esquema no captura.
2. **Proponer** — se registra en el Log del día con la evidencia (qué nota, qué faltó).
3. **Aprobar** — decisión explícita del usuario (AskUserQuestion o instrucción directa).
4. **Editar SOLO `Admin/esquema.yaml`** (sube `schema_version` si cambia el contrato).
5. **Regenerar las vistas** — este Catálogo, plantillas, skill `clasificar-nota`; si hay notas existentes que migrar, `ops/migrar_vault.py`.
6. **El portero lo exige** — `python3 -m obsidiana validar-vault` (en `obsidiana/vault.py`) valida contra el YAML nuevo; además el **gate** (hooks en `.claude/`) lo corre solo al escribir/cerrar el turno.

**Regla de nacimiento de campos** (decisión del usuario, 2026-07-16): *un campo solo nace de una **pregunta repetida** que no se puede responder sin él* ([[Preguntas de la Base]]). Cada campo es una promesa de consistencia que se cumple en CADA ingesta para siempre — se mantiene el **mínimo indispensable**.

Precedentes: `org_type` += `party`/`collective` (2026-07-16) · `org_type` += `business` (2026-07-16, para empresas privadas tipo NSO Group/Grupo KBH; espeja `role: business` de person) · `updated` (opcional) += person/organization (2026-07-16, fecha del expediente; skill `expediente`) · `actors_*` + relaciones persona↔persona + `victims`→`deaths` (2026-07-16, auditoría de arquitectura) · **recorte v4**: −`sesnsp_tipo/subtipo/modalidad`, −`cve_ent`, −`cp` en `event` (2026-07-16, Paso 0: ninguna pregunta del vault los pagaba) · campo `evidence` **descartado** (el nivel de evidencia vive en la prosa, Reglas §4).

Relacionado: [[Guía de Estilo]] · [[Reglas del Vault]] · [[Auditoría Arquitectura 2026-07-16]]
