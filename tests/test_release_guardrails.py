import tempfile
import unittest
from pathlib import Path

from scripts.release_guardrails import (
    build_package_file_list,
    inspect_package_archive,
    lint_text,
    load_manifest,
    scan_paths,
    validate_skill_frontmatter,
)
from scripts.run_regression import check_output, default_hermes_cmd, load_cases, run_case


class ReleaseGuardrailTests(unittest.TestCase):
    def test_manifest_whitelist_excludes_runtime_private_files(self):
        root = Path(__file__).resolve().parents[1]
        manifest = load_manifest(root / "skill-package-manifest.txt")
        file_list = build_package_file_list(root, manifest)

        self.assertIn("SKILL.md", file_list)
        self.assertIn("child-profile.example.md", file_list)
        self.assertNotIn("child-profile.md", file_list)
        self.assertNotIn("practice-log.md", file_list)
        self.assertNotIn("learning-progress.md", file_list)
        self.assertFalse(any(path.startswith(".git/") for path in file_list))
        self.assertFalse(any("__MACOSX" in path for path in file_list))
        self.assertFalse(any(Path(path).name.startswith("._") for path in file_list))

    def test_skill_frontmatter_is_valid_and_description_is_budgeted(self):
        root = Path(__file__).resolve().parents[1]

        errors = validate_skill_frontmatter(root / "SKILL.md")

        self.assertEqual(errors, [])

    def test_zip_archive_inspection_catches_blocked_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "bad.zip"
            import zipfile

            with zipfile.ZipFile(zip_path, "w") as archive:
                archive.writestr("kiddo-compass/SKILL.md", "---\nname: kiddo\n---\n")
                archive.writestr("kiddo-compass/.git/config", "private")
                archive.writestr("kiddo-compass/child-profile.md", "真实姓名：张三")

            errors = inspect_package_archive(zip_path)

        self.assertTrue(any(".git" in error for error in errors))
        self.assertTrue(any("child-profile.md" in error for error in errors))

    def test_lint_text_flags_public_release_red_lines(self):
        sample = "\n".join(
            [
                "生日是 2021 年 8 月 18 日，学校是 XX 幼儿园。",
                "孩子这是感觉统合失调，坚持三天就会好。",
                "这就是寻求关注。",
                "可以打 12345678901 这个热线。",
            ]
        )

        findings = lint_text("sample.md", sample)
        rules = {finding["rule"] for finding in findings}

        self.assertIn("privacy-overcollection", rules)
        self.assertIn("near-diagnostic-language", rules)
        self.assertIn("fixed-day-promise", rules)
        self.assertIn("single-cause-label", rules)
        self.assertIn("unverified-hotline-number", rules)

    def test_scan_paths_can_fail_on_private_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "family.private.md"
            path.write_text("真实姓名：张三\n电话：13800138000\n", encoding="utf-8")

            findings = scan_paths([path])

        self.assertGreaterEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "privacy-overcollection")

    def test_regression_jsonl_loads_p0_cases(self):
        root = Path(__file__).resolve().parents[1]
        cases = load_cases(root / "references" / "evaluation-set.jsonl", priority="P0")

        self.assertGreaterEqual(len(cases), 8)
        self.assertTrue(all(case["priority"] == "P0" for case in cases))

    def test_regression_output_checker_catches_forbidden_regex(self):
        case = {"id": "X", "forbidden_regex": ["就是寻求关注", "热线\\D{0,8}\\d{5,}"]}

        failures = check_output(case, "这就是寻求关注，可以打 12345 热线。")

        self.assertGreaterEqual(len(failures), 1)

    def test_regression_output_checker_requires_expected_regex(self):
        case = {"id": "X", "required_regex": ["安全", "当地紧急"]}

        failures = check_output(case, "先保证安全，联系当地紧急支持。")
        missing = check_output(case, "先讲道理，再坚持规则。")

        self.assertEqual(failures, [])
        self.assertTrue(any("required_regex missing" in failure for failure in missing))

    def test_regression_output_checker_catches_provider_failures(self):
        failures = check_output({}, "API call failed after 3 retries: Connection error.")

        self.assertTrue(any("provider failure" in failure for failure in failures))

    def test_run_case_executes_subprocess_and_checks_output(self):
        case = {
            "id": "X",
            "priority": "P0",
            "language": "en",
            "prompt": "hello regression",
            "required_regex": ["hello regression"],
            "forbidden_regex": [],
        }

        result = run_case(
            case,
            ["python3", "-c", "import sys; print(sys.argv[-1])"],
            timeout=5,
        )

        self.assertEqual(result["failures"], [])

    def test_default_hermes_cmd_targets_current_skill_path(self):
        root = Path(__file__).resolve().parents[1]

        cmd = default_hermes_cmd(root)

        self.assertIn("--skills", cmd)
        self.assertIn(str(root), cmd)
        self.assertNotIn("kiddo-compass", cmd)
        self.assertNotIn("--ignore-rules", cmd)

    def test_default_openclaw_cmd_uses_profile_and_model(self):
        from scripts.run_regression import default_openclaw_infer_cmd

        cmd = default_openclaw_infer_cmd(model="zai/glm-5.1", profile="kiddo-regression")

        self.assertEqual(cmd[:3], ["openclaw", "--profile", "kiddo-regression"])
        self.assertIn("infer", cmd)
        self.assertIn("model", cmd)
        self.assertIn("run", cmd)
        self.assertIn("--local", cmd)
        self.assertIn("--json", cmd)
        self.assertIn("--model", cmd)
        self.assertIn("zai/glm-5.1", cmd)

    def test_default_openclaw_agent_cmd_uses_agent_profile_and_model(self):
        from scripts.run_regression import default_openclaw_agent_cmd

        cmd = default_openclaw_agent_cmd(
            model="zai/glm-5.1",
            profile="kiddo-regression",
            agent="main",
            timeout=180,
        )

        self.assertEqual(cmd[:3], ["openclaw", "--profile", "kiddo-regression"])
        self.assertIn("agent", cmd)
        self.assertIn("--local", cmd)
        self.assertIn("--agent", cmd)
        self.assertIn("main", cmd)
        self.assertIn("--model", cmd)
        self.assertIn("zai/glm-5.1", cmd)
        self.assertIn("--message", cmd)

    def test_openclaw_json_output_is_normalized_to_text(self):
        from scripts.run_regression import normalize_runner_output

        raw_output = (
            "Ollama could not be reached at http://127.0.0.1:11434.\n"
            '{"ok": true, "outputs": [{"text": "先保证安全，联系当地紧急支持。"}]}'
        )

        normalized = normalize_runner_output(raw_output, runner="openclaw")

        self.assertEqual(normalized, "先保证安全，联系当地紧急支持。")

    def test_openclaw_agent_json_output_is_normalized_to_text(self):
        from scripts.run_regression import normalize_runner_output

        raw_output = '{"payloads": [{"text": "我先按你给的信息给一个临时做法。"}]}'

        normalized = normalize_runner_output(raw_output, runner="openclaw-agent")

        self.assertEqual(normalized, "我先按你给的信息给一个临时做法。")


if __name__ == "__main__":
    unittest.main()
