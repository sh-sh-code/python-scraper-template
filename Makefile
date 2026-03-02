.PHONY: run test lint clean

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

clean:
	rm -f data.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
