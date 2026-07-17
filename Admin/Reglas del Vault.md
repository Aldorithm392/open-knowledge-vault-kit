---
type: reference
categories: [OSINT, Methodology, Administration]
title: "Reglas del Vault — Proyecto Obsidiana"
timestamp: "2026-07-16T01:14:45Z"
aliases: [Reglas, Constitución del Vault]
---

# Reglas del Vault (notas rojas — OKF + Kepano + ética OSINT)

> La "constitución" de este vault. Sistema **híbrido**: estructura legible por máquinas (**OKF**, Google — Markdown+YAML portable, graph-shaped) + mínima fricción y foco en conexiones (**Kepano**, "file-over-app"). Vocabulario en [[Catálogo de Metadatos]]; formato en [[Guía de Estilo]].

## 1. Filosofía
- **File-over-app:** todo Markdown + YAML plano, portable, sin lock-in; **exportable** a cualquier DB (relacional o grafo).
- **Homologación:** el frontmatter refleja 1:1 las columnas del maestro (`datos/notas_rojas_maestro.csv`) → el vault y el CSV son **la misma verdad**.
- **Grafo:** cada entidad = un nodo; cada relación = un `[[enlace]]`. Un dato aislado vale poco; enlazado revela la red.

## 2. Frontmatter
- **Limpio y desglosado** en las notas; explicaciones/enums/mapeos en [[Catálogo de Metadatos]].
- **Claves en inglés** (portables/exportables a otras DB); títulos y texto libre en español. El mapeo a las columnas (español) del maestro se documenta en [[Catálogo de Metadatos]].
- **Vocabulario cerrado:** `type` ∈ `event · context · person · organization · investigation`. No inventar campos ni valores (proponer + confirmar antes).
- **Sin `tags`, sin `categories`, sin `confianza`** (decisión del proyecto, por mantenibilidad): el filtrado lo hacen `type`/`case`/los campos; la corroboración se ve por los backlinks.

## 3. Relaciones = enlaces en el frontmatter
Las relaciones (`classification`, `place`, `entities`, `theme`) van como `[[enlaces]]` **en el frontmatter** → Obsidian las grafica y otro sistema las parsea directo. (`entities` = actores mencionados —persona/organización/institución—; el `type` de cada uno vive en su nodo.) Además, entre entidades existen **relaciones tipadas** (`person_relations`, `alleged_link`, `org_relations`) — detalle en [[Catálogo de Metadatos]] §2.5; las **simétricas son recíprocas y su ausencia es ERROR del portero** (auto-reparable: `obsidiana entidades reparar --apply`), mientras que `alleged_link` y `faction_of` son de un solo sentido.

## 4. Confianza y procedencia
Nunca inventes datos: sin fuente, se omite o se marca *por verificar*. En el cuerpo, marca **Hecho / Autoreportado / Inferencia**. Las "fuentes" de una ficha `person`/`organization` = los `event` que la enlazan (backlinks).

## 5. ÉTICA (política del proyecto — decidida 2026-07-16)
- **FIEL AL ORIGEN (vault LOCAL):** el vault es un **registro fiel** de la fuente — conserva los **nombres reales** tal como los reporta el medio (víctimas, presuntos, funcionarios, e **incluso menores**). **NO se anonimiza en la captura.** Es un registro de investigación local, no una publicación.
- **Presuntos:** nombre real + `alleged: true` + **atribución a la fuente** ("según X…"); presunción de inocencia por **encuadre**, nunca afirmes culpabilidad como hecho.
- **La salvaguarda está en la PUBLICACIÓN, no en la captura:** el vault es **LOCAL** (gitignored, PII de fuentes públicas / LFPDPPP, no se difunde); lo que se publica se **anonimiza/agrega** (`PUBLICACION.md`). Ese split local↔publicado es la protección.
- OSINT de medios = **intensidad de reporteo**, no cifras oficiales (SESNSP/INEGI).

## 6. Registro de cambios
Cada cambio al vault se anota en `Admin/Log/` — **una nota por día** (`log-AAAA-MM-DD.md`), con `## HH:MM — Título`. Es la memoria del proyecto (no una nota por cambio).
- **Orden cronológico inverso (lo más reciente ARRIBA):** cada entrada nueva se inserta **justo debajo del `# H1`**, empujando las anteriores hacia abajo. **No** se anexa de forma continua al final. Así, al abrir el log, lo primero que se lee es lo último que pasó.

## 7. Ingesta
La recolección de noticias del proyecto **escribe estos `.md` directo al vault** (`event`/`context`), además del maestro CSV. Las fichas `person`/`organization` se crean al **analizar** los eventos (extraer actores/organizaciones y enlazarlos).

Relacionado: [[Catálogo de Metadatos]] · [[Guía de Estilo]]
