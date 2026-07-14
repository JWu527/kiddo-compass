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
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RUNTIME_PRIVATE_FILES = {
    "child-profile.md",
    "practice-log.md",
    "learning-progress.md",
}

WORKSPACE_ZIP_HINT = (
    "请不要压缩整个工作区，请使用 make audit-bundle 或 "
    "scripts/build_audit_bundle.py 生成白名单发布包。"
)

BLOCKED_PACKAGE_PATTERNS = (
    re.compile(r"(^|/)\.git(/|$)"),
    re.compile(r"(^|/)\.kiddo-compass-state(/|$)"),
    re.compile(r"(^|/)(kiddo-compass-state|live-state|runtime-state|private-state|private-state-root)(/|$)"),
    re.compile(r"(^|/)(study-private|archive)(/|$)"),
    re.compile(r"(^|/)dist(/|$)"),
    re.compile(r"(^|/)__MACOSX(/|$)"),
    re.compile(r"(^|/)__pycache__(/|$)"),
    re.compile(r"(^|/)\._[^/]+$"),
    re.compile(r"(^|/)\.DS_Store$"),
    re.compile(r"(^|/)\.env(?:\.|$)"),
    re.compile(r"\.log$"),
    re.compile(r"\.private\.md$"),
    re.compile(r"\.local\.md$"),
    re.compile(r"\.pyc$"),
    re.compile(r"(^|/)\.handoff(/|$)"),
    re.compile(r"\.pdf$"),
)

INTERNAL_STUDY_NOTES_REQUIRING_COPYRIGHT_REVIEW = {
    "archive/legacy-learning-path.md",
    "study-private/learning-map.md",
    "study-private/tool-cards.md",
    "study-private/adler-psychology.md",
    "study-private/core-concepts.md",
    "study-private/practice-diary.md",
}

RUNTIME_CORE_SKILL_REFERENCES = {
    "references/content-map.md",
    "references/methodology.md",
    "references/safety-triage.md",
    "references/routing-guide.md",
    "references/dialogue-modes.md",
    "references/accessibility-i18n.md",
    "references/evidence-matrix.md",
    "references/scenario-template.md",
    "references/english-response-guide.md",
    "references/state-schema.md",
}

SKILL_REFERENCE_PATTERN = re.compile(
    r"(?:`|\b)(references/[A-Za-z0-9_./-]+|study-private/[A-Za-z0-9_./-]+|archive/[A-Za-z0-9_./-]+)"
)

SKIP_STATIC_LINT_PATHS = {
    "references/evaluation-set.md",
    "references/evaluation-set.jsonl",
}

