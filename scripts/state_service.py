#!/usr/bin/env python3
"""Local private state service for Kiddo Compass.

This is the reference implementation for platform state APIs. Product
surfaces can map their consent UI and account storage to this contract.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


DIRECT_IDENTIFIER_FIELD_RE = re.compile(
    r"(real_?name|full_?name|exact_?birthday|birth_?date|birthday|school|"
    r"kindergarten|phone|mobile|address|id_?number|medical_?id)",
    re.IGNORECASE,
)
DIRECT_IDENTIFIER_VALUE_RE = re.compile(
    r"(真实姓名|姓名|出生日期|生日|学校|幼儿园|电话|手机号|地址|身份证|"
    r"real name|full name|birthday|school|kindergarten|phone|address|"
    r"\d{4}-\d{1,2}-\d{1,2}|\d{5,})",
    re.IGNORECASE,
)


class StateStore:
    def __init__(self, root: Path):
        self.root = root
        self.path = root / "state.json"
        self.root.mkdir(parents=True, exist_ok=True)

    def _today(self) -> str:
        return date.today().isoformat()

    def _empty_state(self) -> dict[str, Any]:
        return {
            "Household": {
                "schema_version": "1",
                "household_id": "local-household",
                "locale": "zh-CN",
                "storage_scope": "local-private",
            },
            "ChildProfile": {
                "schema_version": "1",
                "child_id": "local-child",
                "household_id": "local-household",
                "nickname": "",
                "age_band": "unknown",
                "caregiver_mode": "unknown",
                "facts": [],
                "hypotheses": [],
            },
            "Case": [],
            "Intervention": [],
            "Outcome": [],
            "ConsentLog": [],
            "LearningTrack": [],
        }

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._empty_state()
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, state: dict[str, Any]) -> dict[str, Any]:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)
        return state

    def _contains_identifier(self, value: Any, *, key_hint: str = "") -> bool:
        if key_hint and DIRECT_IDENTIFIER_FIELD_RE.search(key_hint):
            return True
        if isinstance(value, dict):
            return any(
                self._contains_identifier(child, key_hint=str(key))
                for key, child in value.items()
            )
        if isinstance(value, list):
            return any(self._contains_identifier(item) for item in value)
        if isinstance(value, str):
            return bool(DIRECT_IDENTIFIER_VALUE_RE.search(value))
        return False

    def _redact_identifiers(self, value: Any, *, key_hint: str = "") -> Any:
        if isinstance(value, dict):
            return {
                key: self._redact_identifiers(child, key_hint=str(key))
                for key, child in value.items()
            }
        if isinstance(value, list):
            return [self._redact_identifiers(item) for item in value]
        if isinstance(value, str) and self._contains_identifier(value, key_hint=key_hint):
            return "[redacted direct identifier]"
        if key_hint and DIRECT_IDENTIFIER_FIELD_RE.search(key_hint):
            return ""
        return value

    def prepare_write(
        self,
        entity: str,
        fields: dict[str, Any],
        *,
        action_type: str,
    ) -> dict[str, Any]:
        contains_identifying_info = self._contains_identifier(fields)
        return {
            "entity": entity,
            "action_type": action_type,
            "fields_to_write": sorted(fields.keys()),
            "contains_identifying_info": contains_identifying_info,
            "desensitized": not contains_identifying_info,
            "requires_user_confirmation": True,
        }

    def _append_consent(
        self,
        state: dict[str, Any],
        action_type: str,
        scope: str,
        confirmation_summary: dict[str, Any],
    ) -> None:
        state["ConsentLog"].append(
            {
                "schema_version": "1",
                "consent_id": f"consent-{len(state['ConsentLog']) + 1}",
                "action_type": action_type,
                "confirmed_at": self._today(),
                "scope": scope,
                "confirmation_summary": confirmation_summary,
            }
        )

    def _next_id(self, state: dict[str, Any], entity: str, id_field: str) -> str:
        return f"{entity.lower()}-{len(state[entity]) + 1}"

    def _require_confirmation(self, confirmed: bool, summary: dict[str, Any]) -> None:
        if not confirmed:
            raise PermissionError(
                "write requires user confirmation; call prepare_write first and confirm summary"
            )

    def create_profile(
        self,
        *,
        nickname: str,
        age_band: str,
        caregiver_mode: str,
        consent_scope: str,
        confirmed: bool = True,
    ) -> dict[str, Any]:
        fields = {
            "nickname": nickname,
            "age_band": age_band,
            "caregiver_mode": caregiver_mode,
        }
        summary = self.prepare_write("ChildProfile", fields, action_type=consent_scope)
        self._require_confirmation(confirmed, summary)
        state = self._read()
        state["ChildProfile"].update(
            {
                "nickname": nickname,
                "age_band": age_band,
                "caregiver_mode": caregiver_mode,
                "facts": [
                    {
                        "value": f"nickname={nickname}; age_band={age_band}; caregiver_mode={caregiver_mode}",
                        "source_type": "user_confirmed",
                        "source_turn": "local-state-service",
                        "last_updated": self._today(),
                    }
                ],
            }
        )
        self._append_consent(state, consent_scope, "minimal profile fields", summary)
        return self._write(state)

    def create_case(
        self,
        *,
        child_id: str,
        scene_type: str,
        risk_route: str,
        pattern_frequency: str,
        source_type: str,
        confirmed: bool = True,
        **extra_fields: Any,
    ) -> dict[str, Any]:
        fields = {
            "child_id": child_id,
            "scene_type": scene_type,
            "risk_route": risk_route,
            "pattern_frequency": pattern_frequency,
            "source_type": source_type,
            **extra_fields,
        }
        summary = self.prepare_write("Case", fields, action_type="store_case")
        self._require_confirmation(confirmed, summary)
        state = self._read()
        record = {
            "schema_version": "1",
            "case_id": self._next_id(state, "Case", "case_id"),
            **fields,
            "created_at": self._today(),
        }
        state["Case"].append(record)
        self._append_consent(state, "store_case", f"Case.{record['case_id']}", summary)
        self._write(state)
        return record

    def create_intervention(
        self,
        *,
        case_id: str,
        recommendation_type: str,
        evidence_label: str,
        action: str,
        source_type: str,
        confirmed: bool = True,
    ) -> dict[str, Any]:
        fields = {
            "case_id": case_id,
            "recommendation_type": recommendation_type,
            "evidence_label": evidence_label,
            "action": action,
            "source_type": source_type,
        }
        summary = self.prepare_write("Intervention", fields, action_type="store_intervention")
        self._require_confirmation(confirmed, summary)
        state = self._read()
        record = {
            "schema_version": "1",
            "intervention_id": self._next_id(state, "Intervention", "intervention_id"),
            **fields,
            "delivered_at": self._today(),
        }
        state["Intervention"].append(record)
        self._append_consent(
            state,
            "store_intervention",
            f"Intervention.{record['intervention_id']}",
            summary,
        )
        self._write(state)
        return record

    def create_outcome(
        self,
        *,
        intervention_id: str,
        result_type: str,
        notes: str,
        source_type: str,
        confirmed: bool = True,
    ) -> dict[str, Any]:
        fields = {
            "intervention_id": intervention_id,
            "result_type": result_type,
            "notes": notes,
            "source_type": source_type,
        }
        summary = self.prepare_write("Outcome", fields, action_type="store_outcome")
        self._require_confirmation(confirmed, summary)
        state = self._read()
        record = {
            "schema_version": "1",
            "outcome_id": self._next_id(state, "Outcome", "outcome_id"),
            **fields,
            "updated_at": self._today(),
        }
        state["Outcome"].append(record)
        self._append_consent(state, "store_outcome", f"Outcome.{record['outcome_id']}", summary)
        self._write(state)
        return record

    def view_state(self) -> dict[str, Any]:
        return self._read()

    def export_state(self) -> dict[str, Any]:
        return self._read()

    def correct_field(
        self,
        entity: str,
        field: str,
        value: str,
        *,
        confirmed: bool = True,
    ) -> dict[str, Any]:
        summary = self.prepare_write(entity, {field: value}, action_type="correct")
        self._require_confirmation(confirmed, summary)
        state = self._read()
        if entity not in state or not isinstance(state[entity], dict):
            raise ValueError(f"entity is not editable: {entity}")
        if field not in state[entity]:
            raise ValueError(f"field does not exist on {entity}: {field}")
        state[entity][field] = value
        self._append_consent(state, "correct", f"{entity}.{field}", summary)
        return self._write(state)

    def anonymize(self, *, confirmed: bool = True) -> dict[str, Any]:
        summary = self.prepare_write(
            "State",
            {"operation": "anonymize"},
            action_type="anonymize",
        )
        self._require_confirmation(confirmed, summary)
        state = self._read()
        state["ChildProfile"]["nickname"] = "child"
        for fact in state["ChildProfile"].get("facts", []):
            fact["value"] = "minimal anonymized profile retained"
            fact["source_type"] = "user_confirmed"
            fact["last_updated"] = self._today()
        for entity in ["Case", "Intervention", "Outcome", "LearningTrack"]:
            state[entity] = self._redact_identifiers(state.get(entity, []))
        self._append_consent(state, "anonymize", "direct identifiers removed", summary)
        return self._write(state)

    def delete_entity(self, entity: str, *, confirmed: bool = True) -> dict[str, Any]:
        summary = self.prepare_write(
            entity,
            {"operation": "delete"},
            action_type="delete",
        )
        self._require_confirmation(confirmed, summary)
        state = self._read()
        if entity == "ChildProfile":
            state["ChildProfile"] = self._empty_state()["ChildProfile"]
            state["Case"] = []
            state["Intervention"] = []
            state["Outcome"] = []
            state["LearningTrack"] = []
        elif entity in {"Case", "Intervention", "Outcome", "ConsentLog", "LearningTrack"}:
            state[entity] = []
        else:
            raise ValueError(f"entity is not deletable: {entity}")
        self._append_consent(state, "delete", entity, summary)
        return self._write(state)

    def delete_state(self) -> None:
        if self.path.exists():
            self.path.unlink()


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(".kiddo-compass-state"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare-write")
    prepare.add_argument("--entity", required=True)
    prepare.add_argument("--action-type", required=True)
    prepare.add_argument("--fields-json", default="{}")

    create = subparsers.add_parser("create-profile")
    create.add_argument("--nickname", required=True)
    create.add_argument("--age-band", required=True)
    create.add_argument("--caregiver-mode", default="unknown")
    create.add_argument("--consent-scope", default="store_minimal_profile")

    case = subparsers.add_parser("create-case")
    case.add_argument("--child-id", default="local-child")
    case.add_argument("--scene-type", required=True)
    case.add_argument("--risk-route", default="unknown")
    case.add_argument("--pattern-frequency", default="unknown")
    case.add_argument("--source-type", default="user_confirmed")
    case.add_argument("--notes")

    intervention = subparsers.add_parser("create-intervention")
    intervention.add_argument("--case-id", required=True)
    intervention.add_argument("--recommendation-type", required=True)
    intervention.add_argument("--evidence-label", required=True)
    intervention.add_argument("--action", required=True)
    intervention.add_argument("--source-type", default="user_confirmed")

    outcome = subparsers.add_parser("create-outcome")
    outcome.add_argument("--intervention-id", required=True)
    outcome.add_argument("--result-type", required=True)
    outcome.add_argument("--notes", required=True)
    outcome.add_argument("--source-type", default="observed_feedback")

    subparsers.add_parser("view")
    subparsers.add_parser("export")

    correct = subparsers.add_parser("correct")
    correct.add_argument("--entity", required=True)
    correct.add_argument("--field", required=True)
    correct.add_argument("--value", required=True)

    subparsers.add_parser("anonymize")
    delete = subparsers.add_parser("delete")
    delete.add_argument("--entity")

    args = parser.parse_args(argv)
    store = StateStore(args.root)

    if args.command == "prepare-write":
        print_json(
            store.prepare_write(
                args.entity,
                json.loads(args.fields_json),
                action_type=args.action_type,
            )
        )
    elif args.command == "create-profile":
        print_json(
            store.create_profile(
                nickname=args.nickname,
                age_band=args.age_band,
                caregiver_mode=args.caregiver_mode,
                consent_scope=args.consent_scope,
            )
        )
    elif args.command == "create-case":
        extra = {"notes": args.notes} if args.notes else {}
        print_json(
            store.create_case(
                child_id=args.child_id,
                scene_type=args.scene_type,
                risk_route=args.risk_route,
                pattern_frequency=args.pattern_frequency,
                source_type=args.source_type,
                **extra,
            )
        )
    elif args.command == "create-intervention":
        print_json(
            store.create_intervention(
                case_id=args.case_id,
                recommendation_type=args.recommendation_type,
                evidence_label=args.evidence_label,
                action=args.action,
                source_type=args.source_type,
            )
        )
    elif args.command == "create-outcome":
        print_json(
            store.create_outcome(
                intervention_id=args.intervention_id,
                result_type=args.result_type,
                notes=args.notes,
                source_type=args.source_type,
            )
        )
    elif args.command == "view":
        print_json(store.view_state())
    elif args.command == "export":
        print_json(store.export_state())
    elif args.command == "correct":
        print_json(store.correct_field(args.entity, args.field, args.value))
    elif args.command == "anonymize":
        print_json(store.anonymize())
    elif args.command == "delete":
        if args.entity:
            print_json(store.delete_entity(args.entity))
        else:
            store.delete_state()
            print_json({"deleted": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
