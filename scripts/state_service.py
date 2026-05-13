#!/usr/bin/env python3
"""Local private state service for Kiddo Compass.

This is the reference implementation for platform state APIs. Product
surfaces can map their consent UI and account storage to this contract.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


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

    def _append_consent(self, state: dict[str, Any], action_type: str, scope: str) -> None:
        state["ConsentLog"].append(
            {
                "schema_version": "1",
                "consent_id": f"consent-{len(state['ConsentLog']) + 1}",
                "action_type": action_type,
                "confirmed_at": self._today(),
                "scope": scope,
            }
        )

    def create_profile(
        self,
        *,
        nickname: str,
        age_band: str,
        caregiver_mode: str,
        consent_scope: str,
    ) -> dict[str, Any]:
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
        self._append_consent(state, consent_scope, "minimal profile fields")
        return self._write(state)

    def view_state(self) -> dict[str, Any]:
        return self._read()

    def export_state(self) -> dict[str, Any]:
        return self._read()

    def correct_field(self, entity: str, field: str, value: str) -> dict[str, Any]:
        state = self._read()
        if entity not in state or not isinstance(state[entity], dict):
            raise ValueError(f"entity is not editable: {entity}")
        if field not in state[entity]:
            raise ValueError(f"field does not exist on {entity}: {field}")
        state[entity][field] = value
        self._append_consent(state, "correct", f"{entity}.{field}")
        return self._write(state)

    def anonymize(self) -> dict[str, Any]:
        state = self._read()
        state["ChildProfile"]["nickname"] = "child"
        for fact in state["ChildProfile"].get("facts", []):
            fact["value"] = "minimal anonymized profile retained"
            fact["source_type"] = "user_confirmed"
            fact["last_updated"] = self._today()
        self._append_consent(state, "anonymize", "direct identifiers removed")
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

    create = subparsers.add_parser("create-profile")
    create.add_argument("--nickname", required=True)
    create.add_argument("--age-band", required=True)
    create.add_argument("--caregiver-mode", default="unknown")
    create.add_argument("--consent-scope", default="store_minimal_profile")

    subparsers.add_parser("view")
    subparsers.add_parser("export")

    correct = subparsers.add_parser("correct")
    correct.add_argument("--entity", required=True)
    correct.add_argument("--field", required=True)
    correct.add_argument("--value", required=True)

    subparsers.add_parser("anonymize")
    subparsers.add_parser("delete")

    args = parser.parse_args(argv)
    store = StateStore(args.root)

    if args.command == "create-profile":
        print_json(
            store.create_profile(
                nickname=args.nickname,
                age_band=args.age_band,
                caregiver_mode=args.caregiver_mode,
                consent_scope=args.consent_scope,
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
        store.delete_state()
        print_json({"deleted": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
