# CLAUDE.md — Copiloto de este vault

> Cómo operar aquí. **Gemelo de `AGENTS.md`** (mismas reglas — si editas uno, actualiza el
> otro; ese gemelo es a propósito, ver README). Filosofía **file-over-app** (Kepano) + **OKF**
> (Google). La constitución vive en **`Admin/`**; el manual completo está en `AGENTS.md`.

## Empieza aquí
1. Lee la constitución en **`Admin/`**: `Reglas del Vault.md`, `Catálogo de Metadatos.md`
   (vocabulario + enums), `Guía de Estilo.md` (formato + carpetas), y
   `Open Knowledge Format — cómo funciona.md` (el estándar, y dónde este vault se desvía de él
   a propósito).
2. Antes de crear una nota: busca si la entidad ya existe (título + `aliases`) para no duplicar
   nodos.
3. Parte de una plantilla de `Admin/Templates/`. Si estás adaptando este kit a tu propio
   dominio, no edites mis cinco plantillas directamente — parte de
   `Admin/Templates/_plantilla-okf-genérica.md` (ver README, sección "Cómo adaptarlo a lo
   tuyo").
4. Usa las skills de `.claude/skills/`: la sintaxis de Obsidian la dan `obsidian-markdown`,
   `obsidian-bases`, `json-canvas` y `obsidian-cli` (plugin oficial de Kepano; instrucciones de
   instalación en el README). El *contenido* permitido lo da `Admin/Catálogo de Metadatos.md` —
   las skills nunca inventan vocabulario.

## Estructura
`Notes/` (plano: tus tipos de "evento" — lo efímero) · `Entities/` (plano: tus tipos de
"sustantivo" — lo fijo) · `Bases/` = vistas `.base` (**el clasificador**, no las carpetas) ·
`Admin/` = la constitución · `Inbox/` = material sin clasificar todavía · raíz limpia.

## Reglas sagradas
1. **Frontmatter en inglés**, limpio y desglosado (títulos y texto libre en el idioma que
   prefieras). Mapeo y enums en `Admin/Catálogo de Metadatos.md`.
2. **Vocabulario cerrado.** `type` es un enum fijo (aquí, cinco valores de ejemplo — cámbialos
   por los de tu dominio). No inventes campos ni valores; propón el cambio y espera confirmación.
   Un **gate determinista** (hooks en `.claude/`) corre el portero al escribir y al cerrar el
   turno, y **bloquea** valores fuera de enum — corrige el valor, no sortees el hook (detalle de
   qué trae este kit y qué falta: README, sección "Sobre el portero").
3. **Sin `tags`, sin `categories`, sin campo de confianza.** La corroboración se ve por
   backlinks, no se teclea a mano (README, sección "Los superpoderes que esto le da a un LLM").
4. **Relaciones = enlaces `[[ ]]` en el frontmatter**, nunca en el cuerpo. Cuando definas
   relaciones simétricas entre entidades (pareja, rivalidad, alianza…), hazlas **recíprocas** —
   su ausencia debería ser un error que tu portero rechace, no un aviso que se ignora.
5. **Registra todo cambio** en `Admin/Log/log-AAAA-MM-DD.md` (`## HH:MM — Título`); **lo más
   reciente ARRIBA** (orden cronológico inverso, nunca se anexa al final).

## Ética, si tu dominio la necesita
Este kit nació de un vault para un dominio concreto (nota roja mexicana) que sí exige una
política ética explícita: fiel al origen en la captura, presunción de inocencia por encuadre,
anonimización solo en la publicación — nunca en el vault de trabajo. El detalle real está en
`Admin/Reglas del Vault.md` §5, como caso de estudio, no como receta universal. Si tu dominio
toca personas, menores, salud o cualquier dato sensible, define tu propia política **antes** de
capturar la primera nota — no la improvises a medio proyecto.
