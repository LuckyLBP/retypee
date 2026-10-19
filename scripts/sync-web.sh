#!/usr/bin/env bash
# The browser build runs the same engine as the local app. Run this after
# changing anything in pdfedit/ so web/py/pdfedit stays identical.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p web/py/pdfedit
cp pdfedit/__init__.py pdfedit/core.py pdfedit/fonts.py web/py/pdfedit/
echo "Synced pdfedit/ -> web/py/pdfedit/"