MAX_DESCRIPTION_CHARS = 220
# Accommodates the required runtime contract set (safety triage, action-first
# output, context-before-tool, motive/praise/consequence boundaries). Deep
# content stays in study-private/archive; raise only when adding a mandated rule.
MAX_RUNTIME_METHODOLOGY_CHARS = 4000
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
        "hardcoded-style",
        re.compile(
            r"(必须|只能|统一|固定|结尾|每条回复).{0,24}"
            r"(宝贝|爸爸妈妈|爸爸|妈妈|父母|家长|🌱|emoji|表情)"
        ),
        "Avoid hardcoded names, roles, or decorative emoji requirements in runtime content.",
    ),
    LintRule(
        "hardcoded-style",
        re.compile(r"用[\"“]?宝贝[\"”]?.{0,12}不用"),
        "Do not force the assistant to use one child nickname term.",
    ),
    LintRule(
        "hardcoded-style",
        re.compile(r"默认.{0,12}(爸爸妈妈|爸爸|妈妈|父母|家长)"),
        "Do not assume one caregiver role by default.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(真实姓名|姓名|精确生日|出生日期|生日|学校|地址|电话|手机号)[:：是为]\s*"
            r"(?!$|（?可选|不要|不需要|不默认|无|空|XX|xxx|\[|<|example)"
            r"[^，。；;\n]+"
        ),
        "Potentially stores or requests identifying family data.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(出生日期|出生时间|完整生日|精确生日|生日)\s*[:：是为]?\s*"
            r"\d{4}\s*[-年/.]\s*\d{1,2}\s*[-月/.]\s*\d{1,2}\s*日?"
        ),
        "Potential full birthday in release material.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(学校|幼儿园|托班|园所|就读学校)\s*[:：是为]\s*"
            r"(?!$|不|不要|不需要|无|空|XX|xxx|\[|<|example|当地|本地|可信)"
            r"[\u4e00-\u9fffA-Za-z0-9_-]{2,}(?:幼儿园|学校|托班|园|中心)?"
        ),
        "Potential school or kindergarten identifier in release material.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(真实姓名|姓名|孩子叫|宝宝叫|宝贝叫|小名叫|昵称叫)\s*[:：是为]?\s*"
            r"(?!$|可选|不要|不需要|不默认|无|空|XX|xxx|\[|<|example)"
            r"[\u4e00-\u9fff]{2,4}"
        ),
        "Potential real child name in release material.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(
            r"(家庭结构|兄弟姐妹|主要照顾者|照顾模式)\s*[:：是为]\s*"
            r"(?!$|可选|不要|不需要|不默认|无|空|XX|xxx|\[|<|example)"
            r"[^\n，。；;]*(?:爷爷|奶奶|外公|外婆|祖辈|父母|爸爸|妈妈|独生|兄弟|姐妹|双职工|单亲|离异|再婚)[^\n，。；;]*"
        ),
        "Potential detailed family structure in release material.",
    ),
    LintRule(
        "privacy-overcollection",
        re.compile(r"^\*\*(场景|过程|效果|反思|下一步):\*\*\s*\S+", re.MULTILINE),
        "Potential real child behavior tracking log in release material.",
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
    LintRule(
        "unimplemented-automation-claim",
        re.compile(
            r"(Agent\s*)?自动(维护|整理写入|保存|生成|追加|更新)|"
            r"巡检自动生成|每月\s*1\s*日由巡检"
        ),
        "Do not claim unimplemented automatic state maintenance or patrol behavior.",
    ),
)

