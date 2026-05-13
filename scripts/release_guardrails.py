#!/usr/bin/env python3
"""Release packaging and privacy guardrails for Kiddo Compass.

The release package is built from an explicit whitelist manifest. Ignored local
runtime files may exist in a maintainer workspace, but they must never be part
of a public artifact.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RUNTIME_PRIVATE_FILES = {
    "child-profile.md",
    "practice-log.md",
    "learning-progress.md",
}

BLOCKED_PACKAGE_PATTERNS = (
    re.compile(r"(^|/)\.git(/|$)"),
    re.compile(r"(^|/)__MACOSX(/|$)"),
    re.compile(r"(^|/)__pycache__(/|$)"),
    re.compile(r"(^|/)\._[^/]+$"),
    re.compile(r"(^|/)\.env(?:\.|$)"),
    re.compile(r"\.log$"),
    re.compile(r"\.private\.md$"),
    re.compile(r"\.local\.md$"),
    re.compile(r"\.pyc$"),
)

INTERNAL_STUDY_NOTES_REQUIRING_COPYRIGHT_REVIEW = {
    "references/30-day-plan.md",
    "references/learning-map.md",
    "references/tool-cards.md",
    "references/adler-psychology.md",
    "references/core-concepts.md",
    "references/practice-diary.md",
}

SKIP_STATIC_LINT_PATHS = {
    "references/evaluation-set.md",
    "references/evaluation-set.jsonl",
}

MAX_DESCRIPTION_CHARS = 220
REQUIRED_FRONTMATTER_FIELDS = {
    "name",
    "version",
    "description",
    "metadata.openclaw.skillKey",
    "metadata.openclaw.emoji",
    "metadata.openclaw.homepage",
}


@dataclass(frozen=True)
class LintRule:
    name: str
    pattern: re.Pattern[str]
    message: str


LINT_RULES = (
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(真实姓名|精确生日|出生日期|生日|学校|地址|电话|手机号)[:：是为]\s*"
            r"(?!$|（?可选|不要|不需要|不默认|无|空|XX|xxx|\[|<|example)"
            r"[^，。；;\n]+"
        ),
        "Potentially stores or requests identifying family data.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(r"(手机号|电话|热线)[:：]?\s*\d{7,}"),
        "Potential phone number or hotline in release material.",
    ),
    LintRule(
        "near-diagnostic-language",
        re.compile(r"(这是|就是|诊断为|确诊为|属于).{0,12}(感觉统合失调|ADHD|自闭症)"),
        "Avoid diagnostic or near-diagnostic claims.",
    ),
    LintRule(
        "fixed-day-promise",
        re.compile(r"(坚持|连续|用|做).{0,8}(三天|3天|三到五天|3到5天).{0,12}(就会|明显|一定|好|停止|减少)"),
        "Avoid fixed-time outcome promises.",
    ),
    LintRule(
        "single-cause-label",
        re.compile(r"(就是|一定是|只是).{0,8}(寻求关注|争夺权力|寻求权力|权力斗争)"),
        "Avoid single-cause behavior labels.",
    ),
    LintRule(
        "unverified-hotline-number",
        re.compile(r"(热线|电话|拨打|打)[^\n\d]{0,40}\d{5,}"),
        "Do not publish unverified hotline or agency numbers.",
    ),
)

ANSWER_ONLY_RULES = (
    LintRule(
        "internal-label-leak",
        re.compile(r"(行为解码|管教前三问|三步应对法|错误目的|寻求权力|权力斗争)"),
        "Normal user-facing answers must not expose internal labels.",
    ),
)

NEGATIVE_CONTEXT_MARKERS = (
    "不说",
    "不要说",
    "不要",
    "禁止",
    "避免",
    "不得",
    "Fail if",
    "fail if",
    "Do not",
    "do not",
    "Avoid",
    "avoid",
    "forbidden",
    "Forbidden",
)


def load_manifest(path: Path) -> list[str]:
    entries: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def _is_blocked_package_path(path: str) -> bool:
    name = Path(path).name
    if name in RUNTIME_PRIVATE_FILES:
        return True
    return any(pattern.search(path) for pattern in BLOCKED_PACKAGE_PATTERNS)


def _strip_archive_root(path: str) -> str:
    parts = Path(path).parts
    if len(parts) > 1 and parts[0] == "kiddo-compass":
        return Path(*parts[1:]).as_posix()
    return path


def build_package_file_list(root: Path, manifest_entries: Iterable[str]) -> list[str]:
    package_files: list[str] = []
    for entry in manifest_entries:
        normalized = entry.strip().rstrip("/")
        if not normalized:
            continue
        if _is_blocked_package_path(normalized):
            raise ValueError(f"manifest contains blocked private path: {entry}")
        target = root / normalized
        if not target.exists():
            raise FileNotFoundError(f"manifest entry does not exist: {entry}")
        if target.is_dir():
            for child in sorted(target.rglob("*")):
                if child.is_file():
                    rel = child.relative_to(root).as_posix()
                    if not _is_blocked_package_path(rel):
                        package_files.append(rel)
        else:
            package_files.append(normalized)
    return sorted(dict.fromkeys(package_files))


def _extract_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4 :]


def _frontmatter_values(frontmatter: str) -> dict[str, str]:
    values: dict[str, str] = {}
    in_metadata = False
    in_openclaw = False
    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" "):
            in_metadata = stripped == "metadata:"
            in_openclaw = False
            if ":" in stripped:
                key, raw_value = stripped.split(":", 1)
                value = raw_value.strip().strip('"').strip("'")
                if value:
                    values[key] = value
            continue
        if in_metadata and line.startswith("  ") and not line.startswith("    "):
            in_openclaw = stripped == "openclaw:"
            continue
        if in_metadata and in_openclaw and line.startswith("    ") and ":" in stripped:
            key, raw_value = stripped.split(":", 1)
            value = raw_value.strip().strip('"').strip("'")
            values[f"metadata.openclaw.{key}"] = value
    return values


def validate_skill_frontmatter(path: Path) -> list[str]:
    errors: list[str] = []
    frontmatter, _ = _extract_frontmatter(path.read_text(encoding="utf-8"))
    if frontmatter is None:
        return [f"{path}: missing YAML frontmatter"]

    values = _frontmatter_values(frontmatter)
    for field in sorted(REQUIRED_FRONTMATTER_FIELDS):
        if not values.get(field):
            errors.append(f"{path}: missing frontmatter field {field}")

    description = values.get("description", "")
    if len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(
            f"{path}: description is {len(description)} chars; budget is {MAX_DESCRIPTION_CHARS}"
        )
    if not description.startswith("Use when "):
        errors.append(f"{path}: description must start with 'Use when '")

    if values.get("metadata.openclaw.skillKey") != values.get("name"):
        errors.append(f"{path}: metadata.openclaw.skillKey must match name")

    homepage = values.get("metadata.openclaw.homepage", "")
    if homepage and not homepage.startswith(("https://", "http://")):
        errors.append(f"{path}: metadata.openclaw.homepage must be an absolute URL")
    return errors


def _line_has_negative_context(line: str) -> bool:
    return any(marker in line for marker in NEGATIVE_CONTEXT_MARKERS)


def lint_text(path: str, text: str, *, answer_mode: bool = False) -> list[dict[str, object]]:
    rules = list(LINT_RULES)
    if answer_mode:
        rules.extend(ANSWER_ONLY_RULES)

    findings: list[dict[str, object]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        skip_negative_line = _line_has_negative_context(line)
        for rule in rules:
            if skip_negative_line and rule.name != "privacy-overcollection":
                continue
            match = rule.pattern.search(line)
            if match:
                findings.append(
                    {
                        "path": path,
                        "line": lineno,
                        "rule": rule.name,
                        "match": match.group(0),
                        "message": rule.message,
                    }
                )
    return findings


def scan_paths(paths: Iterable[Path], *, answer_mode: bool = False) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        findings.extend(lint_text(path.as_posix(), text, answer_mode=answer_mode))
    return findings


def inspect_package_archive(path: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            normalized = _strip_archive_root(member.filename.rstrip("/"))
            if _is_blocked_package_path(normalized):
                errors.append(f"blocked private path in archive: {member.filename}")
            if member.is_dir() or Path(normalized).suffix not in {".md", ".jsonl"}:
                continue
            try:
                text = archive.read(member).decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"non-utf8 text file in archive: {member.filename}")
                continue
            if normalized in SKIP_STATIC_LINT_PATHS:
                continue
            for finding in lint_text(member.filename, text):
                errors.append(
                    f"{finding['path']}:{finding['line']}: "
                    f"{finding['rule']}: {finding['match']}"
                )
    return errors


def validate_regression_jsonl(path: Path) -> list[str]:
    errors: list[str] = []
    p0_count = 0
    seen_ids: set[str] = set()
    required_fields = {"id", "priority", "language", "mode", "prompt", "expected", "forbidden_regex"}

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{lineno}: invalid JSON: {exc}")
            continue
        missing = required_fields - set(item)
        if missing:
            errors.append(f"{path}:{lineno}: missing fields: {', '.join(sorted(missing))}")
        case_id = item.get("id")
        if case_id in seen_ids:
            errors.append(f"{path}:{lineno}: duplicate id: {case_id}")
        seen_ids.add(case_id)
        if item.get("priority") == "P0":
            p0_count += 1
        for pattern in item.get("forbidden_regex", []):
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(f"{path}:{lineno}: invalid forbidden_regex {pattern!r}: {exc}")

    if p0_count < 8:
        errors.append(f"{path}: expected at least 8 P0 regression cases, found {p0_count}")
    return errors


def check_release(root: Path) -> int:
    manifest_path = root / "skill-package-manifest.txt"
    manifest = load_manifest(manifest_path)
    package_files = build_package_file_list(root, manifest)

    errors: list[str] = []
    errors.extend(validate_skill_frontmatter(root / "SKILL.md"))
    for rel in package_files:
        if _is_blocked_package_path(rel):
            errors.append(f"blocked private path in package list: {rel}")
    for rel in INTERNAL_STUDY_NOTES_REQUIRING_COPYRIGHT_REVIEW:
        if rel in package_files:
            errors.append(f"copyright-positioning review required before packaging: {rel}")

    scanned_paths = [
        root / rel
        for rel in package_files
        if Path(rel).suffix in {".md", ".jsonl"} and rel not in SKIP_STATIC_LINT_PATHS
    ]
    findings = scan_paths(scanned_paths)
    for finding in findings:
        errors.append(
            f"{finding['path']}:{finding['line']}: {finding['rule']}: {finding['match']}"
        )

    regression_path = root / "references" / "evaluation-set.jsonl"
    if regression_path.exists():
        errors.extend(validate_regression_jsonl(regression_path))
    else:
        errors.append("missing references/evaluation-set.jsonl")

    if errors:
        print("Release guardrails failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"release guardrails ok: {len(package_files)} whitelisted files")
    return 0


def write_package(root: Path, output: Path) -> int:
    if check_release(root) != 0:
        return 1
    manifest = load_manifest(root / "skill-package-manifest.txt")
    package_files = build_package_file_list(root, manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in package_files:
            archive.write(root / rel, arcname=f"kiddo-compass/{rel}")
    archive_errors = inspect_package_archive(output)
    if archive_errors:
        print("Release archive inspection failed:", file=sys.stderr)
        for error in archive_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"wrote {output} with {len(package_files)} files")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Run release privacy and packaging checks.")
    subparsers.add_parser("list", help="Print whitelisted package files.")
    inspect_parser = subparsers.add_parser("inspect", help="Inspect an already-built release zip.")
    inspect_parser.add_argument("archive", type=Path)
    package_parser = subparsers.add_parser("package", help="Write a zip package from the whitelist.")
    package_parser.add_argument("--output", type=Path, default=Path("dist/kiddo-compass.zip"))

    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.command == "check":
        return check_release(root)
    if args.command == "list":
        manifest = load_manifest(root / "skill-package-manifest.txt")
        for rel in build_package_file_list(root, manifest):
            print(rel)
        return 0
    if args.command == "inspect":
        errors = inspect_package_archive(args.archive)
        if errors:
            print("Release archive inspection failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"release archive ok: {args.archive}")
        return 0
    if args.command == "package":
        return write_package(root, args.output)

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
