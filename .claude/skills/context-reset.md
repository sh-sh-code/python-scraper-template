---
name: context-reset
description: Prepare for a new task by summarizing current state and clearing context. Use when switching between unrelated tasks.
---

# Context Reset Skill

When switching tasks, follow this protocol:

## Steps

1. **Summarize** — Write a brief summary of what was accomplished in the current task
2. **Record** — If there are learnings worth keeping, invoke the task-diary skill
3. **Check** — Ensure all changes are committed or stashed
4. **Clear** — Suggest the user run `/clear` to reset context
5. **Orient** — After clear, re-read CLAUDE.md and relevant files for the new task

## Output Format

```
## Task Switch Summary
- Completed: [what was done]
- Status: [committed / stashed / uncommitted changes]
- Learnings: [any new insights, or "none"]
- Ready for: /clear
```
