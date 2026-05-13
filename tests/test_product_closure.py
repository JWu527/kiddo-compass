import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.quality_dashboard import build_dashboard
from scripts.semantic_score import score_results
from scripts.source_freshness import check_freshness
from scripts.state_service import StateStore


class ProductClosureTests(unittest.TestCase):
    def scratch_dir(self, name: str) -> Path:
        path = ROOT / ".tmp-product-closure-test" / name
        if path.exists():
            for child in sorted(path.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            path.rmdir()
        path.mkdir(parents=True)
        return path

    def test_github_actions_runs_public_beta_gate(self):
        root = Path(__file__).resolve().parents[1]
        workflow = root / ".github" / "workflows" / "public-beta.yml"
        text = workflow.read_text(encoding="utf-8")

        self.assertIn("python3 -m unittest discover -s tests -p 'test_*.py'", text)
        self.assertIn("python3 scripts/release_guardrails.py check", text)
        self.assertIn("python3 scripts/beta_kpi_gate.py", text)
        self.assertIn("python3 scripts/build_release_package.py --output dist/kiddo-compass.zip", text)
        self.assertIn("python3 scripts/release_guardrails.py inspect dist/kiddo-compass.zip", text)
        self.assertIn("python3 scripts/semantic_score.py --report dist/regression-p0.json", text)

    def test_state_store_supports_consent_and_data_rights(self):
        state_dir = self.scratch_dir("state")
        store = StateStore(state_dir)
        profile = store.create_profile(
            nickname="小明",
            age_band="3-5y",
            caregiver_mode="parent",
            consent_scope="store_minimal_profile",
        )
        exported = store.export_state()

        self.assertEqual(profile["ChildProfile"]["nickname"], "小明")
        self.assertEqual(exported["ChildProfile"]["age_band"], "3-5y")
        self.assertEqual(exported["ConsentLog"][0]["action_type"], "store_minimal_profile")

        store.correct_field("ChildProfile", "nickname", "星星")
        self.assertEqual(store.view_state()["ChildProfile"]["nickname"], "星星")

        anonymized = store.anonymize()
        self.assertEqual(anonymized["ChildProfile"]["nickname"], "child")
        self.assertEqual(anonymized["ChildProfile"]["age_band"], "3-5y")

        store.delete_state()
        self.assertFalse((state_dir / "state.json").exists())

    def test_quality_dashboard_summarizes_metrics_and_regression(self):
        out = self.scratch_dir("dashboard") / "dashboard.html"
        metrics = {
            "metrics": {"p0_cases": 8, "privacy_static_findings": 0},
            "failures": [],
        }
        regression = {
            "total": 8,
            "failed": 0,
            "results": [{"id": "P0-PRIVACY-01", "failures": []}],
        }

        build_dashboard(metrics, regression, out)
        text = out.read_text(encoding="utf-8")

        self.assertIn("Kiddo Compass Quality Dashboard", text)
        self.assertIn("P0-PRIVACY-01", text)
        self.assertIn("privacy_static_findings", text)

    def test_regional_resources_and_sources_are_fresh(self):
        root = Path(__file__).resolve().parents[1]

        failures = check_freshness(root, today="2026-05-13")

        self.assertEqual(failures, [])

    def test_semantic_score_flags_missing_required_assertions(self):
        report = {
            "results": [
                {"id": "A", "failures": [], "output": "安全 当地紧急"},
                {"id": "B", "failures": ["required_regex missing '安全'"], "output": "讲道理"},
            ]
        }

        scored = score_results(report)

        self.assertEqual(scored["failed"], 1)
        self.assertEqual(scored["passed"], 1)
        self.assertFalse(scored["ok"])

    def test_deep_scenario_packs_cover_core_tracks(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "deep-scenario-packs.md").read_text(encoding="utf-8")

        for token in [
            "sleep",
            "feeding",
            "toileting",
            "aggression",
            "separation",
            "grandparent-alignment",
            "official-consensus",
            "practice-pattern",
            "review prompt",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
