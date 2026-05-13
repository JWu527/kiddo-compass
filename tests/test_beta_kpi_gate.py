import unittest
from pathlib import Path

from scripts.beta_kpi_gate import (
    REQUIRED_MODES,
    compute_metrics,
    parse_evidence_topics,
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


if __name__ == "__main__":
    unittest.main()
