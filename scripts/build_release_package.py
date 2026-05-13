#!/usr/bin/env python3
"""Build the Kiddo Compass release zip through the guarded whitelist path."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.release_guardrails import write_package


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("dist/kiddo-compass.zip"))
    args = parser.parse_args(argv)
    return write_package(args.root.resolve(), args.output)


if __name__ == "__main__":
    raise SystemExit(main())