LIVE_STATE_CONTENT_RULES = (
    LintRule(
        "live-state-content",
        re.compile(r"^# 孩子画像$", re.MULTILINE),
        "Live child profile content must not be packaged.",
    ),
    LintRule(
        "live-state-content",
        re.compile(r"^# [^（\n]+ 实践日记$", re.MULTILINE),
        "Live practice log content must not be packaged.",
    ),
    LintRule(
        "live-state-content",
        re.compile(r"^# 正面管教学习进度\s+—", re.MULTILINE),
        "Live learning-progress content must not be packaged.",
    ),
    LintRule(
        "live-state-content",
        re.compile(r"^\s*-\s*主要照顾者[:：]\s*\S+", re.MULTILINE),
        "Live family structure details must not be packaged.",
    ),
    LintRule(
        "live-state-content",
        re.compile(r"^\s*-\s*已完成[:：]\s*\d+\s*/\s*30\s*天?", re.MULTILINE),
        "Live 30-day learning progress must not be packaged.",
    ),
    LintRule(
        "live-state-content",
        re.compile(r"^\*\*场景:\*\*\s*\S+", re.MULTILINE),
        "Live practice-log scenes must not be packaged.",
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
    "不再",
    "禁止",
    "避免",
    "不得",
    "不能",
    "不会",
    "未实现",
    "Spec-only",
    "spec-only",
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


def _normalize_archive_path(path: str) -> str:
    normalized = path.replace("\\", "/").strip().rstrip("/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _is_blocked_package_path(path: str) -> bool:
    normalized = _normalize_archive_path(path)
    name = Path(normalized).name
    if name in RUNTIME_PRIVATE_FILES:
        return True
    return any(pattern.search(normalized) for pattern in BLOCKED_PACKAGE_PATTERNS)


def _strip_archive_root(path: str) -> str:
    parts = [
        part
        for part in _normalize_archive_path(path).split("/")
        if part and part != "."
    ]
    if len(parts) > 1 and parts[0] == "kiddo-compass":
        return "/".join(parts[1:])
    return "/".join(parts)


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


def find_root_live_state_files(root: Path) -> list[str]:
    """Return root-level live state files that must stay in private storage."""
    errors: list[str] = []
    for name in sorted(RUNTIME_PRIVATE_FILES):
        if (root / name).exists():
            errors.append(
                f"root live state file must be migrated to .kiddo-compass-state/: {name}"
            )
    return errors


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


def _normalize_skill_reference(raw_reference: str) -> str:
    return raw_reference.strip().rstrip("`.,);:]}")


def validate_skill_content_layers(path: Path) -> list[str]:
    """Ensure runtime instructions only point at runtime-core references."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    seen: set[str] = set()
    for match in SKILL_REFERENCE_PATTERN.finditer(text):
        reference = _normalize_skill_reference(match.group(1))
        if reference in seen:
            continue
        seen.add(reference)
        if reference.startswith(("study-private/", "archive/")):
            errors.append(f"{path}: references private/archive layer: {reference}")
            continue
        if reference.startswith("references/") and reference not in RUNTIME_CORE_SKILL_REFERENCES:
            errors.append(f"{path}: non-runtime-core reference: {reference}")
    return errors


def validate_runtime_methodology(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: missing runtime methodology"]

    text = path.read_text(encoding="utf-8")
    if len(text) > MAX_RUNTIME_METHODOLOGY_CHARS:
        errors.append(
            f"{path}: runtime methodology is {len(text)} chars; "
            f"budget is {MAX_RUNTIME_METHODOLOGY_CHARS}"
        )

    required_phrases = (
        "先安全分诊",
        "先给可执行动作",
        "最少必要追问",
        "不诊断",
        "不贴标签",
        "温和但坚定",
        "不惩罚",
        "不羞辱",
        "不放任",
        "适配用户",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{path}: missing runtime behavior rule: {phrase}")

    for finding in lint_text(path.as_posix(), text):
        if finding["rule"] == "hardcoded-style":
            errors.append(
                f"{finding['path']}:{finding['line']}: "
                f"hardcoded-style: {finding['match']}"
            )
    return errors


def _line_has_negative_context(line: str) -> bool:
    return any(marker in line for marker in NEGATIVE_CONTEXT_MARKERS)


def lint_text(path: str, text: str, *, answer_mode: bool = False) -> list[dict[str, object]]:
    rules = [*LINT_RULES, *LIVE_STATE_CONTENT_RULES]
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


def _inspect_archive_member(
    errors: list[str],
    member_name: str,
    *,
    is_dir: bool,
    data: bytes | None,
) -> None:
    normalized = _strip_archive_root(member_name)
    if _is_blocked_package_path(normalized):
        errors.append(f"blocked private path in archive: {member_name}")
    if is_dir or Path(normalized).suffix not in {".md", ".jsonl"}:
        return
    if normalized in SKIP_STATIC_LINT_PATHS:
        return
    if data is None:
        errors.append(f"unable to read text file in archive: {member_name}")
        return
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"non-utf8 text file in archive: {member_name}")
        return
    for finding in lint_text(member_name, text):
        errors.append(
            f"{finding['path']}:{finding['line']}: "
            f"{finding['rule']}: {finding['match']}"
        )


def inspect_package_archive(path: Path) -> list[str]:
    errors: list[str] = []
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                data = None if member.is_dir() else archive.read(member)
                _inspect_archive_member(
                    errors,
                    member.filename,
                    is_dir=member.is_dir(),
                    data=data,
                )
        return errors

    if tarfile.is_tarfile(path):
        with tarfile.open(path, "r:*") as archive:
            for member in archive.getmembers():
                data = None
                if member.isfile():
                    extracted = archive.extractfile(member)
                    if extracted is not None:
                        with extracted:
                            data = extracted.read()
                _inspect_archive_member(
                    errors,
                    member.name,
                    is_dir=member.isdir(),
                    data=data,
                )
        return errors

    errors.append(f"unsupported archive format: {path}")
    return errors


def print_errors_with_workspace_hint(heading: str, errors: Iterable[str]) -> None:
    print(heading, file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    print(WORKSPACE_ZIP_HINT, file=sys.stderr)


def validate_regression_jsonl(path: Path) -> list[str]:
    errors: list[str] = []
    p0_count = 0
    seen_ids: set[str] = set()
    required_fields = {
        "id",
        "priority",
        "language",
        "mode",
        "input",
        "expected_constraints",
        "forbidden_patterns",
    }

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
        for index, constraint in enumerate(item.get("expected_constraints", []), start=1):
            if not isinstance(constraint, dict):
                errors.append(f"{path}:{lineno}: expected_constraints[{index}] must be an object")
                continue
            pattern = constraint.get("required_pattern")
            if not pattern:
                errors.append(
                    f"{path}:{lineno}: expected_constraints[{index}] missing required_pattern"
                )
                continue
            try:
                re.compile(str(pattern))
            except re.error as exc:
                errors.append(
                    f"{path}:{lineno}: invalid expected_constraints[{index}] "
                    f"required_pattern {pattern!r}: {exc}"
                )
        for pattern in [*item.get("forbidden_regex", []), *item.get("forbidden_patterns", [])]:
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(f"{path}:{lineno}: invalid forbidden pattern {pattern!r}: {exc}")

    if p0_count < 8:
        errors.append(f"{path}: expected at least 8 P0 regression cases, found {p0_count}")
    return errors


def check_release(root: Path) -> int:
    manifest_path = root / "skill-package-manifest.txt"
    manifest = load_manifest(manifest_path)
    package_files = build_package_file_list(root, manifest)

    errors: list[str] = []
    errors.extend(find_root_live_state_files(root))
    errors.extend(validate_skill_frontmatter(root / "SKILL.md"))
    errors.extend(validate_skill_content_layers(root / "SKILL.md"))
    errors.extend(validate_runtime_methodology(root / "references" / "methodology.md"))
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
        print_errors_with_workspace_hint("Release guardrails failed:", errors)
        return 1

    print(f"release guardrails ok: {len(package_files)} whitelisted files", flush=True)
    return 0


def _write_package_archive(root: Path, output: Path, package_files: Iterable[str]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in package_files:
            archive.write(root / rel, arcname=f"kiddo-compass/{rel}")


def build_audit_bundle(root: Path, output: Path) -> list[str]:
    """Build the only shareable audit bundle from the public whitelist."""
    if check_release(root) != 0:
        raise RuntimeError("release guardrails failed before audit bundle build")
    manifest = load_manifest(root / "skill-package-manifest.txt")
    package_files = build_package_file_list(root, manifest)
    _write_package_archive(root, output, package_files)
    archive_errors = inspect_package_archive(output)
    if archive_errors:
        details = "\n".join(f"- {error}" for error in archive_errors)
        raise RuntimeError(
            f"release archive inspection failed:\n{details}\n{WORKSPACE_ZIP_HINT}"
        )
    return package_files


def write_package(root: Path, output: Path) -> int:
    if check_release(root) != 0:
        return 1
    manifest = load_manifest(root / "skill-package-manifest.txt")
    package_files = build_package_file_list(root, manifest)
    _write_package_archive(root, output, package_files)
    archive_errors = inspect_package_archive(output)
    if archive_errors:
        print_errors_with_workspace_hint("Release archive inspection failed:", archive_errors)
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
            print_errors_with_workspace_hint("Release archive inspection failed:", errors)
            return 1
        print(f"release archive ok: {args.archive} (blocked path=0, privacy-overcollection finding=0)")
        return 0
    if args.command == "package":
        return write_package(root, args.output)

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
