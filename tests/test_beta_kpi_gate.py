import unittest
from pathlib import Path

from scripts.beta_kpi_gate import (
    REQUIRED_MODES,
    compute_metrics,
    parse_evidence_topics,
    validate_scenario_cards,
    validate_planned_work_artifacts,
)


class BetaKpiGateTests(unittest.TestCase):
    def test_evidence_matrix_has_thirty_topics(self):
        root = Path(__file__).resolve().parents[1]
        topics = parse_evidence_topics(root / "references" / "evidence-matrix.md")

        self.assertGreaterEqual(len(topics), 30)

    def test_beta_metrics_meet_gate(self):
        root = Path(__file__).resolve().parents[1]
        metrics = compute_metrics(root)

        self.assertEqual(metrics["privacy_static_findings"], 0)
        self.assertGreaterEqual(metrics["evidence_topics"], 30)
        self.assertGreaterEqual(metrics["p0_cases"], 8)
        self.assertTrue(REQUIRED_MODES.issubset(metrics["modes"]))
        self.assertEqual(metrics["missing_required_languages"], [])

    def test_audit_plan_artifacts_are_present(self):
        root = Path(__file__).resolve().parents[1]

        failures = validate_planned_work_artifacts(root)

        self.assertEqual(failures, [])

    def test_scenario_cards_have_evidence_and_escalation_contract(self):
        root = Path(__file__).resolve().parents[1]

        failures = validate_scenario_cards(root / "references" / "scenario-template.md")

        self.assertEqual(failures, [])

    def test_methodology_downgrades_mistaken_goal_lens(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8")

        self.assertIn("默认骨架：安全 → 发展/身体/环境校准 → 关系与边界 → 技能训练", text)
        self.assertIn("四个错误目的只能作为学习模式或深度复盘中的可选解释层", text)

    def test_feature_status_and_accessibility_acceptance_are_documented(self):
        root = Path(__file__).resolve().parents[1]
        feature_status = (root / "references" / "feature-status.md").read_text(encoding="utf-8")
        accessibility = (root / "references" / "accessibility-i18n.md").read_text(encoding="utf-8")

        self.assertIn("Implemented", feature_status)
        self.assertIn("Spec-only", feature_status)
        self.assertIn("Deferred", feature_status)
        self.assertIn("one-sentence mode", accessibility)
        self.assertIn("3-6 lines", accessibility)
        self.assertIn("critical action", accessibility)


if __name__ == "__main__":
    unittest.main()
