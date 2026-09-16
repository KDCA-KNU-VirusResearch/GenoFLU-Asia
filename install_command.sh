#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
[[ -f "$PROJECT_DIR/run_genoflu.sh" ]] || { echo 'Place this installer beside run_genoflu.sh.' >&2; exit 1; }
[[ -n "${CONDA_PREFIX:-}" && -x "$CONDA_PREFIX/bin/python" ]] || { echo 'Activate the intended Conda environment first.' >&2; exit 1; }
TARGET="$CONDA_PREFIX/bin/genoflu-asia"
[[ ! -e "$TARGET" && ! -L "$TARGET" ]] || { echo "Command already exists: $TARGET" >&2; exit 1; }
(
  set -o noclobber
  {
    printf '%s\n' '#!/usr/bin/env bash' '# GenoFLU-Asia command launcher' 'set -euo pipefail'
    printf 'RUNNER=%q\n' "$PROJECT_DIR/run_genoflu.sh"
    cat <<'LAUNCHER'
COMMAND_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$COMMAND_DIR:$PATH"
exec bash "$RUNNER" "$@"
LAUNCHER
  } > "$TARGET"
)
chmod 755 "$TARGET"
printf 'Registered: %s\nTry: genoflu-asia --help\n' "$TARGET"
