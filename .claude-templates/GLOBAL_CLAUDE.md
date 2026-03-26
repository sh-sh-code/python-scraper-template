# Global CLAUDE.md Template
#
# Usage: Copy this file to ~/.claude/CLAUDE.md
# This applies to ALL projects and sessions.
# Project-specific rules go in each repo's CLAUDE.md instead.

## Personal Preferences

- 日本語でコミュニケーションする
- コミットメッセージは英語で書く
- コードのコメントは英語で書く

## Workflow Principles

### Context Engineering（コンテキストエンジニアリング）
- プロンプトの工夫だけでなく、プロジェクト全体の「環境」として知識を蓄積する
- CLAUDE.md → プロジェクト固有のルール、~/.claude/CLAUDE.md → 個人の横断的ルール

### Plan → Build → Verify
1. 非自明なタスク（3ステップ以上）は Plan Mode で設計してから実装
2. テストを先に書く or 既存テストの通過を確認
3. `make test` / `pytest` / `npm test` で検証してからコミット

### Context Window Management
- タスク切り替え時は `/clear` でリセット
- リサーチや探索はサブエージェントに委譲してメインコンテキストをクリーンに保つ
- `/compact` で圧縮しつつ重要な情報を保持
- 大きなファイルは必要な部分だけ読む

### Task Diary（タスク日記）
タスク完了時に学びを記録：
- 何を試みたか / 何がうまくいったか / 何が失敗したか / 次回への教訓
- 数セッション分溜まったらCLAUDE.mdに統合して全セッションを底上げ

## Code Quality Defaults

- セキュリティ: OWASP Top 10 を意識（SQL injection, XSS, command injection）
- エラーハンドリング: システム境界（ユーザー入力、外部API）でのみバリデーション
- 不要な抽象化を避ける — 3行の重複は premature abstraction より良い
- 型ヒント / 型注釈を使う（Python: type hints, TypeScript: strict mode）

## Git Conventions

- 機能ブランチで作業し、main への直接コミットは避ける
- コミットは atomic に（1つの論理的変更 = 1コミット）
- `.env`, credentials, secrets をコミットしない
- PR 作成時はテスト通過を確認

## Recommended Skills (npx skills add)

以下は `npx skills add` でインストール可能な汎用スキル：
- プロジェクトの技術スタックに合わせて選択的に追加する
- Skills は SKILL.md の description でトリガー判定されるため、大量に入れてもパフォーマンスへの影響は小さい
- 「常に適用すべきルール」→ CLAUDE.md、「特定作業時だけ必要」→ Skills
