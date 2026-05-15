# Sharing

Never zip or share the workspace directory.

The only shareable public-beta review artifact is:

```text
audit-bundle/kiddo-compass-audit-bundle.zip
```

Build it with:

```bash
make review-snapshot BUNDLE_ONLY=1
```

Why this matters:

- The workspace can contain `.git/`, local caches, ignored build products, and private study/archive material.
- `.kiddo-compass-state/` is local private live state and must never leave the maintainer machine.
- `dist/*.zip` may be stale. Do not use it as release evidence.
- `manual-testing/HERMES_TEST_CASES.md` is non-runtime, non-release manual guardrail material and may intentionally contain red-flag examples.

Before sharing, run:

```bash
python3 scripts/release_guardrails.py inspect audit-bundle/kiddo-compass-audit-bundle.zip
```
