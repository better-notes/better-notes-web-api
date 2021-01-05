format:
	poetry run black .
	poetry run isort -rc -y .
lint:
	poetry run isort --check-only
	poetry run flakehell lint .
	# TODO: poetry run mypy --config-file=.config/mypy.ini .
	poetry run black --check .
test:
	poetry run pytest --cov=web_api --cov-config=.config/.coveragerc --cov-report=term-missing
