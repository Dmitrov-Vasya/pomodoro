.DEFAULT_GOAL := help

run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env

install:
	poetry add $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

uninstall:
	poetry remove $(LIBRARY)

update:
	poetry update $(LIBRARY)