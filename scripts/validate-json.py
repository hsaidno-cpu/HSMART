#!/usr/bin/env python3
"""Strictly validate committed JSON files without third-party dependencies."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key!r}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-standard numeric constant is not valid JSON: {value}")


def discover_json_files(root: Path | None = None) -> list[Path]:
    """Find repository JSON files while pruning generated/vendor directories."""
    search_root = root or ROOT
    files: list[Path] = []

    for current, directories, filenames in os.walk(search_root, followlinks=False):
        current_path = Path(current)
        directories[:] = [
            name
            for name in directories
            if name not in EXCLUDED_DIRS and not (current_path / name).is_symlink()
        ]
        for filename in filenames:
            path = current_path / filename
            if filename.endswith(".json") and not path.is_symlink():
                files.append(path)

    return sorted(files)


def main() -> int:
    files = discover_json_files()
    if not files:
        print("ERROR: no JSON files found under repository root", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(
                    handle,
                    object_pairs_hook=reject_duplicate_keys,
                    parse_constant=reject_nonfinite,
                )
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            failures.append(f"{relative}: {exc}")
        else:
            print(f"valid JSON: {relative}")

    if failures:
        print(f"\n{len(failures)} invalid JSON file(s):", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"\nValidated {len(files)} JSON file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
