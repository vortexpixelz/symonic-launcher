#!/usr/bin/env python3
"""Validate a structured SPLAT Report against its JSON Schema.

Run:
    uv run --with jsonschema python tools/validate_splat_report.py \
      examples/splat-report.example.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


DEFAULT_SCHEMA = Path("schemas/splat-report-0.1.schema.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Symonic SPLAT Report JSON document.")
    parser.add_argument("report", type=Path, help="Path to a SPLAT Report JSON file.")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to the Draft 2020-12 schema.")
    args = parser.parse_args()

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    report = json.loads(args.report.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(error.absolute_path))

    if not errors:
        print(f"valid: {args.report}")
        return 0

    print(f"invalid: {args.report}")
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        print(f"- {location}: {error.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
