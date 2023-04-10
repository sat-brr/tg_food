lint-app:
	poetry run flake8 tg_app
lint-tests:
	poetry run flake8 tests
build-base:
	python3 tg_app/database/create_db.py
run-app:
	python3 tg_app/tg_bot/bot.py
tests-cov:
	poetry run pytest --cov=tg_app --cov-report xml
install:
	poetry install