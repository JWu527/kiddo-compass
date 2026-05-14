.PHONY: audit-bundle release-gate

audit-bundle:
	python3 scripts/build_audit_bundle.py

release-gate:
	python3 scripts/release_gate.py
