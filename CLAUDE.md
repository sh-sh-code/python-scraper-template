# CLAUDE.md — Project Instructions

## Project Overview

FastAPI + SQLite による CRUD API スターターテンプレート。
フリーランス案件でのバックエンド構築を想定した構成。

## Tech Stack

- Python 3.x / FastAPI / Pydantic v2
- SQLite (stdlib) — 本番では PostgreSQL に差し替え可
- pytest + FastAPI TestClient
- uvicorn (ASGI server)

## Key Commands

```bash
make run          # uvicorn --reload で起動 (port 8000)
make test         # pytest -v
make clean        # data.db と __pycache__ を削除
pip install -r requirements.txt
```

## Project Structure

```
app/
  main.py             # FastAPI app, middleware, startup
  api.py              # Route definitions
  schemas.py          # Pydantic request/response models
  crud.py             # Database operations
  db.py               # SQLite connection & schema
  models.py           # Internal data representations
  logging_config.py   # Logger setup with request IDs
tests/
  conftest.py         # Shared fixtures (in-memory DB)
  test_health.py
  test_items.py
.claude/
  settings.json       # Hooks & permissions (チームで共有)
  skills/             # Reusable skill definitions
```

## Coding Conventions

- Type hints を使う（Pydantic v2 スタイル）
- ルーティングは `api.py`、DB操作は `crud.py` に分離
- テストは `tests/` 配下に `test_*.py` で追加
- レスポンスは一貫した JSON 形式（エラー時も `detail` キー）
- ロギングには `logging_config.py` の structured logger を使用
- 新しい依存は `requirements.txt` に追加

## Workflow Guidelines

### Context Engineering（コンテキストエンジニアリング）
プロンプトの工夫ではなく「環境」として知識を蓄積する：
- **CLAUDE.md** → 常に適用されるルール（このファイル）
- **Skills** → 特定の作業時だけ必要な手順（`.claude/skills/`）
- **Hooks** → 確定的に実行される品質保証（`.claude/settings.json`）
- **Task Diary** → セッション横断の知識蓄積（下記参照）

### Plan Mode を活用する
- 3ステップ以上 or アーキテクチャ判断が必要なタスクでは Plan Mode で計画を立ててから実装
- 計画に納得してから auto-accept モードで一気に実装
- 「擬似コード → テスト → 実装 → 検証」の TDD フローを推奨

### テスト駆動（Claudeへの検証手段の提供）
テストは「Claudeが自分の仕事を自己検証できる仕組み」として最も効果が高い：
- 機能追加時は先にテストを書く or 既存テストが通ることを確認してから変更
- `make test` で全テストがパスすることを確認してからコミット
- テストが落ちている状態でコミットしない

### コンテキスト管理
- タスク切り替え時は `/clear` でコンテキストをリセット
- 大きなファイルは必要な部分だけ読む
- リサーチ・探索・並列分析はサブエージェントに委譲
- `/compact` でコンテキストを圧縮しつつ重要情報を保持

### Subagent パターン
まとまった規模のコード改修には並列サブエージェントを活用：
- CLAUDE.md 準拠チェック
- git 履歴からパターン検索
- バグスキャン
- 対立検証（Engineer vs Auditor で異なる視点から議論）

## Hooks による自動品質保証

`.claude/settings.json` に設定済み：
- **PreToolUse**: `.env`・secrets への書き込みブロック、危険コマンド（`rm -rf /`, `--force push`, `DROP TABLE`）のブロック
- **PostToolUse**: ファイル編集後のフック（フォーマッター追加可能）
- **Permissions**: `make test`, `make run`, `pytest` は自動許可。`--force push` や `.env` 読み取りは拒否

> Hooks はプロンプトと違い「保証」として機能する。CLAUDE.md の指示は約80%しか従わないが、Hooks は100%実行される。

## Task Diary Protocol

タスク完了時に `.claude/task-diary.md` へ記録し、知見を蓄積する：
1. 何を試みたか
2. 何がうまくいったか
3. 何が失敗し、なぜか
4. 次回への教訓

### 複利的な蓄積フロー
- Session 1: Task Diary → 学び3つ
- Session 2: Task Diary → 学び2つ + 前回の教訓を活用
- Session 3: 蓄積された学びをこの CLAUDE.md の Accumulated Learnings に統合
- → 以降、すべてのセッションが賢くなる

### Accumulated Learnings

<!-- Task Diary から統合された学びをここに追記 -->
<!-- 例: -->
<!-- - [2026-03-26] conftest.py の DB fixture は各テスト後に自動ロールバックされる -->

## Available Skills

| Skill | 用途 |
|---|---|
| `task-diary` | タスク完了時に学びを記録 |
| `tdd-workflow` | テスト駆動の開発フロー |
| `pre-commit-check` | コミット前の品質チェック |
| `context-reset` | タスク切り替え時のプロトコル |
| `plan-and-build` | Plan → Build → Verify |
| `subagent-review` | 並列サブエージェントレビュー・対立検証 |

## Common Pitfalls

- SQLite は concurrent write に弱い — 負荷テスト時は注意
- FastAPI の `Depends` を使う際は conftest.py のオーバーライドパターンを確認
- `.env` ファイルをコミットしない（`.gitignore` 確認）
- Hooks は設定変更後、セッション再起動が必要（`/hooks` で確認）
