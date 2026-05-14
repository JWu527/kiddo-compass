#!/usr/bin/env python3
"""Generate a Markdown weekly quality report from gate and regression JSON."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

if __package__ is None or __package__ == "":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.run_regression import load_cases


def _pass_fail_by_field(
    results: list[dict[str, Any]],
    cases_by_id: dict[str, dict[str, Any]],
    field: str,
) -> list[str]:
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for result in results:
        case = cases_by_id.get(str(result.get("id", "")), {})
        key = str(case.get(field, "unknown"))
        counts[key][1] += 1
        if not result.get("failures"):
            counts[key][0] += 1
    return [f"- {key}: {passed}/{total} passed" for key, (passed, total) in sorted(counts.items())]


def build_weekly_report(
    metrics: dict[str, Any],
    regression: dict[str, Any],
    cases: list[dict[str, Any]],
    output: Path,
) -> None:
    metric_values = metrics.get("metrics", metrics)
    gate_failures = metrics.get("failures", [])
    results = list(regression.get("results", []))
    total = int(regression.get("total", len(results)))
    failed = int(regression.get("failed", sum(1 for result in results if result.get("failures"))))
    passed = total - failed
    cases_by_id = {str(case.get("id")): case for case in cases}
    high_risk_failures = [
        result
        for result in results
        if result.get("failures") and str(result.get("id", "")).startswith("P0-")
    ]

    lines = [
        "# Kiddo Compass Weekly Quality Report",
        "",
        f"- Regression: {passed}/{total} passed",
        f"- Gate failures: {len(gate_failures)}",
        f"- P0 cases: {metric_values.get('p0_cases', 'unknown')}",
        f"- Privacy static findings: {metric_values.get('privacy_static_findings', 'unknown')}",
        "",
        "## Language Pass Rate",
        *_pass_fail_by_field(results, cases_by_id, "language"),
        "",
        "## Mode Pass Rate",
        *_pass_fail_by_field(results, cases_by_id, "mode"),
        "",
        "## High-Risk Failures",
    ]
    if high_risk_failures:
        for result in high_risk_failures:
            lines.append(f"- {result.get('id')}: {'; '.join(result.get('failures', []))}")
    else:
        lines.append("- none")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=Path("dist/beta-kpi.json"))
    parser.add_argument("--regression", type=Path, default=Path("dist/regression-p0-openclaw.json"))
    parser.add_argument("--cases", type=Path, default=Path("references/evaluation-set.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("dist/weekly-quality-report.md"))
    args = parser.parse_args(argv)
    build_weekly_report(_load_json(args.metrics), _load_json(args.regression), load_cases(args.cases), args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
