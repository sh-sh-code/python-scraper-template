---
name: task-diary
description: Record a task diary entry after completing a task. Use when finishing a feature, bug fix, or investigation.
---

# Task Diary Skill

When invoked, create a structured diary entry in the following format and append it to `.claude/task-diary.md`:

## Entry Format

```markdown
### [DATE] — [Brief Title]

**Goal:** What was attempted
**Approach:** What was done
**Result:** What worked / what didn't
**Lesson:** Key takeaway for future sessions
```

## Rules

1. Be concise — each field should be 1-2 sentences
2. Focus on non-obvious learnings (skip trivial observations)
3. If the diary file has 10+ entries, suggest consolidating key learnings into CLAUDE.md
4. Create `.claude/task-diary.md` if it doesn't exist
