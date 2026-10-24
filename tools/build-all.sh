#!/usr/bin/env bash
# Baut jedes Spiel aus src/<Spiel>/ nach build/<Spiel>/ (HTML plus Bilder).
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly root_dir
readonly src_dir="${root_dir}/src"
readonly build_dir="${root_dir}/build"

quiet=0
verbose=0

usage() {
    echo "Usage: $(basename "$0") [-c] [-q] [-v] [-h]"
    echo "  -c  build/ vorher leeren"
    echo "  -q  keine Ausgabe ausser Fehlern"
    echo "  -v  ausfuehrliche Ausgabe"
    echo "  -h  diese Hilfe"
}

log() {
    if [[ ${quiet} -eq 0 ]]; then echo "$@"; fi
}

clean=0
while getopts "cqvh" opt; do
    case "${opt}" in
        c) clean=1 ;;
        q) quiet=1 ;;
        v) verbose=1 ;;
        h) usage; exit 0 ;;
        *) usage >&2; exit 1 ;;
    esac
done

if ! command -v tweego >/dev/null; then
    echo "tweego nicht gefunden (erwartet in ~/go/bin)" >&2
    exit 1
fi

if [[ ${clean} -eq 1 ]]; then
    rm -rf "${build_dir:?}"/*
fi

# Aus dem Projektordner starten, damit tweego auch storyformats/ hier findet.
cd "${root_dir}"

for game_dir in "${src_dir}"/*/; do
    game="$(basename "${game_dir}")"
    out_dir="${build_dir}/${game}"
    mkdir -p "${out_dir}"

    # Nur die .twee-Dateien uebergeben: bei einem ganzen Ordner wuerde tweego
    # Bilder als Base64-Medienpassagen einbetten und das HTML stark aufblaehen.
    twee_files=("${game_dir}"*.twee)
    tweego -o "${out_dir}/${game}.html" "${twee_files[@]}"

    find "${game_dir}" -maxdepth 1 -type f ! -name '*.twee' -exec cp {} "${out_dir}/" \;

    log "OK ${game}"
    if [[ ${verbose} -eq 1 ]]; then ls -1 "${out_dir}"; fi
done
