#!/usr/bin/env python3
"""Build the only shareable Kiddo Compass audit bundle."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.release_guardrails import build_audit_bundle


DEFAULT_OUTPUT = Path("audit-bundle/kiddo-compass-audit-bundle.zip")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    output = args.output
    if not output.is_absolute():
        output = root / output

    try:
        package_files = build_audit_bundle(root, output)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    inspect_cmd = [
        sys.executable,
        str(root / "scripts" / "release_guardrails.py"),
        "inspect",
        str(output),
    ]
    inspect = subprocess.run(inspect_cmd, text=True)
    if inspect.returncode != 0:
        return inspect.returncode

    print(f"audit bundle ready: {output}")
    print(f"share only this zip; do not zip or publish the workspace directory")
    print(f"bundle file count: {len(package_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
