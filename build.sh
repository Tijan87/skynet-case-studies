#!/usr/bin/env bash
# Rebuild the three pages from src/ into the repo root. Then: git add -A && git commit -m "..." && git push
set -euo pipefail
cd "$(dirname "$0")"
python3 src/build_site.py --out .
