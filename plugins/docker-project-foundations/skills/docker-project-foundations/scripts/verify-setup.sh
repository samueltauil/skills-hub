#!/usr/bin/env bash
# Verify Docker project setup. Run from the project root.
# Usage: bash "<skill-dir>/scripts/verify-setup.sh" [--help]
# <skill-dir> is the directory that contains this skill's SKILL.md.
set -euo pipefail

usage() {
    echo "Usage: bash \"<skill-dir>/scripts/verify-setup.sh\" [--help]"
    echo "Run from the project root; <skill-dir> is the directory that contains this skill's SKILL.md."
    echo "Checks: .dockerignore, Dockerfile, and compose.yaml exist; compose config passes."
}

if [[ "${1:-}" == "--help" && $# == 1 ]]; then
    usage
    exit 0
fi

if (( $# != 0 )); then
    usage >&2
    exit 2
fi

status=0

echo "Checking required files..."
for file in .dockerignore Dockerfile compose.yaml; do
    if [[ -f "$file" ]]; then
        echo "OK: $file"
    else
        echo "MISSING: $file" >&2
        status=1
    fi
done

if [[ -f compose.yaml ]]; then
    echo ""
    echo "Validating compose.yaml..."
    if docker compose config --quiet; then
        echo "OK: compose config valid"
    else
        echo "FAIL: compose config invalid" >&2
        status=1
    fi
fi

exit "$status"
