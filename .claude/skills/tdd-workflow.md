---
name: tdd-workflow
description: Guide test-driven development workflow. Use when adding new features or fixing bugs to ensure tests are written first.
---

# TDD Workflow Skill

Anthropic Security Engineering チームの手法:
「擬似コード → TDD → 信頼性の高いコード」

## Workflow

### Step 1: Understand
- 要件を明確にする（不明点があれば聞く）
- 影響範囲のコードを読む

### Step 2: Pseudocode
- 実装の擬似コードをコメントで書く
- エッジケースを洗い出す

### Step 3: Test First
- 期待する動作をテストとして書く
- 正常系・異常系・エッジケースをカバー
- この時点でテストは FAIL するのが正しい

### Step 4: Implement
- テストが通る最小限の実装を書く
- 過剰な抽象化を避ける

### Step 5: Verify
- 全テストが通ることを確認（`make test`）
- 既存テストが壊れていないことを確認

### Step 6: Refactor (if needed)
- テストが通った状態を維持しつつリファクタ
- 各リファクタ後にテスト再実行

## Key Principle

> Claudeに検証手段を与えることが、最も効果の高いテクニック。
> テストは「Claudeが自分の仕事を自己検証できる仕組み」として機能する。
