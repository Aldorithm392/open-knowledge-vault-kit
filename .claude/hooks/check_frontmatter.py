#!/usr/bin/env python3
"""Hook PreToolUse (Edit|Write) — feedback INMEDIATO al escribir una nota/ficha.

Valida el contenido que un Write/Edit *va a* escribir en Vault-NotasRojas/Notes/
o /Entities/ contra el contrato (Admin/esquema.yaml). Si introduce un valor
FUERA DE ENUM, un `type` inválido o un formato roto, bloquea la escritura
(exit 2) con el motivo, para no tener que esperar al gate Stop del final.

Diseño (importa):
  - Solo bloquea violaciones de VALOR (enum/type/formato): son inequívocas e
    independientes del orden de edición. NO bloquea integridad referencial ni
    entities=unión (un [[link]] puede apuntar a una ficha que se creará en el
    siguiente paso) — eso lo cierra el gate Stop sobre el estado final.
  - Fail-open: ante cualquier duda/anomalía sale 0 (no atrapa la edición). El
    backstop real es el hook Stop (gate_vault.sh), que sí es fail-closed.
  - Las ediciones vía Bash (heredoc/scripts) NO disparan PreToolUse; por eso el
    gate Stop es imprescindible.
"""
import json
import sys
from pathlib import Path

# categorías de error dependientes del orden de edición -> NO bloquean aquí
ORDEN_DEPENDIENTE = (
    "integridad referencial",   # [[X]] sin ficha: puede ser estado intermedio
    "unión de actors_*",         # entities vs actors_*: se completan por pasos
    "obligatorio",               # campo requerido aún sin escribir (construcción)
    "ausentes (schema",          # actors_* faltantes (nota por migrar)
)


def _salir_ok():
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        _salir_ok()

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    fp = ti.get("file_path", "")
    if tool not in ("Write", "Edit") or not fp:
        _salir_ok()

    root = Path(__file__).resolve().parents[2]
    vault = root / "Vault-NotasRojas"
    if not vault.exists():
        _salir_ok()

    ruta = Path(fp)
    if not ruta.is_absolute():
        ruta = (Path(data.get("cwd", root)) / ruta).resolve()

    # ¿es un archivo de datos del vault?
    try:
        partes = ruta.relative_to(vault).parts
    except ValueError:
        _salir_ok()
    if ruta.suffix != ".md" or not partes or partes[0] not in ("Notes", "Entities"):
        _salir_ok()
    es_nota = partes[0] == "Notes"

    # el contenido que QUEDARÍA tras la operación
    if tool == "Write":
        contenido = ti.get("content")
    else:  # Edit: reconstruye aplicando el reemplazo sobre el archivo actual
        if not ruta.exists():
            _salir_ok()
        actual = ruta.read_text(encoding="utf-8")
        old, new = ti.get("old_string", ""), ti.get("new_string", "")
        if not old or old not in actual:
            _salir_ok()  # no podemos reconstruir con certeza -> lo cubre el Stop
        contenido = actual.replace(old, new) if ti.get("replace_all") \
            else actual.replace(old, new, 1)
    if not contenido:
        _salir_ok()

    sys.path.insert(0, str(root))
    try:
        from obsidiana import vault as vlt
        errores, _ = vlt.validar_texto(contenido, es_nota, vault,
                                       nombre="/".join(partes))
    except Exception:
        _salir_ok()  # fail-open: un fallo del hook no debe bloquear la edición

    bloqueantes = [e for e in errores
                   if not any(x in e for x in ORDEN_DEPENDIENTE)]
    if not bloqueantes:
        _salir_ok()

    print("⛔ Esta nota introduce valores fuera del contrato (Admin/esquema.yaml):",
          file=sys.stderr)
    for e in bloqueantes:
        print(f"  · {e}", file=sys.stderr)
    print("\nUsa un valor del enum permitido; no inventes para que quepa. Si el "
          "valor es necesario, propón el cambio de contrato y espera OK.",
          file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
