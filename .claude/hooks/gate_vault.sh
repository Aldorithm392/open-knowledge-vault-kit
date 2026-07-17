#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Hook Stop — GATE DETERMINISTA del vault.
#
# Corre el portero (python3 -m obsidiana validar-vault) una vez al cerrar el
# turno. Si el vault NO cumple el contrato (Admin/esquema.yaml), BLOQUEA el
# cierre (exit 2) y reemite los errores a stderr para que Claude los corrija
# antes de terminar. Automatiza la auditoría "nota por nota".
#
# Es la "garantía" del patrón guiar+garantizar+verificar: CLAUDE.md aconseja,
# el portero obliga. Ver: Vault-NotasRojas/Admin/Mejores prácticas — Claude
# sobre la base.md
#
# Robustez:
#   - No-op (exit 0) si Vault-NotasRojas/ no existe (fresh clone / CI).
#   - Solo mira ERRORES (--sin-avisos); los avisos nunca bloquean.
#   - Antibucle: da UNA pasada fuerte. Si ya venimos de un bloqueo previo
#     (stop_hook_active), libera para no atrapar la sesión; además el tope
#     integrado CLAUDE_CODE_STOP_HOOK_BLOCK_CAP (8) acota cualquier bucle.
# ---------------------------------------------------------------------------
set -uo pipefail

INPUT="$(cat 2>/dev/null || true)"
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
VAULT="$ROOT/Vault-NotasRojas"

# Sin vault local no hay dato que validar.
[ -d "$VAULT" ] || exit 0

# ¿Ya bloqueamos en esta secuencia de cierre? Entonces no insistas (antibucle).
ACTIVE="$(printf '%s' "$INPUT" | python3 -c 'import sys,json;print(1 if json.load(sys.stdin).get("stop_hook_active") else 0)' 2>/dev/null || echo 0)"

cd "$ROOT" || exit 0
SALIDA="$(python3 -m obsidiana validar-vault --sin-avisos 2>&1)"
RC=$?

# Vault en verde -> deja cerrar.
[ "$RC" -eq 0 ] && exit 0

# Ya insistimos antes en este cierre -> libera (el usuario ya vio los errores).
[ "$ACTIVE" = "1" ] && exit 0

{
  echo "⛔ El vault NO cumple el contrato (Admin/esquema.yaml). Corrige antes de cerrar:"
  echo "$SALIDA"
  echo ""
  echo "Un valor fuera del enum es un ERROR que el portero rechaza, no una sugerencia"
  echo "creativa: corrige el valor (o propón el cambio de contrato y espera OK). No"
  echo "'ajustes' el esquema para que quepa. Ver Admin/Mejores prácticas — Claude sobre la base.md"
} >&2
exit 2
