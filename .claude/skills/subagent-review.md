---
name: subagent-review
description: Launch parallel subagents to review code from multiple perspectives. Use for code reviews, pre-PR checks, or architecture validation.
---

# Subagent Review Skill

Launch multiple subagents in parallel to review code from different angles.
This implements the "Opponent Processor" pattern from Anthropic engineers.

## Basic Pattern: Parallel Review

When reviewing code, launch these subagents concurrently:

1. **Standards Checker** — Verify CLAUDE.md conventions and project patterns are followed
2. **Bug Scanner** — Look for obvious bugs, edge cases, and error handling gaps
3. **Security Auditor** — Check for OWASP Top 10 vulnerabilities (injection, XSS, etc.)

## Advanced Pattern: Opponent Processor (対立検証)

For architectural decisions or non-trivial design choices:

1. **Subagent "Engineer"** — Argue FOR the proposed approach, listing its strengths
2. **Subagent "Auditor"** — Argue AGAINST it, listing risks and alternatives
3. **Main agent** — Synthesize both perspectives and make a balanced decision

## Usage

Ask Claude to run a subagent review:
- "subagent review で今の変更をチェックして"
- "対立検証パターンで設計を検証して"

## Output Format

```
## Subagent Review Results

### Standards ✅/❌
- [findings]

### Bugs ✅/❌
- [findings]

### Security ✅/❌
- [findings]

### Decision (if Opponent Processor was used)
- Engineer's case: ...
- Auditor's case: ...
- Conclusion: ...
```
