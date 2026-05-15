.PHONY: audit-bundle release-gate review-snapshot clean-release-artifacts

audit-bundle:
	python3 scripts/build_audit_bundle.py

release-gate:
	python3 scripts/release_gate.py

review-snapshot:
	python3 scripts/release_guardrails.py check
	python3 scripts/review_snapshot.py $(if $(BUNDLE_ONLY),--bundle-only,)

clean-release-artifacts:
	python3 scripts/release_gate.py --clean-release-artifacts
