#!/usr/bin/env bash
# First run creates a virtual environment and installs dependencies.
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  PY=""
  for c in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
  done
  [ -z "$PY" ] && { echo "Python 3 is not installed."; exit 1; }
  echo "Setting up Retypee with $($PY --version)..."
  "$PY" -m venv .venv
  ./.venv/bin/pip install -q --upgrade pip
  ./.venv/bin/pip install -q -r requirements.txt
fi
(sleep 2 && (open http://127.0.0.1:8765 2>/dev/null || xdg-open http://127.0.0.1:8765 2>/dev/null || true)) &
exec ./.venv/bin/python app.py
