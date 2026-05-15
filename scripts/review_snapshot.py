#!/usr/bin/env python3
"""Build the only shareable reviewer snapshot through the audit bundle path."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_audit_bundle import DEFAULT_OUTPUT
from scripts.release_guardrails import build_audit_bundle, inspect_package_archive


PRIVATE_STATE_DIR = ".kiddo-compass-state"


class ReviewSnapshotError(RuntimeError):
    """Raised when the workspace is unsafe for an external review snapshot."""


def private_state_has_content(root: Path) -> bool:
    state_dir = root / PRIVATE_STATE_DIR
    if not state_dir.exists():
        return False
    if not state_dir.is_dir():
        return True
    return any(state_dir.iterdir())


def ensure_share_safe_root(root: Path, *, bundle_only: bool) -> None:
    if bundle_only:
        return
    if private_state_has_content(root):
        raise ReviewSnapshotError(
            f"{PRIVATE_STATE_DIR}/ exists and is non-empty. "
            "Do not create or share a workspace snapshot while private live state is present. "
            "Use make review-snapshot BUNDLE_ONLY=1 only when you want the whitelist audit bundle."
        )


def display_path(path: Path, *, root: Path | None = None) -> str:
    if root is not None:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def print_share_instructions(bundle: Path, *, root: Path | None = None) -> None:
    shown = display_path(bundle, root=root)
    print(f"Share only {shown}")
    print("Do not zip or publish the workspace directory.")


def build_review_snapshot(root: Path, output: Path, *, bundle_only: bool) -> list[str]:
    root = root.resolve()
    output = output if output.is_absolute() else root / output
    ensure_share_safe_root(root, bundle_only=bundle_only)
    package_files = build_audit_bundle(root, output)
    errors = inspect_package_archive(output)
    if errors:
        raise ReviewSnapshotError("review snapshot inspect failed:\n- " + "\n- ".join(errors))
    return package_files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--bundle-only",
        action="store_true",
        help="Build only the whitelist audit bundle even when private local state exists.",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        package_files = build_review_snapshot(root, output, bundle_only=args.bundle_only)
    except ReviewSnapshotError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print_share_instructions(output, root=root)
    print(f"bundle file count: {len(package_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
