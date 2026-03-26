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
プロンプトの工夫ではなく「環境」として知識を蓄積する：
- **CLAUDE.md** → 常に適用されるルール（プロジェクト固有 or 個人横断）
- **Skills** → 特定の作業時だけ必要な手順
- **Hooks** → 確定的に実行される品質保証（CLAUDE.md指示=約80%遵守、Hooks=100%実行）
- **Task Diary** → セッション横断の知識蓄積 → 定期的にCLAUDE.mdに統合

### Plan → Build → Verify
1. 非自明なタスク（3ステップ以上）は Plan Mode で設計してから実装
2. 擬似コード → テスト → 実装 → 検証（TDDフロー）
3. テストは「Claudeが自分の仕事を自己検証できる仕組み」
4. `make test` / `pytest` / `npm test` で検証してからコミット

### Context Window Management
- タスク切り替え時は `/clear` でリセット
- リサーチや探索はサブエージェントに委譲してメインコンテキストをクリーンに保つ
- `/compact` で圧縮しつつ重要な情報を保持
- 大きなファイルは必要な部分だけ読む

### Subagent 活用パターン
まとまった規模のコード改修には並列サブエージェントを活用：
- 基本: タスクリスト → 複数サブエージェントで並列実行
- 対立検証: Engineer vs Auditor で異なる視点から議論させて盲点を発見
- レビュー: 規約チェック・バグスキャン・セキュリティ監査を並列実行

### Task Diary（タスク日記）
タスク完了時に学びを記録 → 複利的に蓄積：
- Session 1-2: Task Diary に個別の学びを記録
- Session 3+: 蓄積された学びを CLAUDE.md に統合 → 全セッションが賢くなる

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

## Hooks Setup Guide

新しいプロジェクトで `.claude/settings.json` に設定すべき推奨 Hooks：

### 1. センシティブファイル保護（PreToolUse: Edit|Write）
`.env`, `secrets/`, `credentials` への書き込みを exit 2 でブロック

### 2. 危険コマンドブロック（PreToolUse: Bash）
`rm -rf /`, `git push --force`, `DROP TABLE` 等を exit 2 でブロック

### 3. 自動フォーマット（PostToolUse: Edit|Write）
ファイル編集後にフォーマッター自動実行（black, prettier, ruff 等）

### 4. 通知（Notification）
Claude が入力待ちの時にデスクトップ通知を送る

> 詳細な設定例は `.claude-templates/settings.json.template` を参照

## Recommended Skills (npx skills add)

以下は `npx skills add` でインストール可能な汎用スキル：
- プロジェクトの技術スタックに合わせて選択的に追加する
- Skills は SKILL.md の description でトリガー判定されるため、大量に入れてもパフォーマンスへの影響は小さい
- 「常に適用すべきルール」→ CLAUDE.md、「特定作業時だけ必要」→ Skills
