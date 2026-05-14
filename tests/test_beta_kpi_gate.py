import json
import unittest
from pathlib import Path

from scripts.beta_kpi_gate import (
    REQUIRED_MODES,
    compute_metrics,
    parse_learning_tracks,
    parse_evidence_topics,
    validate_learning_tracks,
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
        text = (root / "archive" / "methodology.md").read_text(encoding="utf-8")

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

    def test_style_templates_cover_roles_and_avoid_forced_affection(self):
        root = Path(__file__).resolve().parents[1]
        methodology = (root / "references" / "methodology.md").read_text(encoding="utf-8")
        accessibility = (root / "references" / "accessibility-i18n.md").read_text(encoding="utf-8")
        english = (root / "references" / "english-response-guide.md").read_text(encoding="utf-8")
        combined = "\n".join([methodology, accessibility, english])

        for token in [
            "用户自称",
            "爸爸",
            "妈妈",
            "老师",
            "祖辈",
            "保姆",
            "伴侣",
            "其他照护者",
            "不强行称呼",
            "不强制称孩子为",
            "no decorative emoji",
            "formal mode",
            "one-sentence mode",
            "TTS",
        ]:
            self.assertIn(token, combined)

        self.assertNotIn("先把宝贝", accessibility)
        self.assertNotIn("每次结尾", combined)
        self.assertNotIn("固定 emoji", combined)

    def test_learning_tracks_are_goal_driven_with_count_and_experience_metrics(self):
        root = Path(__file__).resolve().parents[1]
        tracks = parse_learning_tracks(root / "references" / "learning-tracks.md")

        required = {
            "sleep",
            "feeding",
            "toileting",
            "aggression",
            "separation",
            "method-basics",
        }

        self.assertTrue(required.issubset(set(tracks)))
        self.assertGreaterEqual(len(tracks), 6)
        for track in required:
            record = tracks[track]
            for field in {
                "goal_type",
                "baseline",
                "practice_action",
                "review_metric",
                "progress_state",
                "completion_rule",
                "last_reviewed_at",
            }:
                self.assertIn(field, record)
            self.assertIn("count_metric", record["review_metric"])
            self.assertIn("experience_metric", record["review_metric"])

        self.assertEqual(validate_learning_tracks(root / "references" / "learning-tracks.md"), [])

    def test_learning_progress_template_uses_goal_schema_not_day_course(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "examples" / "learning-progress.example.md").read_text(encoding="utf-8")

        for field in [
            "goal_type",
            "baseline",
            "practice_action",
            "review_metric",
            "progress_state",
            "completion_rule",
            "last_reviewed_at",
        ]:
            self.assertIn(field, text)

        self.assertNotRegex(text, r"Day\\s*[0-9]|当前天数|已完成\\s*[:：].*30|30\\s*天课程")

    def test_safety_templates_cover_development_and_adult_violence_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        safety = (root / "references" / "safety-triage.md").read_text(encoding="utf-8")
        evidence = (root / "references" / "evidence-matrix.md").read_text(encoding="utf-8")
        scenarios = (root / "references" / "scenario-template.md").read_text(encoding="utf-8")

        for token in [
            "cannot diagnose",
            "single observation",
            "eye contact",
            "cultural",
            "developmental screening",
            "while waiting",
            "low-risk support",
        ]:
            self.assertIn(token, safety)
        for token in [
            "2 岁还没有词",
            "不回应名字",
            "语言明显倒退",
            "社交沟通担忧",
            "眼神接触",
            "文化",
        ]:
            self.assertIn(token, evidence)
        for token in [
            "Adult loss of control",
            "shaking",
            "separate",
            "urgent medical evaluation",
            "do not enter ordinary discipline",
        ]:
            self.assertIn(token, scenarios)

    def test_regional_resources_define_required_slots_without_numbers(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "references" / "regional-resources.json").read_text(encoding="utf-8"))
        regions = {item["region"]: item for item in data["regions"]}

        for region in ["generic-zh", "generic-en", "CN", "SG"]:
            self.assertIn(region, regions)
            self.assertIn("resource_slot", regions[region])
            self.assertIn("emergency_guidance", regions[region])
            self.assertEqual(regions[region]["publishable_phone_numbers"], [])

    def test_state_docs_match_reference_implementation_boundary(self):
        root = Path(__file__).resolve().parents[1]
        state_schema = (root / "references" / "state-schema.md").read_text(encoding="utf-8")
        platform = (root / "references" / "platform-integration.md").read_text(encoding="utf-8")
        feature_status = (root / "references" / "feature-status.md").read_text(encoding="utf-8")
        feedback = (root / "references" / "feedback-and-patrol.md").read_text(encoding="utf-8")
        combined = "\n".join([state_schema, platform, feature_status, feedback])

        for token in [
            "reference implementation",
            "Spec-only",
            "not a production account service",
            "confirmation_summary",
            "ChildProfile",
            "Case",
            "Intervention",
            "Outcome",
            "ConsentLog",
        ]:
            self.assertIn(token, combined)

        for forbidden in ["Agent 自动维护", "自动保存", "自动生成月度回顾"]:
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
