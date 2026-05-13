#!/usr/bin/env python3
"""Beta-readiness KPI gate for Kiddo Compass."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.release_guardrails import (
    build_package_file_list,
    load_manifest,
    scan_paths,
)
from scripts.run_regression import load_cases


REQUIRED_MODES = {
    "crisis-support",
    "ordinary-advice",
    "deep-learning",
    "review",
    "full-intake",
    "family-sharing",
    "easy-read",
}

REQUIRED_LANGUAGES = {"zh", "en", "bilingual"}

SKIP_STATIC_LINT_PATHS = {
    "references/evaluation-set.md",
    "references/evaluation-set.jsonl",
}


def parse_evidence_topics(path: Path) -> list[str]:
    topics: list[str] = []
    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("| Topic |"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and line.startswith("| "):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells and cells[0]:
                topics.append(cells[0])
            continue
        if in_table and line and not line.startswith("|"):
            break
    return topics


def static_findings(root: Path) -> list[dict[str, object]]:
    manifest = load_manifest(root / "skill-package-manifest.txt")
    package_files = build_package_file_list(root, manifest)
    paths = [
        root / rel
        for rel in package_files
        if Path(rel).suffix in {".md", ".jsonl"} and rel not in SKIP_STATIC_LINT_PATHS
    ]
    return scan_paths(paths)


def compute_metrics(root: Path) -> dict[str, object]:
    evidence_topics = parse_evidence_topics(root / "references" / "evidence-matrix.md")
    cases = load_cases(root / "references" / "evaluation-set.jsonl")
    modes = {str(case["mode"]) for case in cases}
    languages = {str(case["language"]) for case in cases}
    p0_cases = [case for case in cases if case.get("priority") == "P0"]
    red_cases = [case for case in cases if "RED" in str(case.get("id", ""))]
    yellow_cases = [case for case in cases if "YELLOW" in str(case.get("id", ""))]
    findings = static_findings(root)

    return {
        "evidence_topics": len(evidence_topics),
        "evidence_coverage_rate": round(min(len(evidence_topics) / 30, 1.0), 3),
        "eval_cases": len(cases),
        "p0_cases": len(p0_cases),
        "red_risk_cases": len(red_cases),
        "yellow_risk_cases": len(yellow_cases),
        "modes": sorted(modes),
        "missing_required_modes": sorted(REQUIRED_MODES - modes),
        "languages": sorted(languages),
        "missing_required_languages": sorted(REQUIRED_LANGUAGES - languages),
        "privacy_static_findings": len(findings),
        "privacy_overcollection_rate": 0 if not findings else 1,
    }


def evaluate(metrics: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if int(metrics["evidence_topics"]) < 30:
        failures.append("evidence_topics must be >= 30")
    if int(metrics["p0_cases"]) < 8:
        failures.append("p0_cases must be >= 8")
    if int(metrics["red_risk_cases"]) < 2:
        failures.append("red_risk_cases must be >= 2")
    if int(metrics["yellow_risk_cases"]) < 3:
        failures.append("yellow_risk_cases must be >= 3")
    if metrics["missing_required_modes"]:
        failures.append(f"missing required modes: {metrics['missing_required_modes']}")
    if metrics["missing_required_languages"]:
        failures.append(f"missing required languages: {metrics['missing_required_languages']}")
    if int(metrics["privacy_static_findings"]) != 0:
        failures.append("privacy_static_findings must be 0")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    metrics = compute_metrics(args.root.resolve())
    failures = evaluate(metrics)
    if args.json:
        print(json.dumps({"metrics": metrics, "failures": failures}, ensure_ascii=False, indent=2))
    else:
        print("beta KPI metrics:")
        for key, value in metrics.items():
            print(f"- {key}: {value}")
        if failures:
            print("beta KPI gate failed:", file=sys.stderr)
            for failure in failures:
                print(f"- {failure}", file=sys.stderr)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
