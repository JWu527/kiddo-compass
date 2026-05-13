#!/usr/bin/env python3
"""Generate a static quality dashboard from beta gate and regression JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def _rows(mapping: dict[str, Any]) -> str:
    return "\n".join(
        f"<tr><th>{html.escape(str(key))}</th><td>{html.escape(str(value))}</td></tr>"
        for key, value in sorted(mapping.items())
    )


def build_dashboard(metrics: dict[str, Any], regression: dict[str, Any], output: Path) -> None:
    metric_values = metrics.get("metrics", metrics)
    failures = metrics.get("failures", [])
    regression_rows = []
    for result in regression.get("results", []):
        status = "pass" if not result.get("failures") else "fail"
        failure_text = "; ".join(result.get("failures", []))
        regression_rows.append(
            "<tr>"
            f"<td>{html.escape(str(result.get('id', 'unknown')))}</td>"
            f"<td>{status}</td>"
            f"<td>{html.escape(failure_text)}</td>"
            "</tr>"
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Kiddo Compass Quality Dashboard</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 32px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    .fail {{ color: #9b1c1c; font-weight: 600; }}
  </style>
</head>
<body>
  <h1>Kiddo Compass Quality Dashboard</h1>
  <h2>Beta Metrics</h2>
  <table>{_rows(metric_values)}</table>
  <h2>Gate Failures</h2>
  <p>{html.escape(', '.join(failures) if failures else 'none')}</p>
  <h2>Regression Results</h2>
  <table>
    <tr><th>Case</th><th>Status</th><th>Failures</th></tr>
    {''.join(regression_rows)}
  </table>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=Path("dist/beta-kpi.json"))
    parser.add_argument("--regression", type=Path, default=Path("dist/regression-p0.json"))
    parser.add_argument("--output", type=Path, default=Path("dist/quality-dashboard.html"))
    args = parser.parse_args(argv)
    build_dashboard(load_json(args.metrics), load_json(args.regression), args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
