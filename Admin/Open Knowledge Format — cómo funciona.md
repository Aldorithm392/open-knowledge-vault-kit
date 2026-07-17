---
type: reference
title: "Open Knowledge Format — cómo funciona y dónde diverge este vault"
---

# Open Knowledge Format (OKF)

OKF lo publicó Google Cloud en junio de 2026. Formaliza un patrón que ya existía de facto desde
hace más de una década (Jekyll, Hugo, y todo generador de sitio estático que use frontmatter YAML
sobre markdown): el **"LLM-wiki"** — un directorio de archivos markdown con encabezado YAML,
vendor-neutral, sin proveedor de por medio, pensado para que un modelo de lenguaje lo lea sin
que nadie tenga que escribirle un parser a la medida.

## Lo que exige (spec v0.1, §9) — y es sorprendentemente poco

Solo tres reglas duras:

1. Todo `.md` no reservado tiene frontmatter YAML **parseable**.
2. Ese frontmatter tiene un campo `type` **no vacío**.
3. Los archivos reservados (`index.md`, `log.md`, si existen) siguen su estructura esperada.

Eso es todo. OKF reserva seis campos (`type · title · description · resource · tags ·
timestamp`), de los cuales **solo `type` es obligatorio**; el resto son opcionales y cualquier
productor puede agregar los campos custom que necesite.

## Por qué exige tan poco

Porque el estándar no está resolviendo "cómo modelar tu dominio" — eso es tu trabajo, con tu
propio esquema (ver `Admin/esquema.yaml` en este kit). OKF solo resuelve **cómo hacer que
cualquier consumidor (un LLM, un indexador, otro agente) sepa qué está viendo sin que tú le
expliques tu formato caso por caso.** Es un piso de interoperabilidad, no un techo de modelado.

## La plantilla genérica — el punto de partida real

En `Admin/Templates/_plantilla-okf-genérica.md` está el archivo mínimo que el estándar exige,
sin nada de este proyecto encima:

```yaml
---
type: ""
title: ""
description: ""
resource: ""
tags: []
timestamp: ""
---
```

Eso es todo lo que OKF pide. `type` es el único campo obligatorio; los otros cinco son
reservados pero opcionales. Este archivo, tal cual, ya es un bundle OKF conforme — y ya se nota
que no resuelve nada de tu dominio: no sabe qué es un `type` válido para ti, no sabe qué otros
datos necesitas capturar.

**Las cinco plantillas de `Admin/Templates/` (`event`, `context`, `investigation`,
`organization`, `person`) son el resultado de adaptar esta plantilla genérica a un dominio
concreto — nota roja mexicana.** La adaptación, paso a paso, fue:

1. **Cerrar `type`.** De "cualquier string" a un enum de cinco valores fijos. Nada nuevo entra
   sin proponerse antes (`Admin/esquema.yaml → enums.type`).
2. **Renombrar y usar `resource`.** OKF trae el campo `resource` para el identificador del
   recurso; aquí se usa el campo custom `url` en su lugar (permitido — OKF preserva lo que no
   reconoce, solo no lo interpreta especialmente). Ejemplo de una decisión que puedes tomar
   distinto en la tuya.
3. **Prohibir `tags`.** Es reservado pero opcional en OKF; aquí se decidió no usarlo nunca — la
   corroboración se resuelve por backlinks, no por etiquetas (ver "Antes, no después" en el
   README). Sigue siendo 100% conforme: un campo reservado que nunca se llena no rompe nada.
4. **Agregar los campos custom que el dominio necesita.** `state`, `municipality`,
   `classification`, `actors_victim`, `actors_alleged`… ninguno de estos existe en el estándar;
   todos están permitidos por él. Cada uno nació de una pregunta real que el vault necesitaba
   contestar (regla de gobernanza en `Admin/esquema.yaml`), no de imaginación.
5. **Definir uno de estos por cada `type` del enum.** Por eso son cinco plantillas y no una:
   cada `type` trae su propio conjunto de campos custom, aunque los seis reservados de OKF los
   compartan todos.

Para adaptar esto a tu propio dominio, no edites las cinco plantillas de este kit directamente
como punto de partida — vuelve a `_plantilla-okf-genérica.md` y repite los cinco pasos con tus
propios tipos y tus propios campos. Vas a terminar con tu propio número de plantillas, no
necesariamente cinco.

## Dónde este vault es conforme

- Cada nota tiene frontmatter YAML válido: sí, lo exige el portero.
- Cada frontmatter tiene un `type` no vacío: sí, y además más estricto que el estándar — aquí
  `type` es un **enum cerrado de cinco valores**, no cualquier texto. OKF permite cualquier
  string; nosotros no.
- `tags` está prohibido en este vault. OKF lo permite pero no lo exige — prohibirlo es
  **100% conforme** igual (un campo reservado que nunca se usa no rompe nada).

## Dónde este vault se desvía a propósito

OKF enlaza conceptos entre archivos con **links de markdown en el cuerpo del texto**
(`[texto](/ruta/al/archivo.md)`). Este vault, en cambio, pone los vínculos como **wikilinks
dentro del frontmatter** (`entities: ["[[Fulano]]", "[[Cártel X]]"]`).

La razón: los wikilinks en el frontmatter son los que Obsidian grafica. Son el corazón de la
experiencia nativa — el grafo visual, los backlinks automáticos, "buscas un nombre y ves todo lo
que aparece de él". Convertir esos enlaces a markdown-en-cuerpo para cumplir la letra del
estándar habría roto exactamente la parte que hace útil el vault en el día a día.

La consecuencia, y hay que ser honesto sobre ella: un consumidor OKF puro (algo que solo entienda
la spec al pie de la letra, sin saber nada de Obsidian) leería nuestras fichas perfectamente bien,
pero **no reconstruiría nuestras relaciones** — vería `entities: ["[[Fulano]]"]` como un campo
custom con una cadena de texto rara adentro, no como una arista de un grafo.

## La postura: nativo primero, exportable si hace falta

No convertimos el vault de trabajo a la forma OKF-pura. Los wikilinks alimentan el grafo que
usamos todos los días; degradarlos rompería la herramienta para ganar una conformidad que, hoy,
nadie más necesita consumir.

Si algún día hace falta interoperar con un consumidor OKF real (el visualizador de alguien más, un
pipeline ajeno), la respuesta no es reescribir el vault: es un **export**, una tercera proyección
de la misma verdad — igual que ya existen otras dos (el mapa público, el propio grafo). El export
convertiría cada `[[X]]` a `[X](/Entities/X.md)` en el cuerpo, sin tocar el original.

## La lección, si vas a construir el tuyo

Cumplir un estándar abierto no significa dejar que el estándar te quite la razón por la que
construiste la cosa. Cumple lo que te da portabilidad e interoperabilidad (el frontmatter
parseable, el `type` no vacío) y diverge, a propósito y documentado, donde el estándar te
costaría la característica central de tu herramienta. La conformidad es una herramienta a tu
servicio, no un dogma.
