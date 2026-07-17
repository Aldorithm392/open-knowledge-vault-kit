---
name: obsidian-cli
description: Controla tu vault desde la terminal con la Obsidian CLI (v1.12) para leer, crear desde plantilla, mover, enlazar y auditar el grafo (backlinks/huérfanos), y para depurar plugins/temas. Actúa sobre la instancia VIVA de Obsidian (respeta sus ajustes, actualiza wikilinks al mover). Úsala para operar el vault por línea de comandos o triar el inbox.
---

# Obsidian CLI

> Esta skill es una **adaptación** de la skill genérica `obsidian-cli` del plugin oficial de
> Kepano (ver README del kit). El original opera cualquier vault; esta versión la ajustamos al
> vocabulario y a las rutas de nuestro propio esquema (`Admin/esquema.yaml`). Es el ejemplo que
> compartimos de cómo se hace esa adaptación — cámbiala por la tuya.

Opera el vault con el binario `obsidian`. Vía preferida para acciones que deben reflejarse en la app
viva (mover con actualización de wikilinks, crear desde plantilla, tableros `.base`).

> **La verdad de formato vive en `Admin/`.** La CLI da la *mecánica*; el *contenido permitido*
> (`type`, enums, campos) sale de `Admin/Catálogo de Metadatos.md` + `Admin/esquema.yaml` (el
> contrato) y lo exige el **portero** (tu validador, ver `.claude/hooks/`). **Nunca inventes
> vocabulario.**

## Antes de usarla
1. **Obsidian abierto.** Verifica: `obsidian version`. (Requiere instalador 1.12.7+ y el symlink en
   `/usr/local/bin/obsidian` o `~/.local/bin/obsidian`; el toggle Settings→General→Advanced→CLI.)
2. **Vault objetivo:** si el cwd es la raíz de tu vault, es el vault por defecto. Si no, antepón
   `vault="<nombre-del-vault>"` como **primer** parámetro.
3. **Sintaxis:** `param=valor` (comilla si hay espacios); flags sin valor; `total` para contar.

## Estructura (recordatorio)
`Notes/` (plano: tus tipos de "evento") · `Entities/` (plano: tus tipos de "sustantivo") ·
`Bases/*.base` (la capa de consulta, **el clasificador** — no carpetas) · `Admin/` (constitución +
`Templates/` + `Log/`). Raíz limpia.

## Rituales del vault con la CLI

### Registrar en el Log del día
El log es `Admin/Log/log-AAAA-MM-DD.md` — **una nota por día**, memoria de cambios, con
`## HH:MM — Título` y **orden cronológico inverso** (lo nuevo ARRIBA, debajo del `# H1`).
```bash
obsidian read file="Admin/Log/log-2026-07-16.md"        # leer para insertar arriba
# (el orden inverso se edita a mano: la entrada nueva va justo bajo el H1)
```

### Triar el inbox
```bash
obsidian search query="…" path="Inbox"          # crudas por procesar (Bases/Inbox.base = cola)
obsidian read file="<cruda>"                    # o una skill de extracción para triar barato
```
Luego procesa cada cruda con tu propia skill de clasificación → pasa a `Notes/`; retira la cruda.

### Conectar y auditar el grafo (nunca una nota aislada)
```bash
obsidian backlinks file="Nombre Apellido Apellido"      # quién ya apunta aquí
obsidian links file="2026-01-15-clasificacion-municipio-a1b2c3"   # salientes
obsidian orphans                                        # fichas sin enlaces ENTRANTES
obsidian unresolved verbose                             # [[enlaces]] a fichas inexistentes (¿crearlas?)
```

### Crear desde plantilla (nunca frontmatter a mano)
```bash
obsidian templates                                                  # plantillas de Admin/Templates/
obsidian create path="Entities/Nombre Apellido.md" template="person" open
```
Elige la plantilla según el `type` de tu esquema. El portero valida el resultado.

### Tableros y verificación
```bash
obsidian base:query path="Bases/Entidades.base"    # tus entidades (ver skill obsidian-bases)
obsidian base:query path="Bases/Notas.base"        # tus eventos
obsidian properties active                          # frontmatter de la nota activa
```

## Reglas de oro
- **Muestra el plan antes de mover/borrar en lote** y **pregunta antes de borrar** (`delete` → papelera;
  evita `permanent`).
- **Registra todo en el Log** y deja la **raíz limpia**.
- Para *sintaxis* de contenido usa las skills hermanas del plugin original: `obsidian-markdown`
  (wikilinks/callouts/frontmatter), `obsidian-bases` (`.base`), `json-canvas` (`.canvas`).

## Desarrollo de plugins/temas
Ciclo `plugin:reload` → `dev:errors` → `dev:screenshot`/`dev:dom` → `dev:console`; `eval code="…"` para
inspeccionar la app viva.
