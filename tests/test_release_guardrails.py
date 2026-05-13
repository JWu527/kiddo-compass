import tempfile
import unittest
from pathlib import Path

from scripts.release_guardrails import (
    build_package_file_list,
    lint_text,
    load_manifest,
    scan_paths,
)
from scripts.run_regression import check_output, load_cases


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


if __name__ == "__main__":
    unittest.main()
