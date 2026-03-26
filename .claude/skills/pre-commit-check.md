---
name: pre-commit-check
description: Run quality checks before committing. Use before any git commit to ensure code quality.
---

# Pre-Commit Check Skill

Before committing, run through this checklist:

## Steps

1. **Run tests** — Execute the project's test suite (`make test`, `pytest`, `npm test`, etc.)
2. **Check for secrets** — Scan staged files for API keys, passwords, tokens, `.env` contents
3. **Review diff** — `git diff --staged` to verify only intended changes are included
4. **Lint check** — Run linter if configured (`make lint`, `flake8`, `eslint`, etc.)

## On Failure

- If tests fail: fix the issue before committing
- If secrets are found: remove them and add the file to `.gitignore`
- If unintended changes: unstage them with `git reset HEAD <file>`

Report results as a checklist:
- [ ] Tests pass
- [ ] No secrets in staged files
- [ ] Diff reviewed
- [ ] Lint clean (if applicable)
