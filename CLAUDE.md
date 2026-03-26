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
```

## Coding Conventions

- Type hints を使う（Pydantic v2 スタイル）
- ルーティングは `api.py`、DB操作は `crud.py` に分離
- テストは `tests/` 配下に `test_*.py` で追加
- レスポンスは一貫した JSON 形式（エラー時も `detail` キー）
- ロギングには `logging_config.py` の structured logger を使用
- 新しい依存は `requirements.txt` に追加

## Workflow Guidelines

### Plan Mode を活用する
- 3ステップ以上 or アーキテクチャ判断が必要なタスクでは Plan Mode で計画を立ててから実装
- 計画に納得してから auto-accept モードで一気に実装

### テスト駆動
- 機能追加時は先にテストを書く or 既存テストが通ることを確認してから変更
- `make test` で全テストがパスすることを確認してからコミット

### コンテキスト管理
- タスク切り替え時は `/clear` でコンテキストをリセット
- 大きなファイルは必要な部分だけ読む
- サブエージェントを活用してメインのコンテキストをクリーンに保つ

## Task Diary Protocol

タスク完了時に以下を記録し、知見を蓄積する：
1. 何を試みたか
2. 何がうまくいったか
3. 何が失敗し、なぜか
4. 次回への教訓

蓄積された学びは定期的にこの CLAUDE.md に統合する。

## Common Pitfalls

- SQLite は concurrent write に弱い — 負荷テスト時は注意
- FastAPI の `Depends` を使う際は conftest.py のオーバーライドパターンを確認
- `.env` ファイルをコミットしない（`.gitignore` 確認）
