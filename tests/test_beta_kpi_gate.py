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
    EVIDENCE_LABELS,
)


class BetaKpiGateTests(unittest.TestCase):
    def test_evidence_matrix_has_thirty_topics(self):
        root = Path(__file__).resolve().parents[1]
        topics = parse_evidence_topics(root / "references" / "evidence-matrix.md")

        self.assertGreaterEqual(len(topics), 30)

    def test_evidence_taxonomy_recognizes_research_review(self):
        # New independent-evidence class must be recognized by the beta gate.
        self.assertIn("research-review", EVIDENCE_LABELS)
        # Adding it must not weaken the existing required traceability labels.
        for label in [
            "official-consensus",
            "method-source",
            "practice-pattern",
            "needs-evaluation",
        ]:
            self.assertIn(label, EVIDENCE_LABELS)

    def test_methodology_requires_context_before_tool_selection(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8").lower()

        self.assertIn("context before tool", text)
        # The boundary is the full pre-tool checklist, not a single keyword.
        for factor in [
            "age",
            "regulation",
            "pain",
            "sensory load",
            "transition",
            "task difficulty",
            "adult response",
        ]:
            self.assertIn(factor, text)

    def test_methodology_treats_motives_as_hypotheses(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8").lower()

        self.assertIn("motives are hypotheses", text)
        self.assertIn("never", text)
        for forbidden_as_fact in [
            "hidden belief",
            "mistaken goal",
            "manipulation",
            "attention-seeking",
            "power motive",
        ]:
            self.assertIn(forbidden_as_fact, text)

    def test_methodology_does_not_ban_all_praise(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8").lower()

        self.assertIn("praise is contextual", text)
        self.assertIn("not all praise is harmful", text)
        for token in ["specific", "effort", "truthful"]:
            self.assertIn(token, text)

    def test_methodology_consequence_quality_rejects_disguised_punishment(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8").lower()

        for token in ["related", "proportionate", "respectful", "future-focused"]:
            self.assertIn(token, text)
        # A consequence that fails the quality test is named as punishment and replaced.
        self.assertIn("punishment", text)
        for token in ["repair", "prevention", "practice"]:
            self.assertIn(token, text)

    def test_methodology_keeps_internal_theory_terms_out_of_visible_answers(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "methodology.md").read_text(encoding="utf-8").lower()

        self.assertIn("action-first", text)
        for term in ["attunement", "adler", "mistaken goals", "evidence labels", "routing names"]:
            self.assertIn(term, text)

    def test_routing_guide_distinguishes_school_age_from_adolescent(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "routing-guide.md").read_text(encoding="utf-8").lower()

        # The stored 6+y band is preserved; no new persisted age_band value is introduced.
        self.assertIn("6+y", text)
        self.assertNotIn("`13+y`", text)
        self.assertNotIn("`teen`", text)

        # School-age children get shared planning, responsibility, and practice.
        for token in ["school-age", "shared planning", "responsibility", "practice"]:
            self.assertIn(token, text)

        # Adolescents get autonomy, collaborative agreements, privacy, non-patronizing language.
        for token in ["adolescent", "autonomy", "collaborative agreement", "privacy"]:
            self.assertIn(token, text)
        self.assertIn("non-patronizing", text)

        # Toddler-style choices must not be used for a teenager.
        self.assertIn("toddler", text)

        # Adolescence is not inferred from 6+y alone.
        self.assertIn("do not infer adolescence", text)

    def test_scenario_cards_strengthen_whining_lying_homework_repair(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "scenario-template.md").read_text(encoding="utf-8").lower()

        # Whining: no fixed attention-seeking motive; allow specific positive feedback on retry.
        self.assertIn("fixed attention-seeking motive", text)
        self.assertIn("specific positive feedback", text)

        # Lying: do not label the child or infer a fixed motive; prioritize repair and safety.
        self.assertIn("do not label the child", text)
        self.assertIn("make truth safer than concealment", text)
        self.assertIn("prioritize repair and safety", text)

        # Homework: distinguish school-age support from teen autonomy; check the right factors.
        self.assertIn("school-age", text)
        self.assertIn("autonomy", text)
        for token in ["task difficulty", "overload", "anxiety", "sleep"]:
            self.assertIn(token, text)

        # Repair: adult owns behavior without excuses; brief apology does not demand forgiveness; name next plan.
        self.assertIn("without excuses", text)
        self.assertIn("does not demand forgiveness", text)
        self.assertIn("next plan", text)

    def test_scenario_adds_family_problem_solving_meeting_card(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "references" / "scenario-template.md").read_text(encoding="utf-8").lower()

        self.assertIn("family problem-solving meeting", text)
        # Developmental boundary: full participation from age four; younger observe or join one simple part.
        self.assertIn("age four", text)
        # Structure: short, future-focused, with the required building blocks.
        self.assertIn("future-focused", text)
        for token in ["one agenda item", "one safe trial", "one review point"]:
            self.assertIn(token, text)
        # No branded or copied structures.
        for token in ["nine-step", "forced compliment", "branded acronym"]:
            self.assertIn(token, text)
        # Cites the method-level evidence entry.
        self.assertIn("nonviolent discipline method selection", text)

    def test_learning_tracks_include_family_problem_solving(self):
        root = Path(__file__).resolve().parents[1]
        tracks = parse_learning_tracks(root / "references" / "learning-tracks.md")

        self.assertIn("family-problem-solving", tracks)
        record = tracks["family-problem-solving"]

        baseline = record.get("baseline", "").lower()
        for token in ["friction", "age", "safety", "adult pattern"]:
            self.assertIn(token, baseline)

        practice = record.get("practice_action", "").lower()
        for token in ["problem-solving", "jointly selected", "safe solution"]:
            self.assertIn(token, practice)

        review = record.get("review_metric", "").lower()
        self.assertIn("count_metric", review)
        self.assertIn("experience_metric", review)
        self.assertIn("child voice", review)
        self.assertIn("conflict heat", review)

        completion = record.get("completion_rule", "").lower()
        self.assertIn("two review cycles", completion)
        for token in ["coercion", "abuse", "severe distress", "loss of control"]:
            self.assertIn(token, completion)

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
