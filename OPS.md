# Operations

Use this file before publishing a beta build, reviewing incidents, or updating sources.

## Owners

| Role | Responsibility |
| --- | --- |
| release owner | Runs release guardrails, confirms package artifact, writes changelog, and blocks release on P0 failures. |
| content owner | Reviews scenario cards, source labels, tone, and high-risk wording. |
| privacy owner | Reviews state schema, data minimization, package contents, and deletion/anonymization behavior. |

Owner fields may be filled by the maintainer before a public release. Empty owner names mean the release is not ready for public distribution.

## Source freshness

- Official health/development sources: review monthly during beta, then at least quarterly.
- Method and practice sources: review quarterly or when a user incident exposes ambiguity.
- Update `reviewed_at` in `references/evidence-matrix.md` when the source check is complete.
- Update `references/regional-resources.json` when safety resource wording or availability changes.
- If a source becomes stale or unavailable, mark the affected row `needs-evaluation` or remove the claim until reviewed.
- Run `python3 scripts/source_freshness.py` before any public beta artifact is published.

## GitHub Actions

`.github/workflows/public-beta.yml` runs the public-beta gate on pull requests, pushes to `main`, and manual dispatches. It must stay aligned with `PUBLISHING.md`: unit tests, release guardrails, beta KPI gate, whitelist package build, package inspection, and semantic regression scoring.

If CI fails because a regression report is missing, generate it locally with `python3 scripts/run_regression.py --priority P0 --report dist/regression-p0.json` and push the code or fixture fix that makes the report pass.

## Quality dashboard

Generate the local beta dashboard after KPI and regression reports exist:

```bash
python3 scripts/beta_kpi_gate.py --json > dist/beta-kpi.json
python3 scripts/quality_dashboard.py --metrics dist/beta-kpi.json --regression dist/regression-p0.json --output dist/quality-dashboard.html
```

The dashboard is a static local artifact for maintainer review. It is not a production BI dashboard and does not collect user telemetry.

## Incident playbook

Use this flow for privacy leakage, wrong red/yellow triage, unsafe advice, or misleading diagnosis-like language:

1. Freeze public release and stop publishing new artifacts.
2. Save the smallest reproducible input/output sample, minimizing private details.
3. Classify severity: privacy, safety triage, medical/development boundary, copyright/source, or tone harm.
4. Patch the rule, scenario card, regression case, or release guardrail.
5. Add or update a regression case that would have caught the incident.
6. Run `python3 scripts/release_guardrails.py check`, `python3 scripts/beta_kpi_gate.py`, `python3 scripts/source_freshness.py`, and the relevant regression command.
7. Write the resolution in `CHANGELOG.md`.

## Rollback

- Keep the previous known-good release zip in `dist/` or the release system.
- If a published build leaks private data or unsafe advice, unpublish or supersede it immediately.
- Restore the previous tag/package, then publish a patch release with the incident regression included.

## Contributor training checklist

- Privacy minimization: default to nickname, age band, role, and scene.
- Professional boundary: do not diagnose; use local urgent support language for red risk.
- Evidence labels: use `official-consensus`, `method-source`, `practice-pattern`, `needs-evaluation`, or `experience-only`.
- User-facing tone: no internal labels in ordinary answers; crisis answers use no decorative emoji.
- Copyright boundary: summarize concepts and create original practice wording.

## Release exercise

Before a public beta, run one tabletop exercise for each case:

- Privacy leakage in an accidentally zipped `child-profile.md`.
- Missed red/yellow triage in a self-harm or adult-violence prompt.
- Source freshness issue in a health/development recommendation.

Each exercise must identify the owner, detection path, rollback path, regression update, and changelog entry.
