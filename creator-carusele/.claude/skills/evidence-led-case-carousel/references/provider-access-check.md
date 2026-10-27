# Provider Access Check

Read this on the first run in a new environment, when sharing the skill with another person, or whenever the carousel plan depends on Kie/Higgsfield generation.

## Rule

Check access before promising generated visuals. Report capability, not guesses.

## Infisical First

Secrets must be fetched from Infisical first. Do not conclude a key is missing just because it is absent from `.env`.

Use the local Infisical skill/helper if available. Fetch secrets immediately before use and do not print or store secret values.

Expected Kie secret name from the 2026-09-22 test: `kie.ai` in Infisical dev. If the shared environment uses a different name, record the actual name in `source/provider-check.md`, not in the skill.

## Kie Check

Minimum acceptable check:

- secret can be fetched from Infisical or an approved environment variable;
- balance/auth endpoint or a harmless API call succeeds;
- model route intended for key visuals is available;
- record whether a previous test consumed credits.

Known prior test evidence:

- Kie `nano-banana-pro` completed successfully.
- Secret was fetched from Infisical dev.
- One test generation consumed 18 credits.

## Higgsfield Check

Minimum acceptable check:

- CLI or connector exists in the environment;
- help/version/auth command works without generating;
- if a test generation is needed, get approval for cost and produce a visible asset.

Known prior test evidence:

- local CLI path was `/opt/homebrew/bin/higgsfield`;
- `nano_banana_pro` generated a cover asset successfully in the 2026-09-22 test.

## Provider Check Output

Create `source/provider-check.md` with:

```markdown
# Provider Check

- Date:
- Environment/person:
- Kie:
  - secret source checked:
  - auth/balance result:
  - usable models:
  - status: READY / BLOCKED / NOT NEEDED
- Higgsfield:
  - CLI/connector:
  - auth/help result:
  - usable models:
  - status: READY / BLOCKED / NOT NEEDED
- Decision:
```

If both providers are blocked, switch to real assets, HTML/CSS, diagrams, screenshots, or request access before promising generated visuals.

