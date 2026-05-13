#!/usr/bin/env python3
"""Score Kiddo Compass regression reports without requiring a model grader."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def score_results(report: dict[str, Any]) -> dict[str, Any]:
    results = report.get("results", [])
    failed_items = [item for item in results if item.get("failures")]
    passed = len(results) - len(failed_items)
    return {
        "ok": not failed_items,
        "passed": passed,
        "failed": len(failed_items),
        "failed_ids": [str(item.get("id", "unknown")) for item in failed_items],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = json.loads(args.report.read_text(encoding="utf-8"))
    scored = score_results(report)
    text = json.dumps(scored, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0 if scored["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
