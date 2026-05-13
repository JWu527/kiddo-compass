#!/usr/bin/env python3
"""Check source freshness and regional safety-resource hygiene."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _too_old(value: str, today: date, max_age_days: int) -> bool:
    return (today - _parse_date(value)).days > max_age_days


def evidence_review_dates(path: Path) -> list[str]:
    dates: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and "2026-" in line:
            match = DATE_RE.search(line)
            if match:
                dates.append(match.group(0))
    return dates


def check_freshness(root: Path, *, today: str, max_age_days: int = 120) -> list[str]:
    current = _parse_date(today)
    failures: list[str] = []

    for reviewed_at in evidence_review_dates(root / "references" / "evidence-matrix.md"):
        if _too_old(reviewed_at, current, max_age_days):
            failures.append(f"stale evidence review date: {reviewed_at}")

    resources_path = root / "references" / "regional-resources.json"
    resources = json.loads(resources_path.read_text(encoding="utf-8"))
    if _too_old(resources["reviewed_at"], current, max_age_days):
        failures.append(f"stale regional resources review date: {resources['reviewed_at']}")

    for item in resources.get("regions", []):
        if _too_old(item["reviewed_at"], current, max_age_days):
            failures.append(f"stale regional resource {item['region']}: {item['reviewed_at']}")
        numbers = item.get("publishable_phone_numbers", [])
        if numbers and not item.get("verified"):
            failures.append(f"unverified numbers configured for {item['region']}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--max-age-days", type=int, default=120)
    args = parser.parse_args(argv)
    failures = check_freshness(args.root.resolve(), today=args.today, max_age_days=args.max_age_days)
    if failures:
        print("source freshness failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("source freshness ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
