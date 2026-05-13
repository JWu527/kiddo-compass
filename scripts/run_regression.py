#!/usr/bin/env python3
"""Run Kiddo Compass JSONL regression prompts through Hermes."""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
from pathlib import Path


DEFAULT_SUFFIX = "只输出给家长看的正文，不要 Status/Target/Metrics/标题，请简短回答。"


def load_cases(path: Path, priority: str | None = None) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        case = json.loads(line)
        case["_line"] = lineno
        if priority and case.get("priority") != priority:
            continue
        cases.append(case)
    return cases


def check_output(case: dict[str, object], output: str) -> list[str]:
    failures: list[str] = []
    for pattern in case.get("forbidden_regex", []):
        if re.search(str(pattern), output, flags=re.IGNORECASE | re.MULTILINE):
            failures.append(f"forbidden_regex matched {pattern!r}")
    return failures


def run_case(case: dict[str, object], hermes_cmd: list[str], timeout: int) -> dict[str, object]:
    prompt = str(case["prompt"])
    if case.get("language") == "zh" and DEFAULT_SUFFIX not in prompt:
        prompt = f"{prompt}\n\n{DEFAULT_SUFFIX}"
    process = subprocess.Popen(
        [*hermes_cmd, prompt],
        text=True,
        capture_output=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
    output = (stdout or "") + (stderr or "")
    failures = check_output(case, output)
    if timed_out:
        failures.append(f"hermes timed out after {timeout}s")
    if process.returncode != 0:
        failures.append(f"hermes exited {process.returncode}")
    return {
        "id": case["id"],
        "priority": case["priority"],
        "returncode": process.returncode,
        "failures": failures,
        "output": output.strip(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("references/evaluation-set.jsonl"))
    parser.add_argument("--priority", choices=["P0", "P1"])
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--hermes-cmd",
        nargs="+",
        default=["hermes", "--ignore-user-config", "--ignore-rules", "--skills", "kiddo-compass", "-z"],
    )
    args = parser.parse_args(argv)

    cases = load_cases(args.cases, priority=args.priority)
    if args.dry_run:
        for case in cases:
            print(json.dumps({"id": case["id"], "prompt": case["prompt"]}, ensure_ascii=False))
        return 0

    all_ok = True
    for case in cases:
        result = run_case(case, args.hermes_cmd, args.timeout)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        if result["failures"]:
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
