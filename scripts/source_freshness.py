#!/usr/bin/env python3
"""Check source freshness and regional safety-resource hygiene."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
TRACEABLE_EVIDENCE_LEVELS = {"official-consensus", "needs-evaluation"}
SOURCE_ID_SPLIT_RE = re.compile(r"\s*(?:;|,|<br\s*/?>)\s*", re.IGNORECASE)


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _too_old(value: str, today: date, max_age_days: int) -> bool:
    return (today - _parse_date(value)).days > max_age_days


def _normalize_header(value: str) -> str:
    return value.strip().strip("`").lower().replace(" ", "_").replace("/", "_")


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_evidence_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            if headers and line:
                break
            continue
        cells = _split_markdown_row(line)
        normalized = [_normalize_header(cell) for cell in cells]
        if normalized and normalized[0] == "topic":
            headers = normalized
            continue
        if not headers or all(set(cell) <= {"-"} for cell in cells):
            continue
        if len(cells) != len(headers):
            rows.append({"topic": cells[0] if cells else "<unknown>", "_parse_error": line})
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def _source_ids(value: str) -> list[str]:
    return [item.strip("` ").removeprefix("registry:") for item in SOURCE_ID_SPLIT_RE.split(value) if item.strip()]


def _has_todo(value: str) -> bool:
    return bool(re.search(r"\bTODO\b", value, re.IGNORECASE))


def _load_registry(path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    failures: list[str] = []
    if not path.exists():
        return {}, [f"missing source registry: {path}"]
    data = json.loads(path.read_text(encoding="utf-8"))
    registry: dict[str, dict[str, str]] = {}
    for index, source in enumerate(data.get("sources", []), start=1):
        source_id = str(source.get("source_id", "")).strip()
        label = source_id or f"source #{index}"
        if not source_id:
            failures.append(f"source registry {label}: missing source_id")
            continue
        if source_id in registry:
            failures.append(f"source registry {label}: duplicate source_id")
        registry[source_id] = {key: str(value) for key, value in source.items()}
        for field in ["source_title", "issuer", "reviewed_at", "next_review_at", "evidence_level"]:
            if not str(source.get(field, "")).strip():
                failures.append(f"source registry {label}: missing {field}")
        if not str(source.get("source_url", "") or source.get("source_ref", "")).strip():
            failures.append(f"source registry {label}: missing source_url or source_ref")
        for field in ["source_url", "source_ref"]:
            value = str(source.get(field, "")).strip()
            if value and _has_todo(value):
                failures.append(f"source registry {label}: TODO source reference")
    return registry, failures


def _check_date_field(
    failures: list[str],
    *,
    label: str,
    field: str,
    value: str,
    today: date,
    max_age_days: int,
) -> None:
    if not value:
        failures.append(f"{label}: missing {field}")
        return
    try:
        parsed = _parse_date(value)
    except ValueError:
        failures.append(f"{label}: invalid {field}: {value}")
        return
    if field == "reviewed_at" and (today - parsed).days > max_age_days:
        failures.append(f"stale evidence review date: {value}")
    if field == "next_review_at" and parsed < today:
        failures.append(f"{label}: next_review_at due: {value}")


def validate_evidence_matrix(
    root: Path,
    *,
    today: date,
    max_age_days: int,
) -> list[str]:
    failures: list[str] = []
    matrix_path = root / "references" / "evidence-matrix.md"
    registry, registry_failures = _load_registry(root / "references" / "source-registry.json")
    failures.extend(registry_failures)

    for source_id, source in registry.items():
        label = f"source registry {source_id}"
        _check_date_field(
            failures,
            label=label,
            field="reviewed_at",
            value=source.get("reviewed_at", ""),
            today=today,
            max_age_days=max_age_days,
        )
        _check_date_field(
            failures,
            label=label,
            field="next_review_at",
            value=source.get("next_review_at", ""),
            today=today,
            max_age_days=max_age_days,
        )

    for row in parse_evidence_rows(matrix_path):
        topic = row.get("topic", "<unknown>")
        label = f"evidence matrix {topic}"
        if "_parse_error" in row:
            failures.append(f"{label}: could not parse row")
            continue

        evidence_level = row.get("evidence_level", "")
        required_trace = any(level in evidence_level for level in TRACEABLE_EVIDENCE_LEVELS)

        for field in ["source_id", "source_title", "issuer"]:
            if not row.get(field, "").strip():
                failures.append(f"{label}: missing {field}")
        source_ref = row.get("source_ref", "") or row.get("source_url", "") or row.get("source_url_or_ref", "")
        if not source_ref.strip():
            failures.append(f"{label}: missing source_url or source_ref")
        if _has_todo(source_ref):
            failures.append(f"{label}: TODO source reference")

        _check_date_field(
            failures,
            label=label,
            field="reviewed_at",
            value=row.get("reviewed_at", ""),
            today=today,
            max_age_days=max_age_days,
        )
        _check_date_field(
            failures,
            label=label,
            field="next_review_at",
            value=row.get("next_review_at", ""),
            today=today,
            max_age_days=max_age_days,
        )

        ids = _source_ids(row.get("source_id", ""))
        if required_trace and not ids:
            failures.append(f"{label}: missing source_id")
        for source_id in ids:
            if source_id not in registry:
                failures.append(f"{label}: source_id not found in registry: {source_id}")
    return failures


def check_freshness(root: Path, *, today: str, max_age_days: int = 120) -> list[str]:
    current = _parse_date(today)
    failures: list[str] = []

    failures.extend(validate_evidence_matrix(root, today=current, max_age_days=max_age_days))

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
