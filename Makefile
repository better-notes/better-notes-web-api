format:
	poetry run black .
	poetry run isort .
lint:
	poetry run isort . --check
	poetry run flakehell lint .
	# TODO: poetry run mypy --config-file=.config/mypy.ini .
	poetry run black --check .
test:
	poetry run pytest --cov=web_api --cov-report=term-missing
