---
name: plan-and-build
description: Structure a non-trivial task with Plan Mode before implementation. Use for tasks with 3+ steps or architectural decisions.
---

# Plan and Build Skill

For non-trivial tasks, follow the Plan → Build → Verify workflow.

## When to Use

- 3ステップ以上の実装タスク
- アーキテクチャ上の判断が必要
- 複数ファイルにまたがる変更
- 新機能の追加

## Phase 1: Plan

1. Enter Plan Mode
2. Analyze the task requirements
3. Identify affected files and modules
4. List implementation steps in order
5. Note potential risks or trade-offs
6. Iterate on the plan until satisfied

## Phase 2: Build

1. Switch to implementation mode
2. Follow the plan step by step
3. Write tests alongside implementation
4. Keep changes atomic and focused

## Phase 3: Verify

1. Run the full test suite
2. Review the diff for unintended changes
3. Verify the feature works as expected
4. Commit with a clear message describing the "why"

## Output

Present the plan as a numbered checklist before starting implementation.
