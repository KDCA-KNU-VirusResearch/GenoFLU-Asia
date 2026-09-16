#!/usr/bin/env bash
set -euo pipefail

# Defaults retain the original no-argument behavior; flags override these paths.
FASTA_DIR="$HOME/genoflu_fasta"
OUTPUT_DIR="$HOME/genoflu_output"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'HELP'
GenoFLU-Asia
Usage: genoflu-asia [--input DIR] [--output DIR]
       ./run_genoflu.sh [--input DIR] [--output DIR]

  -i, --input DIR   Folder containing lowercase .fasta files
                   Default: $HOME/genoflu_fasta
  -o, --output DIR  Folder for new timestamped result workbooks
                   Default: $HOME/genoflu_output
  -h, --help        Show help without running an analysis

Nucleotide identity threshold: fixed at 97%.

Relative paths are resolved from the directory where the command is invoked.
Example: genoflu-asia --input ./input --output ./output
HELP
}
fail() { printf 'Error: %s\n' "$*" >&2; exit 2; }
while (( $# )); do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -i|--input|-o|--output)
      (( $# >= 2 )) && [[ -n "$2" && "$2" != -* ]] || fail "Missing directory after $1"
      if [[ "$1" == -i || "$1" == --input ]]; then FASTA_DIR="$2"; else OUTPUT_DIR="$2"; fi
      shift 2 ;;
    --input=*) FASTA_DIR="${1#*=}"; [[ -n "$FASTA_DIR" ]] || fail 'Empty input directory'; shift ;;
    --output=*) OUTPUT_DIR="${1#*=}"; [[ -n "$OUTPUT_DIR" ]] || fail 'Empty output directory'; shift ;;
    *) fail "Unknown argument: $1. Use --help." ;;
  esac
done
[[ -d "$FASTA_DIR" ]] || fail "Input directory does not exist: $FASTA_DIR"
# Resolve before changing directories, so ./input refers to the caller's folder.
FASTA_DIR="$(cd -- "$FASTA_DIR" && pwd)"
mkdir -p -- "$OUTPUT_DIR"
OUTPUT_DIR="$(cd -- "$OUTPUT_DIR" && pwd)"
shopt -s nullglob
FILES=("$FASTA_DIR"/*.fasta)
(( ${#FILES[@]} )) || fail "No .fasta files found in: $FASTA_DIR"
GENOFLU_SCRIPT="$SCRIPT_DIR/genoflu.py"
DEPENDENCIES_FASTAS="$SCRIPT_DIR/dependencies/asia_fastas"
GENOTYPE_KEY="$SCRIPT_DIR/dependencies/genotype_key_asia.xlsx"
[[ -f "$GENOFLU_SCRIPT" && -f "$GENOTYPE_KEY" ]] || fail 'Program or genotype key is missing'
REFS=("$DEPENDENCIES_FASTAS"/*.fasta)
(( ${#REFS[@]} )) || fail "No reference FASTA files in: $DEPENDENCIES_FASTAS"
for executable in python blastn makeblastdb; do
  command -v "$executable" >/dev/null || fail "$executable is unavailable; activate the genoflu-asia Conda environment"
done
mkdir -p -- "$OUTPUT_DIR"
cd -- "$SCRIPT_DIR"
printf 'Input: %s\nOutput: %s\n' "$FASTA_DIR" "$OUTPUT_DIR"
python "$GENOFLU_SCRIPT" -f "${FILES[@]}" -i "$DEPENDENCIES_FASTAS" -c "$GENOTYPE_KEY" --output "$OUTPUT_DIR"
printf 'All files processed.\n'
