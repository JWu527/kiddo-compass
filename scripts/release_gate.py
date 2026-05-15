#!/usr/bin/env python3
"""Run the full public-beta release gate as one hard-fail command."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.release_guardrails import build_package_file_list, load_manifest


DEFAULT_REPORT = Path("dist/regression-p0.json")
DEFAULT_BUNDLE = Path("audit-bundle/kiddo-compass-audit-bundle.zip")
STALE_RELEASE_ARTIFACT_PATTERNS = (
    "dist/*.zip",
    "dist/regression-*.json",
    "dist/beta-kpi.json",
    "dist/quality-dashboard.html",
    "dist/weekly-quality-report.md",
)


class GateFailure(RuntimeError):
    """Raised when a public-beta release gate step fails."""


@dataclass(frozen=True)
class GateStep:
    name: str
    command: tuple[str, ...] = ()
    action: str | None = None
    covers: tuple[str, ...] = ()
    hard_fail: bool = True


def _script(path: str) -> str:
    return f"scripts/{path}"


def _resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def _relative_or_absolute(root: Path, path: Path) -> str:
    if path.is_absolute():
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return str(path)
    return path.as_posix()


def _regression_command(
    *,
    report: Path,
    runner: str,
    timeout: int,
    openclaw_model: str | None,
    openclaw_profile: str | None,
    openclaw_agent: str,
    openclaw_session_prefix: str | None,
) -> tuple[str, ...]:
    command: list[str] = [
        sys.executable,
        _script("run_regression.py"),
        "--priority",
        "P0",
        "--report",
        report.as_posix(),
        "--runner",
        runner,
        "--timeout",
        str(timeout),
    ]
    if openclaw_model:
        command.extend(["--openclaw-model", openclaw_model])
    if openclaw_profile:
        command.extend(["--openclaw-profile", openclaw_profile])
    if runner == "openclaw-agent":
        command.extend(["--openclaw-agent", openclaw_agent])
        if openclaw_session_prefix:
            command.extend(["--openclaw-session-prefix", openclaw_session_prefix])
    return tuple(command)


def build_gate_plan(
    root: Path,
    *,
    report: Path = DEFAULT_REPORT,
    bundle: Path = DEFAULT_BUNDLE,
    regression_runner: str = "hermes",
    regression_timeout: int = 120,
    openclaw_model: str | None = None,
    openclaw_profile: str | None = None,
    openclaw_agent: str = "main",
    openclaw_session_prefix: str | None = "public-beta",
) -> list[GateStep]:
    report_arg = Path(_relative_or_absolute(root, _resolve(root, report)))
    bundle_arg = Path(_relative_or_absolute(root, _resolve(root, bundle)))
    return [
        GateStep(
            "clear previous candidate artifacts",
            action="clear_artifacts",
            covers=("stale regression report prevention", "stale public-beta candidate prevention"),
        ),
        GateStep(
            "clean stale release artifacts",
            action="clear_stale_release_artifacts",
            covers=("stale local release package prevention", "stale regression report prevention"),
        ),
        GateStep(
            "unit tests",
            command=(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"),
            covers=("unit tests",),
        ),
        GateStep(
            "release guardrails check",
            command=(sys.executable, _script("release_guardrails.py"), "check"),
            covers=(
                "SKILL.md runtime reference lint",
                "live state leak check",
                "release whitelist static check",
                "privacy static scan",
            ),
        ),
        GateStep(
            "beta KPI gate",
            command=(sys.executable, _script("beta_kpi_gate.py")),
            covers=("public beta metric gate", "planned artifact gate"),
        ),
        GateStep(
            "source freshness",
            command=(sys.executable, _script("source_freshness.py")),
            covers=("source_id traceability", "next_review_at freshness", "official source registry"),
        ),
        GateStep(
            "run P0 regression",
            command=_regression_command(
                report=report_arg,
                runner=regression_runner,
                timeout=regression_timeout,
                openclaw_model=openclaw_model,
                openclaw_profile=openclaw_profile,
                openclaw_agent=openclaw_agent,
                openclaw_session_prefix=openclaw_session_prefix,
            ),
            covers=("regression P0 must run",),
        ),
        GateStep(
            "require regression report",
            action="require_regression_report",
            covers=("missing regression report check",),
        ),
        GateStep(
            "semantic score",
            command=(sys.executable, _script("semantic_score.py"), "--report", report_arg.as_posix()),
            covers=("semantic body rescan", "stale regression report check"),
        ),
        GateStep(
            "build audit bundle",
            command=(sys.executable, _script("build_audit_bundle.py"), "--output", bundle_arg.as_posix()),
            covers=("audit bundle build", "release_guardrails inspect during build"),
        ),
        GateStep(
            "inspect audit bundle",
            command=(sys.executable, _script("release_guardrails.py"), "inspect", bundle_arg.as_posix()),
            covers=("release_guardrails inspect", "archive privacy scan"),
        ),
        GateStep(
            "audit bundle allowlist",
            action="check_audit_bundle_allowlist",
            covers=("audit bundle content whitelist check",),
        ),
        GateStep(
            "no stale dist zips",
            action="assert_no_stale_dist_zips",
            covers=("stale local release package prevention",),
        ),
    ]


def clear_previous_artifacts(*, report: Path, bundle: Path) -> None:
    for path in [report, bundle]:
        if path.exists():
            path.unlink()


def clear_stale_release_artifacts(root: Path) -> list[Path]:
    removed: list[Path] = []
    for pattern in STALE_RELEASE_ARTIFACT_PATTERNS:
        for path in sorted(root.glob(pattern)):
            if path.is_file():
                path.unlink()
                removed.append(path)
    return removed


def assert_no_stale_dist_zips(root: Path) -> None:
    stale = sorted(path for path in (root / "dist").glob("*.zip") if path.is_file())
    if stale:
        listed = ", ".join(path.relative_to(root).as_posix() for path in stale)
        raise GateFailure(f"stale dist zip remains after release gate: {listed}")


def require_regression_report(report: Path) -> None:
    if not report.exists():
        raise GateFailure(
            f"missing regression report: {report}. "
            "P0 regression must produce this file before semantic_score runs."
        )
    if report.stat().st_size == 0:
        raise GateFailure(f"empty regression report: {report}")


def _archive_entries(bundle: Path) -> set[str]:
    if not zipfile.is_zipfile(bundle):
        raise GateFailure(f"audit bundle is not a zip archive: {bundle}")
    with zipfile.ZipFile(bundle) as archive:
        return {
            member.filename.removeprefix("kiddo-compass/")
            for member in archive.infolist()
            if not member.is_dir()
        }


def check_audit_bundle_allowlist(root: Path, bundle: Path) -> None:
    if not bundle.exists():
        raise GateFailure(f"missing audit bundle: {bundle}")
    manifest = load_manifest(root / "skill-package-manifest.txt")
    expected = set(build_package_file_list(root, manifest))
    actual = _archive_entries(bundle)
    extra = sorted(actual - expected)
    missing = sorted(expected - actual)
    if extra or missing:
        details: list[str] = []
        if extra:
            details.append(f"not in whitelist: {extra}")
        if missing:
            details.append(f"missing from bundle: {missing}")
        raise GateFailure("audit bundle allowlist mismatch: " + "; ".join(details))


def _run_command(step: GateStep, *, root: Path) -> None:
    if not step.command:
        raise GateFailure(f"{step.name}: missing command")
    print(f"\n==> {step.name}", flush=True)
    print(" ".join(step.command), flush=True)
    result = subprocess.run(step.command, cwd=root)
    if result.returncode != 0:
        raise GateFailure(f"{step.name} failed with exit code {result.returncode}")


def run_gate(
    root: Path,
    *,
    report: Path = DEFAULT_REPORT,
    bundle: Path = DEFAULT_BUNDLE,
    regression_runner: str = "hermes",
    regression_timeout: int = 120,
    openclaw_model: str | None = None,
    openclaw_profile: str | None = None,
    openclaw_agent: str = "main",
    openclaw_session_prefix: str | None = "public-beta",
) -> None:
    root = root.resolve()
    report_path = _resolve(root, report)
    bundle_path = _resolve(root, bundle)
    plan = build_gate_plan(
        root,
        report=report,
        bundle=bundle,
        regression_runner=regression_runner,
        regression_timeout=regression_timeout,
        openclaw_model=openclaw_model,
        openclaw_profile=openclaw_profile,
        openclaw_agent=openclaw_agent,
        openclaw_session_prefix=openclaw_session_prefix,
    )

    for step in plan:
        try:
            if step.action == "clear_artifacts":
                print(f"\n==> {step.name}", flush=True)
                clear_previous_artifacts(report=report_path, bundle=bundle_path)
            elif step.action == "clear_stale_release_artifacts":
                print(f"\n==> {step.name}", flush=True)
                removed = clear_stale_release_artifacts(root)
                if removed:
                    print(
                        "removed: "
                        + ", ".join(path.relative_to(root).as_posix() for path in removed),
                        flush=True,
                    )
            elif step.action == "require_regression_report":
                print(f"\n==> {step.name}", flush=True)
                require_regression_report(report_path)
            elif step.action == "check_audit_bundle_allowlist":
                print(f"\n==> {step.name}", flush=True)
                check_audit_bundle_allowlist(root, bundle_path)
            elif step.action == "assert_no_stale_dist_zips":
                print(f"\n==> {step.name}", flush=True)
                assert_no_stale_dist_zips(root)
            else:
                _run_command(step, root=root)
        except GateFailure:
            raise
        except (OSError, subprocess.SubprocessError, ValueError, zipfile.BadZipFile, shutil.Error) as exc:
            raise GateFailure(f"{step.name} failed: {exc}") from exc

    print("\npublic-beta release gate passed")
    print(f"public-beta candidate: {bundle_path}")
    print(f"P0 regression report: {report_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--regression-runner", choices=["hermes", "openclaw", "openclaw-agent"], default="hermes")
    parser.add_argument("--regression-timeout", type=int, default=120)
    parser.add_argument("--openclaw-model")
    parser.add_argument("--openclaw-profile")
    parser.add_argument("--openclaw-agent", default="main")
    parser.add_argument("--openclaw-session-prefix", default="public-beta")
    parser.add_argument("--print-plan", action="store_true")
    parser.add_argument("--clean-release-artifacts", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if args.clean_release_artifacts:
        removed = clear_stale_release_artifacts(root)
        for path in removed:
            print(f"removed {path.relative_to(root).as_posix()}")
        print(f"clean release artifacts complete: {len(removed)} removed")
        return 0

    if args.print_plan:
        for step in build_gate_plan(
            root,
            report=args.report,
            bundle=args.bundle,
            regression_runner=args.regression_runner,
            regression_timeout=args.regression_timeout,
            openclaw_model=args.openclaw_model,
            openclaw_profile=args.openclaw_profile,
            openclaw_agent=args.openclaw_agent,
            openclaw_session_prefix=args.openclaw_session_prefix,
        ):
            print(f"{step.name}: {' '.join(step.command) if step.command else step.action}")
        return 0

    try:
        run_gate(
            root,
            report=args.report,
            bundle=args.bundle,
            regression_runner=args.regression_runner,
            regression_timeout=args.regression_timeout,
            openclaw_model=args.openclaw_model,
            openclaw_profile=args.openclaw_profile,
            openclaw_agent=args.openclaw_agent,
            openclaw_session_prefix=args.openclaw_session_prefix,
        )
    except GateFailure as exc:
        print(f"\npublic-beta release gate failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
