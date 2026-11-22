#!/usr/bin/env sh
set -eu

PYTHON_BIN=$(printenv PYTHON_BIN || printf 'python3')
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3.12 is required. Set PYTHON_BIN to a Python 3.12 executable." >&2
  exit 1
fi

PY_MINOR=$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$PY_MINOR" != "3.12" ]; then
  echo "Expected Python 3.12; found $PY_MINOR." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
echo "HSMART contract-validation environment is ready. Run: python -m pytest -q"
